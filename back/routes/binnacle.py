from flask import Flask, request, redirect, make_response
from flask_restful import Resource
from flask_restful_swagger import swagger
from business.facade.facade import Facade
import json
from datetime import datetime, timedelta
from business.services.commonsService import CommonsService
import config as CONF

commonsService = CommonsService()

facade = Facade()

class BinnacleReportsRoutes (Resource):
   @swagger.operation(notes='Devuelve registros de la bitácora')
   def get(self):
      response = 200
      if 'xlsx' not in request.args:
         if 'today' in request.args:
            startdate = (commonsService.getServerTime(CONF.APP['debug'])).strftime('%Y/%m/%d')
            enddate = commonsService.getServerTime(CONF.APP['debug']).strftime('%Y/%m/%d')
            params = {
               'start': startdate,
               'end': enddate
            }
            records = facade.getBinnacleRecords(params)
            respuesta = {
               'response': True,
               'message': "Información obtenida con éxito",
               'data': records
            }
         elif ('startdate' in request.args and 'enddate' in request.args):
            #FECHAS 2020/01/31
            startdate = request.args.get('startdate')
            enddate = request.args.get('enddate')
            params = {
               'start': startdate,
               'end': enddate
            }
            records = facade.getBinnacleRecords(params)
            respuesta = {
               'response': True,
               'message': "Rango de fechasssss",
               'data': records
            }
         else:
            respuesta = {
               'message': "Rango de fechas"
            }
            response = 409
      else:
         if 'today' in request.args:
            startdate = (commonsService.getServerTime(CONF.APP['debug']) - timedelta(days = 3)).strftime('%Y/%m/%d')
            enddate = commonsService.getServerTime(CONF.APP['debug']).strftime('%Y/%m/%d')
            params = {
               'start': startdate,
               'end': enddate
            }
            xlsxURL = facade.getXLSXFromBinnacle(params)
            respuesta = {
               'response': True,
               'message': "Información obtenida con éxito",
               'data': xlsxURL
            }
         elif ('startdate' in request.args and 'enddate' in request.args):
            startdate = request.args.get('startdate')
            enddate = request.args.get('enddate')
            params = {
               'start': startdate,
               'end': enddate
            }
            xlsxURL = facade.getXLSXFromBinnacle(params)
            respuesta = {
               'response': True,
               'message': "Rango de fechas",
               'data': xlsxURL
            }
         else:
            respuesta = {
               'message': "Rango de fechas"
            }
            response = 409
      return make_response(respuesta, response)