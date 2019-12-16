import requests
import json

app_name = 'mainapp'
fichier_conf = "conf.json"
fichier = app_name + "/" + fichier_conf

http = ""
server = ""
port = ""
port_sep = ""
url_sep = ""
header_content_type = ""
app = ""
url_operation = ""
headers = ""


def charger_parametre_service(nom_service, operation):

    with open(fichier) as json_data:
        data_dict = json.load(json_data)

        http = data_dict["services"][nom_service]["debut_requete"]
        server = data_dict["services"][nom_service]["serveur_ip"]
        port = data_dict["services"][nom_service]["serveur_port"]
        port_sep = data_dict["services"][nom_service]["port_separateur"]
        url_sep = data_dict["services"][nom_service]["url_separateur"]

        header_content_type = data_dict["services"][nom_service]["header_content_type"]
        app = data_dict["services"][nom_service]["nom_application"]
        url_operation = data_dict["services"][nom_service]["operations"][operation]["url"]

        url = http + server + port_sep + port + url_sep + app + url_sep + url_operation + url_sep

        return url, header_content_type


def creation_etudiant(etudiant_data):
    
    url, header = charger_parametre_service("etudiant_service","creation")

    headers = {'content-type': header}

    r = requests.post(url, headers=headers, data = json.dumps(etudiant_data))
    return r

def liste_etudiants():

    url, header = charger_parametre_service("etudiant_service","liste")

    headers = {'content-type': header}

    r = requests.get(url, headers=headers)
    etudiants = r.json()
    
    return etudiants

def recherche_etudiant(recherche,trier_par):

    url, header = charger_parametre_service("etudiant_service","recherche")

    headers = {'content-type': header}

    donnees_recherche ="?recherche="+ recherche +"&trier_par=" + trier_par
    
    url = url + donnees_recherche
    
    #print(url)

    r = requests.get(url, headers=headers)
    etudiants = r.json()
    
    return etudiants

def suppression_etudiant(id):

    url, header = charger_parametre_service("etudiant_service","suppression")
    headers = {'content-type': header}
    url = url + id

    r = requests.delete(url, headers=headers)
    
    return "suppression effectuée"

def modification_etudiant(id, etudiant_data):

    url, header = charger_parametre_service("etudiant_service","modification")
    headers = {'content-type': header}
    url = url + id

    r = requests.put(url, headers=headers, data = json.dumps(etudiant_data))
    etudiants = r.json()

    return etudiants
