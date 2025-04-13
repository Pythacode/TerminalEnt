import sys, os, json

# Ajouter le dossier parent au chemin
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './../')))
from config import *

print()

log('Please choice file path\n')

with open(inputf(''), 'w', encoding='utf-8') as f :
    json.dump({'cookies' : cookies}, f, indent=4)
