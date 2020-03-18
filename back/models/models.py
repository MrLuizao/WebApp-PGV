from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class BaseModel(db.Model):
   """Base data model for all objects"""
   __abstract__ = True

class Invitacion(BaseModel, db.Model):
   """Model for invitacion table"""
   __tablename__ = 'invitation'

   id = db.Column(
      db.Integer,
      primary_key = True,
      autoincrement = True
   )
   #id graph event
   ds_event_id = db.Column(
      db.String(2000),
      unique = True
   )
   #id nombre evento
   ds_event_name = db.Column(
      db.String(2000)
   )
   #lugar del evento
   ds_event_place = db.Column(
      db.String(2000)
   )
   #dia del evento
   dt_event_date = db.Column(
      db.DateTime
   )
   #dia que fue creado el evento
   dt_event_created = db.Column(
      db.DateTime
   )
   #correo del anfitrion
   ds_host_email = db.Column(
      db.String(255)
   )
   ds_invitation_config = db.Column(
      db.JSON
   )
   kn_attended = db.Column(
      db.Integer,
      default = 0
   )
   ds_graph_id = db.Column(
      db.String(2000)
   )
   kn_cancelled = db.Column(
      db.Integer, #0 default NO CANCELADO, 1 CANCELADO
      default = 0
   )
   ds_host_name = db.Column(
      db.String(255)
   )
   dt_event_date_end = db.Column(
      db.DateTime
   )
   ds_event_place_coord = db.Column(
      db.JSON
   )

class Invitados(BaseModel, db.Model):
   __tablename__ = 'invitation_details'
   id = db.Column(
      db.Integer,
      primary_key = True,
      autoincrement = True
   )
   kn_event_id = db.Column(
      db.Integer,
      db.ForeignKey("invitation.id")
   )
   ds_email_invitado = db.Column(
      db.String(255)
   )
   ds_name_invitado = db.Column(
      db.String(255)
   )
   ds_event_response  = db.Column(
      db.String(255)
   )
   kn_email_sent = db.Column(
      db.Integer,
      default = 0
   )
   kn_checkin = db.Column(
      db.Integer,
      default = 0
   )
   dt_checkin = db.Column(
      db.DateTime
   )
   dt_checkout = db.Column(
      db.DateTime
   )
   ds_json_devices = db.Column(
      db.JSON
   )
   __table_args__ = (db.UniqueConstraint('kn_event_id', 'ds_email_invitado', name='_invitados_uc'),)

class Users(BaseModel, db.Model):
   __tablename__ = 'users'

   id = db.Column(
      db.Integer,
      primary_key = True,
      autoincrement = True
   )
   ds_name_register = db.Column(
      db.String(255)
   )
   ds_email_register= db.Column(
      db.String(255)
   )
   ds_pass_register = db.Column(
      db.String(255)
   )
   tel_user_register = db.Column(
      db.String(255)
   )
   ds_json_devices = db.Column(
      db.JSON
   )
   ds_user_role = db.Column(
      db.String(255)
   )

class Subscription(BaseModel, db.Model):
   __tablename__ = "subscription"

   id = db.Column(
      db.Integer,
      primary_key = True,
      autoincrement = True
   )
   ds_subscription = db.Column(
      db.String(255)
   )
   ds_graph_token = db.Column(
      db.String(3000)
   )
   ds_graph_nextlink = db.Column(
      db.String(2000)
   )
   ds_graph_refresh_token = db.Column(
      db.String(3000)
   )

class Binnacle(BaseModel, db.Model):
   __tablename__ = "binnacle"

   id = db.Column(
      db.Integer,
      primary_key = True,
      autoincrement = True
   )
   dt_reg_date = db.Column(
      db.DateTime
   )
   kn_event_id = db.Column(
      db.Integer,
      db.ForeignKey("invitation.id")
   )
   kn_type = db.Column(
      db.Integer
   )
   ds_guest_name = db.Column(
      db.String(500)
   )
   ds_guest_email = db.Column(
      db.String(500)
   )
   ds_host_name = db.Column(
      db.String(500)
   )
   ds_host_email = db.Column(
      db.String(500)
   )
   kn_status = db.Column(
      db.Integer
   )
   ds_json_devices = db.Column(
      db.JSON
   )
   base64_image = db.Column(
      db.LargeBinary(length = (2**32)-1)
   )
   ds_badge_number = db.Column(
      db.String(500)
   )
   base64_signature = db.Column(
      db.LargeBinary(length = (2**32)-1)
   )

class Directory(BaseModel, db.Model):
   __tablename__ = "directory"

   id = db.Column(
      db.Integer,
      primary_key = True,
      autoincrement = True
   )
   ds_name = db.Column(
      db.String(500)
   )
   ds_email = db.Column(
      db.String(200)
   )
   ds_phone = db.Column(
      db.String(255)
   )
   ds_department = db.Column(
      db.String(100)
   )
   ds_position = db.Column(
      db.String(100)
   )

class Employees(BaseModel, db.Model):
   __tablename__ = "internal_employees"

   id = db.Column(
      db.Integer,
      primary_key = True,
      autoincrement = True
   )
   kn_employee_id = db.Column(
      db.Integer
   )
   ds_employee_name = db.Column(
      db.String(100)
   )
   ds_employee_name2 = db.Column(
      db.String(100)
   )
   ds_employee_lastname = db.Column(
      db.String(100)
   )
   ds_employee_lastname2 = db.Column(
      db.String(100)
   )
   ds_employee_email = db.Column(
      db.String(100)
   )
   ds_employee_office = db.Column(
      db.String(100)
   )
   ds_employee_country = db.Column(
      db.String(100)
   )
   ds_employee_fullname = db.Column(
      db.String(200)
   )
