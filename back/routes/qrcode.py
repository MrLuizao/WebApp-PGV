from flask import Flask, request, redirect, make_response
from flask_restful import Resource
from flask_restful_swagger import swagger
from business.facade.facade import Facade
import json

facade = Facade()

class QRCode (Resource):
   @swagger.operation(notes='Consulta los datos de un evento mediante url desde un codigo qr')
   def get(self):
      params = dict()
      if 'email' in request.args:
         params['email'] = request.args.get('email')
      if 'kn_event_id' in request.args:
         params['event_id'] = request.args.get('kn_event_id')
      if 'checkout' not in request.args:
         eventInfo = facade.getEventInfoFromQR(params)
         if eventInfo is not False:
            if facade.isCheckedIn(params) == False:
               respuesta = {
                  'response': True,
                  'message': "Información obtenida con éxito.",
                  'data': eventInfo,
                  'error': ""
               }
            else:
               respuesta = {
                  'response': False,
                  'message': "El invitado ha realizado checkin anteriormente.",
                  'error': "El invitado ha realizado checkin anteriormente.",
                  'data': {}
               }   
         else:
            respuesta = {
               'response': False,
               'message': "El código QR no corresponde a un evento.",
               'error': "El código QR no corresponde a un evento.",
               'data': {}
            }
         return respuesta
      else:
         params['checkout'] = request.args.get('checkout')
         eventInfo = facade.getEventInfoFromQR(params)
         if eventInfo is not False:
            if facade.isCheckedIn(params) == True:
               respuesta = {
                  'response': True,
                  'message': "Información obtenida con éxito.",
                  'data': eventInfo
               }
            else:
               respuesta = {
                  'response': False,
                  'message': "El invitado no realizó checkin.",
                  'error': "El invitado no realizó checkin.",
                  'data': {}
               }   
         else:
            respuesta = {
               'response': False,
               'message': "El código QR no corresponde a un evento.",
               'error': "El código QR no corresponde a un evento.",
               'data': {}
            }
         return respuesta


   @swagger.operation(notes='Realiza el checkin correspondiente y guarda la foto.')
   def post(self):
      params = dict()
      if 'email' in request.args:
         params['email'] = request.args.get('email')
      if 'kn_event_id' in request.args:
         params['event_id'] = request.args.get('kn_event_id')
      body = request.get_json()
      if 'checkout' not in request.args:
         eventInfo = facade.getEventInfoFromQR(params)
         if eventInfo is not False:
            if facade.isCheckedIn(params) == False:
               binnacleID = facade.checkIn(
                  eventInfo,
                  body
               )
               if binnacleID != False:
                  respuesta = {
                     'response': True,
                     'message': "Checkin realizado con éxito.",
                     'data': eventInfo,
                     'binnacleID': binnacleID,
                     'error': ""
                  }
               else:
                  respuesta = {
                     'response': False,
                     'message': "No se hizo el checkin de forma correcta.",
                     'error': "No se hizo el checkin de forma correcta.",
                     'data': {}
                  }
            else:
               respuesta = {
                  'response': False,
                  'message': "El invitado ha realizado checkin anteriormente.",
                  'error': "El invitado ha realizado checkin anteriormente.",
                  'data': {}
               }   
         else:
            respuesta = {
               'response': False,
               'message': "El código QR no corresponde a un evento.",
               'error': "El código QR no corresponde a un evento.",
               'data': {}
            }
         return respuesta
      else:
         params['checkout'] = request.args.get('checkout')
         eventInfo = facade.getEventInfoFromQR(params)
         if eventInfo is not False:
            if facade.isCheckedOut(params) == False:
               binnacleID = facade.checkOut(
                  eventInfo,
                  params
               )
               if binnacleID != False:
                  respuesta = {
                     'response': True,
                     'message': "Checkout realizado correctamente.",
                     'data': eventInfo,
                     'binnacleID': binnacleID
                  }
               else:
                  respuesta = {
                     'response': False,
                     'message': "No se hizo el checkout de forma correcta.",
                     'error': "No se hizo el checkout de forma correcta.",
                     'data': {}                 
                  }
            else:
               respuesta = {
                  'response': False,
                  'message': "El invitado ha realizado checkout anteriormente.",
                  'error': "El invitado ha realizado checkout anteriormente.",
                  'data': {}
               }   
         else:
            respuesta = {
               'response': False,
               'message': "El código QR no corresponde a un evento.",
               'error': "El código QR no corresponde a un evento.",
               'data': {}
            }
         return respuesta

