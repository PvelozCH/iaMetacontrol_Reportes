import traceback,sys
import sqlite3
import requests
import os
from dotenv import load_dotenv
load_dotenv() 


class uniController:
    def getTokenUnifier():
        token = ""
        data = ""
        try:

            url = os.getenv("tokenUrlUNIFIER")
            username = os.getenv("UserUNIFIER")
            password = os.getenv("PasswordUNIFIER")

            response = requests.get(url, auth=(username,password))

            if response.status_code == 200:
                data = response.json()
                token = data['token']
            else:
                print("ERROR",response.status_code,response.text)
        except Exception as e:
            print("Error completo : ",traceback.format_exc())
            print("Error con Token : ",e)
        return token
    # Carga reporte y solamente trae json completo sin formatear (clásico)
    def loadReportUnifier(token,nomReporte):
        data =""
        report_header =""
        report_row = ""
        try:

            url = os.getenv("udrUrlUNIFIER")

            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            payload = {
                "reportname":nomReporte
            }
            response = requests.post(url,json=payload,headers=headers)

            # Para enviar a 
            if response.status_code == 200:
                # Json que contiene la data completa
                data = response.json()
                # Json que contiene solo las cabeceras
                report_header = response.json()['data'][0]['report_header']
                # Json que contiene los datosdel reporte
                report_row = response.json()['data'][0]['report_row']
            else:
                print("ERROR",response.status_code,response.text)
        except Exception as e:
            print("Error completo : ",traceback.format_exc())
            print("Error reporte Unifier: ",e)
        return data

    # Carga de reporte normalizado, extraerá cabeceras y campos de manera ordenada lista para ingresar en tabla sqlite
    def loadReportUnifierV2(token,nomReporte):
        try:

            """
            - Consume el reporte de Unifier (JSON)
            - Normaliza el JSON usando los nombres reales del header
            - Crea una tabla SQLite con nombres correctos
            - Inserta las filas del reporte
            """
            nom_tabla = nomReporte.replace(" ","_").replace("-","_")
            normalized_rows = []
            data =""
            report_header =""
            report_row = ""
            url = os.getenv("udrUrlUNIFIER")

            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            payload = {
                "reportname":nomReporte
            }
            response = requests.post(url,json=payload,headers=headers)

            # Para enviar a 
            if response.status_code == 200:
                # Json que contiene la data completa
                data = response.json()

                # Json que contiene solo las cabeceras
                report_header = response.json()['data'][0]['report_header']
                column_map = {col : report_header[col]["name"] for col in report_header} # lista de los campos que vienen como headers

                # Json que contiene los datosdel reporte
                report_row = response.json()['data'][0]['report_row']

                # Cada row se agrega a lista "normalizada"
                for row in data["data"][0]["report_row"]:
                    new_row = {}
                    for col, value in row.items():
                        new_row[column_map[col]] = value
                    normalized_rows.append(new_row)
            else:
                print("===========")
                print("###ERROR :: ",response.status_code,response.text," ###")
                print("===========")
        except Exception as e:
            print("Error completo : ",traceback.format_exc())
            print("Error reporte Unifier : ",e)

        return column_map,normalized_rows,nom_tabla
    
    def creacionDbUnifier(column_map,normalized_rows,nom_tabla):
        try:
            # Conexión
            nomDB ="UnifierDB.db"
            conn = sqlite3.connect(nomDB)
            cur = conn.cursor()
            
            # Toma columnas para automatizar creación de tabla 
            columnas = list(normalized_rows[0].keys())
            ddl = ", ".join([f'"{col}" TEXT' for col in columnas])

            # FALTA CREAR TABLA O NO HACERLO EN CASO DE QUE YA EXISTA!!!!!!
            cur.execute(f"DROP TABLE IF EXISTS {nom_tabla}")
            cur.execute(f"CREATE TABLE {nom_tabla}({ddl})")

            registros = ", ".join(["?"] * len(columnas))

            for r in normalized_rows:
                cur.execute(f'INSERT INTO "{nom_tabla}" VALUES ({registros})',list(r.values()))
            
            print(f"Tabla '{nom_tabla}' creada con exito con {len(normalized_rows)} filas en BDD {nomDB}")

            #print(cur.execute(f"SELECT * FROM {nom_tabla}"))

            conn.commit()
            conn.close()


        
        except Exception as e:
            print("Error completo : ",traceback.format_exc())
            print("Error : ",e)
        
    def fetchBPrecordList(token):
        data =""
        bpname = os.getenv("nomBpnameUNIFIER")
        process = "ADM-0067"
        url = os.getenv("bpFetchUNIFIER",process)

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "bpname":bpname,
            "lineitem":"yes"
        }
        response = requests.post(url,json=payload,headers=headers)

        if response.status_code == 200:
            # Json que contiene la data completa
            data = response.json()
        else:
            print("ERROR",response.status_code,response.text)
        
        return data
    
    def getShell(token):
        data =""
        a = {
            "filter":{
                "shell_type":"Project"
            }
        }
        opc = "options:",a
        url = os.getenv("shellUNIFIER",opc)

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        response = requests.get(url,headers=headers)

        if response.status_code == 200:
            # Json que contiene la data completa
            data = response.json()
        else:
            print("ERROR",response.status_code,response.text)
        
        return data
    
