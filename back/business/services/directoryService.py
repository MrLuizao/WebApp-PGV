from models.models import *
from datetime import datetime
import json
import requests
import uuid
import config as CONF

class DirectoryService():
   db = db

   def getDirectoryList(self):
      directoryList = Directory.query.all()
      json_data = []
      for record in directoryList:
         directory = dict()
         directory['id'] = record.id
         directory['name'] = record.ds_name
         directory['email'] = record.ds_email
         directory['phone'] = record.ds_phone
         directory['department'] = record.ds_department
         directory['position'] = record.ds_position
         json_data.append(directory)
      return json_data

   def addToDirectory(
      self,
      data
   ):
      newReg = Directory(
         ds_name = data['name'],
         ds_email = data['email'],
         ds_phone = data['phone'],
         ds_department = data['department'],
         ds_position = data['position']
      )
      try:
         db.session.add(newReg)
         db.session.commit()
         return newReg.id
      except Exception as e:
         return False

   def getDirectoryByID(
      self,
      id
   ):
      try:
         record = Directory.query.get(id)
         directory = dict()
         directory['id'] = record.id
         directory['name'] = record.ds_name
         directory['email'] = record.ds_email
         directory['phone'] = record.ds_phone
         directory['department'] = record.ds_department
         directory['position'] = record.ds_position
         return directory
      except Exception as e:
         return False

   def updateDirectoryByID(
      self,
      data
   ):
      try:
         record = Directory.query.get(data['id'])
         record.ds_name = data['name']
         record.ds_email = data['email']
         record.ds_phone = data['phone']
         record.ds_department = data['department']
         record.ds_position = data['position']
         db.session.add(record)
         db.session.commit()
         db.session.close()
         return True
      except Exception as e:
         return False

   def deleteDirectoryByID(
      self,
      id
   ):
      try:
         record = Directory.query.get(id)
         db.session.delete(record)
         db.session.commit()
         db.session.close()
         return True
      except Exception as e:
         return False

   def userDirectoryExist(self, data):
      user = Directory.query.filter(
         Directory.ds_email == data['email']
      ).first()
      if user != None:
         return True 
      else:
         return False