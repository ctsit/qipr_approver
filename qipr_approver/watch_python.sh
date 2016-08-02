#!/bin/sh

root=$1

while true; do
    echo 'Finding python files.'
    targets=$(find $root -regex '.*\.py' | grep -v \#)
    echo 'Watching python files.'
    if inotifywait $targets;
    then
        echo 'Restarting Apache.'
        sudo service apache2 restart;
    fi;
    echo '==============================='
done;
