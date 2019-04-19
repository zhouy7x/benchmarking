machine = {
    "host": "v8onxeon-8180.sh.intel.com",
    "user": "benchmark",
    }
benchs = [
    "octane",
    "web_tooling_benchmark",
    # "startup",
    "start_stop_time",
    "node-dc-ssr",
    "node-dc-eis",
    "node-api",
    "acmeair",
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
NODE = "/home/benchmark/node-v12.0.0-pre/bin/node"