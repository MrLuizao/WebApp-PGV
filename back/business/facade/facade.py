from business.services.invitationService import InvitationService
from business.services.eventService import EventService
from business.services.userServices import UserService
from business.services.subscriptionService import SubscriptionService
from business.services.guestService import GuestService
from business.services.directoryService import DirectoryService
from business.services.binnacleService import BinnacleService
from business.services.guestProfileService import GuestProfileService
from business.services.privacityService import PrivacityService
from business.services.employeeService import EmployeeService
import json

invitationService = InvitationService()
eventService = EventService()
usuarioService = UserService()
subscriptionService = SubscriptionService()
guestService = GuestService()
directoryService = DirectoryService()
binnacleService = BinnacleService()
guestProfileService = GuestProfileService()
privacityService = PrivacityService()
employeeService = EmployeeService()

class Facade():
   def getAllInvitaciones(self):
      invitaciones = invitationService.getAllInvitaciones()
      return invitaciones

   def newEvents(self, events):
      invitationService.newEvents(events)
      return True

   def getEventsByDate(self, date):
      invitaciones = invitationService.getEventsByDate(date)
      return True

   def getNotification(self, notification):
      notification = eventService.getNotification(notification)
      return notification

   def initEventsWithDelta(
      self,
      token,
      refreshToken,
      subscriptionID
   ):
      subscription = subscriptionService.saveSubscriptionToDB(
         subscriptionID,
         token,
         refreshToken
      )
      if subscription is not None:
         nextLink = eventService.initEventsWithDelta(subscription)
         if nextLink is not None:
            subscriptionService.updateSubscriptionToDB(
               subscription,
               nextLink
            )
            return nextLink
      else:
         return False

   def userRegister(self, user):
      usuario = usuarioService.addUser(user)
      if usuario == True:
         return True
      else:
         return False

   def loginUser(self, user):
      return usuarioService.loginUser(user)


   def getEvents(self, params = False):
      eventos = eventService.getEvents(params)
      return eventos

   def userExist(
      self,
      data
   ):
      exist = usuarioService.userExist(data)
      return exist

   def userDirectoryExist(
      self,
      data
   ):
      exist = directoryService.userDirectoryExist(data)
      return exist

   def getEventInfoFromQR(
      self,
      params
   ):
      eventInfo = eventService.getEventInfoFromQR(params)
      return eventInfo

   def checkIn(
      self,
      eventInfo,
      body
   ):
      checkin = guestService.checkIn(
         eventInfo,
         body
      )
      return checkin

   def isCheckedIn(
      self,
      params
   ):
      return guestService.isCheckedIn(params)

   def confirmCheckIn(
      self,
      data
   ):
      isCheckIn, msg, event_id, guest_email, dt_checkin, guest_name, badge_number = guestService.confirmCheckIn(data)
      return isCheckIn, msg, event_id, guest_email, dt_checkin, guest_name, badge_number

   def updateGuestInvitationDetail(
      self,
      event_id,
      guest_email,
      dt_checkin,
      badge_number
   ):
      return eventService.updateGuestInvitationDetail(
         event_id,
         guest_email,
         dt_checkin,
         badge_number
      )

   def getBinnaclePendingRegistry(self):
      return guestService.getBinnaclePendingRegistry()

   def sendSMSToOrganizer(
      self,
      msg,
      directoryList
   ):
      return guestService.sendSMSToOrganizer(msg, directoryList)

   def getDirectoryList(self):
      return directoryService.getDirectoryList()

   def addToDirectory(
      self,
      data
   ):
      return directoryService.addToDirectory(data)

   def getDirectoryByID(
      self, 
      id
   ):
      return directoryService.getDirectoryByID(id)

   def updateDirectoryByID(
      self,
      data
   ):
      return directoryService.updateDirectoryByID(data)

   def deleteDirectoryByID(
      self,
      id
   ):
      return directoryService.deleteDirectoryByID(id)

   def setInvitationConfig(
      self,
      data
   ):
      return eventService.setInvitationConfig(data)

   def isCheckedOut(
      self,
      params
   ):
      return guestService.isCheckedOut(params)

   def checkOut(
      self,
      eventInfo,
      params
   ):
      return guestService.checkOut(
         eventInfo,
         params
      )

   def getDirectoryListFromEvent(
      self,
      event_id
   ):
      return eventService.getDirectoryListFromEvent(event_id)

   def updateAttendedEvent(
      self,
      params
   ):
      return eventService.updateAttendedEvent(params)

   def getDevicesInfo(
      self,
      params
   ):
      return eventService.getDevicesInfo(params)

   def setDevicesConfig(
      self,
      data
   ):
      return eventService.setDevicesConfig(data)


   def getProfileDevicesInfo(
      self,
      params
   ):
      getDevice = usuarioService.getProfileDevicesInfo(params)
      return getDevice


   def setProfileDevicesConfig(
      self,
      data
   ):
      setDevice = usuarioService.setProfileDevicesConfig(data)
      return setDevice

   def getBinnacleRecords(
      self,
      fechas
   ):
      return binnacleService.getBinnacleRecords(fechas)

   def getGuestNameByEmail(
      self,
      email
   ):
      return guestProfileService.getGuestNameByEmail(email)

   def createInvitationAndDetails(
      self,
      data
   ):
      return eventService.createInvitationAndDetails(data)

   def manualCheckIn(
      self,
      data
   ):
      return guestService.manualCheckIn()

   def getXLSXFromBinnacle(
      self,
      fechas
   ):
      return binnacleService.getXLSXFromBinnacle(fechas)

   def checkOutGafete(
      self, 
      badgeNumber
   ):
      return guestService.checkOutGafete(badgeNumber)

   def renewSubscription(
      self
   ):
      return eventService.renewSubscription()

   def getRoleList(self):
      return usuarioService.getUserListByRole()

   def getSignature( self,
      email
      ):
      return guestService.getSignature(email)

   def getSignaturePrivacity(self, 
      email
      ):
      return privacityService.getSignaturePrivacity(email)
   
   def getEmployeesList(self, 
      nameString
      ):
      return employeeService.getEmployeesList(nameString)
