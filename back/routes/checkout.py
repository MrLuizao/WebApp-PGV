from flask import Flask, request, redirect, make_response
from flask_restful import Resource
from flask_restful_swagger import swagger
from business.facade.facade import Facade
import json

facade = Facade()

class CheckoutRoutes(Resource):
   @swagger.operation(notes='Realiza el checkout con el numero de gaffete.')
   def post(self):
      response = True
      httpresponse = 200
      msg = 'Chek Out realizado correctamente.'
      body = request.get_json()
      badgeNumber = body['badgeNumber']
      checkout = facade.checkOutGafete(badgeNumber)
      if checkout == False:
         response = False
         httpresponse = 400
         msg = 'Hubo un problema en el checkout, intente de nuevo.'
      else:
         response = True
         httpresponse = 200
      respuesta = {
         'response': response,
         'message': msg,
         'error': msg,
         'data': None
      }
      return make_response(respuesta, httpresponse)