from flask import Flask, request, redirect, make_response
from flask_restful import Resource
from flask_restful_swagger import swagger
from business.facade.facade import Facade
import json

facade = Facade()

class ManualCheckinRoutes (Resource):
   @swagger.operation(notes='Servicio post que crea un evento con los datos proporcionados.')
   def post(self):
      response = True
      httpresponse = 200
      msg = 'Chek In realizado correctamente'
      body = request.get_json()
      event = facade.createInvitationAndDetails(body)
      if event == False:
         response = False
         httpresponse = 400
         msg = 'Hubo un problema en el registro, intente de nuevo.'
      else:
         params = dict()
         params['email'] = event['email']
         params['event_id'] = event['kn_event_id']
         body = event
         eventInfo = facade.getEventInfoFromQR(params)
         if eventInfo is not False:
            if facade.isCheckedIn(params) == False:
               binnacleID = facade.checkIn(
                  eventInfo,
                  body
               )
               if binnacleID != False:
                  response = True
                  httpresponse = 200
                  msg = "Check In realizado con éxito."
               else:
                  response = False
                  httpresponse = 400
                  msg = "No se hizo el checkin de forma correcta."
            else:
               response = False
               httpresponse = 409
               msg = "El invitado ha realizado checkin anteriormente."
         else:
            response = True
            httpresponse = 404
            msg = "No existe el evento, por favor verifique."
      respuesta = {
         'response': response,
         'message': msg,
         'error': msg,
         'data': None
      }
      return make_response(respuesta, httpresponse)







