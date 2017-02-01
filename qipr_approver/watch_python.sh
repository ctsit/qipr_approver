#!/bin/sh

root=$1

source /var/www/qipr_approver/venv/bin/activate

while true; do
    echo 'Finding python files.'
    targets=$(find $root -regex '.*\.py' | grep -v \#)
    echo 'Watching python files.'
    if inotifywait -e modify -e attrib -e create -e delete $targets;
    then
        echo 'Restarting Apache.'
        sudo service apache2 restart;
        echo 'Running tests.'
	python3 /var/www/qipr_approver/manage.py test
    fi;
    echo '==============================='
done;
