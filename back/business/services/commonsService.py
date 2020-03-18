from datetime import datetime, timedelta
import json
import config as CONF

class CommonsService():

   def getServerTime(
      self,
      debug
   ):
      if debug == True:
         serverTime = datetime.now()
      else:
         serverTime = datetime.now() - timedelta(hours = 6)
      return serverTime
