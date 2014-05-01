#!/usr/bin/env python
# -*- coding: utf-8
from oauth_hook import OAuthHook
import requests
import json
from  urlparse import parse_qs
import MySQLdb
import string

def value_from_file(fl,default_value):
    try:
        VALUE = (open(fl).read(1000)).strip()
    except:
        VALUE = default_value
    return VALUE

try:
    CONSUMER_KEY    = (open('auth/consumer_key').read(1000)).strip()
    CONSUMER_SECRET = (open('auth/consumer_secret').read(1000)).strip()
    ACCESS_TOKEN    = (open('auth/access_token').read(1000)).strip()
    ACCESS_TOKEN_SECRET = (open('auth/access_token_secret').read(1000)).strip()
except:
    print "run auth.py first"
    quit()
LAST_ID = value_from_file('values/last_id',"")
TAG     = value_from_file('values/tag',"")
USER    = value_from_file('values/username',"ural_im")
OAuthHook.consumer_key = CONSUMER_KEY
OAuthHook.consumer_secret = CONSUMER_SECRET
oauth_hook = OAuthHook(ACCESS_TOKEN, ACCESS_TOKEN_SECRET , header_auth=True)
client = requests.session(hooks={'pre_request': oauth_hook})
response = client.get('https://api.500px.com/v1/photos?feature=user&username='+USER+'&sort=created_at&image_size=4&include_store=store_download&include_states=voted&tags=1')
results = json.loads(response.content)

mysql_login = value_from_file('auth/mysql_login','root')
mysql_password = value_from_file('auth/mysql_password','');
mysql_host     = value_from_file('auth/mysql_host','localhost');
mysql_dbname   = value_from_file('auth/mysql_dbname','');
db = MySQLdb.connect(host=mysql_host, user=mysql_login, 
                     passwd=mysql_password, db=mysql_dbname, charset='utf8')
cursor = db.cursor()

#print results
CUR_LAST_ID = str(results['photos'][0]['id'])
f = open('values/last_id', 'w')
f.write(CUR_LAST_ID)
f.close()
if (LAST_ID==""):
    quit()
for photo in results['photos']:
    if (str(photo['id']) == LAST_ID):
       print "LAST_ID is reached"
       quit()
    if (TAG != ""):
       if (TAG not in photo['tags']):
           continue
    print photo['name']
    print photo['url']
    print photo['images'][0]['url']
    print photo['description']
    print photo['tags']
    descr = """<img src="%(img)s" alt="" align="center"><br /><br />%(descr)s<br /><br />"""%{"img":photo['images'][0]['url'],"descr":photo['description']} 
    sql = """INSERT INTO posts (Title,datetime,Description,uid,moderated) VALUES ( '%(name)s', NOW( ) ,  '%(descr)s',  '10',  '1');"""%{"name":"500px.com/"+photo['name'], "descr":descr}
        # исполняем SQL-запрос
    cursor.execute(sql)
    print "\n\n\n"