from flask import Flask, request, redirect, make_response
from flask_restful import Resource
from flask_restful_swagger import swagger
from business.facade.facade import Facade
import json

facade = Facade()

class BinnaclePending(Resource):
   @swagger.operation(notes='Obtiene el ultimo registro de un checkin pendiente desde la bitacora')
   def get(self):
      isGetBinnacleData, binnacleData = facade.getBinnaclePendingRegistry()
      respuesta = {
         'response': False,
         'message': "No hay datos pendientes."
      }
      if isGetBinnacleData:
         eventData = facade.getEventInfoFromQR(binnacleData)
         if eventData is not False:
            respuesta = {
               'response': True,
               'message': "Información obtenida con éxito",
               'data': eventData,
               'bitacoraID': binnacleData['bitacoraID']
            }
      return respuesta