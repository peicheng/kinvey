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

import argparse
import base64
import json
import requests

import pprint
import sys

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

def get_app_kinvey_authz(token):
    return 'Kinvey %s' % token

def app_login(url, app_id, app_secret, user, passwd):
    '''
    Logs in user and returns the _id and authtoken.
    
    app_login(url, app_id, app_secret, user, passwd) -> (_id, authtoken)
    '''
    app_authz = get_app_basic_authz(app_id, app_secret)
    body = json.dumps({'username':user, 'password':passwd})
    r = requests.post(url + '/login', data=body, headers={'Authorization':app_authz,
                                                          'Content-Type':'application/json'})
    response_info = json.loads(r.text)
    user_id = response_info['_id']
    authtoken = response_info['_kmd']['authtoken']
    return (user_id, authtoken)

def app_logout(url, user_authz):
    logout_r = requests.post(url + '/_logout', headers={'Authorization':user_authz,
                                                        'Content-Type':'application/json'})

def print_json(data):
    '''
    Print JSON data.
    '''
    # NOTE: Stub until I have something nicer.
    pprint.pprint(data)

def create_user(url, app_id, app_secret, user, passwd):
    '''
    Create a new application user.
    '''
    app_authz = get_app_basic_authz(app_id, app_secret)
    body = json.dumps({'username':user, 'password':passwd})
    r = requests.post(url, data=body, headers={'Authorization':app_authz,
                                               'Content-Type':'application/json'})
    
    response_info = json.loads(r.text)
    
    if r.ok:
        print('== Success ==')
        for key in response_info.keys():
            value = response_info[key]
            # There should be a better way than testing if we have a
            # unicode string.
            if type(value) is unicode:
                print('%s: %s' % (key, value))
            else:
                print('%s:' % key)
                for sub_key in response_info[key].keys():
                    print('  %s: %s' % (sub_key, response_info[key][sub_key]))
        
    else:
        print('== Error ==')
        for key in response_info.keys():
            print('%s: %s' % (key, response_info[key]))

def me_user(url, app_id, app_secret, user, passwd):
    '''
    Return logged in user's info
    '''
    user_id, auth_token = app_login(url, app_id, app_secret, user, passwd)
    user_authz = get_app_kinvey_authz(auth_token)
    r = requests.get(url + '/_me', headers={'Authorization':user_authz,
                                            'Content-Type':'application/json'})
    response_info = json.loads(r.text)
    print_json(response_info)
    app_logout(url, user_authz)

def update_user(url, app_id, app_secret, user, passwd, field, value):
    '''
    Alter an attribute on a user.
    '''
    # Login user using application creds.
    user_id, auth_token = app_login(url, app_id, app_secret, user, passwd)
    user_authz = get_app_kinvey_authz(auth_token)
    
    # Alter the value on our user
    body = json.dumps({field:value})
    alter_r = requests.put(url + '/' + user_id, data=body,
                           headers={'Authorization':user_authz,
                                    'Content-Type':'application/json'})
    
    # Logout
    app_logout(url, user_authz)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['create', 'update', 'retrieve', 'me', 'lookup', 'delete'],
                        help="action to perform")
    # Common args
    parser.add_argument("-u", "--user", dest='user', default=NEW_USER, help="Username to add.")
    parser.add_argument("-p", "--password", dest='passwd', default=NEW_USER_PASS, help="User's password")
    
    # alter args
    parser.add_argument('-f', '--field', dest='field', help='Field to alter.')
    parser.add_argument('-v', '--value', dest='field_value', help='Value to alter field to.')

    # And now compile them all.
    args = parser.parse_args()
    
    url = KINVEY_EP + KINVEY_USERS_PATH + '/' + KINVEY_APP_ID
    if args.action == 'create':
        create_user(url, KINVEY_APP_ID, KINVEY_APP_SECRET, args.user, args.passwd)
    elif args.action == 'update':
        update_user(url, KINVEY_APP_ID, KINVEY_APP_SECRET, args.user, args.passwd, args.field, args.field_value)
    elif args.action == 'me':
        me_user(url, KINVEY_APP_ID, KINVEY_APP_SECRET, args.user, args.passwd)
        
    sys.exit(0)