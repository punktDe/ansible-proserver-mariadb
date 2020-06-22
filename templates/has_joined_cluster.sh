#!/bin/sh

# Check if cluster node is ready and has

# Config
# ------
total_maxwait_seconds={{ mariadb.galera.join.max_wait }}
# Pause zwischen 2 Versuchen in Sekunden
sleeptime_seconds={{ mariadb.galera.join.check_pause }}

starttime=`date +%s`
endtime=`expr $starttime + $total_maxwait_seconds`

while [ `date +%s` -lt $endtime ]
do
    if echo "SHOW STATUS LIKE 'wsrep_ready';" | mysql | grep 'ON'
    then
            exit 0
    fi
    if [ $sleeptime_seconds -ge 1 ]
    then
            sleep $sleeptime_sleeptime_seconds
    fi
done

exit 1
