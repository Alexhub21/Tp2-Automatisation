import os
import shutil
import time
import argparse
from datetime import datetime
import psutil
CACHE_DIR = "cache_usb"
LOG_FILE = "log.txt"

def ecrire_log(message):
    date = datetime.now()
    timestamp = date.strftime("%Y-%m-%d %H:%M:%S")
    ligne = "[ " + timestamp + " ] " + message 
    fichier = open(LOG_FILE, "a" ,encoding="utf-8")
    fichier.write(ligne + "\n")
    fichier.close()
    print(ligne)

def detecter_unites_usb():
    ...

def taille_dossier(chemin):
      ...
def espace_libre(lecteur):
     ...
def copier_contenu(source, destination):
    ... 
