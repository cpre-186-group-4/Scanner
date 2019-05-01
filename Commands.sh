#for deleting last x files
#can't have spaces in files
#! /bin/bash
cd ~/Scans
threshold="85"
result=`df -kh |grep -v "Filesystem" | awk '{ print $5 }' | sed 's/%//g' | head -n 1`
while [ result > threshold ]
do
ls -t | tail -5 | xargs rm
result=`df -kh |grep -v "Filesystem" | awk '{ print $5 }' | sed 's/%//g' | head -n 1`
done
