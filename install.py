# coding=utf-8


from multiprocessing import Pool
from fabric.api import run, env, hosts, local, settings
from fabric.operations import put
from fabric.api import sudo
from fabric.contrib.files import exists
from fabric.exceptions import CommandTimeout
from time import sleep
import datetime
import json
import math
import os

# 远程服务器和数据库的参数
IS_FIRST_SITE_ON_THIS_SERVER = True
PGSQL_ROOT_PASSWORD = 'Ylzjfww89'
HOST = '123.206.183.58'
USER = 'ubuntu'
PASSWORD = 'Ylzjfww89'


# 以下是每个协会网站的参数
PROJECT_NAME = 'myproject'
PROJECT_DOMAIN = 'www.xxxx.com'

DB_NAME = PROJECT_NAME
DB_USER = '%suser' % PROJECT_NAME
DB_PASSWORD = 'password'
DB_HOST = 'postgres-am41dydo.sql.tencentcdb.com'
DB_PORT = '25522'

DJANGO_RUNSERVER_PORT = '8008'

EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'noreply@kunshanfa.com'
EMAIL_HOST_PASSWORD = 'EMAIL_HOST_PASSWORD'
DEFAULT_FROM_EMAIL = "noreply@kunshanfa.com"

wechatpay_appid= 'wx5ffdd61764dc7066',  # 必填,微信分配的公众账号ID
wechatpay_key= 'bdc635k2283d4a2ca477339ea8881234',  # 必填,appid 密钥
wechatpay_mchid= '1494664902',  # 必填,微信支付分配的商户号
wechatpay_appsecret= 'WECHATPAY_APPSECRET'


def myrun(command):
    with settings(prompts={'Do you want to continue [Y/n]? ': 'Y',
                           'What do you want to do about modified configuration file grub?': '2'}):
        output = run(command, pty=False)
        lines = output.split('\n')
        print(lines)


def rep_nginx_site_enable_cfg():
    template = '''
server {
    listen              443 ssl;
    listen		80;
    server_name         %s;
    ssl on;
    ssl_certificate     %s.crt;
    ssl_certificate_key %s.key;
    ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers         HIGH:!aNULL:!MD5;

    charset   utf-8;
    keepalive_timeout  165;
    client_max_body_size  30M;
    gzip_types text/css application/javascript text/javascript text/plain text/xml application/xml;
    gzip_vary on;

    root /home/ubuntu/%s;

    location /static/ {
        access_log off;
        expires 30d;
    }

    location /media/ {
        access_log off;
        expires 30d;
    }

    location ^~ /media/export/ {
        return 404;
    }

    location ~ /themes/([a-zA-Z0-9\-\_]+)/media/ {
        access_log off;
    }

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://127.0.0.1:%s/;
    }
    error_page    497    https://$server_name$request_uri;
}
    ''' % (PROJECT_DOMAIN, PROJECT_DOMAIN, PROJECT_DOMAIN, PROJECT_DOMAIN, DJANGO_RUNSERVER_PORT)
    with open(u'/tmp/%s' % PROJECT_DOMAIN, 'w') as w:
        w.write(template)
    put(u'/tmp/%s' % PROJECT_DOMAIN, u'/etc/nginx/sites-enabled/')
    myrun('ln -s /etc/ngix/sites-available/%s /etc/nginx/sites-enabled/%s' % (PROJECT_DOMAIN, PROJECT_DOMAIN))
    # TODO upload .crt .key files
    myrun('service nginx restart')


def rep_qshell_config(fold='media'):
    with open(u'qshell.config', 'r') as f:
        file = f.read()
        file.replace('www.kunshanfa.com/%s' % fold, PROJECT_DOMAIN)
        file.replace('kunshanfa/%s/' % fold, PROJECT_NAME)
        with open(u'/tmp/%s_%s.config' % (PROJECT_NAME, fold), 'w') as w:
            w.write(file)
    put('/tmp/%s_%s.config' % (PROJECT_NAME, fold), '/tmp/')


def get_secret_key():
    return PROJECT_DOMAIN.replace('.','').ljust(19, '1')


def get_site_settings_key():
    key = '%s-%s-%s-%s-%s'
    arr = PROJECT_DOMAIN.replace('.','').ljust(28, '1')
    return key % (arr[0:8], arr[9:12], arr[13:16], arr[17:20], arr[21:28])


def rep_local_settings():
    with open(u'conf/local_settings.py', 'r') as f:
        file = f.read()
        file.replace("SECRET_KEY='Qoh111VG9pq8P9hOapH'",
                     "SECRET_KEY='%s'" % get_secret_key())
        file.replace("SITE_SETTINGS_KEY='bdc635k2-283d-4a2c-a477-339ea888'",
                     "SITE_SETTINGS_KEY='%s'" % get_site_settings_key())

        file.replace("'NAME': 'ams',", "'NAME': '%s'," % DB_NAME)
        file.replace("'HOST': '172.17.0.4',", "'HOST': '%s'," % DB_HOST)
        file.replace("'USER': 'amsuser',", "'USER': '%s'," % DB_USER)
        file.replace("'PASSWORD': 'password',", "'PASSWORD': '%s'," % DB_PASSWORD)
        file.replace("'PORT': 5432,", "'PORT': %s," % DB_PORT)
        file.replace("'filename': '/var/log/tendenci/", "'filename': '/var/log/%s/" % PROJECT_NAME)
        file.replace('EMAIL_USE_SSL = True', 'EMAIL_USE_SSL = %s' % EMAIL_USE_SSL)
        file.replace("EMAIL_HOST = 'smtp.exmail.qq.com'", "EMAIL_HOST = '%s'" % EMAIL_HOST)
        file.replace('EMAIL_PORT = 465','EMAIL_PORT = %s' % EMAIL_PORT)
        file.replace("EMAIL_HOST_USER = 'noreply@kunshanfa.com'", "EMAIL_HOST_USER = '%s'" % EMAIL_HOST_USER)
        file.replace("EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']", "EMAIL_HOST_PASSWORD = %s" % EMAIL_HOST_PASSWORD)
        file.replace('DEFAULT_FROM_EMAIL = "noreply@kunshanfa.com"', 'DEFAULT_FROM_EMAIL = "%s"' % DEFAULT_FROM_EMAIL)
        with open(u'/tmp/local_settings.py', 'w') as w:
            w.write(file)

    put('/tmp/local_settings.py', '/home/ubuntu/%s/conf' % PROJECT_DOMAIN)


def rep_settings():
    with open(u'conf/settings.py', 'r') as f:
        file = f.read()
        file.replace("PROJECT_NAME = 'kunshanfa'", "PROJECT_NAME = '%s'" % PROJECT_NAME)
        # wechat pay config
        file.replace("'wechatpay_appid': 'wx5ffdd61764dc7066',", "'wechatpay_appid': '%s'," % wechatpay_appid)
        file.replace("'wechatpay_key': 'bdc635k2283d4a2ca477339ea8881234',", "'wechatpay_key': '%s'," % wechatpay_key)
        file.replace("'wechatpay_mchid': '1494664902',", "'wechatpay_mchid': '%s'," % wechatpay_mchid)
        file.replace("'wechatpay_appsecret': os.environ['WECHATPAY_APPSECRET']", "'wechatpay_appsecret': %s" %wechatpay_appsecret)
        with open(u'/tmp/settings.py', 'w') as w:
            w.write(file)
    put('/tmp/settings.py', '/home/ubuntu/%s/conf' % PROJECT_DOMAIN)


def rep_supervisor_cfg():
    cmd = '''
        echo '[program:%s]
        command = python /home/ubuntu/%s/manage.py runserver %s
        user = ubuntu
        autostart = true
        autorestart = true' >> /etc/supervisord.conf
    ''' % (PROJECT_DOMAIN, PROJECT_DOMAIN, DJANGO_RUNSERVER_PORT)
    myrun(cmd)


def rep_init_sql():
    sql = '''
        CREATE DATABASE %s;
        CREATE USER %suser WITH PASSWORD '%s';
        ALTER ROLE %suser SET client_encoding TO 'utf8';
        ALTER ROLE %suser SET default_transaction_isolation TO 'read committed';
        ALTER ROLE %suser SET timezone TO 'UTC';
        GRANT ALL PRIVILEGES ON DATABASE %s TO %suser;

        CREATE EXTENSION postgis;
        CREATE EXTENSION postgis_topology;
        CREATE EXTENSION fuzzystrmatch;
        CREATE EXTENSION postgis_tiger_geocoder;
    ''' % (DB_NAME, DB_NAME, DB_PASSWORD, DB_NAME,
           DB_NAME, DB_NAME, DB_NAME, DB_NAME)

    with open(u'/tmp/init_sql.sql', 'w') as w:
        w.write(sql)

    local("export PGPASSWORD='%s'" % PGSQL_ROOT_PASSWORD)
    local('psql -h %s -U root -d postgres -p %s -f /tmp/init_sql.sql' % (DB_HOST, DB_PORT))


def main():
    # 1个服务器只要执行1次的命令
    commands = [
        'sudo locale-gen zh_CN.UTF-8',     # ubuntu不安装中文，读写中文文件会出错
        'sudo apt-get update -y',
        ##### 'sudo apt-get upgrade -y',
        'sudo apt-get dist-upgrade -y',
        'sudo apt-get install build-essential python-dev libevent-dev libpq-dev -y',
        'sudo apt-get install libjpeg8 libjpeg-dev libfreetype6 libfreetype6-dev -y',
        'sudo apt-get install nginx git python-pip gettext -y',
        'sudo apt-get install postgresql postgresql-contrib -y',
        'sudo pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple'
        'sudo pip install supervisor -i https://pypi.tuna.tsinghua.edu.cn/simple',
        'echo_supervisord_conf > /etc/supervisord.conf',
        'sudo pip install -r /tmp/common.txt -i https://pypi.tuna.tsinghua.edu.cn/simple',
        "sudo ufw allow 'Nginx HTTP'",
        'sudo systemctl disable nginx',
        'sudo systemctl enable nginx',
    ]

    commands1 = [
        'sudo mkdir -p /var/log/%s/' % PROJECT_NAME,  # log目录

        'cd',
        #### 'git clone https://github.com/chendong0444/ams.git',     # too slowly
        #### 'sudo mv ams %s' % PROJECT_DOMAIN,
        # upload media themes files to qiniu cloud
        './home/ubuntu/qshell qupload 10 /tmp/%s_media.config' % PROJECT_NAME,
        './home/ubuntu/qshell qupload 10 /tmp/%s_themes.config' % PROJECT_NAME,
        # 'cd %s' % PROJECT_DOMAIN,

        # 'touch "conf/settings.py\nconf/local_settings.py\n" >> .gitignore',
        # 'git rm --cached conf/settings.py',
        # 'git rm --cached conf/local_settings.py',
        # 'git commit',
    ]

    commands2 = [
        'python manage.py migrate',
        'python deploy.py',
        'python manage.py load_creative_defaults',
        'chmod -R -x+X media',
        'python manage.py createsuperuser',
        'python manage.py set_theme creative',
        'cd tendenci',
        'django-admin makemessages',

    ]

    # if IS_FIRST_SITE_ON_THIS_SERVER:
    #     put('requirements/common.txt', '/tmp/common.txt')
    #     for command in commands:
    #         myrun(command)

    # rep_init_sql()
    # rep_qshell_config('media')
    # rep_qshell_config('themes')

    myrun('sudo mkdir -p /home/ubuntu/%s' % PROJECT_DOMAIN)
    # put('/home/ubuntu/demo.ams365.cn', '/home/ubuntu/%s' % PROJECT_DOMAIN, use_sudo=True)
    local('cd')
    local('tar -cvf /tmp/demo.ams365.cn.tar.gz demo.ams365.cn')
    put('/tmp/demo.ams365.cn.tar.gz', '/tmp/', use_sudo=True)
    myrun('tar -xvf /tmp/demo.ams365.cn.tar.gz demo.ams365.cn')
    myrun('sudo mv demo.ams365.cn %s' % PROJECT_DOMAIN)
    for command in commands1:
        myrun(command)

    # rep_local_settings()
    # rep_settings()
    #
    # for command in commands2:
    #     myrun(command)
    #
    # rep_nginx_site_enable_cfg()
    # rep_supervisor_cfg()


if __name__ == '__main__':
    env.host_string = HOST + ':22'
    env.user = USER
    env.password = PASSWORD

    main()