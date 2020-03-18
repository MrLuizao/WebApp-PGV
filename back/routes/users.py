from flask import Flask, request, redirect, make_response
from flask_restful import Resource
from flask_restful_swagger import swagger
from business.facade.facade import Facade
import json

facade = Facade()

class Users (Resource):
   @swagger.operation(notes='Recibe datos del usuario para agregar a DB')
   def post(self):
      #obtener objeto json
      json_data = request.get_json()
      
      access = json_data['login']
      # print(access)
      # print(type(access))
      if access:
         okLogin, rol = facade.loginUser(json_data)
         if okLogin == True:
            json_data['role']= rol
            answer = {
               'idToken': '#7ok3nM0ck.',
               'response': True,
               'message': "Acceso Correcto",
               'registered': True,
               'data': json_data
            }
         else:
            answer = {
               'response': False,
               'message': "Acceso Denegado",
               'registered': False,
               'data': json_data
            }
         return answer
      else:
         exist = facade.userExist(json_data)
         if exist:
            respuesta = {
               'response': False,
               'message': "El correo electrónico ya se encuentra registrado."
            }
            return respuesta
         user = facade.userRegister(json_data)
         if user == True:
            respuesta = {
               'idToken': '#7ok3nM0ck.v2',
               'response': True,
               'message': "Registro correcto!",
               'data': json_data
            }
         else:
            respuesta = {
               'response': False,
               'message': "falló el registro",
               'data': json_data
            }
         return respuesta

