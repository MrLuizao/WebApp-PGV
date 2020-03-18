from models.models import *
import json

class UserService():
   db = db

   def addUser(self, user):
      user = Users(
         ds_name_register = user['name'],
         tel_user_register = user['telephone'],
         ds_email_register = user['email'],
         ds_pass_register = user['password'],
         ds_user_role = user['role']
      )
      try:
         db.session.add(user)
         db.session.commit()
         return True 
      except Exception as e:
         print(e)
         return False

   def loginUser(self, user):
      try:
         userlogin = Users.query.filter(
            Users.ds_email_register == user['email'],
            Users.ds_pass_register == user['password']
         ).first()
         print(userlogin)
         if userlogin != None:
            return True, userlogin.ds_user_role
         else:
            return False, None
      except Exception as e:
         print(e)
         return False, None
   
   def userExist(self, data):
      user = Users.query.filter(
         Users.ds_email_register == data['email']
      ).first()
      if user != None:
         return True 
      else:
         return False 


   def getProfileDevicesInfo(self, params):

      query_devices = Users.query.filter(
         Users.ds_email_register == params['email']
      ).first()

      if query_devices is not None:
         return query_devices.ds_json_devices

      else:
         return False

   def setProfileDevicesConfig(self, data ):

      email = data['email']

      try:
         device = Users.query.filter(
            Users.ds_email_register == email
         ).first()

         if device is not None:
            device.ds_json_devices = data['devices']
            db.session.add(device)
            db.session.commit()
            return True
         else:
            return False

      except Exception as e:
         return False

   def getUserListByRole(self):
      userRoleList = Users.query.all()

      json_data = []

      for record in userRoleList:

         dictionary = dict()

         dictionary['name'] = record.ds_name_register
         dictionary['email'] = record.ds_email_register
         dictionary['telephone'] = record.tel_user_register
         dictionary['role'] = record.ds_user_role

         json_data.append(dictionary)

      return json_data