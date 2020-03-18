from flask import Flask, request, redirect, make_response
from flask_restful import Resource
from flask_restful_swagger import swagger
from business.facade.facade import Facade
import json

facade = Facade()

class EmployeesRoutes (Resource):
   @swagger.operation(notes='Devuelve el listado del correos')
   def get(self):
      nombreString = request.args.get('name')
            
      if request.args.get('name') is not None:
         nameUrl = request.args.get('name')
         employeesList = facade.getEmployeesList(nameUrl)
         if employeesList is not None:
            respuesta = {
               'response': True,
               'message': "Información obtenida con éxito.",
               'data': employeesList
            }
         else:
            respuesta = {
               'response': False,
               'message': "Hubo un error al consultar los datos.",
               'data':[]
            }
      else:
         employeesList = facade.getEmployeesList(nombreString)
         if employeesList is not None:
            respuesta =  employeesList
         else:
            respuesta = []
            
      return respuesta

