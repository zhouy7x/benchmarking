#!/usr/bin/python

import utils


def run_update():
    shell = "bash /home/benchmark/benchmarking/tools/chartGen/chartcron.sh"
    stat, ret = utils.Shell(shell)
    return stat


if __name__ == '__main__':
    run_update()
