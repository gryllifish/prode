import os
import requests
import urllib.parse
import urllib
import json
import http.client

import numpy as np

from flask import redirect, render_template, request, session
from functools import wraps
from urllib.request import urlopen
from bs4 import BeautifulSoup


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def fixture():

    # Contact API / URL: https://fixturedownload.com/feed/json/fifa-world-cup-2022/
    with urllib.request.urlopen("https://fixturedownload.com/feed/json/fifa-world-cup-2018") as url:
        data =json.load(url)

    return data

def lookupTeam(team):
     # Contact API / URL: https://fixturedownload.com/feed/json/fifa-world-cup-2022/
    try:
        url= f"https://fixturedownload.com/feed/json/fifa-world-cup-2018/{team}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None
    try:
        quote = response.json()
        return {
            "HomeTeam": quote[0]["HomeTeam"],
            "HomeTeamScore": quote[0]["HomeTeamScore"],
            "AwayTeam": quote[0]["AwayTeam"],
            "AwayTeamScore": quote[0]["AwayTeamScore"]
            }
    except (KeyError, TypeError, ValueError):
        return None

def sortByKey(dict):
    return dict[0]


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

# Encuentra los equipos de cada grupo
def findMatchFromGroup(fixture, group):
    matchesFromGroup = []
    for match in fixture:
        if match['Group'] == group:
            matchesFromGroup.append(match)
    return matchesFromGroup

# Busca en la lista de diccionarios el value de un key especifico
def getSpecific(d, k):
    listValues = [i[k] for i in d]
    listReturn = []
    for val in listValues:
        if val != None:
            listReturn.append(val)
    return listReturn

# Compara resultados reales con resultados de usuario
def compare(home, away, userH, userA, iterations):
    puntos = 0
    for i in range(iterations):
        try:
            if home[i] == userH[i] and away[i] == userA[i]:
                puntos += 3
            elif home[i] > away[i] and userH[i] > userA[i]:
                puntos += 1
            elif home[i] < away[i] and userH[i] < userA[i]:
                puntos += 1
            elif home[i] == away[i] and userH[i] == userA[i]:
                puntos += 1

        except:
            continue
    return puntos

def compareTwo(dict, keyHome, keyAway):
    puntos = 0
    for i in range(len(dict)):
        try:
            if dict[i][keyHome] == dict[i]['userHome'] and dict[i][keyAway] == dict[i]['userAway']:
                puntos += 3
            if dict[i][keyHome] > dict[i][keyAway] and dict[i]['userHome'] > dict[i]['userAway']:
                puntos += 1
            if dict[i][keyHome] < dict[i][keyAway] and dict[i]['userHome'] < dict[i]['userAway']:
                puntos += 1
            if dict[i][keyHome] == dict[i][keyAway] and dict[i]['userHome'] == dict[i]['userAway']:
                puntos += 1

        except:
            continue
    return puntos

def fixturesTwo():
    # Contact API
    try:
        url = "https://world-cup-json-2022.fly.dev/matches"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return 'Maluma'
    data = response.json()
    return data

def today():
     # Contact API
    try:
        url = "https://world-cup-json-2022.fly.dev/matches/"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return 'Nada por hoy'
    data = response.json()
    return data

def tomorrow():
     # Contact API
    try:
        url = "https://world-cup-json-2022.fly.dev/matches/"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return 'bilbo'
    data = response.json()
    return data

def current():
     # Contact API

    try:
        url = "https://world-cup-json-2022.fly.dev/matches/"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return 'bilbo'
    data = response.json()
    return data



def campeon():
    # Contact API
    try:
        url = "https://world-cup-json-2022.fly.dev/matches?start_date=2022-12-18"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return 'Maluma'
    data = response.json()
    winner = data[0]['winner']
    return winner

def createList(list):
    intList = []
    for sublist in list:
        for item in sublist:
            intList.append(item)
    return intList

def insertKeyValue(dict, list, key):
    for i in range(len(dict)):
        try:
            dict[i][key] = list[i]
        except:
            dict[i][key] = None
        return

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def wikipedia():
    page = requests.get("https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_squads")

    # Scrap webpage
    soup = BeautifulSoup(page.text, 'html.parser')

    list = []
    for tab in soup.find_all('table', {'class':'sortable wikitable plainrowheaders'}):
        for i in tab.find_all('tr', {'class':'nat-fs-player'}):
            for j in i.find_all('th'):
                list.append(j.text.replace('\n', ''))

    return list

def botaDeOro():
    page = requests.get("https://en.wikipedia.org/wiki/2022_FIFA_World_Cup")
    soup = BeautifulSoup(page.text, 'html.parser')
    list = []
    for tab in soup.find_all('table', {'class':'wikitable'}):
        if tab.find_previous() == "Classement du Soulier d'or":
            list.append(tab.text)
    return list











# Hacer función para comprobar si los resultados de la apuesta son correctos.


# PRUEBA LUEGO PARA VERIFICAR QUE EL USUARIO LLENA TODOS LOS PARTIDOS
# si el usuario no llena todos los partidos

