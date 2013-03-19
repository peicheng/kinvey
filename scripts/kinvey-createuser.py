#!/usr/bin/env python
# encoding: utf-8
'''
 -- shortdesc

 is a description

It defines classes_and_methods

@author:     Tom McLaughlin
        
@copyright:  2013 Tom McLaughlin. All rights reserved.
        
@contact:    tmclaugh@gmail.com
'''

import sys
import os

import argparse
import base64
import json
import requests

__all__ = []
__version__ = 0.1
__date__ = '2013-03-19'
__updated__ = '2013-03-19'

KINVEY_EP = 'https://baas.kinvey.com'
KINVEY_APP_ID = 'kid_eP8uJu64Hf'
KINVEY_APP_SECRET = '04750b5b0cdd453ba06c03346f4b7036'

def get_app_auth_str(app_id, app_secret):
    return base64.encodestring('%s:%s' % (app_id, app_secret))

def main(user, passwd):
    authz_str = 'Basic %s' % get_app_auth_str(KINVEY_APP_ID, KINVEY_APP_SECRET)
    data = json.dumps({'username':user, 'password':passwd})
    user_url = '%s/user/%s' % (KINVEY_EP, KINVEY_APP_ID)
    # No sure why getting:
    # '{"error":"This app backend not found"}'
    requests.post(user_url, payload=data, headers={'Authorization':authz_str, 'Content-Type':'application/json'})

if __name__ == "__main__":
    pass