from models.models import *
import json
import requests
import uuid
import qrcode
from utils.auth_api import *
import json
from business.services.xlsx import XLXS_Generales
from datetime import datetime, timedelta
from business.services.commonsService import CommonsService
import config as CONF

commonsService = CommonsService()

class BinnacleService():
   db = db

   def getBinnacleRecords(
      self,
      fechas
   ):
      dtTodayInit = fechas['start']
      dtTodayEnd = fechas['end']
      binnacleQuery = """
         SELECT
                  B.id,
                  B.ds_guest_name AS guestName,
                  I.ds_event_name AS visitReason,
                  B.ds_host_name AS hostName,
                  B.ds_badge_number AS badgeNumber,
                  B.ds_guest_email AS email,
                  CAST(
                     DATE_FORMAT(
                        DATE(B.dt_reg_date),
                        '%d-%m-%Y'
                     ) AS char
                  ) as dateIn,
                  CAST(
                     DATE_FORMAT(
                        B.dt_reg_date,
                        '%H:%i'
                     ) AS char
                  ) as hourIn,
                  COALESCE(
                     CAST(
                        DATE_FORMAT(
                           DATE(BOUT.dt_reg_date),
                           '%d-%m-%Y'
                        ) AS char
                     ),
                     '---'
                  ) as dateOut,
                  COALESCE(   
                     CAST(
                        DATE_FORMAT(
                           BOUT.dt_reg_date,
                           '%H:%i'
                        ) AS char
                     ),
                     '---' 
                  ) as hourOut
         FROM
                  binnacle B
         INNER JOIN
                  invitation I
         ON
                  B.kn_event_id = I.id
         LEFT JOIN
                  binnacle BOUT
         ON
                  (
                     B.ds_guest_email = BOUT.ds_guest_email AND
                     B.kn_event_id = BOUT.kn_event_id AND
                     BOUT.kn_type = 3
                  )
         WHERE
                  B.kn_type = 1
         AND
                  DATE(B.dt_reg_date)
         BETWEEN
                  '{}'
         AND
                  '{}'
         ORDER BY
                  dateIn asc, hourIn asc
      """.format(dtTodayInit, dtTodayEnd)
      records = db.session.execute(binnacleQuery)
      d, a = {}, []
      for record in records:
         for column, value in record.items():
            d = {**d, **{column: value}}
         a.append(d)
      return a

   def getXLSXFromBinnacle(
      self,
      fechas
   ):
      fecha = (commonsService.getServerTime(CONF.APP['debug'])).strftime('%Y_%m_%d-%H_%M_%S')
      nombre_reporte = "reporte_bitacora("+fecha+")"
      datos = self.getBinnacleRecords(fechas)
      xlsx_binnacle = XLXS_Generales(
         nombre_reporte,
      )
      #encabezados del XLSX
      encabezados = []
      encabezado_row = [
         '# GAFETE', 
         'NOMBRE', 
         'MOTIVO',
         'A QUIEN VISITA',
         'FECHA ENTRADA',
         'HORA ENTRADA',
         'FECHA SALIDA',
         'HORA SALIDA'
      ]
      encabezado = []

      for elemento in encabezado_row:
         encabezado.append(
            {
               "data": elemento,
               "tipo": "encabezado"
            }
         )
      encabezados.append(encabezado)
      #datos del xlsx
      fila = 0
      json = []
      hojas = []
      datos_hojas = dict()
      datos_hojas["nombre_hoja"] = 'Bitácora'
      for valor in datos:
         dato = []
         dato.append(
            {
               "data": valor['badgeNumber'].encode("utf-8"),
               "tipo": "texto"
            }
         )
         dato.append(
            {
               "data": valor['guestName'].encode("utf-8"),
               "tipo": "texto"
            }
         )
         dato.append(
            {
               "data": valor['visitReason'].encode("utf-8"),
               "tipo": "texto"
            }
         )
         dato.append(
            {
               "data": valor['hostName'].encode("utf-8"),
               "tipo": "texto"
            }
         )
         dato.append(
            {
               "data": valor['dateIn'].encode("utf-8"),
               "tipo": "texto_centro"
            }
         )
         dato.append(
            {
               "data": valor['hourIn'].encode("utf-8"),
               "tipo": "texto_centro"
            }
         )
         dato.append(
            {
               "data": valor['dateOut'].encode("utf-8"),
               "tipo": "texto_centro"
            }
         )
         dato.append(
            {
               "data": valor['hourOut'].encode("utf-8"),
               "tipo": "texto_centro"
            }
         )
         json.append( dato )
      # carpeta del proyecto
      datos_hojas["dato"] = json
      hojas.append(datos_hojas)
      resultado = xlsx_binnacle.imprimir(
         "",
         encabezados,
         hojas,
         "",
         False
      )
      if resultado["exito"]:
         ruta = resultado["ruta"]
      else:
         ruta = ""

      return ruta