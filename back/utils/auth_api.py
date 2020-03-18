import os
import sys

from urllib.parse import quote, urlencode

import requests
import json
import base64
import time
from uuid import uuid4, uuid1
from flask import Flask, request, redirect, session, url_for
import config as CONF
#from microsoftgraph.client import Client
authorize_url = '{0}{1}'.format(CONF.GRAPH_ENDPOINT['APP_URL_AUTH'], '/?{0}')

def get_signin_url(redirect_uri):
   # Build the query parameters for the signin url
   headers = { 'content-type': 'application/json' }
   params = {
      'client_id': CONF.GRAPH_SETUP['APP_CLIENT_ID'],
      'redirect_uri': redirect_uri,
      'cache_state': False,
      'response_type': 'code',
      'scope': ' '.join(str(i) for i in CONF.GRAPH_SETUP['APP_SCOPES'])
   }
   try:
      response_signin_url = authorize_url.format(urlencode(params))
   except ValueError as e:
      return "Error!", 200
   return response_signin_url, 200

def get_token_from_code(
   auth_code,
   redirect_uri
):
   # Build the post form for the token request
   post_data = {
      'grant_type': 'authorization_code',
      'code': auth_code,
      'cache_state': False,
      'redirect_uri': redirect_uri,
      'scope': ' '.join(str(i) for i in CONF.GRAPH_SETUP['APP_SCOPES']),
      'client_id': CONF.GRAPH_SETUP['APP_CLIENT_ID'],
      'client_secret': CONF.GRAPH_SETUP['APP_CLIENT_SECRET']
   }
   r = requests.post(CONF.GRAPH_ENDPOINT['APP_URL_TOKEN'], data = post_data)
   try:
      #return r.json()
      if r.json().get("access_token") != None:
         return r.json().get("access_token"), r.json().get("refresh_token")
      else:
         return r
   except Exception as e:
      return 'Error retrieving token: {0} - {1}'.format(r.status_code, r.text)

def get_token_from_refresh_token(
   refresh_token,
   redirect_uri
):
   # Build the post form for the token request
   post_data = {
      'grant_type': 'refresh_token',
      'refresh_token': refresh_token,
      'redirect_uri': redirect_uri,
      'scope': ' '.join(str(i) for i in CONF.GRAPH_SETUP['APP_SCOPES']),
      'client_id': CONF.GRAPH_SETUP['APP_CLIENT_ID'],
      'client_secret': CONF.GRAPH_SETUP['APP_CLIENT_SECRET']
   }
              
   r = requests.post(CONF.GRAPH_ENDPOINT['APP_URL_TOKEN'], data = post_data)
   try:
      return r.json().get("access_token"), r.json().get("refresh_token")
   except:
      return 'Error retrieving token: {0} - {1}'.format(r.status_code, r.text)

def get_access_token(request, redirect_uri):
  current_token = request.session['access_token']
  expiration = request.session['token_expires']
  now = int(time.time())
  if (current_token and now < expiration):
    # Token still valid
    return current_token
  else:
    # Token expired
    refresh_token = request.session['refresh_token']
    new_tokens = get_token_from_refresh_token(refresh_token, redirect_uri)

    # Update session
    # expires_in is in seconds
    # Get current timestamp (seconds since Unix Epoch) and
    # add expires_in to get expiration time
    # Subtract 5 minutes to allow for clock differences
    expiration = int(time.time()) + new_tokens['expires_in'] - 300
    
    # Save the token in the session
    request.session['access_token'] = new_tokens['access_token']
    request.session['refresh_token'] = new_tokens['refresh_token']
    request.session['token_expires'] = expiration

    return new_tokens['access_token']
