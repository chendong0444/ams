# coding=utf-8


from multiprocessing import Pool
from fabric.api import run, env, hosts, local
from fabric.operations import put
from fabric.api import sudo
from fabric.contrib.files import exists
from fabric.exceptions import CommandTimeout
from time import sleep
import datetime
import json
import math
import os


PROJECT_NAME = 'myproject'
PROJECT_DOMAIN = 'www.xxxx.com'

DB_NAME = PROJECT_NAME
DB_USER = 'user'
DB_PASSWORD = 'password'
DB_HOST = '1.1.1.1'
DB_PORT = '5432'

def rep_qshell_config(fold='media'):
    with open(u'qshell.config', 'wr') as f:
        file = f.read()
        file.replace('www.kunshanfa.com/%s' % fold, PROJECT_DOMAIN)
        file.replace('kunshanfa/%/' % fold, PROJECT_NAME)
        f.write(file)

def rep_local_settings():
    with open(u'conf/local_settings.py', 'wr') as f:
        file = f.read()
        file.replace("SECRET_KEY='Qoh111VG9pq8P9hOapH'", '')
        file.replace("SITE_SETTINGS_KEY='bdc635k2-283d-4a2c-a477-339ea888'", '')

        file.replace("'NAME': 'ams',", "'NAME': '%s'," % DB_NAME)
        file.replace("'HOST': '172.17.0.4',", "'HOST': '%s'," % DB_HOST)
        file.replace("'USER': 'amsuser',", "'USER': '%s'," % DB_USER)
        file.replace("'PASSWORD': 'password',", "'PASSWORD': '%s'," % DB_PASSWORD)
        file.replace("'PORT': 5432,", "'PORT': %s," % DB_PORT)

        f.write(file)
#         con = '''
# EMAIL_USE_SSL = True
# EMAIL_HOST = 'smtp.exmail.qq.com'
# EMAIL_PORT = 465
# EMAIL_HOST_USER = 'noreply@kunshanfa.com'
# EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
# DEFAULT_FROM_EMAIL = "noreply@kunshanfa.com"
#         '''

def rep_settings():
    with open(u'conf/settings.py', 'wr') as f:
        file = f.read()
        file.replace("PROJECT_NAME = 'kunshanfa'", "PROJECT_NAME = '%s'" % PROJECT_NAME)
        # wechat pay config
        # WECHATPAY_CONFIG = {
        #     'wechatpay_appid': 'wx5ffdd61764dc7066',  # 必填,微信分配的公众账号ID
        #     'wechatpay_key': 'bdc635k2283d4a2ca477339ea8881234',  # 必填,appid 密钥
        #     'wechatpay_mchid': '1494664902',  # 必填,微信支付分配的商户号
        #     'wechatpay_appsecret': os.environ['WECHATPAY_APPSECRET']
        # }
        f.write(file)


def main():
    commands = [
        'sudo mkdir /var/log/tendenci/',   # log目录
        'sudo locale-gen zh_CN.UTF-8',     # ubuntu不安装中文，读写中文文件会出错
        'sudo apt-get update',
        'sudo apt-get dist-upgrade',
        'sudo apt-get install build-essential python-dev libevent-dev libpq-dev',
        'sudo apt-get install libjpeg8 libjpeg-dev libfreetype6 libfreetype6-dev',
        'sudo apt-get install git python-pip gettext',
        'sudo -u postgres psql -d %s -c "CREATE EXTENSION postgis;"' % DB_NAME,
        'sudo -u postgres psql -d %s -c "CREATE EXTENSION postgis_topology;"' % DB_NAME,
        'sudo -u postgres psql -d %s -c "CREATE EXTENSION fuzzystrmatch;"' % DB_NAME,
        'sudo -u postgres psql -d %s -c "CREATE EXTENSION postgis_tiger_geocoder;"' % DB_NAME,
        'cd',
        'git clone https://github.com/chendong0444/ams.git',
        'sudo mv ams %s' % PROJECT_DOMAIN,
        # upload media themes files to qiniu cloud
        './qshell qupload 10 /tmp/%s_media.config' % PROJECT_NAME,
        './qshell qupload 10 /tmp/%s_themes.config' % PROJECT_NAME,
        'cd %s' % PROJECT_DOMAIN,

        'touch "conf/settings.py\nconf/local_settings.py\n" >> .gitignore',
        'git rm --cached conf/settings.py',
        'git rm --cached conf/local_settings.py',
        'git commit',
    ]

    commands2 = [
        'python manage.py migrate',
        'python deploy.py',
        'python manage.py load_creative_defaults',
        'chmod -R -x+X media',
        'python manage.py createsuperuser'
        'cd tendenci',
        'django-admin makemessages',

    ]

    rep_qshell_config('media')
    put('qshell.config', '/tmp/%s_media' % PROJECT_NAME)
    rep_qshell_config('themes')
    put('qshell.config', '/tmp/%s_themes' % PROJECT_NAME)

    for command in commands:
        output = run(command, pty=False)
        lines = output.split('\n')
        print(lines)

    put('conf/settings.py', '/home/ubuntu/%s/conf' % PROJECT_DOMAIN)
    put('conf/local_settings.py', '/home/ubuntu/%s/conf' % PROJECT_DOMAIN)

    for command in commands2:
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