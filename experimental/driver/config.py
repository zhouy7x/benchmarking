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
benchid_dict = {
    'start_stop_time': 1,
    'startup_footprint': 2,
    'require.new': 3,
    'require.cached': 4,
    'acme air throughput': 5,
    'acme air latency': 6,
    'acme air pre footprint': 7,
    'acme air post footprint': 8,
    'octane': 9,
    'dc eis latency': 10,
    'dc eis throughput': 11,
    'webtooling': 12,
    'dc eis pre footprint': 13,
    'dc eis post footprint': 14,
    'dc ssr latency': 15,
    'dc ssr throughput': 16,
    'dc ssr pre footprint': 17,
    'dc ssr post footprint': 18,
}
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
    # 1: 'intel xeon 8180',
    2: 'amd 7601',
    1: 'xeon 8180'
    }
machines = {
    'intel xeon 8180': {
              "host": "v8onxeon-8180.sh.intel.com",
              "user": "benchmark",
    },
    'amd 7601': {
        "host": "amd-7601.sh.intel.com",
        "user": "benchmark",
    },
    'xeon 8180': {
        "host": "xeon-8180.sh.intel.com",
        "user": "benchmark",
    }
}
BRANCH = "master"
NODE = "/home/benchmark/node-v13.0.0-pre/node"
