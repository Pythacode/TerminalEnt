from cryptography.fernet import Fernet
import re
import os
from colorama import init
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from config import *
import config
from getpass import getpass
import json

init(autoreset=True)

#open_driver()

printf(logo)

printf(f"""──────┬────────────────┬──────────────┬─────────────────────────────────────────┬──────────────
     [{secondary_color}1{main_color}] - Collèges   [{secondary_color}2{main_color}] - Lycées   [{secondary_color}3{main_color}] - Lycées de l'enseignement agricole   [{secondary_color}4{main_color}] - Favori
""")

while True:
    choice = inputf("")
    
    print()

    if choice in [str(i) for i in range(1, 5)] :
        break
    else :
        error("Choix invalide.")

url = False
favourite = False

if choice == "4" :

    if os.path.exists("secret.key") :
        
        with open('favourite_url.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        url = data.get("url")

        pattern = r"^https:\/\/.*\.mon-ent-occitanie\.fr\/?"

        if not re.match(pattern, url) or not data.get("url") or not data.get("username") or not data.get("password") or not data.get("etablisement_name"):
            url = False
            error("Aucun favori ou favori mal configuré")
            quit()
        
        else :
            key = load_key()
            f = Fernet(key)
            decrypted = f.decrypt(data.get('password').encode())
            password = decrypted.decode()
            username = data.get('username')
            etablisement_name = data.get("etablisement_name")
            favourite = True

    else :
        error('Aucune clé de déchiffrage')
        quit()


if not url :

    urls = {"1" : ["https://www.mon-ent-occitanie.fr/colleges-et-lycees/colleges/", "http://www.mon-ent-occitanie.fr/colleges-et-lycees/colleges/liste-des-colleges-suite-23009.htm"], "2" : ["https://www.mon-ent-occitanie.fr/colleges-et-lycees/lycees/"]}


    urls = urls.get(choice)

    response = ""

    for url in urls :

        log('Récupération des établisement en cours')

        response += requests.get(url).text

    log('Traitement des données')
    soup = BeautifulSoup(response, 'html.parser')

    tables = soup.select(".wysiwyg__table")

    tables_dict = {}

    for table in tables :
        tables_dict[table.find("a").text] = table

    regions = [table.find("a").text for table in tables]


    printf(generate_menu("Sélectionne ta région", regions))

    while True:
        choice = inputf("")
        
        print()

        try :
            regions[int(choice)-1]
            break
        except :
            error("Choix invalide.")
            print()

    etablisements = tables_dict.get(regions[int(choice)-1]).select("tr")
    del etablisements[0]
    etablisements_dict = {} 
    for etablisement in [etablisement.text.split('\n') for etablisement in etablisements]:
        etablisements_dict[etablisement[1]] = etablisement[3]
        
    etablisements = [etablisement.text.split('\n')[1] for etablisement in etablisements]
    etablisements_formated = etablisements[:]

    for index, etablisement in enumerate(etablisements_formated):
        for start in ["LYCEE PROFESSIONNEL", "LYCEE CITÉ SCOLAIRE", "LYCEE POLYVALENT", "LYCEE", "CITE MIXTE", "CITE SCOLAIRE", "COLLEGE", "Collège"] :
            if normaliser(etablisement).startswith(start) :
                etablisements_formated[index] = etablisement[(len(start) + 1):]
                break

    printf(generate_menu("Sélectionne ton établisement", etablisements_formated))

    while True:
        choice = inputf("")
        
        print()

        try :
            etablisements[int(choice)-1]
            break
        except :
            error("Choix invalide.")
            print()

    school_name = etablisements[int(choice)-1].replace(' ', '_')

while True :

    if not favourite :
        username = inputf("Username")

        password = getpass(f"""\n{main_color}┌──({secondary_color}{user}{main_color}@{secondary_color}{school_name}{main_color})─[{secondary_color}{path}{main_color}]\n└─[{secondary_color}{time()}{main_color}]{secondary_color} Password $ """)

        url = "https://" + etablisements_dict.get(etablisements[int(choice)-1])
        etablisement_name = etablisements[int(choice)-1]
        print()

    

    if connect(username, password, url, etablisement_name) :
        log('I\'m log !')
        user = username
        if not favourite :
            printf(generate_menu("Enregistrer en favoris", ["Oui", "Non"], row=2))
            choice = inputf(f"""{main_color}┌──({secondary_color}{user}{main_color}@{secondary_color}{school_name}{main_color})─[{secondary_color}{path}{main_color}]\n└─[{secondary_color}{time()}{main_color}]{secondary_color} $ """)
            if choice == "1" :
                generate_key()
                key = load_key()
                f = Fernet(key)
                encrypted = f.encrypt(password.encode())
                data = {
                    'url' : url,
                    'username' : username,
                    'password' : encrypted.decode(),
                    'etablisement_name' : etablisement_name
                }
                with open("favourite_url.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)
        break
    else : 
        error('Wrong password or username. Please retry.\n')

while True :
    try :
        options = [file.replace('_', ' ').removesuffix(".py") if file.endswith('.py') else None for file in os.listdir("./exec/")]
        options = [file for file in options if file is not None]

        printf(generate_menu("Options", options))

        choice = inputf("")

        try :
            int(choice)
        except ValueError :
            error('Réponse non valide')
            continue

        if int(choice) > len(options) :
            error('Réponse non valide')
            continue

        script = 'exec/' + options[int(choice)-1].replace(' ', '_') + '.py'

        try :
            path = ["~/" + options[int(choice)-1].replace(' ', '_')]
            with open(script) as f:
                code = f.read()
                exec(code)
        except Exception as e :
            error(e)
            
    except KeyboardInterrupt :
        print()
        log('Au revoir')
        log("Fermeture en cours")
        break
            
    except Exception as e :
        error('e')
        continue

close_driver()