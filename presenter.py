import requests
from PyQt5.QtCore import QObject, pyqtSignal
from model import Weapon

class WeaponPresenter(QObject):
    weapon_loaded = pyqtSignal(Weapon)
    all_weapons_loaded = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    weapon_added = pyqtSignal(int)  
    weapon_deleted = pyqtSignal(int)  
    weapon_updated = pyqtSignal(int)  

    def __init__(self):
        super().__init__()

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
