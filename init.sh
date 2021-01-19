sudo /etc/init.d/mysql start
mysql -uroot -e "create database stepik_web;"
mysql -uroot -e "grant all privileges on stepik_web.* to 'box'@'localhost' with grant option;"
~/web/ask/manage.py makemigrations qa
~/web/ask/manage.py migrate qa

sudo rm -rf /etc/nginx/sites-enabled/default
sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/test.conf
sudo /etc/init.d/nginx restart
sudo ln -s /home/box/web/etc/hello.py /etc/gunicorn.d/hello.py
sudo /etc/init.d/gunicorn restart
#sudo python3 ask/manage.py runserver 0.0.0.0:8000
