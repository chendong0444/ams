# coding=utf-8

from fabric.api import env, sudo, local
from fabric.operations import put
from fabric.context_managers import cd, lcd, shell_env
from fabric.contrib.files import sed


# 远程服务器和数据库的参数
IS_FIRST_SITE_ON_THIS_SERVER = True
HOST = '182.254.223.235'
USER = 'ubuntu'
PASSWORD = 'Ylzjfww89'


# 以下是每个协会网站的参数
PROJECT_NAME = 'wwwams365cn'
PROJECT_DOMAIN = 'www.ams365.cn'
# TODO 域名加A记录指向服务器IP；申请SSL证书，上传.crt .key文件
DB_NAME = PROJECT_NAME
DB_USER = '%suser' % PROJECT_NAME
DB_PASSWORD = 'password'
DB_HOST = '172.17.0.4'
DB_PORT = '5432'

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
# TODO 微信后台配置支付回调地址


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
    put(u'/tmp/%s' % PROJECT_DOMAIN, u'/etc/nginx/sites-enabled/', use_sudo=True)
    sudo('ln -s /etc/nginx/sites-enabled/%s /etc/nginx/sites-available/%s' % (PROJECT_DOMAIN, PROJECT_DOMAIN))
    # TODO upload .crt .key files
    sudo('sudo service nginx restart')

def upload_to_qiniu(fold='media'):
    with open(u'qshell.config', 'r') as f:
        file = f.read()
        file = file.replace('demo.ams365.cn/media', 'demo.ams365.cn/%s' % fold)
        file = file.replace('ams_init/media/', '%s/%s/' % (PROJECT_NAME, fold))
        with open(u'/tmp/%s_%s.config' % (PROJECT_NAME, fold), 'w') as w:
            print(file)
            w.write(file)
        # upload media themes files to qiniu cloud
        local('cd && ./qshell qupload 10 /tmp/%s_%s.config' % (PROJECT_NAME, fold))


def get_secret_key():
    return PROJECT_DOMAIN.replace('.','').ljust(19, '1')


def get_site_settings_key():
    key = '%s-%s-%s-%s-%s'
    arr = PROJECT_DOMAIN.replace('.','').ljust(28, '1')
    return key % (arr[0:8], arr[8:12], arr[12:16], arr[16:20], arr[20:28])


def rep_local_settings():
    with open(u'conf/local_settings.py', 'r') as f:
        file = f.read()
        file = file.replace("SECRET_KEY='demoams365cn1111111'",
                     "SECRET_KEY='%s'" % get_secret_key())
        # 如果数据库从demo直接恢复，不能修改此2值。数据库数据加密会用此2值，修改会不能解密
        # file = file.replace("SITE_SETTINGS_KEY='demoams3-65cn-1111-1111-11111111'",
        #              "SITE_SETTINGS_KEY='%s'" % get_site_settings_key())
        file = file.replace("'NAME': 'myproject',", "'NAME': '%s'," % DB_NAME)
        file = file.replace("'USER': 'myprojectuser',", "'USER': '%s'," % DB_USER)
        file = file.replace("'PASSWORD': 'password',", "'PASSWORD': '%s'," % DB_PASSWORD)
        file = file.replace("'PORT': 5432,", "'PORT': %s," % DB_PORT)
        file = file.replace("'filename': '/var/log/tendenci/", "'filename': '/var/log/%s/" % PROJECT_NAME)
        file = file.replace('EMAIL_USE_SSL = True', 'EMAIL_USE_SSL = %s' % EMAIL_USE_SSL)
        file = file.replace("EMAIL_HOST = 'smtp.exmail.qq.com'", "EMAIL_HOST = '%s'" % EMAIL_HOST)
        file = file.replace('EMAIL_PORT = 465','EMAIL_PORT = %s' % EMAIL_PORT)
        file = file.replace("EMAIL_HOST_USER = 'noreply@kunshanfa.com'", "EMAIL_HOST_USER = '%s'" % EMAIL_HOST_USER)
        file = file.replace("EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']", "EMAIL_HOST_PASSWORD = '%s'" % EMAIL_HOST_PASSWORD)
        file = file.replace('DEFAULT_FROM_EMAIL = "noreply@kunshanfa.com"', 'DEFAULT_FROM_EMAIL = "%s"' % DEFAULT_FROM_EMAIL)
        with open(u'/tmp/local_settings.py', 'w') as w:
            w.write(file)
    put('/tmp/local_settings.py', '/home/ubuntu/%s/conf' % PROJECT_DOMAIN)


def rep_settings():
    with open(u'conf/settings.py', 'r') as f:
        file = f.read()
        file = file.replace("PROJECT_NAME = 'kunshanfa'", "PROJECT_NAME = '%s'" % PROJECT_NAME)
        # wechat pay config
        file = file.replace("'wechatpay_appid': 'wx5ffdd61764dc7066',", "'wechatpay_appid': '%s'," % wechatpay_appid)
        file = file.replace("'wechatpay_key': 'bdc635k2283d4a2ca477339ea8881234',", "'wechatpay_key': '%s'," % wechatpay_key)
        file = file.replace("'wechatpay_mchid': '1494664902',", "'wechatpay_mchid': '%s'," % wechatpay_mchid)
        file = file.replace("'wechatpay_appsecret': os.environ['WECHATPAY_APPSECRET']", "'wechatpay_appsecret': '%s'" %wechatpay_appsecret)
        with open(u'/tmp/settings.py', 'w') as w:
            w.write(file)
    put('/tmp/settings.py', '/home/ubuntu/%s/conf' % PROJECT_DOMAIN)


def rep_supervisor_cfg():
    cmd = '''
echo '[program:%s]
command = gunicorn -w 2 -b 127.0.0.1:%s conf.wsgi:application
directory = /home/ubuntu/%s
user = root
autostart = true
autorestart = true
environment=QINIU_SECRET_KEY="jQAztrxkav_TR0jQeFctik9aZFbrAAHKzdxm5kPW",
EMAIL_HOST_PASSWORD="%s",
WECHATPAY_APPSECRET="%s"' >> /etc/supervisor/conf.d/%s.conf
    ''' % (PROJECT_DOMAIN, DJANGO_RUNSERVER_PORT, PROJECT_DOMAIN,
           EMAIL_HOST_PASSWORD, wechatpay_appsecret, PROJECT_DOMAIN)
    sudo(cmd)

    # sed('/lib/systemd/system/supervisor.service',
    #     'ExecStart=/usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf',
    #     'ExecStart=/usr/bin/supervisord -c /etc/supervisor/supervisord.conf', use_sudo=True)
    # sudo('sudo systemctl daemon-reload', user='root')



def init_db():
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

    local('psql -h %s -U root -d postgres -p %s -f /tmp/init_sql.sql' % (DB_HOST, DB_PORT))
    with lcd('~/pg_dump'):
        #### local('pg_dump -h 172.17.0.4 -U myprojectuser myproject > backup.sql')
        local('psql -h %s -p %s -U %suser %s < backup.sql' % (DB_HOST, DB_PORT, PROJECT_NAME, PROJECT_NAME))


def main():
    # 1个服务器只要执行1次的命令
    commands = [
        'locale-gen zh_CN.UTF-8',     # ubuntu不安装中文，读写中文文件会出错
        'apt-get update -y',
        'apt-get install build-essential python-dev libevent-dev libpq-dev -y',
        'apt-get install libjpeg8 libjpeg-dev libfreetype6 libfreetype6-dev -y',
        'apt-get install openssh-server memcached libmemcached-dev nginx git -y',
        'apt-get install python-pip gettext postgresql postgresql-contrib -y',
        'apt-get install binutils libproj-dev gdal-bin supervisor -y',
        # 'pip install --upgrade pip',
        'sudo pip install -r /tmp/common.txt -i https://pypi.tuna.tsinghua.edu.cn/simple',
        "ufw allow 'Nginx HTTP'",
        'systemctl disable nginx',
        'systemctl enable nginx',
        'service supervisor start',
        # 'apt-get install postfix -y',
    ]

    commands1 = [
        # 'tar -xzvf /tmp/demo.ams365.cn.tar.gz demo.ams365.cn',
        # 'mv demo.ams365.cn %s' % PROJECT_DOMAIN,
        'mkdir -p /var/log/%s/' % PROJECT_NAME,  # log目录
        'touch /var/log/%s/app.log' % PROJECT_NAME,
        'touch /var/log/%s/debug.log' % PROJECT_NAME,
        'chmod 777 /var/log/%s/app.log' % PROJECT_NAME,
        'chmod 777 /var/log/%s/debug.log' % PROJECT_NAME,
    ]

    commands2 = [
        #####   find . ./*/migrations|xargs rm -rf
        # 'python manage.py makemigrations',
        # 'python manage.py migrate',
        # 'python manage.py collectstatic',
        # 'python deploy.py',
        # 'python manage.py load_creative_defaults',
        'chmod -R -x+X media',
        # 'python manage.py createsuperuser',
        # 'python manage.py set_theme creative',
        'echo "30 2 * * * python ~/%s/manage.py run_nightly_commands" >> /var/spool/cron/crontabs/ubuntu' % PROJECT_DOMAIN,
        'echo "*/60 * * * * python ~/%s/manage.py process_unindexed" >> /var/spool/cron/crontabs/ubuntu' % PROJECT_DOMAIN,
        # 'python manage.py runserver %s' % DJANGO_RUNSERVER_PORT,
    ]

    if IS_FIRST_SITE_ON_THIS_SERVER:
        put('requirements/common.txt', '/tmp/common.txt')
        for command in commands:
            sudo(command)
        sed('/etc/memcached.conf', '-m 64', '-m 256', use_sudo=True)
        sudo('systemctl restart memcached')

    init_db()

    static = ['static', 'media', 'themes']
    for s in static:
        upload_to_qiniu(s)

    local('cd && tar -czvf /tmp/demo.ams365.cn.tar.gz demo.ams365.cn')

    put('/tmp/demo.ams365.cn.tar.gz', '/tmp/', use_sudo=True)

    for command in commands1:
        sudo(command)

    rep_local_settings()

    rep_settings()

    rep_supervisor_cfg()

    with shell_env(QINIU_SECRET_KEY="jQAztrxkav_TR0jQeFctik9aZFbrAAHKzdxm5kPW",
                   EMAIL_HOST_PASSWORD="%s" % EMAIL_HOST_PASSWORD,
                   WECHATPAY_APPSECRET='%s' % wechatpay_appsecret):
        with cd('~/%s' % PROJECT_DOMAIN):
            for command in commands2:
                sudo(command)
            sudo('sudo service supervisor restart')

    rep_nginx_site_enable_cfg()


if __name__ == '__main__':
    env.host_string = HOST + ':22'
    env.user = USER
    env.password = PASSWORD

    main()
