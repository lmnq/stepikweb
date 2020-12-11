sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart
sudo ln -sf /home/box/web/hello.py /etc/gunicorn.d/hello.py
gunicorn -b 0.0.0.0:8080 -c etc/gunicorn.conf hello:app
sudo /etc/init.d/gunicorn restart
