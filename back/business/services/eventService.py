from models.models import *
from datetime import datetime, timedelta
import json
import requests
import uuid
import qrcode
import config as CONF
from flask import url_for
from text.invitation_template import invitation_template, configuration_template, bigbang_template
from business.services.subscriptionService import SubscriptionService
from utils.auth_api import *
import json
import nexmo
from business.services.commonsService import CommonsService

nexmoSMS = nexmo.Client(
   key = CONF.NEXMOKEY, 
   secret = CONF.NEXMOSECRET
)

subscriptionService = SubscriptionService()
commonsService = CommonsService()

qrCodeUrl = CONF.APP_URL_BASE_VALIDATION+CONF.API_BASE_ROUTE+CONF.QR_ENDPOINTS['BASE_ENDPOINT']+CONF.QR_ENDPOINTS['CHECKIN']

class EventService():
   db = db
   graph_endpoint = 'https://graph.microsoft.com/v1.0{0}'

   def getNotification(self, notification):
      for element in notification:
         subscriptionID = element['subscriptionId']
         subscription = subscriptionService.getSubscriptionFromSubscriptionID(subscriptionID)
         get_events_url = subscription.ds_graph_nextlink
         token = subscription.ds_graph_token
         print("ESTA ES LA SUSCRIPTION: ", subscriptionID)
         if not subscription:
            print("NO HAY SUBSCRIPTION")
            continue
         notificationType = element['changeType']
         rCE = self.make_api_call(
            'not_init',
            get_events_url,
            token,
            parameters = {},
            subscription = subscription
         )
         if (rCE.status_code == 200):
            print("Respuesta de servicio obtener evento: ", rCE.status_code)
            json_data = json.loads(rCE.text)
            invitationList = json_data['value']
            for invitation in invitationList:
               if "iCalUId" in invitation:
                  if invitation['isOrganizer']:
                     print("ESTA ES LA NOTIIFICACION: ", invitation)
                     id_result = self.findEventByGraphId(invitation['iCalUId'].strip())
                     if id_result is False:
                        create_event_result = self.createEvent(
                           invitation,
                           subscription,
                           subscriptionID
                        )
                     else:
                        update_event_result = self.updateEvent(
                           invitation,
                           subscriptionID
                        )
               else:
                  if '@removed' in invitation:
                     result_deleted = self.deleteEventByGraphID(invitation['id'])
                  else:
                     continue
         else:
            token, refresh_token = get_token_from_refresh_token(
               subscription.ds_graph_refresh_token,
               CONF.APP_ENDPOINT['APP_AUTH']
            )
            subscriptionService.updateSubscriptionToken(
               subscription, 
               token, 
               refresh_token
            )
            return False
      return True

   def createEvent(
      self,
      invitation,
      subscription,
      subscriptionID
   ):
      if "iCalUId" in invitation:
         masterData = self.getMasterDataFromGraphEvent(invitation)
         result = self.saveEventToDB(masterData)
         if result is not False:
            masterData['id'] = result
            attendees = invitation['attendees']
            masterData['details'] = self.getDetailDataFromGraphEvent(
               masterData, 
               attendees, 
               result, 
               subscriptionID
            )
            result = self.saveEventDetailsToDB(masterData['details'])
            enviarEmail = self.prepareEmail(
               masterData,
               subscription
            )
            return True
         else:
            return False
      else:
         return False

   def updateEvent(
      self,
      invitation,
      subscriptionID
   ):
      if 'iCalUId' in invitation:
         invitationInfo = dict()
         invitationInfo['id'] = self.findEventByGraphId(invitation['iCalUId'].strip())
         invitationInfo['ds_event_id'] = invitation['iCalUId'].strip()
         invitationInfo['ds_event_name'] = invitation['subject']
         invitationInfo['ds_event_place'] = invitation['location']['displayName']
         if 'coordinates' in invitation['location']:
            invitationInfo['ds_event_place_coord'] = invitation['location']['coordinates']
         else:
            invitationInfo['ds_event_place_coord'] = None
         invitationInfo['dt_event_date'] = datetime.strptime(
            invitation['start']['dateTime'][0:19],
            "%Y-%m-%dT%H:%M:%S"
         )
         invitationInfo['dt_event_date_end'] = datetime.strptime(
            invitation['end']['dateTime'][0:19],
            "%Y-%m-%dT%H:%M:%S"
         )
         invitationInfo['dt_event_created'] = datetime.strptime(
            invitation['createdDateTime'][0:19],
            "%Y-%m-%dT%H:%M:%S"
         )
         invitationInfo['ds_host_email'] = invitation['organizer']['emailAddress']['address'].lower()
         result = self.updateEventToDB(invitationInfo)
         if result is not False:
            listaInvitados = []
            attendees = invitation['attendees']
            for attendee in attendees:                  
               attendeesData = dict()
               attendeesData['kn_event_id'] = invitationInfo['id']
               attendeesData['ds_email_invitado'] = attendee['emailAddress']['address'].lower()
               attendeesData['ds_name_invitado'] = attendee['emailAddress']['name']
               attendeesData['ds_event_response'] = attendee['status']['response']
               listaInvitados.append(attendeesData)
            invitationInfo['details'] = listaInvitados
            result = self.updateEventDetailsToDB(
               invitationInfo['id'],
               invitationInfo['details']
            )
            enviarEmail = self.prepareEmail(
               invitationInfo,
               subscriptionID
            )
         return True
      else:
         return False

   def findEventByGraphId(self, graph_id):
      query_result = Invitacion.query.filter(
         Invitacion.ds_event_id == graph_id
      ).first()
      if query_result == None:
         return False
      else:
         return query_result.id

   def saveEventToDB(self, data):
      if 'ds_event_id' in data:
         exist = self.findEventByGraphId(data['ds_event_id'])
         if exist == False:
            invitacion = Invitacion(**data)
         else:
            return False
      else:
         invitacion = Invitacion(**data)
      try:
         db.session.add(invitacion)
         db.session.commit()
         return invitacion.id
      except Exception as e:
         db.session.rollback()
         return False

   def updateEventToDB(self, data):
      try:
         invitacion = Invitacion.query.get(data['id'])
         if invitacion is not None:
            invitacion.ds_event_name = data['ds_event_name']
            invitacion.ds_event_place = data['ds_event_place']
            invitacion.ds_event_place_coord = data['ds_event_place_coord']
            invitacion.dt_event_date = data['dt_event_date']
            invitacion.dt_event_date_end = data['dt_event_date_end']
            invitacion.ds_host_email = data['ds_host_email']
            db.session.add(invitacion)
            db.session.commit()
            return True
         else:
            db.session.rollback()
            return False
      except Exception as e:
         return False

   def saveEventDetailsToDB(self, data):
      if len(data) > 0:
         try:
            details = db.session()
            res = details.execute(
               Invitados.__table__.insert(),
               data
            )
            db.session.commit()
            return True
         except Exception as e:
            db.session.rollback()
            return False

   def updateEventDetailsToDB(self, event_id, data):
      if len(data) > 0:
         try:
            for item in data:
               details = Invitados.query.filter(
                  Invitados.kn_event_id == event_id,
                  Invitados.ds_email_invitado == item['ds_email_invitado']
               ).first()
               if details is not None:
                  eventDetail = Invitados.query.get(details.id)
                  eventDetail.ds_event_response = item['ds_event_response']
                  db.session.add(eventDetail)
                  db.session.commit()
               elif details is None:
                  eventDetail = Invitados(
                     kn_event_id = item['kn_event_id'],
                     ds_email_invitado = item['ds_email_invitado'],
                     ds_name_invitado = item['ds_name_invitado'],
                     ds_event_response = item['ds_event_response']
                  )
                  db.session.add(eventDetail)
                  db.session.commit()
            return True
         except Exception as e:
            db.session.rollback()
            return False

   def initEventsWithDelta(self, subscription):
      initDay = self.add_days(0)
      endDay = self.add_days(90)
      get_events_url = self.graph_endpoint.format('/me/calendarView/delta?startdatetime='+initDay+'&enddatetime='+endDay)
      r = self.make_api_call(
         'init',
         get_events_url,
         subscription.ds_graph_token,
         parameters = {}
      )
      if (r.status_code == requests.codes.ok):
         json_data = json.loads(r.text)
         return json_data['@odata.nextLink']
      else:
         return None

   def add_days(self, n_day):
      #now = datetime.datetime.now()
      now = datetime.now()
      #add_days = datetime.timedelta(days=2)
      add_days = timedelta(days=n_day)
      date_end = now + add_days
      return date_end.isoformat(sep='T', timespec='auto')+'z'

   def make_api_call(
      self,
      method,
      url,
      token,
      payload = None,
      parameters = None,
      subscription = None,
   ):
      # Send these headers with all API calls
      headers = {
         'User-Agent' : 'python_tutorial/1.0',
         'Authorization' : 'Bearer {0}'.format(token),
         'Accept' : 'application/json',
         'Content-type': 'application/json',
         'Prefer': "outlook.timezone=\"Central Standard Time\""
      }
                
      # Use these headers to instrument calls. Makes it easier
      # to correlate requests and responses in case of problems
      # and is a recommended best practice.
      request_id = str(uuid.uuid4())
      instrumentation = {
         'client-request-id' : request_id,
         'return-client-request-id' : 'true'
      }
                        
      headers.update(instrumentation)
    
      response = None
    
      if (method == 'init'):
         response = requests.get(
            url,
            headers = headers,
            params = parameters
         )
         if response.status_code != 401:
            json_data = json.loads(response.text)
            nextLink = json_data['@odata.nextLink']
         return response
      elif (method == 'not_init'):
         response = requests.get(
            url,
            headers = headers,
            params = parameters
         )
         print("Respuesta de servicio [deltalink]: ", response.status_code)
         if response.status_code != 401:
            json_data = json.loads(response.text)
            nextLink = json_data['@odata.deltaLink']
            subscriptionService.updateSubscriptionToDB(
               subscription,
               nextLink
            )
         return response
      elif (method == 'mail'):
         response = requests.post(
            url,
            data = json.dumps(payload),
            headers = headers,
            params = parameters
         )
         return response
      elif (method == 'renew'):
         response = requests.patch(
            url,
            data = json.dumps(payload),
            headers = headers
         )
         return response

   def prepareEmail(
      self,
      invitationInfo,
      subscriptionID
   ):
      kn_event_id = invitationInfo['id']
      eventName = invitationInfo['ds_event_name']
      place = invitationInfo['ds_event_place']
      eventDate = self.current_date_format(invitationInfo['dt_event_date'])
      eventHour = invitationInfo['dt_event_date'].strftime('%H:%M') + " - " + invitationInfo['dt_event_date_end'].strftime('%H:%M')
      details = invitationInfo['details']
      for attendee in details:
         email = attendee['ds_email_invitado'].lower()
         guestName = attendee['ds_name_invitado']
         if (attendee['ds_event_response'] == 'accepted' or attendee['ds_event_response'] == 'tentativelyAccepted'):
            checkIfEmailWasSent = self.checkIfEmailWasSent(email, kn_event_id)
            if not checkIfEmailWasSent:
               emailSent = self.sendEmail(
                  email,
                  kn_event_id,
                  eventName,
                  place,
                  eventDate,
                  eventHour,
                  guestName,
                  subscriptionID
               )
      return True

   def checkIfEmailWasSent(
      self,
      email,
      kn_event_id
   ):
      query_result = Invitados.query.filter(
         Invitados.kn_event_id == kn_event_id,
         Invitados.ds_email_invitado == email,
         Invitados.ds_event_response == 'accepted',
         Invitados.kn_email_sent == 1
      ).first()
      if query_result == None:
         return False
      else:
         return True

   def sendEmail(
      self,
      email,
      kn_event_id,
      eventName,
      place,
      eventDate,
      eventHour,
      guestName,
      subscriptionID
   ):
      subscription = subscriptionService.getSubscriptionFromSubscriptionID(subscriptionID)
      token = subscription.ds_graph_token
      urlToQRCode = self.makeQRCode(email, kn_event_id)
      registryURL = CONF.FRONT['FRONT_BASE']+CONF.EVENTREGISTRY['BASE']+CONF.FRONT['PARAM_INDICATOR']+CONF.FRONT['EVENT_ID']+str(kn_event_id)+CONF.FRONT['PARAM_SEPARATOR']+CONF.EVENTREGISTRY['EMAIL']+email
      template = self.validateTemplate(email, kn_event_id, eventName, place, eventDate, eventHour, guestName, subscriptionID, registryURL)
      jsonData = {
        "message": {
          "subject": "Has aceptado asistir al evento ["+eventName+"]",
          "body": {
            "contentType": "HTML",
            "content": template
          },
          "toRecipients": [
            {
              "emailAddress": {
                "address": email
              }
            }
          ],
          "internetMessageHeaders":[
            {
              "name":"x-custom-header-group-name",
              "value":"Nevada"
            },
            {
              "name":"x-custom-header-group-id",
              "value":"NV001"
            }
          ]
        }
      }
      sendEmail = self.make_api_call(
         'mail',
         self.graph_endpoint.format(CONF.SEND_EMAIL_ENDPOINT),
         token,
         payload = jsonData,
         parameters = {}
      )
      if sendEmail.status_code == 202:
         result = self.setEmailSentToTrue(email, kn_event_id)
      return sendEmail

   def makeQRCode(self, email, kn_event_id):
      qrCode = qrcode.QRCode(
         version = 1,
         error_correction =  qrcode.constants.ERROR_CORRECT_L,
         box_size = 10,
         border = 4,
      )
      qrCode.add_data(qrCodeUrl+"?email="+email+"&kn_event_id="+str(kn_event_id))
      qrCode.make(fit = True)
      qrIMG = qrCode.make_image(
         fill_color = "black",
         back_color = "white"
      )
      qrIMG.save(CONF.QR_STATIC_PATH+str(kn_event_id)+"_"+email+".png")
      return url_for('static', filename = "img/qr/"+str(kn_event_id)+"_"+email+".png")

   def setEmailSentToTrue(
      self,
      email,
      kn_event_id
   ):
      try:
         invitado = Invitados.query.filter(
            Invitados.kn_event_id == kn_event_id,
            Invitados.ds_email_invitado == email
         ).first()
         invitado = Invitados.query.get(invitado.id)
         invitado.kn_email_sent = 1
         db.session.add(invitado)
         db.session.commit()
         return True
      except Exception as e:
         db.session.rollback()
         return False

   def getEvents(self, params = False):
      if 'email' in params:
         query_eventos = Invitacion.query.join(Invitados).filter(
            Invitados.ds_email_invitado == params['email'],
            Invitados.ds_event_response == 'accepted',
            Invitacion.dt_event_date_end >= commonsService.getServerTime(CONF.APP['debug']) - timedelta(hours = 3)
         ).order_by(Invitacion.dt_event_date.asc()).all()
         eventos = []
         for item in query_eventos:
            eventoInfo = dict()
            eventoInfo['id'] = item.id
            eventoInfo['ds_event_name'] = item.ds_event_name
            eventoInfo['ds_event_place'] = item.ds_event_place
            eventoInfo['dt_event_date'] = item.dt_event_date.strftime('%m/%d/%Y')
            eventoInfo['event_hour'] = item.dt_event_date.strftime('%H:%M')
            eventoInfo['dt_event_created'] = item.dt_event_created.strftime('%m/%d/%Y %H:%M:%S')
            eventoInfo['ds_host_email'] = item.ds_host_name + "<" + item.ds_host_email + ">"
            eventos.append(eventoInfo)
         return eventos
      elif 'event_id' in params:
         query_eventos = db.session.query(Invitacion, Invitados).join(Invitados).filter(
            Invitados.kn_event_id == Invitacion.id,
            Invitados.kn_event_id == params['event_id']
         ).all()
         eventoInfo = dict()
         eventoInfo['id'] = query_eventos[0].Invitacion.id
         eventoInfo['ds_event_name'] = query_eventos[0].Invitacion.ds_event_name
         eventoInfo['ds_event_place'] = query_eventos[0].Invitacion.ds_event_place
         eventoInfo['dt_event_date'] = query_eventos[0].Invitacion.dt_event_date.strftime('%m/%d/%Y')
         eventoInfo['event_hour'] = query_eventos[0].Invitacion.dt_event_date.strftime('%H:%M') + " - " + query_eventos[0].Invitacion.dt_event_date_end.strftime('%H:%M:%S')
         eventoInfo['dt_event_created'] = query_eventos[0].Invitacion.dt_event_created.strftime('%m/%d/%Y %H:%M:%S')
         eventoInfo['ds_host_email'] = query_eventos[0].Invitacion.ds_host_name + "<" + query_eventos[0].Invitacion.ds_host_email + ">"
         detalles = []
         for item, invitados in query_eventos:
            detalle = dict()
            detalle['ds_email_invitado'] = invitados.ds_email_invitado
            detalle['ds_name_invitado'] = invitados.ds_name_invitado
            detalles.append(detalle)
         eventoInfo['detalles'] = detalles
         return eventoInfo
      elif 'srv' in params:
         query_eventos = db.session.query(Invitados).with_entities(Invitados.kn_event_id).distinct(Invitados.kn_event_id).filter(
            Invitados.ds_email_invitado.in_(CONF.GRALSRV_EMAIL)
         ).all()
         idsEvents = []
         eventos = []
         for element in query_eventos:
            idsEvents.append(element.kn_event_id)
         if len(idsEvents) > 0:
            query_eventos = db.session.query(Invitacion, Invitados).join(Invitados).filter(
               Invitacion.id == Invitados.kn_event_id,
               Invitacion.dt_event_date_end >= commonsService.getServerTime(CONF.APP['debug']) - timedelta(hours = 3),
               Invitacion.id.in_(idsEvents)
            ).order_by(Invitacion.dt_event_date.asc()).all()
            idTemporal = None
            eventInfo = dict()
            for inv, details in query_eventos:
               if (idTemporal != inv.id):
                  if idTemporal != None:
                     eventos.append(eventInfo)
                  eventInfo = dict()
                  eventInfo['id'] = inv.id
                  eventInfo['ds_event_name'] = inv.ds_event_name
                  eventInfo['ds_event_place'] = inv.ds_event_place
                  eventInfo['dt_event_date'] = inv.dt_event_date.strftime('%d/%m/%Y')
                  eventInfo['event_hour'] = inv.dt_event_date.strftime('%H:%M') + " - " + inv.dt_event_date_end.strftime('%H:%M')
                  eventInfo['dt_event_created'] = inv.dt_event_created.strftime('%m/%d/%Y %H:%M:%S')
                  eventInfo['ds_host_email'] = inv.ds_host_name
                  eventInfo['ds_invitation_config'] = inv.ds_invitation_config
                  eventInfo['kn_attended'] = inv.kn_attended
                  eventInfo['bol_attended'] = True if inv.kn_attended == 1 else False
                  eventInfo['detalles'] = []
                  detalle = dict()
                  detalle['id'] = details.id
                  detalle['kn_event_id'] = details.kn_event_id
                  detalle['ds_email_invitado'] = details.ds_email_invitado
                  detalle['ds_name_invitado'] = details.ds_name_invitado
                  detalle['ds_event_response'] = details.ds_event_response
                  eventInfo['detalles'].append(detalle)
                  idTemporal = inv.id
               else:
                  detalle = dict()
                  detalle['id'] = details.id
                  detalle['kn_event_id'] = details.kn_event_id
                  detalle['ds_email_invitado'] = details.ds_email_invitado
                  detalle['ds_name_invitado'] = details.ds_name_invitado
                  detalle['ds_event_response'] = details.ds_event_response
                  eventInfo['detalles'].append(detalle)
                  idTemporal = inv.id
            eventos.append(eventInfo)
         return eventos
      elif 'today' in params:
         startdate = (commonsService.getServerTime(CONF.APP['debug'])).strftime('%Y/%m/%d')
         enddate = (commonsService.getServerTime(CONF.APP['debug'])+ timedelta(days = 1)).strftime('%Y/%m/%d')

         query_eventos = db.session.query(Invitacion).filter(
            Invitacion.dt_event_date >= startdate,
            Invitacion.dt_event_date <= enddate,
            Invitacion.ds_event_id != None
         ).order_by(Invitacion.dt_event_date.asc()).all()
         eventos = []
         for item in query_eventos:
            eventoInfo = dict()
            eventoInfo['id'] = item.id
            eventoInfo['ds_event_name'] = item.ds_event_name
            eventoInfo['ds_event_place'] = item.ds_event_place
            eventoInfo['dt_event_date'] = item.dt_event_date.strftime('%m/%d/%Y')
            eventoInfo['event_hour'] = item.dt_event_date.strftime('%H:%M')
            eventoInfo['dt_event_created'] = item.dt_event_created.strftime('%m/%d/%Y %H:%M:%S')
            eventoInfo['ds_host_email'] = item.ds_host_name + "<" + item.ds_host_email + ">"
            eventos.append(eventoInfo)
         return eventos
           

   def current_date_format(self, date):
      months = (
         "Enero",
         "Febrero",
         "Marzo",
         "Abri", 
         "Mayo", 
         "Junio", 
         "Julio", 
         "Agosto", 
         "Septiembre", 
         "Octubre", 
         "Noviembre", 
         "Diciembre"
      )
      day = date.day
      month = months[date.month - 1]
      year = date.year
      messsage = "{} de {} del {}".format(day, month, year)

      return messsage

   def getTokenFromSubscriptionID(
      self,
      id
   ):
      subscription = Subscription.query.get(id)
      if query_result == None:
         return False
      else:
         return subscription

   def getEventInfoFromQR(
      self,
      params
   ):
      item = db.session.query(Invitacion, Invitados).join(Invitados).filter(
         Invitados.ds_email_invitado == params['email'],
         Invitados.kn_event_id == params['event_id']
      ).first()
      if item is not None:
         eventInfo = dict()
         eventInfo['id'] = item.Invitacion.id
         eventInfo['ds_event_name'] = item.Invitacion.ds_event_name
         eventInfo['ds_event_place'] = item.Invitacion.ds_event_place
         eventInfo['dt_event_date'] = item.Invitacion.dt_event_date.strftime('%m/%d/%Y')
         eventInfo['str_event_date'] = self.current_date_format(item.Invitacion.dt_event_date)
         eventInfo['event_hour'] = item.Invitacion.dt_event_date.strftime('%H:%M') + " - " + item.Invitacion.dt_event_date_end.strftime('%H:%M')
         eventInfo['dt_event_created'] = item.Invitacion.dt_event_created.strftime('%m/%d/%Y %H:%M:%S')
         eventInfo['ds_host_email'] = item.Invitacion.ds_host_email
         eventInfo['ds_host_name'] = item.Invitacion.ds_host_name
         eventInfo['ds_email_invitado'] = item.Invitados.ds_email_invitado
         eventInfo['ds_name_invitado'] = item.Invitados.ds_name_invitado
         
         if 'checkout' not in params:
            if item.Invitados.ds_json_devices is None:
               eventInfo['devices'] = []
            else:
               eventInfo['devices'] = item.Invitados.ds_json_devices
            return eventInfo
         else:
            binnacle = Binnacle.query.filter(
               Binnacle.kn_event_id == params['event_id'],
               Binnacle.ds_guest_email == params['email'],
               Binnacle.kn_type == 1
            ).first()
            if binnacle is not None:
               eventInfo['foto'] = binnacle.base64_image.decode('utf-8')
               eventInfo['devices'] = binnacle.ds_json_devices
               eventInfo['signature'] = binnacle.base64_signature.decode('utf-8')
         return eventInfo
      else:
         return False

   def updateGuestInvitationDetail(
      self,
      event_id,
      guest_email,
      dt_date,
      checkout = False
   ):
      try:
         detail = Invitados.query.filter(
            Invitados.kn_event_id == event_id,
            Invitados.ds_email_invitado == guest_email
         ).first()
         if not checkout:
            detail.kn_checkin = 1
            detail.dt_checkin = dt_date
         else:
            detail.dt_checkout = dt_date
         db.session.add(detail)
         db.session.commit()
         return True
      except Exception as e:
         db.session.rollback()
         return False

   def sendEmailToGS(
      self,
      kn_event_id,
      organizer,
      eventName,
      place,
      eventDate,
      eventHour,
      subscriptionID
   ):
      subscription = subscriptionService.getSubscriptionFromSubscriptionID(subscriptionID)
      token = subscription.ds_graph_token
      configURL = CONF.FRONT['FRONT_BASE']+CONF.FRONT['CONFIG_WIZARD']+CONF.FRONT['PARAM_INDICATOR']+CONF.FRONT['EVENT_ID']+str(kn_event_id)
      htmlEmail = configuration_template.format(
         CONF.APP_URL_BASE_VALIDATION+url_for('static', filename='img/logo-header.png'),
         CONF.APP_URL_BASE_VALIDATION+url_for('static', filename='img/logo-footer.webp'),
         eventName,
         place,
         eventDate,
         eventHour,
         configURL
      )
      jsonData = {
        "message": {
          "subject": "Por favor, configura tu evento ["+eventName+"]",
          "body": {
            "contentType": "HTML",
            "content": htmlEmail
          },
          "toRecipients": [
            {
              "emailAddress": {
                "address": organizer
              }
            }
          ],
          "internetMessageHeaders":[
            {
              "name":"x-custom-header-group-name",
              "value":"Nevada"
            },
            {
              "name":"x-custom-header-group-id",
              "value":"NV001"
            }
          ]
        }
      }
      sendEmail = self.make_api_call(
         'mail',
         self.graph_endpoint.format(CONF.SEND_EMAIL_ENDPOINT),
         token,
         payload = jsonData,
         parameters = {}
      )
      return sendEmail

   def setInvitationConfig(
      self,
      data
   ):
      event_id = data['event_id']
      try:
         invitacion = Invitacion.query.get(event_id)
         if invitacion is not None:
            invitacion.ds_invitation_config = data['data']
            db.session.add(invitacion)
            db.session.commit()
            self.enviarSMSToGS(invitacion.ds_event_name, invitacion.id)
            if data['data']['mkt'] is not None:
               self.enviarSMSToMKT(invitacion.ds_event_name, invitacion.id)
            return True
         else:
            return False
      except Exception as e:
         db.session.rollback()
         return False

   def getDirectoryListFromEvent(
      self,
      event_id
   ):
      organizerNumber = None
      try:
         directory = []
         invitacion = Invitacion.query.get(event_id)
         directory_query = Directory.query.filter(
            Directory.ds_email == invitacion.ds_host_email
         ).first()
         if directory_query is not None:
            organizerNumber = directory_query.ds_phone
            directory.append(organizerNumber)
         if invitacion is not None:
            configuracion = invitacion.ds_invitation_config
            if configuracion is not None:
               notificar = configuracion['notificar']
               for el in notificar:
                  directory.append(el['phone'])
         return directory
      except Exception as e:
         return False

   def updateAttendedEvent(
      self,
      params
   ):
      try:
         event = Invitacion.query.get(params['event_id'])
         attended = 0
         if params['attended'] == 'true':
            attended = 1
         event.kn_attended = attended
         db.session.add(event)
         db.session.commit()
         return True
      except Exception as e:
         db.session.rollback()
         return False

   def getMasterDataFromGraphEvent(
      self,
      invitation
   ):
      newInvitation = dict()
      newInvitation['ds_event_id'] = invitation['iCalUId'].strip()
      newInvitation['ds_graph_id'] = invitation['id'].strip()
      newInvitation['ds_event_name'] = invitation['subject']
      newInvitation['ds_event_place'] = invitation['location']['displayName']
      if 'coordinates' in invitation['location']:
         newInvitation['ds_event_place_coord'] = invitation['location']['coordinates']
      else:
         newInvitation['ds_event_place_coord'] = None
      newInvitation['dt_event_date'] = datetime.strptime(
         invitation['start']['dateTime'][0:19],
         "%Y-%m-%dT%H:%M:%S"
      )
      newInvitation['dt_event_date_end'] = datetime.strptime(
         invitation['end']['dateTime'][0:19],
         "%Y-%m-%dT%H:%M:%S"
      )
      newInvitation['dt_event_created'] = datetime.strptime(
         invitation['createdDateTime'][0:19],
         "%Y-%m-%dT%H:%M:%S"
      )
      newInvitation['ds_host_email'] = invitation['organizer']['emailAddress']['address'].lower()
      newInvitation['ds_host_name'] = invitation['organizer']['emailAddress']['name'].title()
      return newInvitation

   def getDetailDataFromGraphEvent(
      self,
      newInvitation,
      attendees,
      result,
      subscriptionID
   ):
      emailSendGeneralServices = False
      listaInvitados = []
      for attendee in attendees:
         attendeesData = dict()
         attendeesData['kn_event_id'] = result
         attendeesData['ds_email_invitado'] = attendee['emailAddress']['address'].lower()
         attendeesData['ds_name_invitado'] = attendee['emailAddress']['name']
         attendeesData['ds_event_response'] = attendee['status']['response']
         listaInvitados.append(attendeesData)
         if (attendee['emailAddress']['address'].lower() in CONF.GRALSRV_EMAIL and emailSendGeneralServices == False):
            self.sendEmailToGS(
               result,
               newInvitation['ds_host_email'],
               newInvitation['ds_event_name'],
               newInvitation['ds_event_place'],
               self.current_date_format(newInvitation['dt_event_date']),
               newInvitation['dt_event_date'].strftime('%H:%M') + " - " + newInvitation['dt_event_date_end'].strftime('%H:%M'),
               subscriptionID
            )
            emailSendGeneralServices = True
      return listaInvitados

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
      eventoInfo['event_hour'] = query_eventos[0].Invitacion.dt_event_date.strftime('%H:%M')
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
      name = data['name']
      try:
         invitado = Invitados.query.filter(
            Invitados.kn_event_id == event_id,
            Invitados.ds_email_invitado == email
         ).first()
         if invitado is not None:
            invitado.ds_json_devices = data['devices']
            invitado.ds_name_invitado = data['name']
            db.session.add(invitado)
            db.session.commit()
            return True
         else:
            return False
      except Exception as e:
         db.session.rollback()
         return False

   def deleteEventByGraphID(
      self,
      graph_id
   ):
      try:
         invitation = Invitacion.query.filter(
            Invitacion.ds_graph_id == graph_id
         ).first()
         if invitation is not None:
            invitation.kn_cancelled = 1
            db.session.add(invitation)
            db.session.commit()
            return True
         else:
            return False
      except Exception as e:
         db.session.rollback()
         return False

   def enviarSMSToGS(
      self, 
      event_name, 
      id
   ):
      try:
         directory = Directory.query.filter(
            Directory.ds_email.in_(CONF.GRALSRV_EMAIL)
         ).all()
         for el in directory:
            nexmoSMS.send_message({
               'from': 'Nexmo',
               'to': '52'+el.ds_phone,
               'text': "Han generado un evento donde se requiere intervencion de servicios generales <{} - {}>.".format(event_name, str(id)),
            })
         return True
      except Exception as e:
         return False

   def createInvitationAndDetails(
      self,
      data
   ):
      invitation = self.getMasterDataFromBody(data)
      result = self.saveEventToDB(invitation)
      if result is not False:
         invitation['details'] = self.getDetailDataFromBody(
            result,
            data
         )
         result = self.saveEventDetailsToDB(invitation['details'])
         if result is not False:
            eventInfo = dict()
            eventInfo['email'] = invitation['details']['ds_email_invitado']
            eventInfo['kn_event_id'] = invitation['details']['kn_event_id']
            eventInfo['devices'] = invitation['details']['ds_json_devices']
            eventInfo['foto'] = data['foto']
            eventInfo['signature'] = data['signature']
            return eventInfo
      else:
         return False

   def getMasterDataFromBody(
      self,
      data
   ):
      invitation = dict()
      invitation['dt_event_date'] = commonsService.getServerTime(CONF.APP['debug'])
      invitation['dt_event_date_end'] = commonsService.getServerTime(CONF.APP['debug'])
      invitation['dt_event_created'] = commonsService.getServerTime(CONF.APP['debug'])
      invitation['ds_host_name'] = data['visita'].title()
      invitation['ds_event_name'] = data['motivo'].title()
      invitation['ds_event_place'] = "Corporativo Axity Dos Patios"
      return invitation

   def getDetailDataFromBody(
      self,
      kn_event_id,
      data
   ): 
      invitado = dict()
      invitado['kn_event_id'] = kn_event_id
      invitado['ds_email_invitado'] = data['email'].lower()
      invitado['ds_name_invitado'] = data['nombre'].title()
      invitado['ds_event_response'] = 'accepted'
      invitado['kn_email_sent'] = 1
      invitado['ds_json_devices'] = data['devices']
      return invitado

   def enviarSMSToMKT(
      self, 
      event_name, 
      id
   ):
      try:
         directory = Directory.query.filter(
            Directory.ds_email.in_(CONF.MKT_EMAIL)
         ).all()
         for el in directory:
            nexmoSMS.send_message({
               'from': 'Nexmo',
               'to': '52'+el.ds_phone,
               'text': "Han generado un evento donde se requiere intervención de Marketing <{} - {}>.".format(event_name, str(id)),
            })
         return True
      except Exception as e:
         return False

   def renewSubscription(
      self
   ):
      response = False
      failed_attempts = 0
      while True:
         subscriptions = Subscription.query.all()
         renewDate = self.add_days(1)
         counter = 0
         for subscription in subscriptions:
            result = self.renewThisSubscription(
               renewDate,
               subscription
            )
            if result == False:
               failed_attempts = failed_attempts + 1
               break
            else:
               counter = counter + 1
               failed_attempts = 0
         if counter == len(subscriptions):
            response = True
            break
         if failed_attempts == 20:
            break
      return response

   def renewThisSubscription(
      self,
      renewDate,
      subscription,
   ):
      token = subscription.ds_graph_token
      refresh_token = subscription.ds_graph_refresh_token
      strSubscription = subscription.ds_subscription
      renew = self.make_api_call(
         'renew',
         CONF.GRAPH_ENDPOINT['APP_SUBSCRIPTIONS']+"/"+strSubscription,
         token,
         payload = {"expirationDateTime": renewDate}
      )
      if (renew.status_code == 200):
         return True
      else:
         token, refresh_token = get_token_from_refresh_token(
            refresh_token,
            CONF.APP_ENDPOINT['APP_AUTH']
         )
         subscriptionService.updateSubscriptionToken(
            subscription, 
            token, 
            refresh_token
         )
         return False

   def validateTemplate(self, email, kn_event_id, eventName, place, eventDate, eventHour, guestName, subscriptionID, registryURL):
      if place.replace(" ", "") != 'BigBangMX':
         htmlEmail = invitation_template.format(
            CONF.APP_URL_BASE_VALIDATION+url_for('static', filename='img/logo-header.png'),
            CONF.APP_URL_BASE_VALIDATION+url_for('static', filename='img/qr/'+str(kn_event_id)+'_'+email+'.png'),
            CONF.APP_URL_BASE_VALIDATION+url_for('static', filename='img/avatar-polux.png'),
            CONF.APP_URL_BASE_VALIDATION+url_for('static', filename='img/logo-footer.webp'),
            guestName,
            eventName,
            place,
            eventDate,
            eventHour,
            CONF.APP_URL_BASE_VALIDATION+url_for('static', filename='img/axity-map.png'),
            registryURL
         )
      else:
         htmlEmail = bigbang_template.format(
            CONF.APP_URL_BASE_VALIDATION+url_for('static', filename='img/logo-header.png'),
            CONF.APP_URL_BASE_VALIDATION+url_for('static', filename='img/qr/'+str(kn_event_id)+'_'+email+'.png'),
            CONF.APP_URL_BASE_VALIDATION+url_for('static', filename='img/avatar-polux.png'),
            CONF.APP_URL_BASE_VALIDATION+url_for('static', filename='img/logo-footer.webp'),
            guestName,
            eventName,
            place,
            eventDate,
            eventHour,
            CONF.APP_URL_BASE_VALIDATION+url_for('static', filename='img/axity-map.png'),
            registryURL,
            CONF.APP_URL_BASE_VALIDATION+url_for('static', filename='alexa.png')
            )
      return htmlEmail