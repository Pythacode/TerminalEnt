import sys, os, requests
# Ajouter le dossier parent au chemin
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './../')))
from config import *
import config
from bs4 import BeautifulSoup

url = config.url + "/sg.do?PROC=MESSAGERIE&ACTION=LISTER_COMMUNICATION&CONSERVER_SELECTION=false&PAGINATION=false&ID_DOSSIER=7515308"


cookies = {cookie['name']: cookie['value'] for cookie in cookies}

response = requests.get(url, cookies=cookies)


soup = BeautifulSoup(response.text, 'html.parser')

containeur = soup.find(id="js_boite_reception")

messages = containeur.find_all('li')

for message in messages :

    # Récupérer l'expéditeur
    expediteur = message.select("div.col--xs-3.col--full span.text--ellipsis span[title]")[1].text.strip()

    # Récupérer le sujet
    sujet = message.select_one("a.js-consulterMessage").text.strip()

    # Récupérer la date
    date = message.select_one("time").text.strip()

    log("Sujet : " + sujet)
    log("Expéditeur : " + expediteur)
    log("Date : " + date)
    if message != messages[-1] : log('────────────────────────────────')