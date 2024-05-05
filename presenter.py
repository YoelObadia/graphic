import requests
from PyQt5.QtCore import QObject, pyqtSignal
from model import Weapon

# The `WeaponPresenter` class in Python defines methods to interact with a REST API for loading,
# adding, updating, and deleting weapon data, as well as searching for keywords and using an OpenAI
# model or Imagga.
class WeaponPresenter(QObject):
    # These lines are defining custom signals using PyQt5's `pyqtSignal` class. Each signal
    # corresponds to a specific event that can occur in the application. 
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
        

    def create_weapon_from_data(self, weapon_data):
        """
        This function creates a Weapon object using data provided in a dictionary.
        
        :param weapon_data: The `weapon_data` parameter is a dictionary containing information about a
        weapon. The keys in the dictionary represent different attributes of the weapon such as 'id',
        'name', 'type', 'manufacturer', 'caliber', 'magazineCapacity', 'fireRate', 'ammoCount', and
        optionally '
        :return: A Weapon object is being returned, created using the data provided in the `weapon_data`
        dictionary. The `Weapon` object is initialized with the values extracted from the `weapon_data`
        dictionary for attributes such as id, name, type, manufacturer, caliber, magazineCapacity,
        fireRate, ammoCount, and images.
        """
        return Weapon(weapon_data['id'], weapon_data['name'], weapon_data['type'],
                    weapon_data['manufacturer'], weapon_data['caliber'],
                    weapon_data['magazineCapacity'], weapon_data['fireRate'],
                    weapon_data['ammoCount'], weapon_data.get('images')) 

    def load_weapon(self, weapon_id):
        """
        This function loads a weapon by sending a GET request to a specific API endpoint and emits
        signals based on the response status.
        
        :param weapon_id: The `weapon_id` parameter is the unique identifier of the weapon that you want
        to load. It is used to make a request to the API endpoint to retrieve the data of the specific
        weapon with that ID
        """
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
        """
        The function `weapon_exists` checks if a weapon with a given ID exists by making a GET request
        to a specific API endpoint. 
        This function is called in the view for the functions load, update
        and delete weapon to ensure that the weapon exists before performing the operation.
        
        :param weapon_id: The `weapon_exists` method you provided is a function that checks if a weapon
        with a specific `weapon_id` exists by making a GET request to a local API endpoint. If the
        response status code is 200, it returns `True`, indicating that the weapon exists. If there is
        an error
        :return: The function `weapon_exists` returns a boolean value indicating whether a weapon with
        the specified `weapon_id` exists. It returns `True` if the HTTP response status code is 200
        (indicating success), and `False` if there is an error during the request or the weapon does not
        exist.
        """
        try:
            response = requests.get(f"http://localhost:5166/api/Weapon/{weapon_id}")
            return response.status_code == 200
        except Exception as e:
            print(f"An error occurred while checking weapon existence: {str(e)}")
            return False

    def load_all_weapons(self):
        """
        This function loads all weapons data from a specified API endpoint and emits signals based on
        the success or failure of the operation.
        """
        try:
            response = requests.get("http://localhost:5166/api/Weapon")
            if response.status_code == 200:
                weapons_data = response.json()
                weapons = [self.create_weapon_from_data(weapon_data) for weapon_data in weapons_data]  
                self.all_weapons_loaded.emit(weapons)
            else:
                self.error_occurred.emit(f"Failed to load weapons: {response.status_code}")
        except Exception as e:
            self.error_occurred.emit(f"An error occurred: {str(e)}")

    def add_weapon(self, weapon_data):
        """
        The function `add_weapon` sends a POST request to a specified API endpoint to add a new weapon
        and emits signals based on the response status.
        
        :param weapon_data: The `weapon_data` parameter is the data that contains information about the
        weapon to be added. This data should be in JSON format and include details such as the weapon's
        name, type, damage, etc. This data will be sent in the POST request to the specified API
        endpoint for adding a new
        """
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
        """
        This Python function sends a PUT request to update a weapon's data using the provided weapon ID
        and updated data.
        
        :param weapon_id: The `weapon_id` parameter in the `update_weapon` method is the unique
        identifier of the weapon that you want to update. It is used to specify which weapon's data
        should be updated in the API
        :param updated_weapon_data: The `update_weapon` method you provided is a function that sends a
        PUT request to update a weapon with the specified `weapon_id` using the `updated_weapon_data`.
        The `updated_weapon_data` parameter should be a dictionary containing the new data that you want
        to update for the weapon
        :return: The `update_weapon` method returns a boolean value indicating whether the weapon update
        was successful or not. It returns `True` if the response status code is either 200 or 204,
        indicating a successful update. If an exception occurs during the update process, it returns
        `False` after printing an error message.
        """
        try:
            response = requests.put(f"http://localhost:5166/api/Weapon/{weapon_id}", json=updated_weapon_data)
            return response.status_code in {200, 204}
        except Exception as e:
            print(f"An error occurred while updating weapon: {str(e)}")
            return False

    def load_weapon_details(self, weapon_id):
        """
        The function `load_weapon_details` sends a GET request to a specified API endpoint to retrieve
        weapon details based on the provided `weapon_id`.
        
        :param weapon_id: The `load_weapon_details` method is used to retrieve details of a weapon from
        a specific API endpoint based on the provided `weapon_id`. If the request is successful (status
        code 200), it parses the JSON response and creates a weapon object using the
        `create_weapon_from_data` method. If
        :return: The `load_weapon_details` method is returning the result of the
        `create_weapon_from_data` method, which is called with the `weapon_data` obtained from the API
        response.
        """
        try:
            response = requests.get(f"http://localhost:5166/api/Weapon/{weapon_id}")
            if response.status_code == 200:
                weapon_data = response.json()
                return self.create_weapon_from_data(weapon_data)  
            else:
                self.error_occurred.emit(f"Failed to load weapon details: {response.status_code}")
        except Exception as e:
            self.error_occurred.emit(f"An error occurred: {str(e)}")

    def delete_weapon(self, weapon_id):
        """
        The function `delete_weapon` sends a DELETE request to a specified API endpoint to delete a
        weapon by its ID, emitting signals based on the response status.
        
        :param weapon_id: The `delete_weapon` method takes a `weapon_id` as a parameter. This
        `weapon_id` is used to identify the specific weapon that needs to be deleted from the API. The
        method sends a DELETE request to the API endpoint with the specified `weapon_id` to delete the
        corresponding weapon
        """
        try:
            response = requests.delete(f"http://localhost:5166/api/Weapon/{weapon_id}")
            if response.status_code == 200:
                self.weapon_deleted.emit(weapon_id)
            else:
                self.error_occurred.emit(f"Failed to delete weapon: {response.status_code}")
        except Exception as e:
            self.error_occurred.emit(f"An error occurred: {str(e)}")

    def search_keyword(self, keyword):
        """
        The function `search_keyword` sends a request to a local API endpoint with a keyword parameter
        and emits signals based on the response status.
        
        :param keyword: The `search_keyword` method is a function that sends a GET request to a local
        API endpoint with a specific keyword parameter. The response is then checked, and if successful
        (status code 200), the content is emitted through the `keyword_founded` signal. If there is an
        error during the
        """
        try:
            response = requests.get(f"http://localhost:5166/api/Imagga/classify?keyword={keyword}")
            if response.status_code == 200:
                self.keyword_founded.emit(response.content.decode('utf-8'))
            else:
                self.error_occurred.emit(f"Failed to retrieve weapons: {response.status_code}")
        except Exception as e:
            self.error_occurred.emit(f"An error occurred: {str(e)}")

    def search_openai(self, prompt):
        """
        The function `search_openai` sends a POST request to an ASP.NET server with a prompt message and
        emits signals based on the response received.
        
        :param prompt: The `prompt` parameter in the `search_openai` function is the message or input
        that you want to send to the OpenAI model for generating a response. It is the text that you
        provide as an input to the OpenAI model to get a response or completion based on that input
        """
        
        # Prepare data with prompt
        data = {
            "Message": prompt
        }

        try:
            response = requests.post("http://localhost:5166/api/ChatGPT", json=data)
            if response.status_code == 200:
                result = response.json().get("response", "")
                self.openai_founded.emit(result)
            else:
                self.error_occurred.emit(f"OpenAI error: {response.status_code}")
        except Exception as e:
            self.error_occurred.emit(f"Server connection error: {str(e)}")