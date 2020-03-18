from flask import Flask, request, redirect, make_response
from flask_restful import Resource
from flask_restful_swagger import swagger
from business.facade.facade import Facade
import json

facade = Facade()

class Events (Resource):
   @swagger.operation(notes='Consulta los eventos, puede recibir parametros de correo electrónico')
   def get(self):
      params = dict()
      if 'email' in request.args:
         params['email'] = request.args.get('email')
      if 'event_id' in request.args:
         params['event_id'] = request.args.get('event_id')
      if 'srv' in request.args:
         params['srv'] = request.args.get('srv')
      if 'today' in request.args:
         params['today'] = 'today'
      json_data = facade.getEvents(params)
      respuesta = {
         'response': True,
         'message': "Información obtenida con éxito",
         'data': json_data
      }
      return respuesta

   @swagger.operation(notes='Servicio POST que sirve para setear configuracion del evento')
   def post(self):
      body = request.get_json()
      setConfig = facade.setInvitationConfig(body)
      if setConfig:
         message = "Configuracion guardada con éxito."
      else:
         message = "Hubo un error al guardar la configuración."
      respuesta = {
         'response': setConfig,
         'message': message
      }
      return respuesta

   @swagger.operation(notes='Servicio PUT para actualizar si el evento ha sido atendido por servicios generales')
   def put(self):
      params = dict()
      if 'attended' in request.args:
         params['attended'] = request.args.get('attended')
         if 'event_id' in request.args:
            params['event_id'] = request.args.get('event_id')
            result = facade.updateAttendedEvent(params)
            msg = "Información actualizada con éxito."
            if not result:
               msg = "Hubo un problema al actualizar la información."
         else:
            result = False
            msg = "No se encontró el parámetro event_id."
      else:
         result = False
         msg = "No se encontró el parámetro attended."
      respuesta = {
         'response': result,
         'message': msg
      }
      return respuesta