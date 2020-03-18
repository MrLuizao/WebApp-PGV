from models.models import *
from datetime import datetime, timedelta
import json
import requests
import uuid
import config as CONF
from flask import url_for
from utils.auth_api import *
import json

class PrivacityService():
  db = db

  def getSignaturePrivacity(
      self,
      email
   ):
     # rs_guest = db.session.query(Binnacle.base64_signature).filter(
     #   Binnacle.ds_guest_email == email
     # ).first()
      rs_guest = Binnacle.query.filter_by(ds_guest_email=email).first()
      print('rs_guest.base64_signature')
      if rs_guest is not None:
       if rs_guest.base64_signature is not None:
         guest = dict()
         guest['name'] = rs_guest.base64_signature.decode("utf-8")
         return guest
       else:
          return False  
      else:
         return False  
		 