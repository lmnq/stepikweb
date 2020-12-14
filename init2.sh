sudo /etc/init.d/mysql start
mysql -uroot -e "create database stepik_web;"
mysql -uroot -e "grant all privileges on stepik_web.* to 'box'@'localhost' with grant option;"
~/web/ask/manage.py makemigrations qa
~/web/ask/manage.py migrate qa
