import xlsxwriter
from PIL import Image
import os
from datetime import datetime
import config as CONF
from flask import url_for

class XLXS_Generales():

   def __init__(
      self,
      nombre_reporte
   ):
      self.nombre_reporte = nombre_reporte
      path = os.path.join(
         "back/static/"
      )
      nombre = "{}.xlsx".format(nombre_reporte)
      ruta_archivo = "{}/{}".format(path, nombre)
      if not os.path.isdir(path):
         os.makedirs(path)
      self.workbook = xlsxwriter.Workbook(ruta_archivo)
      self.ruta = CONF.APP_URL_BASE+'/static/{}'.format(nombre)

   def imprimir(
      self,
      titulos, #diccionario de titulos que contiene el reporte (ej. Nombre de la empresa, dirección, periodo)
      encabezados, #encabezados de la tabla
      hojas, #json de hojas del excel con datos
      logo_path, #ruta de la imagen
      aplica_encabezado, #True si aplica titulos. False si no aplica titulos
      con_lineas = False, #True si el archivo debe verse sin lineas de las celdas (gridlines)
      fecha = False, #True si los titulos incluyen fecha
      no_fila_titulo = 6, #número de filas que contiene el array de titulos
      celdas_titulos = "" #diccionario que contiene la posición de los títulos (imagen, titulos, fecha)
   ):
      for hoja in hojas:
         workbook = self.workbook
         worksheet = workbook.add_worksheet(hoja["nombre_hoja"])
         worksheet.set_paper(1)
         if con_lineas:
            worksheet.hide_gridlines(2)

         formatos_numeros = [
            "moneda_encabezado",
            "moneda",
            "numero",
            "moneda_totales",
            "moneda_encabezado_derecha",
            "moneda_simple",
            "moneda_simple_peso_bottom",
            "moneda_totales_bottom",
            "moneda_encabezado_derecha_simple"
         ]

         #Estableciando medidas de las columnas
         worksheet.set_column("A:Z", 15)

         #Estableciando formatos para el libro
         formato_titulo_centrado = workbook.add_format(
            {
               "bold": 1,
               "font_size" : 10,
               "align": "center"
            }
         )

         formato_titulo_izquierda = workbook.add_format(
            {
               "bold": 1,
               "font_size" : 10,
               "align": "left"
            }
         )

         #se carga el logotipo y se escala
         if aplica_encabezado:
            if logo_path:
               logo = Image.open(logo_path)
               image_width, image_height = logo.size
               cell_width = 200.0
               cell_height = 80.0
               x_scale = cell_width / image_width
               y_scale = cell_height / image_height

               #encabezado del Archivo
               worksheet.insert_image(
                  celdas_titulos["imagen"][0] if celdas_titulos else 0,
                  celdas_titulos["imagen"][1] if celdas_titulos else 1,
                  logo_path,
                  {
                     "x_scale": x_scale,
                     "y_scale": y_scale
                  }
               )

            fila = 0
            for titulo in titulos:
               worksheet.merge_range(
                  fila,
                  celdas_titulos["titulos"][0] if celdas_titulos else int(len(encabezados[0]) / 2) - 1,
                  fila,
                  celdas_titulos["titulos"][1] if celdas_titulos else int(len(encabezados[0]) / 2) + 1,
                  titulo.decode("utf-8"),
                  formato_titulo_centrado
               )
               fila = fila + 1

            if not fecha:
               worksheet.write(
                  "I2",
                  self.nombre_reporte.decode("utf-8").upper(),
                  formato_titulo_centrado
               )
            else:
               worksheet.merge_range(
                  2,
                  celdas_titulos["fecha"][0] if celdas_titulos else len(encabezados[0]) - 2,
                  2,
                  celdas_titulos["fecha"][1] if celdas_titulos else len(encabezados[0]) - 1,
                  "Fecha: {}".format(datetime.today().strftime("%d/%m/%Y")),
                  formato_titulo_centrado
               )

            fila = no_fila_titulo
         else:
            fila = 0
         #Imprimiendo los diversos encabezados del XLSX
         for encabezado in encabezados:
            columna = 0
            for elemento in encabezado:
               formato = self.definir_formato(elemento["tipo"], workbook)
               if elemento["data"] != None:
                  valor = elemento["data"]
               else:
                  valor = ""
               if 'merge' not in elemento:
                  if elemento["tipo"] in formatos_numeros:
                     worksheet.write(
                        fila,
                        columna,
                        valor,
                        formato
                     )
                  else:
                     worksheet.write(
                        fila,
                        columna,
                        valor.upper(),
                        formato
                     )
               else:
                  if elemento["tipo"] in formatos_numeros:
                     worksheet.merge_range(
                        fila,
                        columna,
                        (fila + elemento["merge"][0]),
                        (columna + elemento["merge"][1]),
                        valor,
                        formato
                     )
                  else:
                     worksheet.merge_range(
                        fila,
                        columna,
                        (fila + elemento["merge"][0]),
                        (columna + elemento["merge"][1]),
                        valor.decode("utf-8").upper(),
                        formato
                     )
                  columna = columna + elemento["merge"][1]
               columna = columna + 1
            fila = fila + 1
         for dato in hoja["dato"]:
            columna = 0
            for elemento in dato:
               formato = self.definir_formato(elemento["tipo"], workbook)
               if elemento["data"] != None:
                  valor = elemento["data"]
               else:
                  valor = ""
               if 'merge' not in elemento:
                  if elemento["tipo"] in formatos_numeros:
                     worksheet.write(
                        fila,
                        columna,
                        valor,
                        formato
                     )
                  else:
                     worksheet.write(
                        fila,
                        columna,
                        valor.decode("utf-8"),
                        formato
                     )
               else:
                  if elemento["tipo"] in formatos_numeros:
                     worksheet.merge_range(
                        fila,
                        columna,
                        (fila + elemento["merge"][0]),
                        (columna + elemento["merge"][1]),
                        valor,
                        formato
                     )
                  else:
                     worksheet.merge_range(
                        fila,
                        columna,
                        (fila + elemento["merge"][0]),
                        (columna + elemento["merge"][1]),
                        valor.decode("utf-8").upper(),
                        formato
                     )
                  columna = columna + elemento["merge"][1]
               columna = columna + 1
            fila = fila + 1

         worksheet.set_margins(0.7, 0.7, 0.3, 1)
         worksheet.set_footer("&CPAG &P DE &N", {"margin": 0.7})
         worksheet.set_print_scale(65)
      self.exito = True
      self.workbook.close()
      return dict( exito = self.exito, ruta = self.ruta )

   def definir_formato(self, tipo, workbook):
      formato = ""
      if tipo == "moneda_encabezado":
         formato = workbook.add_format(
            {
               "bold": 1,
               "font_size" : 8,
               "align": "center",
               "border": 1,
               "bg_color": "#CACFD2",
               "num_format": "$#,##0.00"
            }
         )
      elif tipo == "encabezado":
         formato = workbook.add_format(
            {
               "bold": 1,
               "font_size" : 8,
               "align": "center",
               "border": 1,
               "bg_color": "#CACFD2"
            }
         )
      elif tipo == "texto":
         formato = workbook.add_format(
            {
               "font_size" : 8,
               "align": "left",
               "border": 1,
            }
         )
      elif tipo == "texto_centro":
         formato = workbook.add_format(
            {
               "font_size" : 8,
               "align": "center",
               "border": 1
            }
         )
      elif tipo == "moneda":
         formato = workbook.add_format(
            {
               "bold": 1,
               "font_size" : 8,
               "align": "right",
               "border": 1,
               "num_format": "$#,##0.00"
            }
         )
      elif tipo == "numero":
         formato = workbook.add_format(
            {
               "bold": 1,
               "font_size" : 8,
               "align": "right",
               "border": 1,
               "num_format": "#,##0.00"
            }
         )
      elif tipo == "moneda_totales":
         formato = workbook.add_format(
            {
               "bold": 1,
               "font_size" : 10,
               "align": "right",
               "border": 1,
               "num_format": "$#,##0.00"
            }
         )
      elif tipo == "encabezado_izquierda":
         formato = workbook.add_format(
            {
               "bold": 1,
               "font_size" : 8,
               "align": "left",
               "border": 1,
               "bg_color": "#CACFD2"
            }
         )
      elif tipo == "moneda_encabezado_derecha":
         formato = workbook.add_format(
            {
               "bold": 1,
               "font_size" : 8,
               "align": "right",
               "border": 1,
               "bg_color": "#CACFD2",
               "num_format": "$#,##0.00"
            }
         )
      elif tipo == "encabezado_derecha":
         formato = workbook.add_format(
            {
               "bold": 1,
               "font_size" : 8,
               "align": "right",
               "border": 1,
               "bg_color": "#CACFD2",
               "num_format": "$#,##0.00"
            }
         )
      elif tipo == "moneda_simple":
         formato = workbook.add_format(
            {
               "font_size" : 10,
               "align": "right",
               "num_format": "#,##0.00"
            }
         )
      elif tipo == "encabezado_simple":
         formato = workbook.add_format(
            {
               "bold": 1,
               "font_size" : 10,
               "align": "left"
            }
         )
      elif tipo == "texto_10":
            formato = workbook.add_format(
            {
               "font_size" : 10,
               "align": "left"
            }
         )
      elif tipo == "negritas":
         formato = workbook.add_format(
            {
               "bold": 1,
               "font_size": 8,
               "align": "left",
               "border": 1
            }
         )
      elif tipo == "negritas_centro":
         formato = workbook.add_format(
            {
               "bold": 1,
               "font_size": 8,
               "align": "center",
               "border": 1
            }
         )
      elif tipo == "moneda_simple_peso_bottom":
         formato = workbook.add_format(
            {
               "font_size": 10,
               "align":"right",
               "num_format": "$#,##0.00",
               "bottom": 1,
               "bottom_color": "#CACFD2"
            }
         )
      elif tipo == "texto_10_bottom":
         formato = workbook.add_format(
            {
               "font_size" : 10,
               "align": "left",
               "bottom":1,
               "bottom_color": "#CACFD2"
            }
         )
      elif tipo == "encabezado_simple_bottom":
         formato = workbook.add_format(
            {
               "bold": 1,
               "font_size" : 10,
               "align": "left",
               "bottom": 1,
               "bottom_color": "#CACFD2"
            }
         )
      elif tipo == "moneda_totales_bottom":
         formato = workbook.add_format(
            {
               "bold": 1,
               "font_size" : 10,
               "num_format": "$#,##0.00",
               "bottom": 1,
               "bottom_color": "#CACFD2",
               "align":"right"
            }
         )
      elif tipo == "moneda_encabezado_derecha_simple":
         formato = workbook.add_format(
            {
               "bold": 1,
               "font_size" : 10,
               "align": "right",
               "bg_color": "#CACFD2",
               "num_format": "$#,##0.00"
            }
         )
      elif tipo == "encabezado_izquierda_simple":
         formato = workbook.add_format(
            {
               "bold": 1,
               "font_size" : 10,
               "align": "left",
               "bg_color":"#CACFD2"
            }
         )
      elif tipo == "encabezado_simple_wrap":
         formato = workbook.add_format(
            {
               "bold": 1,
               "font_size" : 10,
               "align": "left",
               "text_wrap": "wrap"
            }
         )
      elif tipo == "texto_10_wrap":
         formato = workbook.add_format(
            {
               "font_size" : 10,
               "align": "left",
               "text_wrap": "wrap"

            }
         )
      else:
         formato = workbook.add_format(
            {
               "font_size" : 8,
               "align": "left"
            }
         )
      return formato