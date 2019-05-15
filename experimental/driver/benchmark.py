# vim: set ts=4 sw=4 tw=99 et:
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
import os
import time
import utils
from config import *


class Benchmark(object):
    def __init__(self, suite, version, folder):
        self.suite = suite
        self.version = suite+" "+version
        self.folder = folder

    def run(self, submit, native, modes, includes, excludes):
        if includes != None and includes.find(self.suite) < 0:
            return
        if excludes != None and excludes.find(self.suite) >= 0:
            return
        with utils.chdir(os.path.join(utils.BenchmarkPath, self.folder)):
            return self._run(submit, native, modes)

    def omit(self, mode):
        if mode.name == 'noasmjs':
            return True
        if 'ContentShell' in mode.name:
            return True
        if 'JerryScript' in mode.name:
            return True
        if 'IoTjs' in mode.name:
            return True

    def _run(self, submit, native, modes):
        for mode in modes:
            if self.omit(mode):
                continue
            try:
                tests = None
                print('Running ' + self.version + ' under ' + mode.shell + ' ' + ' '.join(mode.args))
                beginTime = time.time()
                tests = self.benchmark(mode.shell, mode.env, mode.args)
                passTime = time.time() - beginTime
                print('Suite-Time ' + self.version + ':'), passTime
            except Exception as e:
                print('Failed to run ' + self.version + '!')
                print("Exception: " + repr(e))
                pass
            if tests:
                submit.AddTests(tests, self.suite, self.version, mode.name)


class Octane(Benchmark):
    def __init__(self):
        super(Octane, self).__init__('octane', '2.0.1', 'octane')

    def benchmark(self, shell, env, args):
        full_args = [shell]
        if args:
            full_args.extend(args)
        full_args.append('run.js')

        print(os.getcwd())
        output = utils.RunTimedCheckOutput(full_args, env=env)

        tests = []
        lines = output.splitlines()

        for x in lines:
            m = re.search("(.+): (\d+)", x)
            if not m:
                continue
            name = m.group(1)
            score = m.group(2)
            if name[0:5] == "Score":
                name = "__total__"
            tests.append({ 'name': name, 'time': score})
            print(score + '    - ' + name)

        return tests


# add WebTooling benchmark
class WebTooling(Benchmark):
    def __init__(self):
        super(WebTooling, self).__init__('WebTooling', '', 'web-tooling-benchmark')

    def benchmark(self, shell, env, args):
        full_args = [shell]
        
        if args:
            full_args.extend(args)
        full_args.append('dist/cli.js')
        
        print(os.getcwd())
        output = utils.RunTimedCheckOutput(full_args, env=env)
        
        tests = []
        lines = output.splitlines()
        print('lines=',lines)
        for x in lines:
            m = re.search("(.+):  ?(\d+\.?\d+)", x)
            if not m:
                print(x, 'is wrong!')
                continue
            name = m.group(1).lstrip()
            score = m.group(2)
            if name[0:9] == "Geometric":  # Geometric mean:  2.78 runs/sec
                name = "__total__"
            tests.append({'name':name, 'time':score}) 
            print(score + '     - '+ name)

        return tests


Benchmarks = [Octane(),
              WebTooling()
              ]

def run(submit, native, modes, includes, excludes):
    for benchmark in Benchmarks:
        benchmark.run(submit, native, modes, includes, excludes)
    submit.Finish(1)

#def run(slave, submit, native, modes):
#    slave.rpc(sys.modules[__name__], submit, native, modes, async=True)
#
#default_function = run_
if __name__ == "__main__":
    pass
