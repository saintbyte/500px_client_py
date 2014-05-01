#!/usr/bin/env python
# -*- coding: utf-8
from oauth_hook import OAuthHook
import requests
from  urlparse import parse_qs
try:
    CONSUMER_KEY=(open('auth/consumer_key').read(1000)).strip()
except:
    print "put CONSUMER KEY to auth/consumer_key file"
    quit()
try:
    CONSUMER_SECRET=(open('auth/consumer_secret').read(1000)).strip()
except:
    print "put CONSUMERSECRET to auth/consumer_key file"
    quit()

px500_oauth_hook = OAuthHook(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
response = requests.post('https://api.500px.com/v1/oauth/request_token', hooks={'pre_request': px500_oauth_hook})
qs = parse_qs(response.text)
oauth_token = qs['oauth_token'][0]
oauth_secret = qs['oauth_token_secret'][0]
print "Go to https://api.500px.com/v1/oauth/authorize?oauth_token=%s allow the app and copy your PIN or oauth_verifier parametr:" % oauth_token
oauth_verifier = raw_input('Please enter your PIN:')

px500_2_oauth_hook = OAuthHook(oauth_token, oauth_secret, CONSUMER_KEY,CONSUMER_SECRET)
response = requests.post('https://api.500px.com/v1/oauth/access_token', {'oauth_verifier': oauth_verifier}, hooks={'pre_request': px500_2_oauth_hook})
response = parse_qs(response.content)
final_token = response['oauth_token'][0]
final_token_secret = response['oauth_token_secret'][0]
f = open('auth/access_token', 'w')
f.write(final_token)
f.close()
f = open('auth/access_token_secret', 'w')
f.write(final_token_secret)
f.close()
print "\n\n"
print 'access_token:'+final_token +"\n"
print 'access_token_secret:'+final_token_secret+"\n"
print "\n\n"
