from flask import Flask, request, redirect,make_response
from flask_restful import Resource
from flask_restful_swagger import swagger
from utils.auth_api import *
from business.facade.facade import Facade

import json

facade = Facade()

class Privacity (Resource):
   @swagger.operation(notes='Devuelve la firma del usuario registrado')
   def get(self):
      response = 200
      if 'email' in request.args:
         email = request.args.get('email')
         guest = facade.getSignaturePrivacity(email)
         if guest is not False:
            respuesta = {
            'message': "Firma obtenida con éxito",
               'data': guest
            }
         else:
            response = 200
            respuesta = {
             'message': "No se encontro la firma",
               'data': guest
            }
      else:
         response = 500
         respuesta = {
           'message': "Internal server error",
               'data': guest
         }
      return make_response(respuesta, response)