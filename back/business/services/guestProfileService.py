from models.models import *
from datetime import datetime, timedelta
import json
import requests
import uuid
import config as CONF
from flask import url_for
from utils.auth_api import *
import json

class GuestProfileService():
   db = db

   def getGuestNameByEmail(
      self,
      email
   ):
      rs_guest = db.session.query(Invitados.ds_name_invitado).filter(
         Invitados.ds_email_invitado == email
      ).first()
      if rs_guest is not None:
       if rs_guest.ds_name_invitado is not None:
         guest = dict()
         guest['name'] = rs_guest.ds_name_invitado
         return guest
       else:
         return False
      else:
         return False