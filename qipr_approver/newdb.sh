#ONLY do this if you know what you are doing
#This file will delete all your existing data but it will make the migrations
#up to date and make your database clean

sudo mysql -u qipr_a_admin_api -p -e "drop database qipr_approver;"
sudo mysql -u qipr_a_admin_api -p -e "create database qipr_approver character set utf8;"
sudo rm -rf /var/www/qipr-approver/approver/migrations
#Need to Comment out all the urls for the approver app, else the migrations fail
pushd qipr_approver
sudo cp urls.py temp_urls.py
sudo rm urls.py
sudo cp migration_urls.py urls.py
popd
sudo rm -rf ./approver/migrations
sudo python3 manage.py makemigrations approver
sudo python3 manage.py migrate
sudo python3 manage.py loaddata ./approver/fixtures/user.json
sudo python3 manage.py loaddata ./approver/fixtures/*
sudo pushd qipr_approver
#Adding back the proper urls
sudo rm urls.py
sudo cp temp_urls.py urls.py
sudo rm temp_urls.py
popd

#Uncomment below line if you need a superuser for Admin login:Prompts for email,username,password
#python3 manage.py createsuperuser 
