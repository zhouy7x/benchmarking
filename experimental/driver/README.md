## Test Machine
#### System
* ubuntu server 16.04.6 LTS

#### Source
* benchmarking
```shell
rsync -a benchmark@vox.sh.intel.com:~/benchmarking /home/benchmark
```

#### Related packages 
* openssh-server (sudo apt-get install openssh-server)
* numactl
* unzip
* mongodb
* python2.7 
* gcc=5.4
* g++=5.4
* java=1.7
* bc (sudo apt-get install bc)
* pip (sudo apt install python-pip)
* numpy (pip install numpy)
* matplotlib (sudo apt-get install python-matplotlib)
* requests (pip install requests)
* eventlet (pip install eventlet)
* subprocess32 (pip install subprocess32)
* expect


## Data Machine
#### System
* ubuntu 16.04 LTS

#### Source
* benchmarking
```shell
git clone https://github.com/zhouy7x/benchmarking.git
```

* log file directory
```shell
mkdir -p ~/logs
``` 

#### Automatic login
* set authorized keys
```shell
ssh-keygen
ssh-copy-id -i ~/.ssh/id_rsa.pub username@hostname
```

#### Related packages 
* mysql-server
* gcc=5.4
* g++=5.4
* subprocess32 (pip install subprocess32)
* node (v4.x)
* npm

## Steps ##

1. Auto run every Saturday:
```shell
crontab -e
```
then add this line:
```text
0 3 * * 6 /bin/bash  /home/benchmark/benchmarking/experimental/driver/schedule-run.sh >> /home/benchmark/logs/schedule-run.sh 2>&1 
````

2. Guide of scripts:
```shell
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