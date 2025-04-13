import sys, os, requests
# Ajouter le dossier parent au chemin
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './../')))
from config import *

url = "https://joliot-curie.mon-ent-occitanie.fr/sg.do?PROC=MESSAGERIE&ACTION=LISTER_COMMUNICATION&CONSERVER_SELECTION=false&PAGINATION=false&ID_DOSSIER=7515308"

cookies = {cookie['name']: cookie['value'] for cookie in cookies}

response = requests.get(url, cookies=cookies)

with open("out.html", 'w', encoding='utf-8') as f :
    f.write(response.text)
