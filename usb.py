import os
import shutil
import time
import argparse
from datetime import datetime
from pathlib import Path
import psutil
CACHE_DIR = "cache_usb"
LOG_FILE = "log.txt"

def detecter_unites_usb():
    lecteurs = []

    for lettre in "DEFGHIJKLMNOPQRSTUVWXYZ":
        chemin = lettre + ":\\"
        if os.path.exists(chemin):
            lecteurs.append(chemin)

    return lecteurs

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
    # Dossiers système à ignorer
    dossiers_ignores = {"$Recycle.Bin", "System Volume Information", "pagefile.sys", "hiberfil.sys", "$RECYCLE.BIN"}
    
    try:
        if not os.path.exists(destination):
            os.makedirs(destination)

        for element in os.listdir(source):
            # Ignorer les dossiers système
            if element in dossiers_ignores:
                ecrire_log(f"Dossier système ignoré : {element}")
                continue
            
            chemin_source = os.path.join(source, element)
            chemin_destination = os.path.join(destination, element)

            try:
                if os.path.isfile(chemin_source):
                    shutil.copy2(chemin_source, chemin_destination)
                    print(f"Fichier copié : {element}")
                elif os.path.isdir(chemin_source):
                    shutil.copytree(chemin_source, chemin_destination)
                    print(f"Dossier copié : {element}")
            except PermissionError:
                ecrire_log(f"Accès refusé : {element}")
                continue
            except Exception as e:
                ecrire_log(f"Erreur pour {element} : {str(e)}")
                continue

    except Exception as e:
        ecrire_log("Erreur lors de la copie du contenu : " + str(e))

def nettoyer_lecteur(lecteur):
    # Dossiers système à ignorer
    dossiers_ignores = {"$Recycle.Bin", "System Volume Information", "pagefile.sys", "hiberfil.sys", "$RECYCLE.BIN"}
    
    try:
        for element in os.listdir(lecteur):
            # Ignorer les dossiers système
            if element in dossiers_ignores:
                continue
                
            chemin_element = os.path.join(lecteur, element)
            try:
                if os.path.isfile(chemin_element):
                    os.remove(chemin_element)
                    print(f"Fichier supprimé : {chemin_element}")
                elif os.path.isdir(chemin_element):
                    shutil.rmtree(chemin_element)
                    print(f"Dossier supprimé : {chemin_element}")
            except PermissionError:
                ecrire_log(f"Accès refusé lors du nettoyage : {element}")
                continue
            except Exception as e:
                ecrire_log(f"Erreur lors du nettoyage de {element} : {str(e)}")
                continue
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

# fonction dupliquer
def dupliquer_vers_cible(lecteur ,effacer):
    try:

       ecrire_log("Début de la copie vers la clé cible : " + lecteur) 
       taille_cache = taille_dossier(CACHE_DIR)
       libre = espace_libre(lecteur)
       if taille_cache > libre:
          ecrire_log("Espace insuffisant sur la clé cible pour la duplication.")
          return    
       if effacer:
            ecrire_log("Nettoyage de la clé cible avant la duplication.")
            nettoyer_lecteur(lecteur)
       copier_contenu(CACHE_DIR, lecteur)
       ecrire_log("Duplication vers la clé cible terminée : " + lecteur)

    except Exception as e:
        ecrire_log("Erreur lors de la duplication vers la clé cible : " + str(e))
    
    #verifier la talle
    # test a faire
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--effacer", action="store_true")
    args = parser.parse_args()

    source_initialisee = False
    source_usb = None
    anciennes_cles = []

    ecrire_log("Démarrage du programme...")

    while True:
        cles = detecter_unites_usb()

        # CAS 1 : aucune clé source encore choisie
        if not source_initialisee:
            if len(cles) > 0:
                source_usb = cles[0]
                initialiser_source(source_usb)
                source_initialisee = True
            else:
                print("En attente d'une clé USB source...")

        # CAS 2 : la source existe déjà, on attend les cibles
        else:
            # détecter les nouvelles clés
            for cle in cles:
                if cle not in anciennes_cles:
                    if cle != source_usb:
                        ecrire_log("Nouvelle clé cible détectée : " + cle)
                        dupliquer_vers_cible(cle, args.effacer)

            # détecter les clés retirées
            for ancienne in anciennes_cles:
                if ancienne not in cles:
                    if ancienne == source_usb:
                        ecrire_log("Clé source débranchée.")
                    else:
                        ecrire_log("Clé cible débranchée.")

        anciennes_cles = cles.copy()
        time.sleep(3)


if __name__ == "__main__":
    main()