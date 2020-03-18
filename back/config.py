import os
import sys

APPNAME = "__main__"

MYSQL = {
   'driver': 'mysql+pymysql',
   'user': 'managevisitors@manage-visitors',
   'pw': 'Axity2k19.!',
   'db': 'gestion_invitados',
   'host': 'manage-visitors.mysql.database.azure.com',
   'port': '3306',
}

APP = {
   'port': 8580,
   'host': '0.0.0.0',
   'debug': False,
}

SWAGGER = {
  'apiVersion': '0.1',
  'api_spec_url': '/doc'
}

QR_STATIC_PATH = "static/img/qr/"

########################ENDPOINTS PYTHON API####################################

API_BASE_ROUTE = "/api/v1"

EVENT_ENDPOINTS = {
   'BASE_ENDPOINT': '/events',
   'GET_EVENTS': '/'
}

QR_ENDPOINTS = {
   'BASE_ENDPOINT': '/qrcode',
   'CHECKIN': '/checkin',
   'CHECKOUT': '/checkout'
}

GUEST_ENDPOINTS = {
   'BASE_ENDPOINT': '/guest',
   'CONFIRM': '/confirm',
   'PENDING': '/pending'
}

DIRECTORY_ENDPOINTS = {
   'BASE_ENDPOINT': '/directory'
}

DEVICES_ENDPOINTS = {
   'BASE_ENDPOINT': '/devices'
}

PROFILE_DEVICES_ENDPOINTS = {
   'BASE_ENDPOINT': '/profile',
   'DEVICES': '/devices'   
}

BINNACLE_ENDPOINTS = {
   'BASE_ENDPOINT': '/binnacle',
   'PRIVACITY': '/privacity'
}

GUESTPROFILE_ENDPOINTS = {
   'BASE_ENDPOINT': '/guest'
}

MANUAL_CHECKIN_ENDPOINTS = {
   'BASE_ENDPOINT': '/checkin',
   'MANUAL': '/manual',
   'SIGNATURE': '/signature'
}

MANUAL_CHECKOUT_ENDPOINTS = {
   'BASE_ENDPOINT': '/checkout',
   'MANUAL': '/manual'
}

EMPLOYEES_ENDPOINTS = {
   'BASE_ENDPOINT': '/employees'
}
########################FRONT URL################################################
FRONT = {
   'FRONT_BASE': 'http://managevisitors.z20.web.core.windows.net',
   'CONFIG_WIZARD': '/wizard',
   'PARAM_INDICATOR': '?',
   'EVENT_ID': 'eventID=',
   'PARAM_SEPARATOR': '&'
}
EVENTREGISTRY = {
   'BASE': '/pre-registro',
   'EVENT_ID': 'event_id=',
   'EMAIL': 'email='
}

GRALSRV_EMAIL = [
   'pedro.hernandez@axity.com'
]

MKT_EMAIL = [
   'luis.vazquezr@axity.com'
]
########################MICROSOFT GRAPH CONFIGURATION###########################
GRAPH_SETUP = {
   'APP_CLIENT_ID' : '15953f75-177b-4797-8b26-93c70547e556',
   'APP_CLIENT_SECRET' : 'KP5ap6f=PQmozu0=V1kjDzI:.UxYXa9/',
   'APP_SCOPES' : [ 
      'openid',
      'offline_access',
      'User.Read',
      'Mail.Read',
      'Calendars.Read'
   ]
}
APP_AUTHORITY_URL = 'https://login.microsoftonline.com/common'
APP_AUTH_ENDPOINT = '/oauth2/v2.0/authorize'
APP_TOKEN_ENDPOINT = '/oauth2/v2.0/token'
SEND_EMAIL_ENDPOINT = '/me/sendMail'
GRAPH_ENDPOINT = {
   'APP_URL_AUTH' : APP_AUTHORITY_URL + APP_AUTH_ENDPOINT,
   'APP_URL_TOKEN' : APP_AUTHORITY_URL + APP_TOKEN_ENDPOINT,
   'APP_RESOURCE' : 'https://graph.microsoft.com/',
   'APP_API_VERSION' :'v1.0',
   'APP_SUBSCRIPTIONS' : 'https://graph.microsoft.com/v1.0/subscriptions'
}
APP_URL_BASE = 'https://manage-visitors.azurewebsites.net' #NGROK
APP_URL_BASE_VALIDATION = 'https://manage-visitors-validation.azurewebsites.net'
MICROSOFT_GRAPH = '/microsoft'
GRAPH_AUTH = '/auth'
GRAPH_CODEAUTH = '/codeAuth'
GRAPH_URLTOKEN = '/urlToken'
GRAPH_SUB = '/sub'
APP_ENDPOINT = {
   'APP_URL_BASE' : APP_URL_BASE,
   'APP_INI' : APP_URL_BASE+API_BASE_ROUTE+MICROSOFT_GRAPH+GRAPH_AUTH,
   'APP_AUTH' : APP_URL_BASE+API_BASE_ROUTE+MICROSOFT_GRAPH+GRAPH_CODEAUTH,
   'APP_TOKEN' : APP_URL_BASE+API_BASE_ROUTE+MICROSOFT_GRAPH+GRAPH_URLTOKEN,
   'APP_SUB' : APP_URL_BASE+API_BASE_ROUTE+MICROSOFT_GRAPH+GRAPH_SUB,
}
APP_ENDPOINT_VALIDATION = {
   'APP_URL_BASE' : APP_URL_BASE_VALIDATION,
   'APP_INI' : APP_URL_BASE_VALIDATION+API_BASE_ROUTE+MICROSOFT_GRAPH+GRAPH_AUTH,
   'APP_AUTH' : APP_URL_BASE_VALIDATION+API_BASE_ROUTE+MICROSOFT_GRAPH+GRAPH_CODEAUTH,
   'APP_TOKEN' : APP_URL_BASE_VALIDATION+API_BASE_ROUTE+MICROSOFT_GRAPH+GRAPH_URLTOKEN,
   'APP_SUB' : APP_URL_BASE_VALIDATION+API_BASE_ROUTE+MICROSOFT_GRAPH+GRAPH_SUB,
}
GRAPH_AUTH_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize/?client_id='+GRAPH_SETUP['APP_CLIENT_ID']+'&redirect_uri='+APP_ENDPOINT['APP_AUTH']+'&cache_state=False&response_type=code&scope=openid+offline_access+User.Read+Mail.Read+Calendars.Read+Mail.Send+Files.ReadWrite+Files.ReadWrite.All'

##########################NEXMO API FOR SMS#######################################
NEXMOKEY = "8f198342"
NEXMOSECRET = "e29JNLTJSoJR50r7"