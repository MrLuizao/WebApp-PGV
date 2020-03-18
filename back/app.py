#IMPORTAR LIBRERIAS
from flask import Flask, request, redirect
from models.models import db
from flask_restful import Api, Resource
from flasgger import Swagger
from flasgger.utils import swag_from
from flask_restful_swagger import swagger
from routes.routes import Inicio
from routes.graph_routes import *
from routes.users import Users
import config as CONF
from flask_cors import CORS, cross_origin
from routes.events import Events
from routes.qrcode import QRCode
from routes.guest import GuestRoutes
from routes.pending import BinnaclePending
from routes.directory import DirectoryRoutes
from routes.devices import DevicesRoutes
from routes.profile_devices import ProfileDevicesRoutes
from routes.binnacle import BinnacleReportsRoutes
from routes.guestprofile import GuestProfile
from routes.manualcheckin import ManualCheckinRoutes
from routes.checkout import CheckoutRoutes
from routes.roles import RolesRoutes
from routes.signature import Signature
from routes.privacity import Privacity
from routes.employees import EmployeesRoutes


app = Flask(
   __name__,
   template_folder="html/"
)
CORS(app)
api = Api(app)
api = swagger.docs(
   Api(app),
   apiVersion = CONF.SWAGGER['apiVersion'],
   api_spec_url = CONF.SWAGGER['api_spec_url']
)

app.config['DEBUG'] = True
app.config[
   'SQLALCHEMY_DATABASE_URI'
] = '{}://{}:{}@{}:{}/{}'.format(
   CONF.MYSQL['driver'],
   CONF.MYSQL['user'],
   CONF.MYSQL['pw'],
   CONF.MYSQL['host'],
   CONF.MYSQL['port'],
   CONF.MYSQL['db']
)
db.init_app(app)

#DECLARACION DE RUTAS

api.add_resource(
   Inicio,
   CONF.API_BASE_ROUTE+'/'
)

api.add_resource(
	GraphAuth,
	CONF.API_BASE_ROUTE+CONF.MICROSOFT_GRAPH+CONF.GRAPH_AUTH
)

api.add_resource(
	GraphCode,
	CONF.API_BASE_ROUTE+CONF.MICROSOFT_GRAPH+CONF.GRAPH_CODEAUTH
)

api.add_resource(
	GraphSub,
	CONF.API_BASE_ROUTE+CONF.MICROSOFT_GRAPH+CONF.GRAPH_SUB
)

api.add_resource(
   Users,
   CONF.API_BASE_ROUTE+'/users/access'
)

api.add_resource(
   Events,
   CONF.API_BASE_ROUTE+CONF.EVENT_ENDPOINTS['BASE_ENDPOINT']+CONF.EVENT_ENDPOINTS['GET_EVENTS']
)

api.add_resource(
   QRCode,
   CONF.API_BASE_ROUTE+CONF.QR_ENDPOINTS['BASE_ENDPOINT']+CONF.QR_ENDPOINTS['CHECKIN']
)

api.add_resource(
   GuestRoutes,
   CONF.API_BASE_ROUTE+CONF.GUEST_ENDPOINTS['BASE_ENDPOINT']+CONF.GUEST_ENDPOINTS['CONFIRM']  
)

api.add_resource(
   BinnaclePending,
   CONF.API_BASE_ROUTE+CONF.GUEST_ENDPOINTS['BASE_ENDPOINT']+CONF.GUEST_ENDPOINTS['PENDING']  
)

api.add_resource(
   DirectoryRoutes,
   CONF.API_BASE_ROUTE+CONF.DIRECTORY_ENDPOINTS['BASE_ENDPOINT']
)

api.add_resource(
   DevicesRoutes,
   CONF.API_BASE_ROUTE+CONF.DEVICES_ENDPOINTS['BASE_ENDPOINT']
)

api.add_resource(
   ProfileDevicesRoutes,
   CONF.API_BASE_ROUTE+CONF.PROFILE_DEVICES_ENDPOINTS['BASE_ENDPOINT']+CONF.PROFILE_DEVICES_ENDPOINTS['DEVICES']
)

api.add_resource(
   BinnacleReportsRoutes,
   CONF.API_BASE_ROUTE+CONF.BINNACLE_ENDPOINTS['BASE_ENDPOINT']
)

api.add_resource(
   Privacity,
   CONF.API_BASE_ROUTE+CONF.BINNACLE_ENDPOINTS['PRIVACITY']
)
api.add_resource(
   GuestProfile,
   CONF.API_BASE_ROUTE+CONF.GUESTPROFILE_ENDPOINTS['BASE_ENDPOINT']
)

api.add_resource(
   ManualCheckinRoutes,
   CONF.API_BASE_ROUTE+CONF.MANUAL_CHECKIN_ENDPOINTS['BASE_ENDPOINT']+CONF.MANUAL_CHECKIN_ENDPOINTS['MANUAL']
)

api.add_resource(
   CheckoutRoutes,
   CONF.API_BASE_ROUTE+CONF.MANUAL_CHECKOUT_ENDPOINTS['BASE_ENDPOINT']+CONF.MANUAL_CHECKOUT_ENDPOINTS['MANUAL']
)

api.add_resource(
   Signature,
   CONF.API_BASE_ROUTE+CONF.MANUAL_CHECKIN_ENDPOINTS['BASE_ENDPOINT']+CONF.MANUAL_CHECKIN_ENDPOINTS['SIGNATURE']
)

api.add_resource(
   RolesRoutes,
   CONF.API_BASE_ROUTE+'/roles'
)

api.add_resource(
   EmployeesRoutes,
   CONF.API_BASE_ROUTE+CONF.EMPLOYEES_ENDPOINTS['BASE_ENDPOINT']
)

if __name__ == CONF.APPNAME:
	app.secret_key = b'_6#y7L"F9Q1z\n\gex]/'
	app.run(
		host = CONF.APP['host'],
		port = CONF.APP['port'],
		debug = CONF.APP['debug']
	)