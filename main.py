from datetime import datetime
from flask import Flask, render_template, request, session, redirect, jsonify, json
import os
from data import dabut_no_DB, ieraksta, pieslegties, dabut_info, iegut_datus, insert_into_celojums, get_celojuma_id, insert_into_dienas, get_dienas_id, insert_into_pieturvietas, insert_into_celojums_stasts, dabut_cel_sarakstu, dabut_celojumus, panemt_popularakos_celojumus, dabut_celojumus_stastiem, dabut_komentarus, dabut_kordinates, upload_image_to_drive, mainitDatus

app = Flask('app')
app.secret_key = os.environ['ATSLEGA']


@app.route('/')
def Index_page():
  if 'login' not in session:
    session['login'] = False
  return render_template('GalvenaLapa.html',
                         login=session['login'],
                         popcelojumi=panemt_popularakos_celojumus())


@app.route('/RIHARDS', methods=('GET', 'POST'))
def RIHARDS():
  if request.method == 'POST':
    print("nospiesta Poga")
    epastsLogin = request.form['email']
    paroleLogin = request.form['password']
    if pieslegties(epastsLogin, paroleLogin):
      session['user'] = request.form['email']
      session['login'] = True
      dati = iegut_datus(epastsLogin)
      print(dati)
      session['lietotajs'] = {
        'lietotajvards': dati[0],
        'vards': dati[1],
        'uzvards': dati[2],
        'lietotaja_id': dati[3]
      }
      return redirect('/')

  return render_template('RIHARDS.html',
                         popcelojumi=panemt_popularakos_celojumus())


# sign up


@app.route("/logout")
def logout():
  session.pop('user')
  session['login'] = False

  return redirect('/')


@app.route('/marsruti', methods=('GET', 'POST'))
def marsruti():
  visi = [{
    'nosaukums':
    'Kuldīga',
    'apraksts':
    'Nevajag braukt',
    'id':
    0,
    'likes':
    10,
    'commentCount':
    5,
    'img':
    'https://whc.unesco.org/uploads/thumbs/site_1658_0005-750-750-20220427120355.jpg'
  }]
  # = dabut_cel_sarakstu()
  dati = {}
  dati["id"] = visi[0]
  return render_template('marsruti.html',
                         login=session['login'],
                         marsruti=visi,
                         popcelojumi=panemt_popularakos_celojumus())


@app.route('/stasti')
def stasti():
  visi = []
  dati = dabut_celojumus_stastiem()
  for d in dati:

    viens = {
      'nosaukums': d[2],
      'celojuma_info': d[8],
      'id': d[0],
      'likes': d[7],
      'tiessaiste': d[9],
      'izveides-datums': d[4],
      'celojuma-datums': d[5],
      'commentCount': d[11]
    }
    if viens['tiessaiste'] == None:
      viens['tiessaiste'] = 'https://static.lsm.lv/media/2020/11/large/1/e6dq.jpg'
    visi_komenti = []
    komentari = dabut_komentarus(d[0])
    for komentars in komentari:
      viens_koments = {'lietotajvards': komentars[0], 'comment': komentars[1]}
      visi_komenti.append(viens_koments)
    viens['comments'] = visi_komenti
    visi.append(viens)

  return render_template('stasti.html',
                         login=session['login'],
                         celojumi=visi,
                         popcelojumi=panemt_popularakos_celojumus())


@app.route('/students')
def students():
  return render_template('Studentu.html', login=session['login'])


@app.route('/celsaraksts')
def ceļsaraksts():
  visi = [""]
  # = dabut_cel_sarakstu()
  dati = {}
  dati["id"] = visi[0]
  return render_template('CeļSaraksts.html',
                         login=session['login'],
                         visi_dati=dati,
                         popcelojumi=panemt_popularakos_celojumus())


@app.route('/eksperts', methods=('GET', 'POST'))
def eksperts():
  return render_template('CeļSaraksts.html',
                         login=session['login'],
                         popcelojumi=panemt_popularakos_celojumus())


@app.route('/flag')
def flag():
  return render_template('flag.html',
                         login=session['login'],
                         popcelojumi=panemt_popularakos_celojumus())


@app.route('/country')
def country():
  return render_template('country.html',
                         login=session['login'],
                         popcelojumi=panemt_popularakos_celojumus())


@app.route('/forums')
def forums():
  return render_template('Forums.html',
                         login=session['login'],
                         popcelojumi=panemt_popularakos_celojumus())


@app.route('/jaunumi')
def jaunumi():
  return render_template('Jaunumi.html',
                         login=session['login'],
                         popcelojumi=panemt_popularakos_celojumus())


@app.route('/padomi')
def padomi():
  return render_template('Padomi.html',
                         login=session['login'],
                         popcelojumi=panemt_popularakos_celojumus())


@app.route('/profils')
def profils():
  return render_template('profils.html',
                         login=session['login'],
                         popcelojumi=panemt_popularakos_celojumus())


@app.route('/register', methods=('GET', 'POST'))
def registre():
  if request.method == 'POST':
    print("nospiesta Poga")
    lietotajvards = request.form['RegUsername']
    vards = request.form['RegName']
    uzvards = request.form['RegSurname']
    epasts = request.form['RegMail']
    parole = request.form['RegPassword']
    print(lietotajvards, vards, uzvards, epasts, parole)
    ieraksta(lietotajvards, vards, uzvards, epasts, parole)
    # if "admins" not in request.form:
    #   admins = False
    # else:
    #   admins = True

  return render_template('register.html',
                         login=session['login'],
                         popcelojumi=panemt_popularakos_celojumus())


@app.route('/index')
def index():
  return render_template('index.html',
                         login=session['login'],
                         popcelojumi=panemt_popularakos_celojumus())


@app.route('/mikus')
def mikus():
  visi = []
  info = dabut_no_DB()
  for viens in info:
    celojumainfo = {}
    celojumainfo["nosaukums"] = "Bauska"
    visi.append(celojumainfo)
    print(visi)
  return render_template('GalvenaLapa.html',
                         celojumi=visi,
                         login=session['login'],
                         popcelojumi=panemt_popularakos_celojumus())


@app.route('/Leonards')
def leonards():
  return render_template('celojumi.html',
                         login=session['login'],
                         popcelojumi=panemt_popularakos_celojumus())


@app.route('/tests')
def tests():
  return render_template('tests.html',
                         login=session['login'],
                         popcelojumi=panemt_popularakos_celojumus())


@app.route('/postans', methods=('GET', 'POST'))
def postans():
  # return render_template('postans.html',  login=session['login'])
  return redirect("/postans/1")


@app.route('/postans/<celid>')
def celojums(celid):
  viens = {}
  information, dienusk = dabut_info(celid)
  print(information)
  viens["id"] = information[0][0]
  viens["apraksts"] = information[0][3]
  viens["apraksts2"] = information[0][9]
  viens["atzina"] = [information[0][4].strftime("%d/%m/%Y")]
  if information[0][7] != None:
    viens["atzina"].append(", " + str(information[0][7]))
  else:
    viens["atzina"].append("")
  viens["laiks"] = information[0][6]
  viens["nosaukums"] = information[0][2]
  viens["dienu_skaits"] = dienusk[0]
  i = 1
  d_id = information[0][10]
  viens[str(i) + "diena_apraksts"] = information[0][11]
  viens[str(i) + "nakts_mitne"] = information[0][12]
  pieturas = []
  for rinda in information:
    nosaukums = rinda[13]
    apraksts = rinda[14]
    transports = rinda[15]
    if nosaukums == None:
      nosaukums = "Nav nosaukuma"
    if apraksts == None:
      apraksts = "Nav apraksta"
    if transports == None:
      transports = "Nav transporta"
    if d_id == rinda[10]:
      pieturas.append([nosaukums, apraksts, transports])
      continue
    viens[str(i) + "pieturvieta"] = pieturas
    pieturas = [[nosaukums, apraksts, transports]]
    i += 1
    d_id = rinda[10]
    viens[str(i) + "diena_apraksts"] = rinda[11]
    viens[str(i) + "nakts_mitne"] = rinda[12]
  viens[str(i) + "pieturvieta"] = pieturas

  coords_list = dabut_kordinates(celid)
  array_coords = [coord for coord in coords_list[0]]
  cordinates = array_coords
  return render_template('postans.html',
                         login=session['login'],
                         celojums=viens,
                         cor=cordinates,
                         popcelojumi=panemt_popularakos_celojumus())


@app.route('/piev')
def pub():
  return render_template('veidot.html',
                         login=session['login'],
                         popcelojumi=panemt_popularakos_celojumus())


@app.route('/publish')
def publish():
  return render_template('Publish.html',
                         login=session['login'],
                         popcelojumi=panemt_popularakos_celojumus())


@app.route('/publish/send', methods=['POST', 'GET'])
def postToServer():
  if request.method == "GET":
    trip_name = request.args.get("celojumaNosaukums")
    trip_description = request.args.get("celojumaApraksts")
    # trip_additional = request.args.get('celojumaInfo') # pagaidam nav ieksa datubaze
    trip_youtube = request.args.get('celojumaYoutube')
    trip_image = request.args.get('celojumaFiles')
    # upload_image_to_drive(trip_image)
    trip_days_description = request.args.getlist('celojumaDienasApraksts')
    trip_days_accommodation = request.args.getlist('celojumaDienasNaktsmitnes')
    tripTransportToAccommodation = request.args.getlist(
      'celojumaTransportsUzNaktsmitni')
    trip_date = request.args.get('tripStartDate')
    trip_route = request.args.get('tripRoute')
    print(trip_route)
  insert_into_celojums(session['lietotajs']['lietotaja_id'], trip_name,
                       trip_description, trip_youtube, trip_date, trip_route)
  celojumaId = get_celojuma_id()
  for day in range(len(trip_days_description)):
    insert_into_dienas(celojumaId, trip_days_description[day],
                       trip_days_accommodation[day], day + 1,
                       tripTransportToAccommodation[day])
    dienas_id = get_dienas_id()
    trip_days_plan = request.args.getlist('celojumaDienasPlans' + str(day + 1))
    for pieturvieta in range(len(trip_days_plan)):
      insert_into_pieturvietas(dienas_id, pieturvieta + 1,
                               trip_days_plan[pieturvieta])

  return render_template('GalvenaLapa.html',
                         login=session['login'],
                         popcelojumi=panemt_popularakos_celojumus())


@app.route('/publish2')
def publish2():
  return render_template('Publish2.html',
                         login=session['login'],
                         popcelojumi=panemt_popularakos_celojumus())


@app.route('/publish2/send', methods=['POST', 'GET'])
def postToServer2():
  if request.method == "GET":
    trip_name = request.args.get("celojumaNosaukums")
    trip_description = request.args.get("celojumaApraksts")
    trip_date = request.args.get('tripStartDate')
    trip_route = request.args.get('tripRoute')
  insert_into_celojums_stasts(session['lietotajs']['lietotaja_id'], trip_name,
                              trip_description, trip_date, trip_route)

  return render_template('GalvenaLapa.html',
                         login=session['login'],
                         popcelojumi=panemt_popularakos_celojumus())


@app.route('/mansprofils', methods=['GET', 'POST'])
def mansprofils():

  if request.method == 'POST':
    lietotajvards = request.form['lietotajvards']
    vards = request.form['vards']
    uzvards = request.form['uzvards']
    epasts = request.form['epasts']
    mainitDatus(lietotajvards, vards, uzvards, epasts,
                session['lietotajs']['lietotaja_id'])
    session['lietotajs']["lietotajvards"] = lietotajvards
    session['lietotajs']["vards"] = vards
    session['lietotajs']["uzvards"] = uzvards
    session['user'] = epasts

  pats = {
    'lietotajvards': session['lietotajs']['lietotajvards'],
    'vards': session['lietotajs']['vards'],
    'uzvards': session['lietotajs']['uzvards'],
    'e-pasts': session['user'],
    'lietotaja_id': session['lietotajs']['lietotaja_id']
  }

  celojumi = dabut_celojumus(session['lietotajs']['lietotaja_id'])
  return render_template('mansprofils.html',
                         login=session['login'],
                         lietotajs=pats,
                         celojumi=celojumi,
                         popcelojumi=panemt_popularakos_celojumus())


app.run(host='0.0.0.0', port=81)

# [(0, 'celojums uz bausku', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'tas nav verts to naudu', 'nakamreiz zinasu', datetime.datetime(2023, 4, 12, 11, 41, 41, 98057), None), (1, 'celojums uz bausku', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'tas nav verts to naudu', 'nakamreiz zinasu', datetime.datetime(2023, 4, 18, 9, 18, 20, 954071), 'kribasmaizes')]
