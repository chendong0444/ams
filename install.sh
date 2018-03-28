
PROJECT_NAME='myproject'
DOMAIN='www.xxxx.com'

sudo apt-get install git
sudo apt-get install python-pip
sudo apt-get install gettext

sudo -u postgres psql -d $DB_NAME -c "CREATE EXTENSION postgis;"
sudo -u postgres psql -d $DB_NAME -c "CREATE EXTENSION postgis_topology;"
sudo -u postgres psql -d $DB_NAME -c "CREATE EXTENSION fuzzystrmatch;"
sudo -u postgres psql -d $DB_NAME -c "CREATE EXTENSION postgis_tiger_geocoder;"


cd
git clone https://github.com/chendong0444/ams.git
sudo mv ams $DOMAIN
cd $DOMAIN

touch "
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myproject',
        'USER': 'myprojectuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}
" >> conf/local_settings.py


python manage.py migrate
python deploy.py
python manage.py load_creative_defaults
chmod -R -x+X media

cd tendenci
django-admin makemessages