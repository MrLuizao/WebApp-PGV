from flask import Flask, request, redirect, make_response
from flask_restful import Resource
from flask_restful_swagger import swagger
from business.facade.facade import Facade
import json

facade = Facade()

class RolesRoutes (Resource):
   @swagger.operation(notes='Devuelve lista de usuarios y sus roles')
   def get(self):
      roleListUser = facade.getRoleList()
      if roleListUser is not False:
         respuesta = {
            'response': True,
            'message': "Información obtenida con éxito",
            'data': roleListUser
         }
      else:
         respuesta = {
            'response': False,
            'message': "Hubo un error al consultar los datos."
         }
      return respuesta

