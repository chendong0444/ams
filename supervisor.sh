pip install supervisor
echo_supervisord_conf > /etc/supervisord.conf
echo '[program:ams]
command = python /home/ubuntu/ams/manage.py runserver
user = ubuntu
autostart = true
autorestart = true' >> /etc/supervisord.conf


python manage.py dumpdata --indent 2 --exclude=files.MultipleFile --exclude=events.StandardRegForm --exclude=help_files> ams.json
python manage.py dumpdata --indent 2 --exclude=files.MultipleFile --exclude=events.StandardRegForm --exclude=help_files --natural-foreign --natural-primary > ams.json