from models.models import *
from datetime import datetime
import json
import requests
import uuid
import config as CONF
import nexmo
from business.services.eventService import EventService
from business.services.commonsService import CommonsService

eventService = EventService()
commonsService = CommonsService()

nexmoSMS = nexmo.Client(
   key = CONF.NEXMOKEY, 
   secret = CONF.NEXMOSECRET
)

class GuestService():
   db = db

   def checkIn(
      self,
      eventInfo,
      body
   ):
      devices = []
      if len(body['devices']) > 0:
         devices = body['devices']
      now = commonsService.getServerTime(CONF.APP['debug'])
      binnacle = Binnacle(
         dt_reg_date = now,
         kn_event_id = eventInfo['id'],
         kn_type = 1, #checkin = 1, checkout = 2 seguridad, checkout = 3 recepcion
         ds_guest_name = eventInfo['ds_name_invitado'],
         ds_guest_email = eventInfo['ds_email_invitado'],
         ds_host_name = eventInfo['ds_host_name'],
         ds_host_email = eventInfo['ds_host_email'],
         kn_status = 0,
         ds_json_devices = devices,
         base64_image = body['foto'].encode('utf-8'),
         base64_signature = body['signature'].encode('utf-8')
      )
      try:
         db.session.add(binnacle)
         db.session.commit()
         return binnacle.id
      except Exception as e:
         return False

   def isCheckedIn(
      self,
      params
   ):
      binnacle = Binnacle.query.filter(
         Binnacle.kn_event_id == params['event_id'],
         Binnacle.ds_guest_email == params['email'],
         Binnacle.kn_type == 1
      ).first()
      if binnacle == None:
         return False
      else:
         return True

   def confirmCheckIn(
      self,
      data
   ):
      binnacle = Binnacle.query.filter(
         Binnacle.id == data['bitacoraID']
      ).first()
      if binnacle is not None:
         if binnacle.kn_status == 0:
            event_id = binnacle.kn_event_id
            guest_email = binnacle.ds_guest_email
            dt_checkin = binnacle.dt_reg_date
            guest_name = binnacle.ds_guest_name
            badge_number = binnacle.ds_badge_number
            if data['confirm']:
               binnacle.kn_status = 1
               binnacle.ds_badge_number = data['badgeNumber']
               db.session.add(binnacle)
               db.session.commit()
               return True, "Check-In confirmado.", event_id, guest_email, dt_checkin, guest_name, badge_number
            else:
               db.session.delete(binnacle)
               db.session.commit()
               return False, "El invitado ha sido rechazado.", None, None, None, None, None
         else:
            return False, "El registro de la bitácora no se puede modificar.", None, None, None, None, None
      else:
         return False, "No se encontró ningun registro en la bitácora.", None, None, None, None, None

   def getBinnaclePendingRegistry(self):
      binnacle = Binnacle.query.filter(
         Binnacle.kn_status == 0,
         Binnacle.kn_type == 1
      ).first()
      if binnacle is not None:
         binnacleData = dict()
         binnacleData['bitacoraID'] = binnacle.id
         binnacleData['event_id'] = binnacle.kn_event_id
         binnacleData['email'] = binnacle.ds_guest_email
         return True, binnacleData
      else:
         return False, None

   def sendSMSToOrganizer(
      self,
      msg,
      directoryList
   ):
      try:
         for el in directoryList:
            nexmoSMS.send_message({
               'from': 'Nexmo',
               'to': '52'+el,
               'text': msg,
            })
         return True
      except Exception as e:
         return False

   def isCheckedOut(
      self,
      params
   ):
      inCheckoutType = []
      checkoutType = params['checkout']
      if checkoutType == "1":
         inCheckoutType = [2, 3]
      elif checkoutType == "2":
         inCheckoutType = [3]
      binnacle = Binnacle.query.filter(
         Binnacle.kn_event_id == params['event_id'],
         Binnacle.ds_guest_email == params['email'],
         Binnacle.kn_type.in_(inCheckoutType)
      ).first()
      if binnacle == None:
         return False
      else:
         return True

   def checkOut(
      self,
      eventInfo,
      params
   ):
      checkInData = Binnacle.query.filter(
         Binnacle.kn_event_id == params['event_id'],
         Binnacle.ds_guest_email == params['email']
      ).first()
      if checkInData is not None:
         now = commonsService.getServerTime(CONF.APP['debug'])
         binnacle = Binnacle(
            dt_reg_date = now,
            kn_event_id = eventInfo['id'],
            kn_type = 2 if params['checkout'] == "1" else 3, #checkin = 1, checkout = 2 seguridad, checkout = 3 recepcion
            ds_guest_name = eventInfo['ds_name_invitado'],
            ds_guest_email = eventInfo['ds_email_invitado'],
            ds_host_name = eventInfo['ds_host_name'],
            ds_host_email = eventInfo['ds_host_email'],
            kn_status = 1,
            ds_json_devices = eventInfo['devices'],
            ds_badge_number = checkInData.ds_badge_number,
            base64_image = checkInData.base64_image
         )
         try:
            db.session.add(binnacle)
            db.session.commit()
            eventService.updateGuestInvitationDetail(
               eventInfo['id'],
               eventInfo['ds_email_invitado'],
               now,
               True
            )
            return binnacle.id
         except Exception as e:
            db.session.rollback()
            return False
      else:
         return False

   def checkOutGafete(
      self,
      badgeNumber
   ):
      checkInData = Binnacle.query.filter(
         Binnacle.ds_badge_number == badgeNumber
      ).order_by(Binnacle.dt_reg_date.desc()).first()
      if checkInData is not None:
         now = commonsService.getServerTime(CONF.APP['debug'])
         binnacle = Binnacle(
            dt_reg_date = now,
            kn_event_id = checkInData.kn_event_id,
            kn_type = 3, #checkin = 1, checkout = 2 seguridad, checkout = 3 recepcion
            ds_guest_name = checkInData.ds_guest_name,
            ds_guest_email = checkInData.ds_guest_email,
            ds_host_name = checkInData.ds_host_name,
            ds_host_email = checkInData.ds_host_email,
            kn_status = 1,
            ds_json_devices = checkInData.ds_json_devices,
            ds_badge_number = checkInData.ds_badge_number,
            base64_image = checkInData.base64_image
         )
         try:
            db.session.add(binnacle)
            db.session.commit()
            return True
         except Exception as e:
            db.session.rollback()
            return False
      else:
         return False

   def getSignature(
      self,
      email
   ):
      rs_guest = Binnacle.query.filter_by(ds_guest_email=email).first()
      #rs_guest = db.session.query(Binnacle.base64_signature).filter(
         #Binnacle.ds_guest_email == email
      #).first()
      if rs_guest is not None:
       if rs_guest.ds_guest_name is not None:
         guest = dict()
         guest['name'] = rs_guest.ds_guest_name
         return guest
       else:
          return False  
      else:
         return False  