benchs = [
    "start_stop_time",
    # "startup",
    "node-api",
    "acmeair",
    "octane",
    "web_tooling_benchmark",
    "node-dc-eis",
    "node-dc-ssr",
    "all"
]
branchs = [
    'master',
    'v4.x',
    'v0.12.x',
    'v6.x',
    'v7.x',
    'v8.x',
    'canary',
    'v10.x'
]
streams = {
    0: 'all',
    1: 'intel xeon 8180',
    2: 'amd 7601'
}
machines = {
    'intel xeon 8180': {
              "host": "v8onxeon-8180.sh.intel.com",
              "user": "benchmark",
    },
    'amd 7601': {
        "host": "amd-7601.sh.intel.com",
        "user": "benchmark",
    }
}
BRANCH = "master"
NODE = "/home/benchmark/node-v12.0.0-pre/node"
