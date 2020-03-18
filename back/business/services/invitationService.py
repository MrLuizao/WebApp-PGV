from models.models import *
import json

class InvitationService():
	db = db

	def getAllInvitaciones(self):
		invitaciones = Invitacion.query.all()
		json_data = []
		for inv in invitaciones:
			invitacion = dict()
			invitacion['id'] = inv.id
			invitacion['dt_invitation_date'] = inv.dt_invitation_date.strftime('%m/%d/%Y')
			invitacion['dt_event_date'] = inv.dt_event_date.strftime('%m/%d/%Y')
			invitacion['ds_host_email'] = inv.ds_host_email
			invitacion['ds_place'] = inv.ds_place
			json_data.append(invitacion)
		return json_data

	def newEvents(self, events):
		if len(events) > 0:
			s = db.session()
			res = s.execute(
				Invitacion.__table__.insert(),
				events
			)
			db.session.commit()
			s.close()
		
		return True

	def getEventsByDate(self, date):
		invitaciones = Invitacion.query.filter(Invitacion.dt_invitation_date == date).all()
		print (invitaciones)
		return True
