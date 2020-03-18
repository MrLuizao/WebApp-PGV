from flask import Flask, request, redirect, make_response
from flask_restful import Resource
from flask_restful_swagger import swagger
from business.facade.facade import Facade
import json

facade = Facade()

class DirectoryRoutes (Resource):
   @swagger.operation(notes='Devuelve el listado del directorio')
   def get(self):
      directoryID = request.args.get('id')
      if directoryID is not None:
         directoryRecord = facade.getDirectoryByID(directoryID)
         if directoryRecord is not False:
            respuesta = {
               'response': True,
               'message': "Información obtenida con éxito.",
               'data': [directoryRecord]
            }
         else:
            respuesta = {
               'response': False,
               'message': "Hubo un error al consultar los datos."
            }
         return respuesta
      directoryList = facade.getDirectoryList()
      respuesta = {
         'response': True,
         'message': "Información obtenida con éxito",
         'data': directoryList
      }
      return respuesta

   @swagger.operation(notes='Inserta un nuevo registro en el directorio')
   def post(self):
      json = request.get_json()

      exist = facade.userDirectoryExist(json)
      print( exist )
      if exist:
         respuesta = {
            'response': False,
            'message': "El correo electrónico ya se encuentra registrado."
         }
      else:
         registry = facade.addToDirectory(json)
         if registry is not False:
            respuesta = {
               'response': True,
               'message': "Información guardada con éxito."
            }
         
         else: 
            respuesta = {
               'response': False,
               'message': "Ocurrió un error al guardar los datos."
            }
      return respuesta

   def put(self):
      json = request.get_json()
      update = facade.updateDirectoryByID(json)
      if update:
         message = "Información actualizada con éxito."
      else:
         message = "Hubo un error al actualizar el registro."
      respuesta = {
         'response': update,
         'message': message
      }
      return respuesta

   def delete(self):
      directoryID = request.args.get('id')
      delete = facade.deleteDirectoryByID(directoryID)
      if delete:
         message = "El registro fue eliminado con éxito."
      else:
         message = "Hubo un problema al borrar el registro."
      respuesta = {
         'response': delete,
         'message': message
      }
      return respuesta