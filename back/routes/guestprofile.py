from flask import Flask, request, redirect, make_response
from flask_restful import Resource
from flask_restful_swagger import swagger
from business.facade.facade import Facade
import json

facade = Facade()

class GuestProfile (Resource):
   @swagger.operation(notes='Devuelve el nombre de la persona, conforme al correo enviado por url')
   def get(self):
      response = 200
      if 'email' in request.args:
         email = request.args.get('email')
         guest = facade.getGuestNameByEmail(email)
         if guest is not False:
            respuesta = {
               'message': "Información obtenida con éxito",
               'data': guest
            }
         else:
            response = 200
            respuesta = {
               'message': 'El correo electrónico proporcionado no arrojó ninguna coincidencia.',
               'data' : {}
            }
      else:
         response = 500
         respuesta = {
            'message': "Falta el parámetro 'email'."
         }
      return make_response(respuesta, response)