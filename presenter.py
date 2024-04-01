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

    def load_weapon(self, weapon_id):
        try:
            response = requests.get(f"http://localhost:5166/api/Weapon/{weapon_id}")
            if response.status_code == 200:
                weapon_data = response.json()
                weapon = Weapon(weapon_data['id'], weapon_data['name'], weapon_data['type'],
                                weapon_data['manufacturer'], weapon_data['caliber'],
                                weapon_data['magazineCapacity'], weapon_data['fireRate'],
                                weapon_data['ammoCount'])
                self.weapon_loaded.emit(weapon)
            else:
                self.error_occurred.emit(f"Failed to load weapon: {response.status_code}")
        except Exception as e:
            self.error_occurred.emit(f"An error occurred: {str(e)}")

    def load_all_weapons(self):
        try:
            response = requests.get("http://localhost:5166/api/Weapon")
            if response.status_code == 200:
                weapons_data = response.json()
                weapons = [Weapon(weapon_data['id'], weapon_data['name'], weapon_data['type'],
                                weapon_data['manufacturer'], weapon_data['caliber'],
                                weapon_data['magazineCapacity'], weapon_data['fireRate'],
                                weapon_data['ammoCount']) for weapon_data in weapons_data]
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

    def update_weapon(self, weapon_id, updated_weapon_data):  # Modification de la signature
        try:
            response = requests.put(f"http://localhost:5166/api/Weapon/{weapon_id}", json=updated_weapon_data)  # Utilisation de l'ID dans l'URL
            if response.status_code == 200:
                self.weapon_updated.emit(weapon_id)
            else:
                self.error_occurred.emit(f"Failed to update weapon: {response.status_code}")
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
