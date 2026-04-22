 
from pathlib import Path
import os

class Item:
    def __init__(self, nom, chemin_parent, date_creation):
        self.nom = nom
        self.chemin_parent = chemin_parent
        self.date_creation = date_creation
        
        # Vérification de l'existence du fichier ou du dossier
        if not Path(self.chemin_parent, self.nom).exists():
            raise FileNotFoundError(f"Le fichier ou dossier '{self.nom}' n'existe pas sur le disque.")
    
    def ouvrir(self):
        raise NotImplementedError("La méthode 'ouvrir' doit être implémentée dans les classes dérivées.")


class Fichier(Item):
    def __init__(self, nom, chemin_parent, date_creation, extension):
        super().__init__(nom, chemin_parent, date_creation)
        self.extension = extension
    
    def ouvrir(self):
        file_path = Path(self.chemin_parent, self.nom)
        os.startfile(str(file_path))


class Dossier(Item):
    def __init__(self, nom, chemin_parent, date_creation):
        super().__init__(nom, chemin_parent, date_creation)
    
    def ouvrir(self):
        folder_path = Path(self.chemin_parent, self.nom)
        os.startfile(str(folder_path))
    
    def retirer_ancien_fichier(self, date):
        folder_path = Path(self.chemin_parent, self.nom)
        for item in folder_path.iterdir():
            if item.is_file() and item.stat().st_mtime < date.timestamp():
                item.unlink()
