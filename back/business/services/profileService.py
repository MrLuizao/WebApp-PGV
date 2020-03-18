from models.models import *
from datetime import datetime, timedelta
import json
import requests
import uuid
import config as CONF
from flask import url_for
from utils.auth_api import *
import json

   def getDevicesInfo(
      self,
      params
   ):
      query_eventos = db.session.query(Invitacion, Invitados).join(Invitados).filter(
         Invitados.kn_event_id == Invitacion.id,
         Invitados.kn_event_id == params['event_id'],
         Invitados.ds_email_invitado == params['email']
      ).all()
      eventoInfo = dict()
      eventoInfo['id'] = query_eventos[0].Invitacion.id
      eventoInfo['ds_event_name'] = query_eventos[0].Invitacion.ds_event_name
      eventoInfo['ds_event_place'] = query_eventos[0].Invitacion.ds_event_place
      eventoInfo['dt_event_date'] = query_eventos[0].Invitacion.dt_event_date.strftime('%m/%d/%Y')
      eventoInfo['event_hour'] = query_eventos[0].Invitacion.dt_event_date.strftime('%H:%M:%S')
      eventoInfo['dt_event_created'] = query_eventos[0].Invitacion.dt_event_created.strftime('%m/%d/%Y %H:%M:%S')
      eventoInfo['ds_host_email'] = query_eventos[0].Invitacion.ds_host_email
      for item, invitados in query_eventos:
         eventoInfo['devices'] = invitados.ds_json_devices
      return eventoInfo

   def setDevicesConfig(
      self,
      data
   ):
      event_id = data['event_id']
      email = data['email']
      try:
         invitado = Invitados.query.filter(
            Invitados.kn_event_id == event_id,
            Invitados.ds_email_invitado == email
         ).first()
         if invitado is not None:
            invitado.ds_json_devices = data['devices']
            db.session.add(invitado)
            db.session.commit()
            return True
         else:
            return False
      except Exception as e:
         return False