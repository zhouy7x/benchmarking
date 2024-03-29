# vim: set ts=4 sw=4 tw=99 et:
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys
import commands
import subprocess
import signal
import ConfigParser

config = None
RepoPath = None
BenchmarkPath = None
DriverPath = None
Timeout = 30*60
PythonName = None
Includes = None
Excludes = None


def InitConfig(name):
    global config, RepoPath, BenchmarkPath, DriverPath, Timeout, PythonName, Includes, Excludes
    config = ConfigParser.RawConfigParser()
    if not os.path.isfile(name):
        raise Exception('could not find file: ' + name)
    config.read(name)
    RepoPath = config.get('main', 'repos')
    BenchmarkPath = config.get('main', 'benchmarks')
    DriverPath = config_get_default('main', 'driver', os.getcwd())
    Timeout = config_get_default('main', 'timeout', str(Timeout))
    # silly hack to allow 30*60 in the config file.
    Timeout = eval(Timeout, {}, {})
    PythonName = config_get_default(name, 'python', sys.executable)
    Includes = config_get_default(name, 'includes', None)
    Excludes = config_get_default(name, 'excludes', None)


class FolderChanger:
    def __init__(self, folder):
        self.old = os.getcwd()
        self.new = folder

    def __enter__(self):
        os.chdir(self.new)

    def __exit__(self, type, value, traceback):
        os.chdir(self.old)


def chdir(folder):
    return FolderChanger(folder)


def check_folder(foo):
    def _inside(folder):
        if os.path.exists(folder):
            return
        foo(folder)
    return _inside


@check_folder
def mkdir(folder):
    print(">> mkdir %s" % folder)
    Run(['mkdir', '-p', folder])


def Run(vec, env=os.environ.copy()):
    print(">> Executing in " + os.getcwd())
    print(' '.join(vec))
    # print("with: " + str(env))
    try:
        o = subprocess.check_output(vec, stderr=subprocess.STDOUT, env=env)
    except subprocess.CalledProcessError as e:
        print 'output was: ' + e.output
        print e
        raise e
    o = o.decode("utf-8")
    try:
        print(o)
    except:
        print("print exception...")
    return o


def Shell(string):
    print(string)
    status, output = commands.getstatusoutput(string)
    print(output)
    return status, output


def config_get_default(section, name, default=None):
    if config.has_option(section, name):
        return config.get(section, name)
    return default


class TimeException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeException()


class Handler:
    def __init__(self, signum, lam):
        self.signum = signum
        self.lam = lam
        self.old = None

    def __enter__(self):
        self.old = signal.signal(self.signum, self.lam)

    def __exit__(self, type, value, traceback):
        signal.signal(self.signum, self.old)
        
    
def RunTimedCheckOutput(args, env=os.environ.copy(), timeout=None, **popenargs):
    if timeout is None:
        timeout = Timeout
    if type(args) == list:
        print('Running: "' + '" "'.join(args) + '" with timeout: ' + str(timeout)+'s')
    elif type(args) == str:
        print('Running: "' + args + '" with timeout: ' + str(timeout) + 's')
    else:
        print('Running: ' + args)
    try:
        if type(args) == list:
            print("list......................")
            p = subprocess.Popen(args, bufsize=-1,  env=env, close_fds=True, preexec_fn=os.setsid, 
                    stdout=subprocess.PIPE, **popenargs)

            with Handler(signal.SIGALRM, timeout_handler):
                try:
                    signal.alarm(timeout)
                    output = p.communicate()[0]
                    # if we get an alarm right here, nothing too bad should happen
                    signal.alarm(0)
                    if p.returncode:
                        print "ERROR: returned" + str(p.returncode)
                except TimeException:
                    # make sure it is no longer running
                    # p.kill()
                    os.killpg(p.pid, signal.SIGINT)
                    # in case someone looks at the logs...
                    print ("WARNING: Timed Out 1st.")
                    # try to get any partial output
                    output = p.communicate()[0]
                    print ('output 1st =', output)

                    # try again.
                    p = subprocess.Popen(args, bufsize=-1, shell=True, env=env, close_fds=True,
                                             preexec_fn=os.setsid,
                                             stdout=subprocess.PIPE, **popenargs)
                    try:
                        signal.alarm(timeout)
                        output = p.communicate()[0]
                        # if we get an alarm right here, nothing too bad should happen
                        signal.alarm(0)
                        if p.returncode:
                            print "ERROR: returned" + str(p.returncode)
                    except TimeException:
                        # make sure it is no longer running
                        # p.kill()
                        os.killpg(p.pid, signal.SIGINT)
                        # in case someone looks at the logs...
                        print ("WARNING: Timed Out 2nd.")
                        # try to get any partial output
                        output = p.communicate()[0]

        else:
            import subprocess32
            p = subprocess32.Popen(args, bufsize=-1, shell=True, env=env, close_fds=True, preexec_fn=os.setsid,
                    stdout=subprocess.PIPE, **popenargs)
            #with Handler(signal.SIGALRM, timeout_handler):
            try:
                output = p.communicate(timeout=timeout)[0]
                # if we get an alarm right here, nothing too bad should happen
                if p.returncode:
                    print "ERROR: returned" + str(p.returncode)
            except subprocess32.TimeoutExpired:
                # make sure it is no longer running
                # p.kill()
                os.killpg(p.pid, signal.SIGINT)
                # in case someone looks at the logs...
                print ("WARNING: Timed Out 1st.")
                # try to get any partial output
                output = p.communicate()[0]
                print ('output 1st =',output)

                # try again.
                p = subprocess32.Popen(args, bufsize=-1, shell=True, env=env, close_fds=True, preexec_fn=os.setsid,
                            stdout=subprocess.PIPE, **popenargs)
                try:
                    output = p.communicate(timeout=timeout)[0]
                    # if we get an alarm right here, nothing too bad should happen
                    if p.returncode:
                        print "ERROR: returned" + str(p.returncode)
                except subprocess32.TimeoutExpired:
                    # make sure it is no longer running
                    # p.kill()
                    os.killpg(p.pid, signal.SIGINT)
                    # in case someone looks at the logs...
                    print ("WARNING: Timed Out 2nd.")
                    # try to get any partial output
                    output = p.communicate()[0]

        print ('output final =',output)
        return output
    except Exception as e:
        pass

