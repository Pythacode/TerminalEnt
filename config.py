from cryptography.fernet import Fernet
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.webdriver import Options
from colorama import Fore
from datetime import datetime
import unicodedata

secondary_color = Fore.WHITE
main_color = Fore.BLUE
error_color = Fore.RED

path = "~/"
user = "NoConnect"
school_name = "NoSelect"

global driver
driver = None

global cookies
cookies = None

logo = """
                ███████╗███╗   ██╗████████╗
                ██╔════╝████╗  ██║╚══██╔══╝
                █████╗  ██╔██╗ ██║   ██║  
                ██╔══╝  ██║╚██╗██║   ██║   
                ███████╗██║ ╚████║   ██║   
                ╚══════╝╚═╝  ╚═══╝   ╚═╝   """

for i in ['╗', '╔', '╝', '═', '╚', '║', '╔', '╚', '╔', '╚', '╔', '╚', '╝', '╔', '╝', '═', '╚', '╝', '═'] : 
    logo = logo.replace(i, f"{secondary_color}{i}{main_color}") # Rend les ombres blanches


def normaliser(texte):
    # Enlève les accents et met en majuscule
    texte = unicodedata.normalize('NFD', texte)
    texte = ''.join(c for c in texte if unicodedata.category(c) != 'Mn')
    return texte.upper()

def generate_menu(title, liste, menu_size=110, row = 3) :
    menu = ""
    height_row=int((menu_size-20)/row)
    height = menu_size
    largeur_title = len(title)
    space = (height / 2) - (largeur_title / 2) - 4

    indexs = [9]

    for _ in range(row-1) :
        indexs.append(indexs[-1] + height_row+7)

    menu += f"{" "*int(space)}┌──{"─"*int(largeur_title)}──┐"
    ligne = f"\n{"─"*int(space)}┤  {secondary_color}{title}{main_color}  ├{"─"*int(space)}"

    ligne = ligne[:5] + ("┬" if ligne[5] == "─" else ligne[5]) + ligne[6:]

    menu += ligne

    ligne = f"\n{" "*int(space)}└──{"─"*int(largeur_title)}──┘{" "*int(space)}"

    ligne = ligne[:5] + ("│" if ligne[5] == " " else ("┬" if ligne[5] == "─" else "├" )) + ligne[6:]

    menu += ligne

    menu += f"\n    └───┬{f"{"─"*int(height_row+6)}┬"*int(row-2)}{"─"*int(height_row+6)}┐" # Le +6 est = à "├─ [0] "
    option = ""

    for index in range(0, len(liste), row):
        elements = liste[index:index+row]

        line = '\n\t'

        for i, elem in enumerate(elements) :
            line += f"{"└" if index + i > len(liste)-4 else "├"}─[{secondary_color}{index+i+1:02}{main_color}] {elem[-height_row:]:<{height_row}}"
            
        option += line
        
    return menu + option + '\n'

def time() :
    return datetime.now().strftime("%H:%M:%S")

def inputf(arg) :
    return input(f"{main_color}┌──({secondary_color}{user}{main_color}@{secondary_color}{school_name}{main_color})─[{secondary_color}{path}{main_color}]\n└─[{secondary_color}{time()}{main_color}]{secondary_color} {arg}{" " if arg != '' else ''}$ ")

def printf(arg) :
    print(main_color + arg) 

def load_key():
    with open("secret.key", "rb") as key_file:
        return key_file.read()
    
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def error(arg) :
    print(f"{error_color}[{secondary_color}{time()}{error_color}] [{secondary_color}!{error_color}] | {arg}")

def log(arg) :
    printf(f"[{secondary_color}{time()}{main_color}] [{secondary_color}>{main_color}] | {arg}")

def open_driver() :
    global driver
    log("Open driver")

    options = Options()
    #options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)
    log('Driver opened')

def connect(username, password, url, etablissement_name) :
    global driver
    global cookies

    if not driver : open_driver()

    if driver.title == "" : open_page = False
    else : open_page = True

    if not open_page :

        driver.get(url)

        #Élève ou parent
        elem = driver.find_element(By.CLASS_NAME, "fo-connect__link")
        elem.click()

        assert "Authentification" in driver.title

        log("Connexion")

        #Élève ou parent
        elem = driver.find_element(By.XPATH, "/html/body/main/div/div/div[1]/div/div/form/fieldset[1]/legend/button")
        elem.click()

        # De l'académie de montpellier 
        elem = driver.find_element(By.XPATH, "/html/body/main/div/div/div[1]/div/div/form/fieldset[1]/ul/li[1]/div/label")
        elem.click()

        #Valider
        elem = driver.find_element(By.ID, "button-submit")
        elem.click()

        log('Éduconnect')

        ## Éduconnect
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "bouton_eleve")))


        assert "ÉduConnect" in driver.title

        #Éleve
        elem = driver.find_element(By.ID, "bouton_eleve")
        elem.click()

    #Username
    username_entry = driver.find_element(By.ID, "username")
    username_entry.clear()
    username_entry.send_keys(username)

    #Password
    password_entry = driver.find_element(By.ID, "password")
    password_entry.clear()
    password_entry.send_keys(password)

    # Valider
    elem = driver.find_element(By.ID, "bouton_valider")
    elem.click()
    
    while not etablissement_name in driver.title : print(etablissement_name, driver.title)

    if driver.find_elements(By.CLASS_NAME, "fr-error-text") == [] :
        cookies = driver.get_cookies()
        return True
    else : return False

def close_driver() :
    global driver
    driver.quit()
    log('driver closed')
