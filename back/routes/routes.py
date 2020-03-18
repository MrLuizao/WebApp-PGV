from flask import Flask, request, redirect
from flask_restful import Resource
from flask_restful_swagger import swagger
from utils.auth_api import *
from business.facade.facade import Facade

import json

facade = Facade()

class Inicio(Resource):
   @swagger.operation(notes='Obtiene todas las invitaciones de la bd, devuelve json con las invitaciones')
   def get(self):
      #obtener algun parámetro de la url
      #ejemplo: http://localhost:5000/?param1=1&param2=2
      json_data = facade.getAllInvitaciones()

      param1 = request.args.get('param1')
      param2 = request.args.get('param2')
      print (param1)
      print (param2)
      respuesta = {
         'response': True,
         'msg': 'Mensaje al usuario',
         'data': json_data
      }
      return respuesta

   @swagger.operation(notes='Inserta un nuevo evento desde un json dado')
   def post(self):
      #obtener objeto json
      json_data = request.get_json()
      resultado = facade.newEvents(json_data['events'])
      #invitacionesByDate = Service.getEventsByDate(db, '2020/06/01')
      respuesta = {
         'response': True,
         'msg': "Mensaje al usuario",
         'data': json_data
      }
      return respuesta