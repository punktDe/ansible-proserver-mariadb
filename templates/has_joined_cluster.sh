#!/bin/sh

# Skript um einen Test solange auszuführen, bis erfolgreich oder timeout

# Konfig
# ------
# maximale Wartezeit in Sekunden
maxwait={{ mariadb.galera.join.max_wait }}
# Pause zwischen 2 Versuchen in Sekunden
pausetime={{ mariadb.galera.join.check_pause }}

starttime=`date +%s`
endtime=`expr $starttime + $maxwait`

while [ `date +%s` -lt $endtime ]
do
        if echo "SHOW STATUS LIKE 'wsrep_ready';" | mysql | grep 'ON'
        then
                exit 0
        fi
        if [ $pausetime -ge 1 ]
        then
                sleep $pausetime
        fi
done

exit 1
