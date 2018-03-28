# coding=utf-8


from multiprocessing import Pool
from fabric.api import run, env, hosts, local
from fabric.api import sudo
from fabric.contrib.files import exists
from fabric.exceptions import CommandTimeout
from time import sleep
import datetime
import json
import math
import os


PROJECT_NAME = 'myproject'
DOMAIN = 'www.xxxx.com'

DB_NAME = PROJECT_NAME
DB_USER = 'user'
DB_PASSWORD = 'password'
DB_HOST = '1.1.1.1'
DB_PORT = '5432'


def main():
    commands = [
        'sudo apt-get install git python-pip gettext',
        'sudo -u postgres psql -d %s -c "CREATE EXTENSION postgis;"' % DB_NAME,
        'sudo -u postgres psql -d %s -c "CREATE EXTENSION postgis_topology;"' % DB_NAME,
        'sudo -u postgres psql -d %s -c "CREATE EXTENSION fuzzystrmatch;"' % DB_NAME,
        'sudo -u postgres psql -d %s -c "CREATE EXTENSION postgis_tiger_geocoder;"' % DB_NAME,
        'cd',
        'git clone https://github.com/chendong0444/ams.git',
        'sudo mv ams %s' % DOMAIN,
        # TODO edit qshell.config
        './qshell qupload 10 qshell.config',
        'cd %s' % DOMAIN,
        # TODO edit settings.py local_settings.py
        'python manage.py migrate',
        'python deploy.py',
        'python manage.py load_creative_defaults',
        'chmod -R -x+X media',
        'python manage.py createsuperuser'
        'cd tendenci',
        'django-admin makemessages',

    ]

    for command in commands:


        output = run(command, pty=False)
        lines = output.split('\n')
        print(lines)


if __name__ == '__main__':
    HOST = '1.1.1.1'
    USER = 'user'
    PASSWORD = 'password'
    env.host_string = HOST + ':22'
    env.user = USER
    env.password = PASSWORD

    main()