from flask import Flask, request, redirect,make_response
from flask_restful import Resource
from flask_restful_swagger import swagger
from utils.auth_api import *
from business.facade.facade import Facade

import json

facade = Facade()

class Signature (Resource):
   @swagger.operation(notes='Devuelve True o False si la firma del usuario ya existe')
   def get(self):
      response = 200
      if 'email' in request.args:
         email = request.args.get('email')
         guest = facade.getSignature(email)
         if guest is not False:
            respuesta = {
               'firma': True
            }
         else:
            response = 200
            respuesta = {
              'firma' : False
            }
      else:
         response = 500
         respuesta = {
           'firma' : False
         }
      return make_response(respuesta, response)