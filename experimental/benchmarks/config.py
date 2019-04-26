file_name = "report.temp"
postit_dir = "/home/benchmark/benchmarking/tools/postResults"
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
streamid_dict = {
    'master': 1,
    '4.x': 2,
    '0.12.x': 3,
    '6.x': 4,
    '7.x': 5,
    '8.x': 6,
    'canary': 7,
    '10.x': 8,
}
streams = {
    1: 'intel xeon 8180',
    2: 'amd 7601'
}