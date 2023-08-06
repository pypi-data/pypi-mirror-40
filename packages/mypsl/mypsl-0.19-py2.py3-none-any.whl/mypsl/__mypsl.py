#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

'''
    mypsl :: MySQL process list watcher and query killer
    Copyright (C) 2014 Kyle Shenk <k.shenk@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from __future__ import print_function
import os
import sys
import argparse
import json
import time, datetime
import signal
import subprocess
from collections import defaultdict
from distutils.spawn import find_executable
from socket import gethostname

PROG_START = time.time()

'''
    Requires pymysql, colorama, and situationally yaml and argcomplete

    argcomplete is supported here as well, if the module is installed. See:
    https://pypi.python.org/pypi/argcomplete for specific information about argcomplete.
    How this is used is explained below.

    Yaml is required if using the config option as well.

    Some output is sent to stderr so you can hide this while running in the terminal if you want.
    --> print("the message", file=sys.stderr)
    i.e. mypsl.py --options 2>/dev/null

    Please see the help section for usage (mypsl.py -h), and please take care when killing queries.

    If using the --config option, 
        - The config file will override any connection information provided in other options.
        - the "$HOME/.mypsl" directory must already exist
        - the config file must be in that directory and be readable
        - you will provide only the filename - not the full path
        - this must be a valid yaml file with just the connection information: i.e. 
            host: hostname
            port: 1234
            user: me
            passwd: mypassword

    If argcomplete is installed, all options will autocomplete, but the --config option has more
    functionality. If the $HOME/.mypsl directory exists and contains files, we'll auto-load the files available
    and will auto-complete the filenames.
    If you choose not to activate global completion, you will need to have this sourced into your environment (.bashrc/.bash_profile)
    eval "$(register-python-argcomplete mypsl.py)"
    Note: as explained on pypi, bash >= 4.2 is required, and your shell must be using it.

    If using the --salt-minion option you will supply the minion id as an argument to the option. This will look for
    eth0 in ip_interfaces in the grains for that minion, and will look for user and pass in
    mysql:connection pillar data.

'''

try:
    import pymysql
    HAS_MYSQL = True
except ImportError:
    HAS_MYSQL = False

try:
    import argcomplete
    HAS_ARGCOMPLETE = True
except ImportError:
    HAS_ARGCOMPLETE = False

try:
    from colorama import init, Fore, Style
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False

## not all have this by default...
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

PROCESS_THRESHOLD_WARN  = 100
PROCESS_THRESHOLD_CRIT  = 200
SLEEPER_THRESHOLD_WARN  = 30
SLEEPER_THRESHOLD_CRIT  = 75
INFO_TRIM_LENGTH        = 1000

USER_WHERE      = []
HOSTNAME        = None
OUT_FORMAT      = "{0:<12}{1:16}{2:20}{3:22}{4:25}{5:<8}{6:28}{7:25}"
MYPSL_CONFIGS   = os.path.join(os.environ.get('HOME'), '.mypsl')

#READ_SEARCH     = ('show', 'select', 'desc')
#WRITE_SEARCH    = ('insert', 'update', 'create', 'alter', 'replace', 'rename', 'delete')
#LOCKED_SEARCH   = ('locked', 'waiting for table level lock', 'waiting for table metadata lock')

class mydb():
    conn            = None
    cursor          = None
    connect_args    = {}

    def __init__(self):

        ## default everything, and override as necessary.
        self.connect_args = {
            'db':           'information_schema',
            'charset':      args.charset,
            'cursorclass':  pymysql.cursors.DictCursor,
            'host':         args.host,
            'port':         args.port,
            'user':         args.user,
            'passwd':       args.passwd
        }

        if args.salt_minion:
            if not self.__load_from_salt():
                sys.exit(1)
        elif args.connect_config:
            self.__load_from_config()
        else:
            if args.host == 'localhost':
                socket = get_mysql_default('socket')
                if socket:
                    self.connect_args['unix_socket'] = socket
                    del self.connect_args['host']
                    del self.connect_args['port']
                else:
                    print(color_val("Unable to use the socket file, will resort to host/port", Fore.RED + Style.BRIGHT), file=sys.stderr)

        pymysql.paramstyle = 'pyformat'

    def connect(self):
        try:
            self.conn = pymysql.connect(**self.connect_args)
        except pymysql.Error as e:
            print(color_val("MySQL Said: {0}: {1}".format(e.args[0],e.args[1]), Fore.RED + Style.BRIGHT))

            msg = "ERROR: Unable to connect to mysql"
            if 'host' in self.connect_args:
                msg = msg + " on {0}.".format(self.connect_args['host'])
            elif 'unix_socket' in self.connect_args:
                msg = msg + " using: {0}.".format(self.connect_args['unix_socket'])

            msg = msg + "\nCheck connection configuration"

            print(color_val(msg, Fore.RED + Style.BRIGHT))
            sys.exit(1)

    def query(self, sql, args=[]):
        try:
            if not self.cursor:
                self.cursor = self.conn.cursor()
            if args:
                self.cursor.execute(sql, args)
            else:
                self.cursor.execute(sql)

        except (AttributeError, pymysql.OperationalError):
            self.connect()
            self.query(sql, args)

        if self.cursor:
            return self.cursor
        return False

    def __load_from_config(self):
        cfile = os.path.join(MYPSL_CONFIGS, args.connect_config)
        if os.path.isfile(cfile):
            with open(cfile, 'r') as f:
                self.connect_args.update(yaml.load(f))
                args.host = self.connect_args['host']
                return True
        return False

    def __load_from_salt(self):
        try:
            import salt.client
        except ImportError:
            print(color_val("Error: Unable to import salt.client.", Fore.RED + Style.BRIGHT))
            return False

        lc = salt.client.LocalClient()

        data = lc.cmd(args.salt_minion, 'network.ip_addrs')

        if not data:
            print(color_val("Error: Unable to get the IP address via network.ip_addrs", Fore.RED + Style.BRIGHT))
            return False

        try:
            self.connect_args['host'] = data[args.salt_minion][0]
        except (KeyError, IndexError, TypeError):
            print(color_val("Error: Unable to get the IP address.", Fore.RED + Style.BRIGHT))
            return False

        data = lc.cmd(args.salt_minion, 'pillar.get', ['mysql:connection'])

        if not data:
            print(color_val("Error: Unable to get mysql:connection from pillar.", Fore.RED + Style.BRIGHT))
            return False

        try:
            self.connect_args['user']   = data[args.salt_minion]['user']
            self.connect_args['passwd'] = data[args.salt_minion]['pass']
        except KeyError:
            print(color_val("Error: Unable to get 'user' or 'pass' from pillar data.", Fore.RED + Style.BRIGHT))
            return False

        return True

    def cursor_close(self):
        if self.cursor:
            self.cursor.close()

    def db_close(self):
        if self.conn:
            self.conn.close()

def get_mysql_default(search_opt):
    my_print_defaults   = find_executable('my_print_defaults')
    my_cnf_file         = find_my_cnf()

    if not my_cnf_file:         return None
    if not my_print_defaults:   return None

    cmd     = [my_print_defaults, '--defaults-file', my_cnf_file, 'mysqld']
    proc    = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.wait()

    if proc.returncode != 0:
        print(color_val(proc.stderr.readlines(), Fore.RED + Style.BRIGHT), file=sys.stderr)
        return None
    defaults = proc.stdout.readlines()

    if not defaults:
        return None

    for d in defaults:
        if d.startswith("--{0}".format(search_opt)):
            return d.split('=')[1].strip()
    return None

def find_my_cnf():
    ## why oh why do different flavors of linux have to put these in different places.
    locations = (
        '/etc/my.cnf',
        '/etc/mysql/my.cnf',
        '/etc/mysql/conf.d/my.cnf',
        '/usr/etc/my.cnf',
    )

    for l in locations:
        ## return the first one we find
        if os.path.isfile(l):
            return l
    return None

def _get_config_files(prefix, parsed_args, **kwargs):
    if not HAS_ARGCOMPLETE:
        return False
    if not os.path.isdir(MYPSL_CONFIGS):
        return False
    return next(os.walk(MYPSL_CONFIGS))[2]

def parse_args():
    parser = argparse.ArgumentParser(description=color_val('MySQL Process list watcher & query killer.', Fore.CYAN + Style.BRIGHT),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    con_opt_group   = parser.add_argument_group(color_val('Connection Options', Fore.YELLOW + Style.BRIGHT))
    config_group    = parser.add_argument_group(color_val('Configuration Options', Fore.YELLOW + Style.BRIGHT))
    kill_group      = parser.add_argument_group(color_val('Kill Options', Fore.RED + Style.BRIGHT))

    con_opt_group.add_argument('-H', '--host', dest='host', type=str, default='localhost',
        help='The host to get the process list from. If localhost, we will attempt to find and use the socket file first.')
    con_opt_group.add_argument('-p', '--port', dest='port', type=int, default=3306,
        help="The host's port. If the host is localhost, we will attempt to find and use the socket file first.")
    con_opt_group.add_argument('-u', '--user', dest='user', type=str, default='root',
        help='The user to connect to the host as.')
    con_opt_group.add_argument('-P', '--pass', dest='passwd', type=str, default='',
        help='The password for authentication.')
    #con_opt_group.add_argument('-S', '--socket', dest='socket', type=str,
    #    help='If connecting locally, optionally use this socket file instead of host/port.')
    con_opt_group.add_argument('-ch', '--charset', dest='charset', type=str, default='utf8',
        help='Charset to use with the database.')
    con_opt_group.add_argument('--config', dest='connect_config', type=str, default=None,
        help='Load connection configuration from a file in {0}. Just provide the filename. '.format(MYPSL_CONFIGS) + \
        'This will override any other connection information provided').completer = _get_config_files
    con_opt_group.add_argument('-sm', '--salt-minion', dest='salt_minion', type=str, default=None,
        help='Connect to mysql running on a salt minion. Do not use any other connection options with this. \
        mysql:connection:user and mysql:connection:pass must exist in pillar data.')

    ## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    config_group.add_argument('-l', '--loop', dest='loop_second_interval', type=int, default=0,
        help='Time in seconds between getting the process list.')
    config_group.add_argument('-dft', '--default', dest='default', action='store_true',
        help='Run with defaults. Loop interval: 3 seconds, command like query or connect, order by time asc, id asc, truncate query to {0}.'.format(INFO_TRIM_LENGTH))
    config_group.add_argument('-c', '--command', dest='command', type=str,
        help='Lookup processes running as this command.')
    config_group.add_argument('-s', '--state', dest='state', type=str,
        help='Lookup processes running in this state.')
    config_group.add_argument('-t', '--time', dest='time', type=int,
        help='Lookup processes running longer than the specified time in seconds.')
    config_group.add_argument('-d', '--database', dest='database', type=str,
        help='Lookup processes running against this database.')
    config_group.add_argument('-q', '--query', dest='query', type=str,
        help='Lookup processes where the query starts with this specification.')
    config_group.add_argument('-i', '--id', dest='id_only', action='store_true',
        help='Only print back the ID of the processes.')
    config_group.add_argument('-isr', '--ignore_system_user', dest='ignore_system_user', action='store_true',
        help="Ignore the 'system user'")
    config_group.add_argument('--debug', dest='debug', action='store_true',
        help='Provide debug output.')
    config_group.add_argument('-o', '--order_by', dest='order_by', type=str,
        help='Order the results by a particular column: "user", "db asc", "db desc", "time desc"...etc')
    config_group.add_argument('-T', '--trim_info', dest='trim_info', action='store_true',
        help='Trim the info field (the query) to {0}'.format(INFO_TRIM_LENGTH))

    ## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    kill_group.add_argument('--kill', dest='kill', action='store_true',
        help='Kill the queries that we find.')
    kill_group.add_argument('-kt', '--kill_threshold', dest='kill_threshold', default=100,
        help="The kill threshold. If a number is provided, we'll need to hit that many total connections before killing queries. You can \
        set this to 'off' as well, which kills queries no matter how many connections there are.")
    kill_group.add_argument('-ka', '--kill_all', dest='kill_all', action='store_true',
        help="If this flag is provided, we'll attempt to kill everything, not only select queries. {0}".format(color_val("Use with caution!", Fore.RED + Style.BRIGHT))) 
    kill_group.add_argument('-ky', '--kill_yes', dest='kill_yes', action='store_true',
        help="If this is provided we won't stop to ask if you are sure that you want to kill queries.")
    kill_group.add_argument('-kl', '--kill_log', dest='kill_log', default='/var/log/killed_queries.log',
        help="Where to log killed queries to, granting permissions to write to this file.")

    if HAS_ARGCOMPLETE:
        argcomplete.autocomplete(parser)
    return parser.parse_args()

def myp(d):
    print(json.dumps(d, indent=4))

def get_now_date():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def print_header():
    ct = get_connected_threads()
    mc = get_max_connections()

    if (ct > (mc * .75)):
        ct_str = color_val(ct, Fore.RED)
    elif (ct > (mc * .5)):
        ct_str = color_val(ct, Fore.YELLOW)
    else:
        ct_str = color_val(ct, Fore.CYAN)

    bar = "-"*35
    header = "%s%s%s %s%s :: %s :: Threads (%s / %s) %s%s%s" % \
        (Fore.YELLOW, bar, Fore.GREEN, get_hostname(), Fore.RESET, get_now_date(), ct_str, mc, Fore.YELLOW, bar, Fore.RESET)

    print(header)
    print("{0}".format(Style.BRIGHT) + OUT_FORMAT.format("ID", "USER", "HOST", "DB", "COMMAND", "TIME", "STATE", "INFO") + "{0}".format(Style.RESET_ALL))

def sig_handler(signal, frame):
    if db:
        try:
            db.cursor_close()
            db.db_close()
        except MySQLdb.ProgrammingError:
            pass
    print()
    sys.exit(0)

def get_long_query_time():
    global LONG_QUERY_TIME

    if LONG_QUERY_TIME:
        return LONG_QUERY_TIME

    LONG_QUERY_TIME = 0

    sql = "SHOW GLOBAL VARIABLES LIKE 'long_query_time'"
    cur = db.query(sql)
    res = cur.fetchone()
    if res and 'Value' in res:
        LONG_QUERY_TIME = int(round(float(res['Value'])))

    return LONG_QUERY_TIME

def get_connected_threads():
    sql = "SHOW GLOBAL STATUS LIKE 'Threads_connected'"
    cur = db.query(sql)
    res = cur.fetchone()
    if res and 'Value' in res:
        return int(res['Value'])
    return 0

def get_max_connections():
    sql = "SHOW GLOBAL VARIABLES LIKE 'max_connections'"
    cur = db.query(sql)
    res = cur.fetchone()
    if res and 'Value' in res:
        return int(res['Value'])
    return 0

def get_num_sleepers():
    sql = "SELECT SQL_NO_CACHE count(id) AS num_sleepers FROM processlist WHERE command = 'Sleep' OR state = 'User sleep'"
    cur = db.query(sql)
    res = cur.fetchone()
    if res and 'num_sleepers' in res:
        return int(res['num_sleepers'])
    return 0

def get_hostname():
    global HOSTNAME

    if HOSTNAME: return HOSTNAME

    if args.salt_minion:
        ## display the salt minion id
        HOSTNAME = args.salt_minion
    elif args.host == 'localhost':
        ## local, just use socket.gethostname
        HOSTNAME = gethostname()
    else:
        ## we're going to ask the remote mysql server
        sql = "SELECT @@hostname AS hostname"
        cur = db.query(sql)
        res = cur.fetchone()
        if res and 'hostname' in res:
            HOSTNAME = res['hostname']

    return HOSTNAME

def color_val(val, color):
    return "%s%s%s" % (color, val, Style.RESET_ALL)

def record_kill(row):
    if os.path.exists(args.kill_log):
        if not os.access(args.kill_log, os.W_OK):
            return
    else:
        try:
            with open(args.kill_log, 'w+') as f:
                pass
        except IOError:
            print(color_val("Unable to create: {0}".format(args.kill_log), Fore.RED + Style.BRIGHT), file=sys.stderr)
            return

    kill_string = "{0} :: {1} :: {2}\n".format(get_now_date(), get_hostname(), ', '.join("%s: %s" % (k, v) for (k, v) in row.iteritems()))
    with open(args.kill_log, 'a') as f:
        f.write(kill_string)

def killah(results):
    ## ok. is it an integer and are the connected threads greater than the kill threshold ?
    try:
        args.kill_threshold = int(args.kill_threshold)
        ct = get_connected_threads()
        if ct < args.kill_threshold:
            print("Connected threads: {0}, Kill threshold: {1}. Not killing at this time".format(ct, args.kill_threshold), file=sys.stderr)
            return
    except ValueError:
        if args.kill_threshold.lower() != 'off':
            ## if we haven't set this to off, then no killing
            print("kill threshold was set but doesn't = off. Not killing at this time.", file=sys.stderr)
            return

    sql = "KILL %s"
    killed = 0
    for row in results:
        if not args.kill_all:
            if not row['info'].lower().startswith('select'):
                continue
        if db.query(sql, (row['id'],)):
            record_kill(row)
            killed += 1
    return killed

def show_processing_time(start, end, text='Processing time'):
    elapsed     = round(end - start, 3)

    if elapsed > 5:
        elapsed_str = color_val(elapsed, Fore.RED)
    elif elapsed > .5:
        elapsed_str = color_val(elapsed, Fore.YELLOW)
    else:
        elapsed_str = color_val(elapsed, Fore.CYAN)

    print("\t({0}): {1}".format(color_val(text, Fore.GREEN), elapsed_str))

def process_row(results):
    calculate_sleepers = False
    if not args.id_only:
        num_reads           = num_writes = num_locked = num_closing = num_opening = num_past_long_query = num_sleepers = 0
        user_count          = defaultdict(int)
        state_count         = defaultdict(int)

    ## the state field would be 'User sleep', so is 'sleep' found in the state argument given ?
    if (args.command and args.command.lower() == 'sleep') or (args.state and 'sleep' in args.state.lower()):
        calculate_sleepers = True
    
    if not calculate_sleepers:
        num_sleepers = get_num_sleepers()

    for row in results:
        if args.id_only:
            print(row['id'])
            continue

        user_count[row['user']]     += 1
        state_count[row['state']]   += 1
        
        if row['info']:
            ## pull the first word of the query out - newline, tab or whitespace, and lowercase it.
            s_info = row['info'].split()[0].lower()
            if args.trim_info and len(row['info']) > 1000:
                row['info'] = "%s ..." % row['info'][:1000]
        else:
            row['info'] = '--'
            s_info = '--'

        if not row['state']:    row['state'] = '--'
        if not row['db']:       row['db'] = '--'

        ## the port number doesn't really tell us much.
        row['host'] = row['host'].split(':')[0]

        if s_info:
            if s_info in READ_SEARCH:   num_reads += 1
            if s_info in WRITE_SEARCH:  num_writes += 1

        if row['state']:
            if row['state'].lower() in LOCKED_SEARCH:           num_locked += 1
            if row['state'] == 'Copying to tmp table on disk':  num_writes += 1
            if row['state'].startswith('Opening table'):        num_opening += 1
            if row['state'].startswith('closing table'):        num_closing += 1

        if int(row['time']) > LONG_QUERY_TIME: num_past_long_query += 1

        if calculate_sleepers and ('sleep' in row['command'].lower()) or ('sleep' in row['state'].lower()):
            num_sleepers += 1

        print(OUT_FORMAT.format(row['id'], row['user'], row['host'], row['db'], row['command'], row['time'], row['state'], row['info'].encode('utf-8')))

    if args.id_only:
        return

    return {
        'num_reads':            num_reads,
        'num_writes':           num_writes,
        'num_locked':           num_locked,
        'num_closing':          num_closing,
        'num_opening':          num_opening,
        'num_sleepers':         num_sleepers,
        'num_past_long_query':  num_past_long_query,
        'user_count':           user_count,
        'state_count':          state_count
    }

def pslist(sql, counter=0):
    start   = time.time()
    cur     = db.query(sql)
    res     = cur.fetchall()

    if not res:
        ## just sending a message to the terminal to let the user that the script is still working, and isn't stuck.
        if counter % 4 == 0:
            print(color_val("{0} :: ({1}) :: Still looking...".format(get_now_date(), get_hostname()), Style.BRIGHT),
                  file=sys.stderr)
        return False

    num_processes       = cur.rowcount
    if args.kill:
        kills = killah(res)
        if kills:
            user_where_str = ' AND '.join(USER_WHERE)
            print("{0}".format(color_val(get_now_date() + " :: " + get_hostname() + \
                " :: Killed: " + str(kills) + " (WHERE {0})".format(user_where_str), Fore.RED + Style.BRIGHT)))
        return

    if not args.id_only:
        print_header()

    _nums               = process_row(res)

    if args.id_only:
        ## then we're done here.
        return True

    num_reads           = _nums['num_reads']
    num_writes          = _nums['num_writes']
    num_locked          = _nums['num_locked']
    num_closing         = _nums['num_closing']
    num_opening         = _nums['num_opening']
    num_sleepers        = _nums['num_sleepers']
    num_past_long_query = _nums['num_past_long_query']
    user_count          = _nums['user_count']
    state_count         = _nums['state_count']

    ## format total processes
    if num_processes >= PROCESS_THRESHOLD_CRIT:
        num_processes = color_val(num_processes, Fore.RED)
    elif num_processes >= PROCESS_THRESHOLD_WARN:
        num_processes = color_val(num_processes, Fore.YELLOW)
    else:
        num_processes = color_val(num_processes, Fore.CYAN)

    ## format the number of queries past the long query time
    if num_past_long_query > 0:
        num_past_long_query = color_val(num_past_long_query, Fore.RED)
    else:
        num_past_long_query = color_val(num_past_long_query, Fore.CYAN)

    ## format the number of sleepers
    if num_sleepers >= SLEEPER_THRESHOLD_CRIT:
        num_sleepers = color_val(num_sleepers, Fore.RED)
    elif num_sleepers >= SLEEPER_THRESHOLD_WARN:
        num_sleepers = color_val(num_sleepers, Fore.YELLOW)
    else:
        num_sleepers = color_val(num_sleepers, Fore.CYAN)

    print("\n\t({0}) PROCESSES: {1}, SLEEPERS: {2}, LOCKED: {3}, READS: {4}, WRITES: {5}, CLOSING: {6}, OPENING: {7}, PAST LQT: {8}"
        .format(color_val(get_hostname(), Fore.GREEN), num_processes, num_sleepers, color_val(num_locked, Fore.CYAN),
            color_val(num_reads, Fore.CYAN), color_val(num_writes, Fore.CYAN), color_val(num_closing, Fore.CYAN),
            color_val(num_opening, Fore.CYAN), num_past_long_query))

    ## this is ok, but the next one sorts by occurrence
    #mystr = "{0}".format( ', '.join("%s: %s" % (k, "{0}".format(color_val(v, Fore.CYAN))) for (k, v) in user_count.iteritems()) )
    user_str = "{0}".format( ', '.join("%s: %s" % (k, "{0}".format(color_val(user_count[k], Fore.CYAN))) \
        for k in sorted(user_count, key=user_count.get, reverse=True)) )
    state_str = "{0}".format(', '.join("%s: %s" % (k, "{0}".format(color_val(state_count[k], Fore.CYAN))) \
        for k in sorted(state_count, key=state_count.get, reverse=True)))

    print("\t({0}) {1}".format(color_val("Users", Fore.GREEN), user_str))
    print("\t({0}) {1}".format(color_val("States", Fore.GREEN), state_str))
    show_processing_time(start, time.time())
    print()
    return True

def main():
    global USER_WHERE
    where           = []
    order_by        = []
    where_str       = ''
    order_by_str    = ''
    select_fields   = ['id']

    if args.id_only and args.kill:
        print(color_val("ERROR: Cannot specify id only (-i, --id) with kill!", Fore.RED + Style.BRIGHT))
        sys.exit(1)

    if args.kill and args.default:
        print(color_val("ERROR: Cannot kill using defaults!", Fore.RED + Style.BRIGHT))
        sys.exit(1)

    if args.kill:
        if not args.kill_yes:
            ans = raw_input(color_val("Are you sure you want to kill queries? ", Style.BRIGHT))
            if ans.lower() not in ('y', 'yes'):
                print("Ok, then only use --kill when you are sure you want to kill stuff.")
                sys.exit(0)

    if not args.id_only:
        select_fields.extend(['user', 'host', 'db', 'command', 'time', 'state', 'info'])

    sql = "SELECT SQL_NO_CACHE {0} FROM processlist".format(', '.join(select_fields))

    if args.default:
        #where.append("(command = 'Query' OR command = 'Connect')")
        where.append("(command != 'Sleep')")
        args.loop_second_interval   = 3
        args.ignore_system_user     = True
        args.trim_info              = True
        order_by                    = ['time ASC', 'id ASC']
    else:
        if args.command:
            where.append("command = '{0}'".format(args.command))
        if args.state:
            where.append("state = '{0}'".format(args.state))
        if args.time:
            where.append("time >= {0}".format(args.time))
        if args.database:
            where.append("db = '{0}'".format(args.database))
        if args.query:
            where.append("info LIKE '{0}%'".format(args.query))
        if args.order_by:
            order_by.append(args.order_by)
        USER_WHERE = list(where)

    if args.kill and not where:
        print(color_val("ERROR: Cannot kill without specifying criteria!", Fore.RED + Style.BRIGHT))
        sys.exit(1)

    where.append("command != 'Binlog Dump'")
    where.append("(db != 'information_schema' OR db IS NULL)") ## confuses me why I had to add OR db IS NULL

    if args.ignore_system_user == True:
        where.append("user != 'system user'")

    if where:
        where_str = ' WHERE {0}'.format(' AND '.join(where))

    if order_by:
        order_by_str = ' ORDER BY {0}'.format(', '.join(order_by))

    sql = ''.join([sql, where_str, order_by_str])

    if args.debug:
        show_processing_time(PROG_START, time.time(), 'Program Preparation')
        print("SQL: {0}".format(color_val(sql, Fore.CYAN)))

    if args.loop_second_interval > 0:
        counter = 0
        while 1:
            counter += 1
            if pslist(sql, counter):
                counter = 0

            time.sleep(args.loop_second_interval)
    else:
        pslist(sql)

## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if not HAS_COLOR:
    print("ERROR: Unable to import colorama!")
    sys.exit(1)

init()

if not HAS_MYSQL:
    print(color_val("ERROR: Unable to import pymysql!", Fore.RED + Style.BRIGHT))
    sys.exit(1)

signal.signal(signal.SIGINT, sig_handler)

args    = parse_args()

if not HAS_YAML and args.connect_config:
    print(color_val('ERROR: Unable to import yaml! You will not be able to use the config option.', Fore.RED + Style.BRIGHT))
    sys.exit(1)

db      = mydb()

LONG_QUERY_TIME     = get_long_query_time()

if __name__ == "__main__":
    main()


