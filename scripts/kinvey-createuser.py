#!/usr/bin/env python
# encoding: utf-8
'''
 -- Create a Kinvy user

 Creates a user using the Kinvey REST API.

It defines classes_and_methods

@author:     Tom McLaughlin
        
@copyright:  2013 Tom McLaughlin. All rights reserved.
        
@contact:    tmclaugh@gmail.com
'''

import base64
import json
import requests

import pprint

__all__ = []
__version__ = 0.1
__date__ = '2013-03-19'
__updated__ = '2013-03-19'

KINVEY_EP = 'https://baas.kinvey.com'
KINVEY_USERS_PATH = '/user'
KINVEY_APP_ID = 'kid_eP8uJu64Hf'
KINVEY_APP_SECRET='04750b5b0cdd453ba06c03346f4b7036'

NEW_USER = 'TestUser1'
NEW_USER_PASS = 'TestPass1'

def get_encoded_str(s):
    return base64.encodestring(s).strip()

def get_app_basic_authz(app_id, app_secret):
    '''
    Take Kinvey App Key and App Secret to create Basic Authorization header
    value for operations that require app credentials 
    '''
    h = get_encoded_str('%s:%s' % (app_id, app_secret))
    return 'Basic %s' % h

def main(url, app_id, app_secret, user, passwd):
    app_authz = get_app_basic_authz(app_id, app_secret)
    body = json.dumps({'username':user, 'password':passwd})
    r = requests.post(url, data=body, headers={'Authorization':app_authz,
                                               'Content-Type':'application/json'})
    print "= REQUEST ="
    pprint.pprint('URL: %s' % r.request.url)
    pprint.pprint('Headers: %s' % str(r.request.headers))
    pprint.pprint('Body: %s' % r.request.body)
    print "\n= RESPONSE ="
    pprint.pprint('Response: %s' % r)
    pprint.pprint('Text: %s' % r.text)
    

if __name__ == "__main__":
    url = KINVEY_EP + KINVEY_USERS_PATH + '/' + KINVEY_APP_ID
    main(url, KINVEY_APP_ID, KINVEY_APP_SECRET, NEW_USER, NEW_USER_PASS)