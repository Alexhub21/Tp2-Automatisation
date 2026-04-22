import os
import shutil
import time
import argparse
from datetime import datetime
import psutil
CACHE_DIR = "cache_usb"
LOG_FILE = "log.txt"

def detecter_unites_usb():
    lecteurs = []

    for partition in psutil.disk_partitions():
        lecteurs.append(partition.device)

    return lecteurs
#print(detecter_unites_usb())

def ecrire_log(message):
    date = datetime.now()
    timestamp = date.strftime("%Y-%m-%d %H:%M:%S")
    ligne = "[ " + timestamp + " ] " + message 
    print(ligne)
    try:
        with open(LOG_FILE, "a" ,encoding="utf-8") as fichier:
            fichier.write(ligne + "\n")
    except:
        print("Erreur d'ecriture du fichier de log")

def copier_contenu(source, destination):
    try:
        if not os.path.exists(destination):
            os.makedirs(destination)
        for element in os.listdir(source):
            chemin_source = os.path.join(source, element)
            chemin_destination = os.path.join(destination, element)
            if os.path.isfile(chemin_source):
                shutil.copy2(chemin_source, chemin_destination)
            elif os.path.isdir(chemin_source):
                shutil.copytree(chemin_source, chemin_destination)
    except Exception as e:
        ecrire_log("Erreur lors de la copie du contenu : " + str(e))
def nettoyer_lecteur(lecteur):
    try:
        for element in os.listdir(lecteur):
            chemin_element = os.path.join(lecteur, element)
            if os.path.isfile(chemin_element):
               os.remove(chemin_element)
               print(f"Fichier supprimé : {chemin_element}")
            elif os.path.isdir(chemin_element):
               shutil.rmtree(chemin_element)
               print("Dossier supprimé :" ,chemin_element)
    except Exception as e:
        ecrire_log("Erreur lors du nettoyage du lecteur : " + str(e))
def initialiser_source(lecteur):
    try:
        ecrire_log("Clé source détectée : " + lecteur)
        if not os.path.exists(CACHE_DIR):
           os.makedirs(CACHE_DIR)
        nettoyer_lecteur(CACHE_DIR)
        ecrire_log("Copie du contenu de la clé source commnencée")
        copier_contenu(lecteur, CACHE_DIR)
        ecrire_log("Copie du contenu de la clé source terminée")
    except Exception as e:
        ecrire_log("Erreur lors de l'initialisation de la source : " + str(e))
# fonction dupliquer le contenu de la cache vers la clé source utilser
# la fonction taille_dossier(...),espace_libre(..)
def taille_dossier(chemin):
    total = 0
    for racine, dossiers, fichiers in os.walk(chemin):
        for fichier in fichiers:
            chemin_fichier = os.path.join(racine, fichier)
            total += os.path.getsize(chemin_fichier)
    return total

def espace_libre(lecteur):
    total, utilise, libre = shutil.disk_usage(lecteur)
    return libre
# Tester les fonctions
# ecrire_log("Démarrage du programme de nettoyage de clé USB")
#ecrire_log("Vérification des lecteurs disponibles...")
   
def main():
    anciennes_cles = []

    while True:
        
        cles = detecter_unites_usb()

        for cle in cles:
            if cle not in anciennes_cles:
                print("Nouvelle clé détectée :", cle)

        anciennes_cles = cles.copy()
        print(detecter_unites_usb())
        time.sleep(3)
if __name__ == "__main__":    main()
