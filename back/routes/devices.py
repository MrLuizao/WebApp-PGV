from flask import Flask, request, redirect, make_response
from flask_restful import Resource
from flask_restful_swagger import swagger
from business.facade.facade import Facade
import json

facade = Facade()

class DevicesRoutes (Resource):
   @swagger.operation(notes='Consulta los dispositivos basado en un evento y un email')
   def get(self):
      params = dict()
      if 'email' in request.args:
         params['email'] = request.args.get('email')
      if 'kn_event_id' in request.args:
         params['event_id'] = request.args.get('kn_event_id')
      devicesInfo = facade.getDevicesInfo(params)
      if devicesInfo is not False:
         respuesta = {
            'response': True,
            'message': "Información obtenida con éxito.",
            'data': devicesInfo
         }   
      else:
         respuesta = {
            'response': False,
            'message': "El código QR no corresponde a un evento."
         }
      return respuesta

   @swagger.operation(notes='Servicio POST que sirve para setear lista de dispositivos en formato json')
   def post(self):
      body = request.get_json()
      setConfig = facade.setDevicesConfig(body)
      if setConfig:
         message = "Dispositivos guardados con éxito."
      else:
         message = "Hubo un error al guardar los dispositivos."
      respuesta = {
         'response': setConfig,
         'message': message
      }
      return respuesta