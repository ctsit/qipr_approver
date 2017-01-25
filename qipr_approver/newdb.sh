#ONLY do this if you know what you are doing
#This file will delete all your existing data but it will make the migrations
#up to date and make your database clean

sudo mysql -e "drop database qipr_approver;"
sudo mysql -e "create database qipr_approver character set utf8;"
rm -rf /var/www/qipr-approver/approver/migrations
#Need to Comment out all the urls for the approver app, else the migrations fail
pushd qipr_approver
popd
rm -rf ./approver/migrations
python3 manage.py makemigrations approver
python3 manage.py migrate
python3 manage.py loaddata ./approver/fixtures/user.json
python3 manage.py loaddata ./approver/fixtures/*
pushd qipr_approver
#Adding back the proper urls
popd

#Uncomment below line if you need a superuser for Admin login:Prompts for email,username,password
#python3 manage.py createsuperuser 
