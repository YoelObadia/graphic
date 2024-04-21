import requests
import openai
from PyQt5.QtCore import QObject, pyqtSignal
from model import Weapon

class WeaponPresenter(QObject):
    weapon_loaded = pyqtSignal(Weapon)
    all_weapons_loaded = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    weapon_added = pyqtSignal(int)  
    weapon_deleted = pyqtSignal(int)  
    weapon_updated = pyqtSignal(int) 
    keyword_founded = pyqtSignal(str)
    openai_founded = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        
    #openai.api_key = "sk-proj-sSqIZQdz54XiGokWUEmiT3BlbkFJUcVZTINcnTAOZUSl0blz"

    def create_weapon_from_data(self, weapon_data):
        return Weapon(weapon_data['id'], weapon_data['name'], weapon_data['type'],
                    weapon_data['manufacturer'], weapon_data['caliber'],
                    weapon_data['magazineCapacity'], weapon_data['fireRate'],
                    weapon_data['ammoCount'], weapon_data.get('images'))  # Ajout de 'images'

    def load_weapon(self, weapon_id):
        try:
            response = requests.get(f"http://localhost:5166/api/Weapon/{weapon_id}")
            if response.status_code == 200:
                weapon_data = response.json()
                weapon = self.create_weapon_from_data(weapon_data)
                self.weapon_loaded.emit(weapon)
            else:
                self.error_occurred.emit(f"Failed to load weapon: {response.status_code}")
        except Exception as e:
            self.error_occurred.emit(f"An error occurred: {str(e)}")

    def weapon_exists(self, weapon_id):
        try:
            response = requests.get(f"http://localhost:5166/api/Weapon/{weapon_id}")
            return response.status_code == 200
        except Exception as e:
            print(f"An error occurred while checking weapon existence: {str(e)}")
            return False

    def load_all_weapons(self):
        try:
            response = requests.get("http://localhost:5166/api/Weapon")
            if response.status_code == 200:
                weapons_data = response.json()
                weapons = [self.create_weapon_from_data(weapon_data) for weapon_data in weapons_data]  # Utiliser create_weapon_from_data
                self.all_weapons_loaded.emit(weapons)
            else:
                self.error_occurred.emit(f"Failed to load weapons: {response.status_code}")
        except Exception as e:
            self.error_occurred.emit(f"An error occurred: {str(e)}")

    def add_weapon(self, weapon_data):
        try:
            response = requests.post("http://localhost:5166/api/Weapon", json=weapon_data)
            if response.status_code == 201:
                new_weapon_id = response.json()['id']
                self.weapon_added.emit(new_weapon_id)
            else:
                self.error_occurred.emit(f"Failed to add weapon: {response.status_code}")
        except Exception as e:
            self.error_occurred.emit(f"An error occurred: {str(e)}")

    def update_weapon(self, weapon_id, updated_weapon_data):
        try:
            response = requests.put(f"http://localhost:5166/api/Weapon/{weapon_id}", json=updated_weapon_data)
            return response.status_code in {200, 204}
        except Exception as e:
            print(f"An error occurred while updating weapon: {str(e)}")
            return False

    def load_weapon_details(self, weapon_id):
        try:
            response = requests.get(f"http://localhost:5166/api/Weapon/{weapon_id}")
            if response.status_code == 200:
                weapon_data = response.json()
                return self.create_weapon_from_data(weapon_data)  # Utiliser create_weapon_from_data
            else:
                self.error_occurred.emit(f"Failed to load weapon details: {response.status_code}")
        except Exception as e:
            self.error_occurred.emit(f"An error occurred: {str(e)}")

    def delete_weapon(self, weapon_id):
        try:
            response = requests.delete(f"http://localhost:5166/api/Weapon/{weapon_id}")
            if response.status_code == 200:
                self.weapon_deleted.emit(weapon_id)
            else:
                self.error_occurred.emit(f"Failed to delete weapon: {response.status_code}")
        except Exception as e:
            self.error_occurred.emit(f"An error occurred: {str(e)}")

    def search_keyword(self, keyword):
        try:
            response = requests.get(f"http://localhost:5166/api/Imagga/classify?keyword={keyword}")
            if response.status_code == 200:
                self.keyword_founded.emit(response.content.decode('utf-8'))
            else:
                self.error_occurred.emit(f"Failed to retrieve weapons: {response.status_code}")
        except Exception as e:
            self.error_occurred.emit(f"An error occurred: {str(e)}")

    def search_openai(self, prompt):
        openai_endpoint = "http://localhost:5166/api/ChatGPT"  # Remplacez par votre endpoint

        # Préparer les données avec le message
        data = {
            "Message": prompt
        }

        try:
            # Envoyer une requête POST au serveur ASP.NET
            response = requests.post(openai_endpoint, json=data)
            if response.status_code == 200:
                # Obtenir le texte de la réponse
                result = response.json().get("response", "")
                # Émettre le signal avec le texte
                self.openai_founded.emit(result)
            else:
                self.error_occurred.emit(f"Erreur OpenAI: {response.status_code}")
        except Exception as e:
            self.error_occurred.emit(f"Erreur de connexion au serveur: {str(e)}")