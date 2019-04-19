## Test Machine
#### Sync git repos:
```shell
rsync -a benchmark@vox.sh.intel.com:~/benchmarking /home/benchmark
```

#### Related packages 
* openssh-server (sudo apt-get install openssh-server)
* numactl
* unzip
* mongodb
* python2.7 
* pip (sudo apt install python-pip)
* numpy (pip install numpy)
* matplotlib (sudo apt-get install python-matplotlib)
* requests (pip install requests)
* eventlet (pip install eventlet)
* subprocess32 (pip install subprocess32)


## Data Machine
#### Related packages 
* mysql
* subprocess32 (pip install subprocess32)
* set auto openssh without password ($HOME/.ssh/authorized_keys)
* node (v4.x)
* npm
* logs directory (mkdir -p ~/logs)

#### Automatic login
* set auto openssh without password ($HOME/.ssh/authorized_keys)

## Steps ##

1. Auto run every Saturday:
```angular2
crontab -e
0 3 * * 6 /bin/bash  /home/benchmark/benchmarking/experimental/driver/schedule-run.sh >> /home/benchmark/logs/schedule-run.sh 2>&1 
```

2. Help of scripts:
```angular2
python dostuff.py --help   ## e.g.  python dostuff.py --benchmark=octane --branch=master --commit-id=4306300b5ea8d8c4ff3daf64c7ed5fd64055ec2f --postdata=false
python benchmarks.py --help
python builders.py --help
```  

### TODO list ###
1. cannot find dir '~/logs'.\
done.
2. postdata.py for different running host.

3. dostuff.py --help message.\
done.
4. node-dc-eis.sh -- add a kill mongod process.