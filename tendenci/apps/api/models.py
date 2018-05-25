import simplejson

from django.db import models
from django.contrib.auth.models import User

class APIAccessKey(models.Model):
    access_id = models.CharField(max_length=50, unique=True)
    secret_key = models.CharField(max_length=50)
    client_name = models.CharField(max_length=200, default='')
    client_url = models.CharField(max_length=200, default='')

    create_dt = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name="apiaccesskey_creator",  null=True)
    update_dt = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)


class DaJiDianYu(models.Model):
    id = models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)
    form = models.CharField(max_length=6, null=True)
    form_name = models.CharField(max_length=100, null=True)
    serial_number = models.FloatField(null=True)
    entry = models.CharField(max_length=4096, null=True)


'''

CREATE TABLE api_dajidianyu (
    id serial NOT NULL,
    form varchar(6) NULL,
    form_name varchar(100) NULL,
    serial_number float NULL,
    entry varchar(2048) NULL
);
ALTER TABLE api_dajidianyu OWNER TO amsuser;
ALTER TABLE api_dajidianyu
   ADD CONSTRAINT api_dajidianyu_pkey
   PRIMARY KEY (id);
CREATE SEQUENCE api_dajidianyu_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE api_dajidianyu_id_seq OWNER TO amsuser;
ALTER SEQUENCE api_dajidianyu_id_seq OWNED BY api_dajidianyu.id;

'''

