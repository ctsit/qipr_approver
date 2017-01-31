#!/bin/sh

root=$1

source /var/www/qipr_approver/venv/bin/activate

while true; do
    echo 'Finding python files.'
    targets=$(find $root -regex '.*\.py' | grep -v \#)
    echo 'Watching python files.'
    if inotifywait -e modify -e attrib -e create -e delete $targets;
    then
        echo 'Touch wsgi'
        touch /var/www/qipr/approver/qipr_approver/wsgi.py;
    fi;
    echo '==============================='
done;
