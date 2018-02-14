pip install supervisor
echo_supervisord_conf > /etc/supervisord.conf
echo '[program:ams]
command = python /home/ubuntu/ams/manage.py runserver
user = ubuntu
autostart = true
autorestart = true' >> /etc/supervisord.conf