# from flask import Flask, render_template, redirect, request, session, jsonify
import os
import psycopg2

import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload

HOST = os.getenv("DB_HOST")
NAME = os.getenv("DB_NAME")
PASSWORD = os.getenv("DB_PASSWORD")

dsn = "host={} dbname={} user={} password={}".format(HOST, NAME, NAME,
                                                     PASSWORD)


def dabut_cel_sarakstu():
  return "OK"


def get_db_connection():
  conn = psycopg2.connect(dsn)
  return conn


def komentari(lietotajs, zinojums):
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute(
    """
      INSERT INTO komentari (lietotajs, zinojums)
      VALUES ({}, {})""", (lietotajs, zinojums))
  conn.commit()
  cur.close()
  conn.close()
  return


def ieraksta(lietotajvards, vards, uzvards, epasts, parole):
  conn = get_db_connection()
  cur = conn.cursor()

  cur.execute(
    """
      INSERT INTO lietotaji (lietotajvards, vards, uzvards, epasts, parole)
      VALUES (%s, %s, %s, %s, crypt(%s, gen_salt('bf')))""",
    (lietotajvards, vards, uzvards, epasts, parole))
  conn.commit()
  cur.close()
  conn.close()
  print("Aizsutits")
  return


def dabut_no_DB():
  return ["kautkas", "cits"]


# Login stuff


def pieslegties(epastsLogin, paroleLogin):
  conn = get_db_connection()
  cur = conn.cursor()

  DabuEpastu = """
      SELECT epasts
      FROM lietotaji
      WHERE epasts = %(s)s"""

  cur.execute(DabuEpastu, {'s': epastsLogin})
  conn.commit()

  VaiIrEpasts = cur.fetchone()
  print(VaiIrEpasts)

  if VaiIrEpasts == None:
    cur.close()
    conn.close()
    return False

  else:
    DabuParoli = """
    SELECT parole
    FROM lietotaji
    WHERE parole = crypt(%s, parole)
    AND epasts = %s;"""

    cur.execute(DabuParoli, (paroleLogin, epastsLogin))
    conn.commit()

    VaiIrParole = cur.fetchone()
    print(VaiIrParole)

    if VaiIrParole == None:
      cur.close()
      conn.close()
      return False

    else:
      cur.close()
      conn.close()
      print("ir ok")
      return True

  return False


def get_one(sql):
  conn = psycopg2.connect(dsn)
  c = conn.cursor()
  c.execute(sql)
  atbilde = c.fetchone()
  c.close()
  conn.commit()
  conn.close()
  return atbilde


def iegut_datus(epasts):
  rezultati = []
  conn = psycopg2.connect(dsn)
  cur = conn.cursor()
  cur.execute(
    """
  SELECT lietotajvards, vards, uzvards, lietotaja_id FROM lietotaji WHERE epasts = %s
  """, (epasts, ))
  conn.commit()
  rezultati = cur.fetchone()
  cur.close()
  conn.close()
  return rezultati


def dabut_kordinates(id):
  conn = psycopg2.connect(dsn)
  cur = conn.cursor()
  cur.execute("""
  SELECT marsruts FROM celojums WHERE celojuma_id = %s
  """, (id, ))
  conn.commit()
  rezultati = cur.fetchone()
  cur.close()
  conn.close()
  return rezultati


def dabut_info(id):
  conn = psycopg2.connect(dsn)
  cur = conn.cursor()
  cur.execute(
    """
   SELECT celojums.celojuma_id, celojums.lietotaja_id, celojums.nosaukums, celojums.apraksts as c_apraksts, celojums.celojuma_datums, celojums.marsruts, celojums.laiku_skaits, celojums.celojuma_info, celojums.celojuma_bilde, celojums.tiessaiste, dienas.dienas_id, dienas.apraksts as d_apraksts, dienas.naktsmitnes, pieturvietas.nosaukums as p_nosaukums, pieturvietas.apraksts, pieturvietas.transports_uz_pieturvietu FROM (celojums FULL JOIN dienas ON celojums.celojuma_id = dienas.celojuma_id) FULL JOIN pieturvietas ON dienas_id = diena_id WHERE celojums.celojuma_id = %s
  """, (id, ))
  conn.commit()
  atbilde = cur.fetchall()
  cur.execute("""
  SELECT COUNT (DISTINCT dienas_id) FROM dienas WHERE celojuma_id = %s 
  """, (id, ))
  conn.commit()
  dienusk = cur.fetchone()
  cur.close()
  conn.close()
  return atbilde, dienusk


def insert_into_celojums(lietotaja_id, nosaukums, apraksts, tiessaiste,
                         celojuma_datums, marsruts):
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute(
    "INSERT INTO celojums (lietotaja_id, nosaukums, apraksts, tiessaiste, izveides_datums, celojuma_datums, marsruts, laiku_skaits) VALUES (%s, %s, %s, %s, CURRENT_DATE, %s, %s, 0)",
    (lietotaja_id, nosaukums, apraksts, tiessaiste, celojuma_datums, marsruts))
  conn.commit()
  cur.close()
  conn.close()


# parsed_json[marsruts]))


def get_celojuma_id():
  conn = conn = get_db_connection()
  cur = conn.cursor()
  cur.execute(
    "SELECT celojuma_id FROM celojums ORDER BY celojuma_id DESC LIMIT 1")
  celojuma_id = cur.fetchone()[0]
  cur.close()
  conn.close()
  return celojuma_id


def insert_into_dienas(celojuma_id, apraksts, naktsmitnes, diena,
                       transports_uz_naktsmitni):
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute(
    "INSERT INTO dienas (celojuma_id, apraksts, naktsmitnes, diena, transports_uz_naktsmitni) VALUES (%s, %s, %s, %s, %s)",
    (celojuma_id, apraksts, naktsmitnes, diena, transports_uz_naktsmitni))
  conn.commit()
  cur.close()
  conn.close()
  return


def get_dienas_id():
  conn = conn = get_db_connection()
  cur = conn.cursor()
  cur.execute("SELECT dienas_id FROM dienas ORDER BY dienas_id DESC LIMIT 1")
  dienas_id = cur.fetchone()[0]
  cur.close()
  conn.close()
  return dienas_id


def insert_into_pieturvietas(diena_id, pieturvieta, apraksts):
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute(
    "INSERT INTO pieturvietas (diena_id, pieturvieta, apraksts) VALUES (%s, %s, %s)",
    (diena_id, pieturvieta, apraksts))
  conn.commit()
  cur.close()
  conn.close()
  return


def insert_into_celojums_stasts(lietotaja_id, nosaukums, apraksts,
                                celojuma_datums, marsruts):
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute(
    "INSERT INTO celojums (lietotaja_id, nosaukums, apraksts, izveides_datums, celojuma_datums, marsruts) VALUES (%s, %s, %s, CURRENT_DATE, %s, %s)",
    (lietotaja_id, nosaukums, apraksts, celojuma_datums, marsruts))
  conn.commit()
  cur.close()
  conn.close()
  return


def panemt_popularakos_celojumus():
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute(
    "SELECT celojuma_id, apraksts, nosaukums, celojuma_bilde, laiku_skaits, lietotajvards FROM celojums JOIN lietotaji ON celojums.lietotaja_id = lietotaji.lietotaja_id ORDER BY laiku_skaits DESC"
  )
  rows = cur.fetchall()
  cur.close()
  conn.close()
  sidebar = []
  for dats in rows:
    viens = {
      'nosaukums': dats[2],
      'id': dats[0],
      'bilde': dats[3],
      'lietotajvards': dats[5],
      'apraksts': dats[1]
    }
    sidebar.append(viens)
  return sidebar


def dabut_celojumus(lietotajs):
  lietotaja_celojumi = []
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute(
    "SELECT lietotaja_id, nosaukums, izveides_datums, tiessaiste, celojuma_id FROM celojums WHERE lietotaja_id = %s",
    (lietotajs, ))
  celojumi = cur.fetchall()
  cur.close()
  conn.close()
  i = 1
  for celojums in celojumi:
    viens = {}
    viens['index'] = i
    viens["id"] = celojums[4]
    viens["datums"] = celojums[2]
    viens["nosaukums"] = celojums[1]
    viens["tiessaiste"] = celojums[3]
    i += 1
    lietotaja_celojumi.append(viens)
  return lietotaja_celojumi


def dabut_celojumus_stastiem():
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute("""SELECT 
celojums.celojuma_id, lietotaja_id, nosaukums, tiessaiste, izveides_datums, celojuma_datums, marsruts, laiku_skaits, celojuma_info, celojuma_bilde, publicetaja_vards, komentu_skaits 

FROM 
celojums LEFT JOIN 
(SELECT komentari.celojuma_id, COUNT(*) as komentu_skaits FROM komentari GROUP BY komentari.celojuma_id) tabula 

ON 
celojums.celojuma_id = tabula.celojuma_id""")
  celojumi_stastiem = cur.fetchall()
  cur.close()
  conn.close()
  return celojumi_stastiem


def dabut_komentarus(celojums):
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute(
    "SELECT lietotajvards, komentars, izveides_laiks FROM komentari JOIN lietotaji ON lietotaji.lietotaja_id = komentari.lietotaja_id WHERE celojuma_id = %s ORDER BY izveides_laiks DESC",
    (celojums, ))
  komentari = cur.fetchall()
  cur.close()
  conn.close()
  return komentari


# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# def upload_image_to_drive(image_filename, folder_id):
#     gauth = GoogleAuth()
#     gauth.LocalWebserverAuth()
#     drive = GoogleDrive(gauth)
#     file1 = drive.CreateFile({'title': image_filename, 'parents': [{'id': folder_id}]})
#     file1.SetContentFile(image_filename)
#     file1.Upload()
# image_filename = "your_image.jpg"
# folder_id = "your_folder_id"
# upload_image_to_drive(image_filename, folder_id)


def download_file_to_drive(real_file_id):
  creds, _ = google.auth.default()
  try:
    service = build("drive", "v3", credentials=creds)
    file_id = real_file_id
    request = service.files().get_media(fileId=file_id)
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    done = False
    while done is False:
      status, done = downloader.next_chunk()

  except HttpError as error:
    print(f"An error occurred: {error}")
    file = None

    return file.getvalue()


def upload_image_to_drive(image_filename):
  creds, _ = google.auth.default()
  try:
    service = build("drive", "v3", credentials=creds)
    file_metadata = {"name": image_filename}
    media = MediaFileUpload(image_filename, mimetype="image/jpeg")
    file = (service.files().create(body=file_metadata,
                                   media_body=media,
                                   fields="id"))
    print(f'File ID: {file.get("id")}')

  except HttpError as error:
    print(f"An error occurred: {error}")
    file = None

  return file.get("id")


def mainitDatus(lietotajvards, vards, uzvards, epasts, lietotaja_id):
  conn = psycopg2.connect(dsn)
  cur = conn.cursor()
  cur.execute("""
  UPDATE lietotaji
SET vards = ' {}' ,
  uzvards = '{}',
  epasts = '{}',
  lietotajvards = '{}'
WHERE lietotaja_id = '{}'
  """.format(vards, uzvards, epasts, lietotajvards, lietotaja_id))
  conn.commit()
  cur.close()
  conn.close()
  return
