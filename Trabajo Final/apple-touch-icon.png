import os
import http.client
import json


from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, make_response
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from urllib.request import urlopen
import operator

from helpers import apology, login_required, fixture, usd, sortByKey, findMatchFromGroup, lookupTeam, getSpecific, compare, fixturesTwo, campeon, createList, insertKeyValue, compareTwo, wikipedia, botaDeOro, today, tomorrow, current

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///futbol.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
     # buscar fecha de hoy
    date= db.execute("""SELECT date('now')""")[0]["date('now')"]

    user = session['user_id']
    usern = db.execute("SELECT username FROM users WHERE id=?", user)
    username = usern[0]["username"]

    # Lista de selecciones para form select
    teams = ['Argentina', 'Brazil', 'England', 'France', 'Spain', 'Belgium', 'Portugal', 'Germany', 'Netherlands', 'Uruguay', 'Croatia', 'Denmark', 'Mexico', 'United States', 'Senegal', 'Wales', 'Poland', 'Australia', 'Japan', 'Morocco', 'Switzerland', 'Ghana', 'Korea Republic', 'Cameroon', 'Serbia', 'Canada', 'Costa Rica', 'Tunisia', 'Saudi Arabia', 'Iran', 'Ecuador', 'Qatar']
    teams.sort()

    # PARTIDOS HOY ,MAÑANA Y AHORA

    hoy = today()
    manana = tomorrow()
    ahora = current()

    seleccion = None

     # //// FASE DE GRUPOS ////
        # ARMAR LISTA CON RESULTADOS DE API
    fixtures = fixture()
    fixtures = fixtures[:48]
    # Ordenar fixture por grupo
    fix = sorted(fixtures, key=operator.itemgetter('Group'))
    # Obtener resultados de Home y Away ORDENADOS por grupo.
    homeScore = getSpecific(fix, 'HomeTeamScore')
    awayScore = getSpecific(fix, 'AwayTeamScore')
    homeScore = homeScore[:48]
    awayScore = awayScore[:48]

    # API para SEGUNDA RONDA
    fixTwoTest = fixturesTwo()
    fixTwo= fixTwoTest[48:]
    homeGoalsSeg = []
    awayGoalsSeg = []
    # Obtener resultados de Home y Away de segunda ronda
    homeScoreSegunda = getSpecific(fixTwo, 'home_team')
    awayScoreSegunda = getSpecific(fixTwo, 'away_team')

    for i in range(len(homeScoreSegunda)):
        try:
            homeGoalsSeg.append(homeScoreSegunda[i]['goals'])
        except:
            break
    for j in range(len(awayScoreSegunda)):
        try:
            awayGoalsSeg.append(awayScoreSegunda[j]['goals'])
        except:
            break

    grupos = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    segundaRonda = ['octavos', 'cuartos', 'semis', 'final']

    # Buscar resultados en database  mediante un loop a través de lista grupos
    dict = {}
    userHome = []
    userAway = []
    userHomeGroups = []
    userHomeSegunda = []
    userAwaySegunda = []

    for i in grupos:
        try:
            userScore = db.execute(f"SELECT resultsHome, resultsAway from Group{i} WHERE userId = ? ORDER BY indice DESC LIMIT 1", user)
            # Split resultados en lista de strings divididos por ,
            userHomeStringG = userScore[0]['resultsHome'].split(',')
            # Convertir a lista de integers
            userHomeGroups = list(map(int, userHomeStringG))
            userHome.append(userHomeGroups)
            # Visitantes
            userAwayStringG = userScore[0]['resultsAway'].split(',')
            userAwayGroups = list(map(int, userAwayStringG))
            userAway.append(userAwayGroups)
            dict[f'group{i}'] = userHome # NO LO ESTOY USANDO
        except:
            continue
    # Crear lista única de userHome y userAway
    groupHomeList = createList(userHome)
    groupAwayList = createList(userAway)
    # Insertar datos de usuario en fix. LO INTENTÉ CON FUNCIÓN Y NO ITERABA. VER.
    for i in range(len(fix)):
            try:
                fix[i]['userHome'] = groupHomeList[i]
                fix[i]['userAway'] = groupAwayList[i]
            except:
                fix[i]['userHome'] = None
                fix[i]['userAway'] = None

    # Comparar resultados de Grupo
    puntosPrimera = compare(homeScore, awayScore, groupHomeList, groupAwayList, 48)
    #puntosPrimera = compareTwo(fix, 'HomeTeamScore', 'AwayTeamScore')

    # Buscar resultados en database y compararlos con resultados de oct, cuart, semi, final
    for j in segundaRonda:
        try:
            userScoreTwo = db.execute(f"SELECT resultsHome, resultsAway from {j} WHERE userId = ? ORDER BY indice DESC LIMIT 1", user)
            # Split resultados en lista de strings divididos por ,
            userHomeString = userScoreTwo[0]['resultsHome'].split(',')
            # Convertir a lista de integers
            userHomeSegunda = list(map(int, userHomeString))
            # Visitantes
            userAwayString = userScoreTwo[0]['resultsAway'].split(',')
            userAwaySegunda = list(map(int, userAwayString))
        except:
            continue

    # Sumar puntos de segunda ronda
    puntosSegunda = compare(homeGoalsSeg, awayGoalsSeg, userHomeSegunda, userAwaySegunda, 16)


    # BUSCAR CAMPEON
    points = 0
    champion = campeon()
    userChampion = db.execute('SELECT campeon FROM users WHERE id = ?', user)
    if champion == userChampion[0]['campeon'] and champion != None:
        if points == 15:
            points += 0
        else:
            points = 15

    # BUSCAR GOLEADOR
    # Lista de jugadores para form select de goleador.
    scorer = wikipedia()
    userGoleador = db.execute('SELECT goleador FROM users WHERE id = ?', user)
    bota = 'Lionel Messi'
    pts = 0

    try:
        if userGoleador[0]['goleador'] in bota:
            pts = 15
    except:
        pts = 0
    # Suma final de Puntos
    puntos = puntosPrimera + puntosSegunda + points + pts

    # Subir puntos a database
    db.execute("UPDATE users SET puntos = ? WHERE id = ?", puntos, user)

    # TABLA DE USUARIOS
    usuarios = db.execute("SELECT username, puntos FROM users ORDER BY puntos DESC")

    # POST
    if request.method == 'POST':
        seleccion = request.form.get("seleccion") # Formulario para seleccion campeona
        goleador = request.form.get("goleador") # Formulario para goleador
        db.execute("UPDATE users SET campeon = ? WHERE id = ?", seleccion, user)
        db.execute("UPDATE users SET goleador = ? WHERE id = ?", goleador, user)

        return render_template('index.html', seleccion=seleccion, goleador=goleador, fixtures=fixtures, username=username, homeScore=homeScore, awayScore=awayScore, userScore=userScore, userHome=userHome, userAway=userAway, puntos=puntos, usuarios=usuarios, fix=fix, teams=teams, userGoleador=userGoleador, scorer=scorer, hoy=hoy, manana=manana, ahora=ahora)

    # GET
    if request.method == 'GET':

        return render_template('index.html', seleccion=seleccion,fixtures=fixtures, username=username, homeScore=homeScore, awayScore=awayScore, userScore=userScore, userHome=groupHomeList, userAway=groupAwayList, puntos=puntos, usuarios=usuarios, fix=fix, teams=teams, fixTwo=fixTwo, date=date, homeGoalsSeg=homeGoalsSeg, homeScoreSegunda=homeScoreSegunda, champion=champion, userGoleador=userGoleador, scorer=scorer, bota=bota, hoy=hoy, manana=manana, ahora=ahora)

@app.route("/tablausuario/<user>")
@login_required
def tablausuario(user):

    # Mostrar una tabla con las apuestas del usuario seleccionado y los resultados reales.
    dataUser = db.execute("SELECT * FROM users WHERE username = ?", user)
    id = dataUser[0]['id']

    homeUserResults = []
    awayUserResults = []

    # Juntar entradas de usuario de partidos de grupo
    grupos = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    for i in grupos:
        try:
            home = db.execute(f"SELECT resultsHome FROM group{i} WHERE userId= ? ORDER BY indice DESC LIMIT 1", id)
            home = home[0]['resultsHome'].split(',')
            userHome = list(map(int, home))
            away = db.execute(f"SELECT resultsAway FROM group{i} WHERE userId= ? ORDER BY indice DESC LIMIT 1", id)
            away = away[0]['resultsAway'].split(',')
            userAway = list(map(int, away))
            homeUserResults.append(userHome)
            awayUserResults.append(userAway)
        except:
            userHome = [".",".",".",".",".","."]
            homeUserResults.append(userHome)
            userAway = [".",".",".",".",".","."]
            awayUserResults.append(userAway)
    # Buscar partidos de grupo en API
    fixtures = fixture()
    fixtures = fixtures[:48]
    # Ordenar fixture por grupo
    fix = sorted(fixtures, key=operator.itemgetter('Group'))
    # Agregar key userhome y useraway a la lista de dicts de la API
    intListHome = []
    intListAway = []
    for sublist in homeUserResults:
        for item in sublist:
            intListHome.append(item)
    for sub in awayUserResults:
        for each in sub:
            intListAway.append(each)

        for i in range(len(fix)):
            try:
                fix[i]['userHome'] = intListHome[i]
                fix[i]['userAway'] = intListAway[i]
            except:
                fix[i]['userHome'] = "-"
                fix[i]['userAway'] = "-"


    return render_template("tablausuario.html", dataUser=dataUser, id=id, homeUserResults=homeUserResults, fix=fix)

@app.route("/primeraronda", methods=["GET", "POST"])
@login_required
def primeraronda():
    # sesion del usuario
    user = session['user_id']
    usern = db.execute("SELECT username FROM users WHERE id=?", user)
    username = usern[0]["username"]

    # variable con data JSON del mundial
    fixtures = fixture()
    fixGrupos = fixtures[0:16]


    # crear variables para todos los partidos de cada grupo
    groupA = findMatchFromGroup(fixtures, "Group A")
    groupB = findMatchFromGroup(fixtures, "Group B")
    groupC = findMatchFromGroup(fixtures, "Group C")
    groupD = findMatchFromGroup(fixtures, "Group D")
    groupE = findMatchFromGroup(fixtures, "Group E")
    groupF = findMatchFromGroup(fixtures, "Group F")
    groupG = findMatchFromGroup(fixtures, "Group G")
    groupH = findMatchFromGroup(fixtures, "Group H")

    if request.method == 'POST':

        # buscar fecha de hoy
        date = db.execute("""SELECT date('now')""")[0]["date('now')"]

        groupAHomeScore = []
        groupAAwayScore = []
        groupBHomeScore = []
        groupBAwayScore = []
        groupCHomeScore = []
        groupCAwayScore = []
        groupDHomeScore = []
        groupDAwayScore = []
        groupEHomeScore = []
        groupEAwayScore = []
        groupFHomeScore = []
        groupFAwayScore = []
        groupGHomeScore = []
        groupGAwayScore = []
        groupHHomeScore = []
        groupHAwayScore = []
        # Requests group A
        for i in range(6):
            score1 = request.form.get(f"groupAHome{i}")
            scoreVis1 = request.form.get(f"groupAAway{i}")

            # Llenar las listas score y scoreVis con los requests
            groupAHomeScore.append(score1)
            groupAAwayScore.append(scoreVis1)
            # Pasar listas a integer y luego unirlas
            stringsScoreHome = [str(x) for x in groupAHomeScore]
            stringsScoreAway = [str(x) for x in groupAAwayScore]
            stringsHome = ','.join(stringsScoreHome)
            stringsAway = ','.join(stringsScoreAway)


        # Subir apuestas del usuario a la base de datos
        db.execute(f"INSERT INTO groupA(userId, resultsHome, resultsAway) VALUES(?, ?, ?)", user, stringsHome, stringsAway)

        # Requests group B
        for i in range(6):
            scoreB = request.form.get(f"groupBHome{i}")
            scoreBAway= request.form.get(f"groupBAway{i}")

            # Llenar las listas score y scoreVis con los requests
            groupBHomeScore.append(scoreB)
            groupBAwayScore.append(scoreBAway)
            # Pasar listas a integer y luego unirlas
            stringsScoreHomeB = [str(x) for x in groupBHomeScore]
            stringsScoreAwayB = [str(x) for x in groupBAwayScore]
            stringsHomeB = ','.join(stringsScoreHomeB)
            stringsAwayB = ','.join(stringsScoreAwayB)


        # Subir apuestas del usuario a la base de datos
        db.execute(f"INSERT INTO groupB(userId, resultsHome, resultsAway) VALUES(?, ?, ?)", user, stringsHomeB, stringsAwayB)

        # requests group C
        for i in range(6):
            scoreC = request.form.get(f"groupCHome{i}")
            scoreCAway = request.form.get(f"groupCAway{i}")

             # Llenar las listas score y scoreVis con los requests
            groupCHomeScore.append(scoreC)
            groupCAwayScore.append(scoreCAway)
            # Pasar listas a integer y luego unirlas
            stringsScoreHomeC = [str(x) for x in groupCHomeScore]
            stringsScoreAwayC = [str(x) for x in groupCAwayScore]
            stringsHomeC = ','.join(stringsScoreHomeC)
            stringsAwayC = ','.join(stringsScoreAwayC)


        # Subir apuestas del usuario a la base de datos
        db.execute(f"INSERT INTO groupC(userId, resultsHome, resultsAway) VALUES(?, ?, ?)", user, stringsHomeC, stringsAwayC)

        # requests group D
        for i in range(6):
            scoreD = request.form.get(f"groupDHome{i}")
            scoreDAway = request.form.get(f"groupDAway{i}")

             # Llenar las listas score y scoreVis con los requests
            groupDHomeScore.append(scoreD)
            groupDAwayScore.append(scoreDAway)
            # Pasar listas a integer y luego unirlas
            stringsScoreHomeD = [str(x) for x in groupDHomeScore]
            stringsScoreAwayD = [str(x) for x in groupDAwayScore]
            stringsHomeD = ','.join(stringsScoreHomeD)
            stringsAwayD = ','.join(stringsScoreAwayD)


        # Subir apuestas del usuario a la base de datos
        db.execute(f"INSERT INTO groupD(userId, resultsHome, resultsAway) VALUES(?, ?, ?)", user, stringsHomeD, stringsAwayD)

        # requests group E
        for i in range(6):
            scoreE = request.form.get(f"groupEHome{i}")
            scoreEAway = request.form.get(f"groupEAway{i}")

            # Llenar las listas score y scoreVis con los requests
            groupEHomeScore.append(scoreE)
            groupEAwayScore.append(scoreEAway)
            # Pasar listas a integer y luego unirlas
            stringsScoreHomeE = [str(x) for x in groupEHomeScore]
            stringsScoreAwayE = [str(x) for x in groupEAwayScore]
            stringsHomeE = ','.join(stringsScoreHomeE)
            stringsAwayE = ','.join(stringsScoreAwayE)


        # Subir apuestas del usuario a la base de datos
        db.execute(f"INSERT INTO groupE(userId, resultsHome, resultsAway) VALUES(?, ?, ?)", user, stringsHomeE, stringsAwayE)

        # requests group F
        for i in range(6):
            scoreF = request.form.get(f"groupFHome{i}")
            scoreFAway = request.form.get(f"groupFAway{i}")

            # Llenar las listas score y scoreVis con los requests
            groupFHomeScore.append(scoreF)
            groupFAwayScore.append(scoreFAway)
            # Pasar listas a integer y luego unirlas
            stringsScoreHomeF = [str(x) for x in groupFHomeScore]
            stringsScoreAwayF = [str(x) for x in groupFAwayScore]
            stringsHomeF = ','.join(stringsScoreHomeF)
            stringsAwayF = ','.join(stringsScoreAwayF)


        # Subir apuestas del usuario a la base de datos
        db.execute(f"INSERT INTO groupF(userId, resultsHome, resultsAway) VALUES(?, ?, ?)", user, stringsHomeF, stringsAwayF)

        # requests group G
        for i in range(6):
            scoreG = request.form.get(f"groupGHome{i}")
            scoreGAway = request.form.get(f"groupGAway{i}")

            # Llenar las listas score y scoreVis con los requests
            groupGHomeScore.append(scoreG)
            groupGAwayScore.append(scoreGAway)
            # Pasar listas a integer y luego unirlas
            stringsScoreHomeG = [str(x) for x in groupGHomeScore]
            stringsScoreAwayG = [str(x) for x in groupGAwayScore]
            stringsHomeG = ','.join(stringsScoreHomeG)
            stringsAwayG = ','.join(stringsScoreAwayG)


        # Subir apuestas del usuario a la base de datos
        db.execute(f"INSERT INTO groupG(userId, resultsHome, resultsAway) VALUES(?, ?, ?)", user, stringsHomeG, stringsAwayG)

        # requests group H
        for i in range(6):
            scoreH = request.form.get(f"groupHHome{i}")
            scoreHAway = request.form.get(f"groupHAway{i}")

            # Llenar las listas score y scoreVis con los requests
            groupHHomeScore.append(scoreH)
            groupHAwayScore.append(scoreHAway)
            # Pasar listas a integer y luego unirlas
            stringsScoreHomeH = [str(x) for x in groupHHomeScore]
            stringsScoreAwayH = [str(x) for x in groupHAwayScore]
            stringsHomeH = ','.join(stringsScoreHomeH)
            stringsAwayH = ','.join(stringsScoreAwayH)

        # Subir apuestas del usuario a la base de datos
        db.execute(f"INSERT INTO groupH(userId, resultsHome, resultsAway) VALUES(?, ?, ?)", user, stringsHomeH, stringsAwayH)
        flash("Recibimos tu apuesta. Nunca arriesgando, qué bárbaro.")
        return render_template('exito.html')

    # GET
    else:
        return render_template('primeraronda.html', fixtures=fixGrupos, groupA=groupA, groupB=groupB, groupC=groupC, groupD=groupD, groupE=groupE, groupF=groupF, groupG=groupG, groupH=groupH, username=username)

# OCTAVOS
@app.route("/octavos", methods=["GET", "POST"])
@login_required
def octavos():
    # sesion del usuario
    user = session['user_id']
    userN  = db.execute("SELECT username FROM users WHERE id=?", user)
    username = userN [0]["username"]
    score = []
    scoreVis = []

    # Buscar partidos de octavos en API 2
    fixtures = fixturesTwo()
    octavos = fixtures[48:56]

    # Guardar partidos de octavos.

    if request.method == 'POST':

        # Octavos
        for i in range(8):
                score1 = request.form.get(f"octavosHome{i}")
                scoreVis1 = request.form.get(f"octavosAway{i}")

                # Llenar las listas score y scoreVis con los requests
                score.append(score1)
                scoreVis.append(scoreVis1)
                # Pasar listas a integer y luego unirlas
                stringsScoreHome = [str(x) for x in score]
                stringsScoreAway = [str(x) for x in scoreVis]
                stringsHome = ','.join(stringsScoreHome)
                stringsAway = ','.join(stringsScoreAway)


        # Subir apuestas del usuario a la base de datos
        db.execute(f"INSERT INTO octavos(userId, resultsHome, resultsAway) VALUES(?, ?, ?)", user, stringsHome, stringsAway)
        flash("Ya tenemos tu apuesta. Un papelón, pero no le vamos a decir nadie.")
        return render_template('exito.html')

    else:
        return render_template('octavos.html', username=username, octavos=octavos)

@app.route("/cuartos", methods=["GET", "POST"])
@login_required
def cuartos():
    # sesion del usuario
    user = session['user_id']
    userN  = db.execute("SELECT username FROM users WHERE id=?", user)
    username = userN [0]["username"]

    # buscar fecha de hoy
    date = db.execute("""SELECT date('now')""")[0]["date('now')"]

    score = []
    scoreVis = []

    # Buscar partidos de octavos en API 2
    fixtures = fixturesTwo()
    cuartos = fixtures[56:60]

    # Guardar partidos de cuartos.
    if request.method == 'POST':
        for i in range(4):
                score1 = request.form.get(f"cuartosHome{i}")
                scoreVis1 = request.form.get(f"cuartosAway{i}")

                # Llenar las listas score y scoreVis con los requests
                score.append(score1)
                scoreVis.append(scoreVis1)
                # Pasar listas a integer y luego unirlas
                stringsScoreHome = [str(x) for x in score]
                stringsScoreAway = [str(x) for x in scoreVis]
                stringsHome = ','.join(stringsScoreHome)
                stringsAway = ','.join(stringsScoreAway)


        # Subir apuestas del usuario a la base de datos
        db.execute(f"INSERT INTO cuartos(userId, resultsHome, resultsAway) VALUES(?, ?, ?)", user, stringsHome, stringsAway)
        flash("Ya tenemos tu apuesta. Muchos errores, mucho corazón.")
        return render_template('exito.html')
    else:
        return render_template('cuartos.html', username=username, cuartos=cuartos)

@app.route("/semis", methods=["GET", "POST"])
@login_required
def semis():
    # sesion del usuario
    user = session['user_id']
    userN  = db.execute("SELECT username FROM users WHERE id=?", user)
    username = userN [0]["username"]

    # buscar fecha de hoy
    date = db.execute("""SELECT date('now')""")[0]["date('now')"]

    score = []
    scoreVis = []

    # Buscar partidos de semis en API 2
    fixtures = fixturesTwo()
    semis = fixtures[62:64]

    # Guardar partidos de semis.
    if request.method == 'POST':
        for i in range(2):
            score1 = request.form.get(f"semisHome{i}")
            scoreVis1 = request.form.get(f"semisAway{i}")

            # Llenar las listas score y scoreVis con los requests
            score.append(score1)
            scoreVis.append(scoreVis1)
            # Pasar listas a integer y luego unirlas
            stringsScoreHome = [str(x) for x in score]
            stringsScoreAway = [str(x) for x in scoreVis]
            stringsHome = ','.join(stringsScoreHome)
            stringsAway = ','.join(stringsScoreAway)
        # Subir apuestas del usuario a la base de datos
        db.execute(f"INSERT INTO semis(userId, resultsHome, resultsAway) VALUES(?, ?, ?)", user, stringsHome, stringsAway)
        flash("Ya tenemos tu apuesta. El riesgo es tu primer nombre.")
        return render_template('exito.html')
    else:
        return render_template('semis.html', username=username, semis=semis)

@app.route("/final", methods=["GET", "POST"])
@login_required
def final():
    # sesion del usuario
    user = session['user_id']
    userN  = db.execute("SELECT username FROM users WHERE id=?", user)
    username = userN [0]["username"]

    # buscar fecha de hoy
    date = db.execute("""SELECT date('now')""")[0]["date('now')"]

    score = []
    scoreVis = []

    # Buscar partido de final en API 2
    fixtures = fixturesTwo()
    final = fixtures[63:]

    if request.method == 'POST':

        # Final
        scoreFinal = request.form.get("finalHome")
        scoreVisFinal = request.form.get("finalAway")

        # Llenar las listas score y scoreVis con los requests
        score.append(scoreFinal)
        scoreVis.append(scoreVisFinal)
        # Pasar listas a integer y luego unirlas
        stringsScoreHome = [str(x) for x in score]
        stringsScoreAway = [str(x) for x in scoreVis]
        stringsHome = ','.join(stringsScoreHome)
        stringsAway = ','.join(stringsScoreAway)

        # Subir apuestas del usuario a la base de datos
        db.execute(f"INSERT INTO final(userId, resultsHome, resultsAway) VALUES(?, ?, ?)", user, stringsHome, stringsAway)
        flash("Ya tenemos tu apuesta. Qué persona poco arriesgada.")
        return render_template('exito.html')
    else:
        return render_template('final.html', username=username, final=final)


@app.route("/first")
def first():
    return render_template("first.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Te olvidaste el nombre de usuario")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("No escribiste la contraseña")
            return render_template("login.html")


        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    # Si entra via post desde el formulario
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        hashed = generate_password_hash(password, method='pbkdf2:sha256')
        alreadyTaken = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # si no crea username
        if not username:
            flash('Se requiere un nombre de usuario.')
            return render_template('register.html'  )

        # si no crea password
        elif not password:
            flash('Se requiere una contraseña.')
            return render_template('register.html')

        # si los password no match
        elif password != confirmation:
            flash('Las contraseñas no coinciden.')
            return render_template('register.html')

        # si el username ya existe
        elif len(alreadyTaken) > 0:
            flash('El usuario ya existe.')
            return render_template('register.html')
        elif len(password) < 8:
            flash('La contraseña debe tener al menos 8 caracteres.')
            return render_template('register.html')
        elif password == username:
            flash('La contraseña no puede ser igual al nombre de usuario.')
            return render_template('register.html')

        db.execute('INSERT INTO users(username, hash) VALUES(?, ?)', username, hashed)



    return redirect('/')
