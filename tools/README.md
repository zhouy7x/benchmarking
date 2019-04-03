# data machine #


## 1. machine dependencies setup

* packages
 ```shell
  sudo apt-get install libfontconfig
  sudo apt-get install mysql-server
  ```

* create user benchmark and ensure user's home directory is /home/benchmark

## 2. Database setup with mysql client
```mysql
  create database benchdb charset=utf8;
  CREATE USER 'bench1'@'localhost' IDENTIFIED BY 'xxxxxx';
  GRANT ALL PRIVILEGES ON *.* To 'bench1'@'localhost';
  use benchdb;
  create TABLE benchresults ( 
  id int(10) primary key not null auto_increment, 
  streamid INT NOT NULL, 
  benchid INT NOT NULL, 
  cset CHAR(60) NOT NULL, 
  time INT(11) NOT NULL, 
  value INT NOT NULL);
```

## 3. node (v4.x) 
* Download the lastest 4.X node version into:

/home/benchmark/node-xxxx

where xxxx is related to the version.  For example:  node-v4.2.2-linux-x64

* add symlink
```shell
ln -s /home/benchmark/node-xxxx /home/benchmark/node
export PATH=$PATH:/home/benchmark/node/bin
```


## 4. Backup setup
in /home/benchmark
create file called creds which contains

  --user=bench1 --password=xxxxxx

where bench1 is user id created in step 2) and xxxxxx is the password set for that user in 2)
make sure it is only accesible to the user

```shell
chmod 600 /home/benchmark/creds
chmod +x /home/benchmark/benchmarking/benchmarkdata/dobackup.sh
crontab -e
8 5 * * 1  /home/benchmark/benchmarking/benchmarkdata/dobackup.sh
```

## 5. Charts setup

Create the file /home/benchmark/benchmarking/tools/chartGen/dbconfig.json which includes
```text
{
  "host": "localhost",
  "user": "bench1",
  "password": "xxxxxx",
  "database": "benchdb"
}
```

Where bench1 and xxxxxx are the userid and password set in step 2)
```shell
chmod 600 /home/benchmark/benchmarking/tools/chartGen/dbconfig.json
```

## 6. Install the npm dependencies
```shell
cd  /home/benchmark/benchmarking/tools/chartGen
npm install
```

## 7. bridge setup
```shell
cp  /home/benchmark/benchmarking/tools/chartGen/dbconfig.json /home/benchmark/benchmarking/tools/acceptResults/dbconfig.json
chmod 600 /home/benchmark/benchmarking/tools/acceptResults/dbconfig.json
```

create the required keys/certs for the server
```shell
cd /home/benchmark/benchmarking/tools/acceptResults/
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem
```


create /home/benchmark/benchmarking/tools/acceptResults/authconfig.json which 
has the name/password as configured in the benchmark jobs
```text
{
  "name": "xxxxx",
  "pass": "yyyyy",
  "realm": "benchmark"
}
```

install the npm depenedencies
```shell
cd  /home/benchmark/benchmarking/tools/acceptResults
npm install
```

