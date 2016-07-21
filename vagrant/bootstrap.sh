#!/bin/bash

export DEBIAN_FRONTEND=noninteractive
SHARED_FOLDER=/vagrant
DB_NAME=qipr_approver
DB_USER=qipr_approver

# import helper functions
. $SHARED_FOLDER/bootstrap_functions.sh

# Exit on first error
set -e

configure_base
install_utils
install_system_packages
install_qipr_approver_fresh_vm
