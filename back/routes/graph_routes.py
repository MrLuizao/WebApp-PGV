from flask import Flask, request, redirect, make_response
from flask_restful import Resource
from flask_restful_swagger import swagger
from utils.auth_api import *
import json
import config as CONF
from datetime import datetime, timedelta
from business.facade.facade import Facade

facade = Facade()

def add_two_days():
   #now = datetime.datetime.now()
   now = datetime.now()
   #add_days = datetime.timedelta(days=2)
   add_days = timedelta(days=2)
   date_end = now + add_days
   return date_end.isoformat(sep='T', timespec='auto')+'z'

class GraphAuth(Resource):
   @swagger.operation(notes='Solicita permisos para leer eventos de una cuenta microsoft')
   def get(self):
      #sign_in_url = get_signin_url(CONF.APP_ENDPOINT['APP_AUTH'])
      url = CONF.GRAPH_AUTH_URL
      return redirect(url)

class GraphCode(Resource):
   @swagger.operation(notes='Recibe token de acceso para peticiones de GRAPH')
   def get(self):
      auth_code = request.args.get('code')
      token, refresh_token = get_token_from_code(
         auth_code,
         CONF.APP_ENDPOINT['APP_AUTH']
      )
      if not token:
         return redirect(CONF.GRAPH_AUTH_URL)
      return redirect(
         CONF.APP_ENDPOINT['APP_SUB']+'?token='+token+'&refresh_token='+refresh_token,
         code=302
      )

class GraphSub(Resource):
   @swagger.operation(notes='Realiza la petición de suscripción para notificaciones')
   def get(self):
      token = request.args.get('token')
      refreshToken = request.args.get('refresh_token')
      headers = {
         'User-Agent' : 'gestion_visitas/1.0',
         'Content-Type': 'application/json',
         'Authorization' : 'Bearer {0}'.format(token)
      }
      dt_string = add_two_days()
      post_data = { 
         "changeType": "Created,Updated,Deleted",
         "resource": "me/events",
         "clientState": "cLIENTsTATEfORvALIDATION",
         "expirationDateTime": dt_string ,
         "notificationUrl": CONF.APP_ENDPOINT_VALIDATION['APP_SUB']
      }
      r = requests.post(
         CONF.GRAPH_ENDPOINT['APP_SUBSCRIPTIONS'],
         data = json.dumps(post_data),
         headers = headers
      )
      if(r.status_code == 201):
         json_data = json.loads(r.text)
         subscriptionID = json_data['id']
         initEvents = facade.initEventsWithDelta(
            token,
            refreshToken,
            subscriptionID
         )
         return 200
      else:
         print(r.text, post_data, CONF.GRAPH_ENDPOINT['APP_SUBSCRIPTIONS'])
         return 400

   @swagger.operation(notes='Retorna respuesta a microsoft para completar la subscripción de notificaciones')
   def post(self):
      token = request.args.get('validationToken')
      print("IMPRESION DE TOKEN: ", token)
      if token != None:
         print("SI HAY TOKEN")
         resp = make_response(token, 200)
         resp.headers['Content-Type'] = 'text/plain'
         return resp
      else:
         msPostedValue = request.get_json()
         notification = msPostedValue['value']
         while True:
            result = facade.getNotification(notification)
            if result == True:
               break
         return 200

   @swagger.operation(notes='Renueva la suscripción de microsoft para los eventos de calendario para todas las cuentas registradas.')
   def patch(self):
      response = True
      httpresponse = 200
      msg = 'Se renovaron todas las suscripciones del sistema.'
      result = facade.renewSubscription()
      if result == False:
         response = False
         httpresponse = 400
         msg = 'Hubo un problema al renovar las suscripciones (Se llegó al limite máximo de intentos).'
      respuesta = {
         'response': response,
         'message': msg,
         'error': msg,
         'data': None
      }
      return make_response(respuesta, httpresponse)