from models.models import *
from datetime import datetime, timedelta
import json
import requests
import uuid
import config as CONF
from flask import url_for
from utils.auth_api import *
import json

class EmployeeService():
  
  db : db

  def getEmployeesList(
      self,
      nameString
  ):
    json_data = []
    if nameString is not None:
        search = "%{}%".format(nameString)
        employeeList =  db.session.query(Employees).filter(
            Employees.ds_employee_fullname.like(search)
        )
        for record in employeeList:
            employee = dict()
            employee['name'] = record.ds_employee_fullname
            employee['email'] = record.ds_employee_email
            json_data.append(employee)
       # return json_data
    else:
        employeeList = Employees.query.all()
        for record in employeeList:
            employee = dict()
            employee['name'] = record.ds_employee_fullname
            employee['email'] = record.ds_employee_email
            json_data.append(employee)
    return json_data
        