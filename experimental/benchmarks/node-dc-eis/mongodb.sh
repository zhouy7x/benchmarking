#!/bin/bash
if [ -z "$1" ]; then
echo "Must pass in start, stop or status"
exit
fi

function kill_mongo(){
# kill mongo
/usr/bin/expect << EOF
set timeout -1
spawn /etc/init.d/mongodb stop
expect {
        "Password" {send "123\r";}
}
expect eof
EOF
}

DIR=`dirname $0`
CURRENT_DIR=`cd $DIR;pwd`
pushd $CURRENT_DIR

case $1 in
start)
#kill_mongo
rm -rf database
mkdir database
rm mongodb.out
mongod --dbpath database >> mongodb.out 2>&1 &
#while [ `grep -c "db version " mongodb.out` -lt 1 ]
while [ `grep -c "waiting for connections " mongodb.out` -lt 1 ]
do 
sleep 2
done
echo "mongo started at `date`"
;;
stop)

mongod --dbpath database  --shutdown
rm -rf database
;;
status)
ps -ef|grep mongod|grep -v grep
;;
esac
popd
