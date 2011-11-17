#!/usr/bin/bash

echo 'hello'
flag='hereismyflag'
while [ 1 == 1 ]
do
	python proxy.py ${flag} &
	sleep 2
	for pid in  `ps aux|grep ${flag}|grep -v grep|awk '{print $2}'`
	do
		echo ${pid}
		kill -9 ${pid}
	done
	echo 'kill older'
done
