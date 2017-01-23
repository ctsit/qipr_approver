#!/bin/bash

function log() {
    echo -n "Log: "
    echo $*
}

function configure_base() {
   # Use local time so we don't have to do math when looking thru logs
   echo "US/Eastern" > /etc/timezone
   dpkg-reconfigure tzdata

   # Update packages
   apt-get update -y
   #apt-get upgrade -y
}

function install_utils() {
   cp $SHARED_FOLDER/dot_files/aliases /home/vagrant/.bash_aliases
   cp $SHARED_FOLDER/dot_files/aliases /root/.bash_aliases

   cp $SHARED_FOLDER/dot_files/vimrc /home/vagrant/.vimrc
   cp $SHARED_FOLDER/dot_files/vimrc /root/.vimrc

   apt-get install -y vim ack-grep nmap
}

function install_system_packages() {
    apt-get install -y \
        libssl-dev \
        apache2 apache2-dev libapache2-mod-wsgi-py3 \
        python3-dev python3-pip \
        mysql-server libmysqlclient-dev \
        libffi-dev \
        inotify-tools \
        libsqlite3-dev;

    pip3 install virtualenv
}

function create_virtualenv() {
    log "Creating virtual environment"
    virtualenv venv
}

function pip_dependencies() {
    log "Activating virtual environment"
    source venv/bin/activate

    log "Installing dependencies"
    pip3 install -r requirements.txt

    log "Leaving virtual environment"
    deactivate
}

function create_database() {
    log "Initial database setup"
    mysql -u root -e "CREATE DATABASE qipr_approver CHARACTER SET utf8"
}

function apache_setup() {
    log "Stop apache in order to disable the default site"
    service apache2 stop
    a2dissite 000-default

    log "Link config files for apache port 80"
    ln -sfv /vagrant/apache.conf /etc/apache2/sites-available/qipr_approver.conf
    ln -sfv /vagrant/apache.conf /etc/apache2/sites-enabled/qipr_approver.conf

    log "Restaring Apache with new config..."
    sleep 2
    service apache2 start
}

function migrate_application_database () {
    source venv/bin/activate
    python3 manage.py migrate
    deactivate
}

function apply_fixtures() {
    source venv/bin/activate
    python3 manage.py loaddata ./approver/fixtures/user.json
    python3 manage.py loaddata ./approver/fixtures/*
    deactivate
}

function handle_static_files() {
    source venv/bin/activate
    python3 manage.py collectstatic
    deactivate
}

function copy_settings_example() {
    pushd /var/www/qipr/approver/qipr_approver/deploy
    if [ -e settings.ini ]; then
        echo "settings.ini already defined"
    else
        echo "settings.ini created from settings.example.ini"
        cp settings.example.ini settings.ini
    fi
    popd
}

function install_qipr_approver_fresh_vm () {
    pushd /var/www/qipr/approver
        create_virtualenv
        pip_dependencies
        create_database
        migrate_application_database
        apply_fixtures
        handle_static_files
        apache_setup
    popd
}

function install_qipr_approver() {
    pushd /var/www/qipr/approver
        create_virtualenv
        pip_dependencies
        migrate_application_database
        apply_fixtures
        handle_static_files
    popd
}
