from flask import Flask, request, redirect, make_response
from flask_restful import Resource
from flask_restful_swagger import swagger
from business.facade.facade import Facade
import json

facade = Facade()

class GuestRoutes (Resource):
   @swagger.operation(notes='Confirma el checkin de un invitado')
   def post(self):
      json_data = request.get_json()
      isCheckIn, msg, event_id, guest_email, dt_checkin, guest_name, badge_number = facade.confirmCheckIn(json_data)
      if isCheckIn:
         isUpdate = facade.updateGuestInvitationDetail(
            event_id,
            guest_email,
            dt_checkin,
            badge_number
         )
         if isUpdate:
            smsMessage = "Tu invitado {} ha llegado a la reunión, te está esperando.".format(guest_name)
            directoryList = facade.getDirectoryListFromEvent(event_id)
            sms = facade.sendSMSToOrganizer(
               smsMessage,
               directoryList
            )
         respuesta = {
            'response': True,
            'message': msg
         }
      else:
         respuesta = {
            'response': False,
            'message': msg
         }
      return respuesta