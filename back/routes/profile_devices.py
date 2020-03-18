from flask import Flask, request, redirect, make_response
from flask_restful import Resource
from flask_restful_swagger import swagger
from business.facade.facade import Facade
import json

facade = Facade()

class ProfileDevicesRoutes (Resource):
   @swagger.operation(notes='Consulta los dispositivos registradoes en el perfil del usuario')

   def get(self):
      params = dict()
      if 'email' in request.args:
         params['email'] = request.args.get('email')
      setDeviceProfile = facade.getProfileDevicesInfo(params)
      if setDeviceProfile is not False:
         respuesta = {
            'response': True,
            'message': "Información obtenida con éxito",
            'data': setDeviceProfile
         }   
      else:
         respuesta = {
            'response': False,
            'message': "Dispositivos registrados correctamente"
         }
      return respuesta


   @swagger.operation(notes='Servicio POST que sirve para setear lista de dispositivos')

   def post(self):
      body = request.get_json()
      setDeviceProfile = facade.setProfileDevicesConfig(body)

      if setDeviceProfile:
         message = "Dispositivos guardados con éxito."
      else:
         message = "Hubo un error al guardar los dispositivos."
      respuesta = {
         'response': setDeviceProfile,
         'message': message
      }

      return respuesta