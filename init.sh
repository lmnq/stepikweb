sudo rm -rf /etc/nginx/sites-enabled/default
sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart
sudo ln -sf /home/box/web/etc/gunicorn.conf /etc/gunicorn.d/gunicorn.conf
sudo ln -sf /home/box/web/etc/gunicorn-django.conf /etc/gunicorn.d/gunicorn-django.conf
sudo /etc/init.d/gunicorn restart
