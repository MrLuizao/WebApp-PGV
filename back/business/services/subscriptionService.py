from models.models import *
from datetime import datetime, timedelta
import json
import requests
import uuid
import config as CONF

class SubscriptionService():
   db = db

   def saveSubscriptionToDB(
      self,
      subscription,
      token,
      refresh_token
   ):
      subscription = Subscription(
         ds_subscription = subscription,
         ds_graph_token = token,
         ds_graph_refresh_token = refresh_token,
         ds_graph_nextlink = None
      )
      try:
         db.session.add(subscription)
         db.session.commit()
         return subscription
      except Exception as e:
         return False

   def updateSubscriptionToDB(
      self,
      subscription,
      ds_graph_nextlink
   ):
      subscription.ds_graph_nextlink = ds_graph_nextlink
      try:
         db.session.add(subscription)
         db.session.commit()
         return True
      except Exception as e:
         return False

   def getSubscriptionFromSubscriptionID(
      self,
      subscriptionID
   ):
      subscription = Subscription.query.filter(
         Subscription.ds_subscription == subscriptionID
      ).first()
      if subscription == None:
         return False
      else:
         return subscription

   def updateSubscriptionToken(
      self,
      subscription,
      token,
      refresh_token
   ):
      subscription.ds_graph_token = token
      subscription.ds_graph_refresh_token = refresh_token
      try:
         db.session.add(subscription)
         db.session.commit()
         return True
      except Exception as e:
         db.session.rollback()
         return False