#!/bin/bash

############################################################
#author joe
#date 2013-4-12

############################################################
# 环境变量


PROJDIR="/usr/local/djblog"

RUNDIR="/var/run/djblog"
LOGDIR="/var/log/uwsgi"
PIDFILE="/var/run/djblog/djblog.pid"


CMD="/opt/uwsgi/uwsgi"

############################################################
# 配置环境


if [ ! -f $cmd ]; then
    echo "Error: not found uwsgi" ;
    exit 1 ;
fi

if [ ! -d $LOGDIR ];then
    mkdir $LOGDIR ;
    echo "create  $LOGDIR" ;
if [ ! -d $RUNDIR ];then
    mkdir $RUNDIR ;
    echo "create $RUNDIR" ;
    

# 启动命令

RUN_CMD="$CMD -x $PROJDIR/etc/uwsgi_djblog.xml";
#echo $RUN_CMD
#exit 0

case "$1" in
    'start')
        if [ -f $PIDFILE ];then
            echo "djblog already started ";
            exit 1;
        $RUN_CMD ;
        echo "djblog start successed";
    ;;
    'stop')
        kill -s kill $(cat $PIDFILE) > /dev/null 2>&1 ;
        rm -f $PIDFILE > /dev/null 2>&1 ;
        echo "djblog stop successed"
    ;;
    'restart')
        kill -s kill $(cat $PIDFILE) > /dev/null 2>&1 ;
        rm -f $PIDFILE > dev/null 2>&1 ; 
        while [ -e $PIDFILE ] ; do
            /bin/sleep 0.1 ;
        done
        $RUN_CMD ;
        echo "djblog restart successed"
    ;;
    *)
        basename=`basename "$0"`;
        echo "Usage: $basename {start|stop|restart}" ;
    exit 1 ;
    ;;
esac

exit 0 ;
