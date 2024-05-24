import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QScrollArea, QMessageBox, QStackedLayout, QHBoxLayout, QGridLayout, QGroupBox
from PyQt5.QtCore import Qt
from presenter import WeaponPresenter
import qdarkstyle

# The class `MyWidgetClass` defines a button style using CSS-like syntax for a QPushButton in PyQt.
class MyWidgetClass:
    
    button_style = """
    QPushButton {
        background-color: qlineargradient(
            spread:pad, x1:0, y1:0, x2:0, y2:1,
            stop:0 #4C4C4C, stop:1 #2C2C2C
        );  
        color: white; 
        border: 2px solid #5C5C5C;  
        border-radius: 5px;  
        padding: 5px 10px; 
        font-size: 14pt; 
    }

    QPushButton:hover {
        background-color: qlineargradient(
            spread:pad, x1:0, y1:0, x2:0, y2:1,
            stop:0 #6C6C6C, stop:1 #4C4C4C
        );  
        border: 2px solid white;  
    }

    QPushButton:pressed {
        background-color: qlineargradient(
            spread:pad, x1:0, y1:0, x2:0, y2:1,
            stop:0 #8C8C8C, stop:1 #6C6C6C
        );  
    }
    """

# The `WeaponView` class in Python represents a GUI application for managing weapon details, including
# functionalities for adding, updating, deleting, searching, and displaying weapons, as well as
# interacting with OpenAI ou Imagga.
class WeaponView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weapon Details")
        self.setGeometry(150, 150, 1400, 800)

        self.presenter = WeaponPresenter()

        # The above code appears to be a Python script that is calling several functions to create
        # different pages related to weapons. These functions include creating pages for getting a
        # weapon by its ID, adding a new weapon, updating a weapon, displaying all weapons, showing
        # details of a specific weapon, searching for weapons, and an OpenAI page.
        self.create_main_page()
        self.create_add_weapon_page()
        self.create_update_weapon_page()
        self.create_all_weapons_page()
        self.create_weapon_details_page()
        self.create_search_page()
        self.create_openai_page()

        # The above code in Python is creating a `QStackedLayout` object and adding several widgets to
        # it. These widgets include `main_widget`, `add_weapon_widget`, `update_weapon_widget`,
        # `all_weapons_widget`, `weapon_details_widget`, `search_widget`, and `openai_widget`. By
        # adding these widgets to the `QStackedLayout`, it allows for switching between these widgets
        # within a single layout, displaying only one widget at a time while hiding the others.
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.main_widget)
        self.stacked_layout.addWidget(self.add_weapon_widget)
        self.stacked_layout.addWidget(self.update_weapon_widget)
        self.stacked_layout.addWidget(self.all_weapons_widget)
        self.stacked_layout.addWidget(self.weapon_details_widget)
        self.stacked_layout.addWidget(self.search_widget)
        self.stacked_layout.addWidget(self.openai_widget)

        # The above code snippet is creating a QWidget instance called `central_widget`, setting its
        # layout to `stacked_layout`, and then setting this `central_widget` as the central widget of
        # the current window or application using `setCentralWidget`. 
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.central_widget)

        # The above code snippet is connecting various buttons in a graphical user interface (GUI) to
        # different functions or methods in the program. Each button is connected to a specific action 
        # using the `clicked.connect()` method. Here is a summary of what each button is connected to:
        
        # OpenAI search
        self.openai_button.clicked.connect(self.openai)
        self.presenter.openai_founded.connect(self.show_openai_page)
        
        # Imagga search by keyword
        self.search_button.clicked.connect(self.search_keyword)
        self.presenter.keyword_founded.connect(self.show_search_page)
        
        # Load weapon by ID
        self.load_button.clicked.connect(self.load_weapon)
        self.presenter.weapon_loaded.connect(self.show_weapon_details_page)
        
        # Load all weapons database
        self.load_all_button.clicked.connect(self.load_all_weapons)
        self.presenter.all_weapons_loaded.connect(self.show_all_weapons_page)
        
        # Add weapon to database
        self.add_button.clicked.connect(self.show_add_weapon_page)
        self.back_button_add.clicked.connect(self.show_main_page)
        self.save_button.clicked.connect(self.add_weapon)
        self.presenter.weapon_added.connect(self.display_weapon_added_message)
        
        # Update weapon by ID
        self.update_button.clicked.connect(self.show_update_weapon_page)
        self.update_save_button.clicked.connect(self.update_weapon)
        self.back_button_update.clicked.connect(self.show_main_page)
        self.presenter.weapon_updated.connect(self.display_weapon_updated_message)
        
        # Delete weapon by ID
        self.delete_button.clicked.connect(self.delete_weapon)
        self.presenter.weapon_deleted.connect(self.display_weapon_deleted_message)
        
        # Error message if invalid or empty ID entered
        self.presenter.error_occurred.connect(self.display_error)

        # The code is setting the stylesheet of a PyQt5 application to use a dark theme provided by
        # the qdarkstyle library.
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        
        

    def create_main_page(self):
        """
        The function creates a 'Get by ID' page with input fields, buttons, and group boxes for loading,
        updating, deleting weapons by ID, additional actions, and searching with OpenAI interaction.
        """
        
        # Create the widget for this page
        self.main_widget = QWidget()  
        main_layout = QVBoxLayout()  # Use a vertical layout for the main structure

        # Group box for ID input and related actions
        id_groupbox = QGroupBox("Load, Update, Delete Weapon by ID")  
        id_layout = QHBoxLayout()  # Horizontal layout for ID input and buttons

        # Input field for weapon ID
        self.weapon_id_input = QLineEdit()  
        self.weapon_id_input.setPlaceholderText("Enter Weapon ID")
        self.weapon_id_input.setToolTip("Enter the ID of the weapon to load, update, or delete.")

        # Create buttons with the custom style
        self.load_button = QPushButton("Load")  
        self.load_button.setToolTip("Load weapon details by ID.")  
        self.load_button.setStyleSheet(MyWidgetClass.button_style)  

        self.update_button = QPushButton("Update")  
        self.update_button.setToolTip("Update weapon details by ID.")  
        self.update_button.setStyleSheet(MyWidgetClass.button_style)  

        self.delete_button = QPushButton("Delete")  
        self.delete_button.setToolTip("Delete weapon by ID.")  
        self.delete_button.setStyleSheet(MyWidgetClass.button_style)  

        # Add widgets to the ID layout
        id_layout.addWidget(QLabel("Weapon ID:"))  # Label for ID
        id_layout.addWidget(self.weapon_id_input)  # Input field
        id_layout.addWidget(self.load_button)      # Load button
        id_layout.addWidget(self.update_button)    # Update button
        id_layout.addWidget(self.delete_button)    # Delete button

        id_groupbox.setLayout(id_layout)  # Set the layout for the group box

        # Group box for additional actions
        actions_groupbox = QGroupBox("Additional Actions")  
        actions_layout = QVBoxLayout()  # Vertical layout for the additional actions

        self.add_button = QPushButton("Add Weapon")  
        self.add_button.setToolTip("Add a new weapon to the system.")  
        self.add_button.setStyleSheet(MyWidgetClass.button_style)  

        self.load_all_button = QPushButton("Load All Weapons")  
        self.load_all_button.setToolTip("Load all weapons in the system.")  
        self.load_all_button.setStyleSheet(MyWidgetClass.button_style)  

        # Add buttons to the actions layout
        actions_layout.addWidget(self.add_button)  # Add Weapon button
        actions_layout.addWidget(self.load_all_button)  # Load All Weapons button

        actions_groupbox.setLayout(actions_layout)  # Apply the layout for the group box

        # Group box for keyword search and OpenAI interaction
        search_groupbox = QGroupBox("Search and OpenAI")  
        search_layout = QVBoxLayout()  # Vertical layout

        self.keyword_input = QLineEdit()  
        self.keyword_input.setPlaceholderText("Search by keyword")
        self.search_button = QPushButton("Search")  
        self.search_button.setToolTip("Search for weapons by keyword.")  
        self.search_button.setStyleSheet(MyWidgetClass.button_style)  

        self.prompt_input = QLineEdit()  
        self.prompt_input.setPlaceholderText("Enter OpenAI prompt")
        self.openai_button = QPushButton("OpenAI")  
        self.openai_button.setToolTip("Send a prompt to OpenAI.")  
        self.openai_button.setStyleSheet(MyWidgetClass.button_style)  

        # Add widgets to the search layout
        search_layout.addWidget(QLabel("Search weapons by Keyword:"))  
        search_layout.addWidget(self.keyword_input)  # Keyword input field
        search_layout.addWidget(self.search_button)  # Search button
        
        search_layout.addWidget(QLabel("OpenAI:"))  
        search_layout.addWidget(self.prompt_input)   # OpenAI input field
        search_layout.addWidget(self.openai_button)  # OpenAI button

        search_groupbox.setLayout(search_layout)  # Apply the layout for the group box

        # Add the group boxes to the main layout
        main_layout.addWidget(id_groupbox)  
        main_layout.addWidget(actions_groupbox)  
        main_layout.addWidget(search_groupbox)  # Group box for search and OpenAI

        # Set the layout for the 'Main' widget
        self.main_widget.setLayout(main_layout)  # Apply the layout

    def show_main_page(self):
        """
        The function `show_main_page` clears the weapon ID input and sets the current index of the
        stacked layout to 0.
        """
        self.weapon_id_input.clear()
        self.stacked_layout.setCurrentIndex(0)

    def display_error(self, error_message):
        """
        The function `display_error` prints an error message with a specific format.
        
        :param error_message: The `error_message` parameter is a string that contains the message
        describing the error that occurred
        """
        print(f"Error: {error_message}")
        

# OpenAI region ------------------------------------------------

    def create_openai_page(self):
        """
        The function creates a page with a result label and a button to go back to the main page.
        """
        
        # Create the widget for this page
        self.openai_widget = QWidget()
        layout = QVBoxLayout()
        self.openai_widget.setLayout(layout)
        self.result_label = QLabel()
        layout.addWidget(self.result_label)
        back_to_main_button = QPushButton("Back to Main")
        back_to_main_button.setStyleSheet(MyWidgetClass.button_style)
        layout.addWidget(back_to_main_button)
        back_to_main_button.clicked.connect(self.show_main_page)
        
    def openai(self):
        """
        This Python function takes user input, clears the input field, and then searches OpenAI using
        the input as a prompt.
        """
        prompt = self.prompt_input.text()
        self.prompt_input.clear()
        self.presenter.search_openai(prompt)
    
    def show_openai_page(self, result):
        """
        This Python function updates the text of a label and changes the current index of a stacked
        layout in a GUI application.
        
        :param result: The `result` parameter in the `show_openai_page` method likely contains the
        content or data that you want to display on the OpenAI page. This method sets the text of the
        `result_label` widget to the content provided in the `result` parameter and then switches the
        current index of
        """
        self.result_label.setText(result)
        self.stacked_layout.setCurrentIndex(6)


# Search region ------------------------------------------------

    def search_keyword(self):
        """
        The `search_keyword` function in Python clears the input field, retrieves the keyword, and then
        searches for that keyword using a presenter.
        """
        keyword = self.keyword_input.text()
        self.keyword_input.clear()
        self.presenter.search_keyword(keyword)

    def create_search_page(self):
        """
        The function creates a search page with a scrollable area to display search results and a button
        to go back to the main page.
        """
        self.search_widget = QWidget()
        layout = QVBoxLayout()  # Disposition verticale
        self.search_widget.setLayout(layout)

        # Create a scroll area to display search results
        self.result_scroll_area = QScrollArea()
        # The widget will adjust its size automatically to fit its contents,
        # allowing for dynamic resizing based on the content within it.
        self.result_scroll_area.setWidgetResizable(True) 
        self.result_widget = QWidget()  # Widget to display results
        self.result_layout = QVBoxLayout()  # Results display
        self.result_widget.setLayout(self.result_layout)
        self.result_scroll_area.setWidget(self.result_widget)  

        # Add result and back button
        layout.addWidget(self.result_scroll_area)
        back_to_main_button = QPushButton("Back to Main")
        back_to_main_button.setStyleSheet(MyWidgetClass.button_style)
        
        layout.addWidget(back_to_main_button)
        back_to_main_button.clicked.connect(self.show_main_page)  

    def show_search_page(self, result):
        """
        The function `show_search_page` displays search results in a PyQt application, handling JSON
        data and potential errors.
        
        :param result: The `result` parameter in the `show_search_page` method is expected to be a JSON
        string representing a dictionnary of weapons. This JSON string will be converted into a Python list of
        dictionaries where each dictionary represents the details of a weapon
        """
        try:
            # Reinitialize the page for avoiding doubles of prevous searches
            for i in reversed(range(self.result_layout.count())):
                self.result_layout.itemAt(i).widget().deleteLater()

            # Convert JSON into weapons dictionnary
            weapons_list = json.loads(result)

            for weapon in weapons_list:
                weapon_info = "<b>Weapon Details:</b><br>"
                for key, value in weapon.items():
                    weapon_info += f"<b>{key}:</b> {value}<br>"

                weapon_label = QLabel()
                weapon_label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # Allow to select text
                weapon_label.setText(weapon_info)

                # Add label to layout
                self.result_layout.addWidget(weapon_label)

            # Display search page
            self.stacked_layout.setCurrentIndex(5)
            
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            error_label = QLabel(error_message)
            self.result_layout.addWidget(error_label)
    
# Add region ------------------------------------------------
    def create_add_weapon_page(self):
        """
        The function `create_add_weapon_page` creates a GUI page for adding weapon information with
        input fields and buttons.
        """
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter weapon name")
        self.type_input = QLineEdit()
        self.type_input.setPlaceholderText("Enter weapon type")
        self.manufacturer_input = QLineEdit()
        self.manufacturer_input.setPlaceholderText("Enter manufacturer")
        self.caliber_input = QLineEdit()
        self.caliber_input.setPlaceholderText("Enter weapon caliber")
        self.magazine_capacity_input = QLineEdit()
        self.magazine_capacity_input.setPlaceholderText("Enter magazine capacity")
        self.fire_rate_input = QLineEdit()
        self.fire_rate_input.setPlaceholderText("Enter fire rate")
        self.ammo_count_input = QLineEdit()
        self.ammo_count_input.setPlaceholderText("Enter ammo count")
        self.images_input = QLineEdit()  
        self.images_input.setPlaceholderText("Enter images URL")
        self.save_button = QPushButton("Add")
        self.save_button.setStyleSheet(MyWidgetClass.button_style)  
        self.back_button_add = QPushButton("Back")
        self.back_button_add.setStyleSheet(MyWidgetClass.button_style)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Type:"))
        layout.addWidget(self.type_input)
        layout.addWidget(QLabel("Manufacturer:"))
        layout.addWidget(self.manufacturer_input)
        layout.addWidget(QLabel("Caliber:"))
        layout.addWidget(self.caliber_input)
        layout.addWidget(QLabel("Magazine Capacity:"))
        layout.addWidget(self.magazine_capacity_input)
        layout.addWidget(QLabel("Fire Rate:"))
        layout.addWidget(self.fire_rate_input)
        layout.addWidget(QLabel("Ammo Count:"))
        layout.addWidget(self.ammo_count_input)
        layout.addWidget(QLabel("Images:"))  
        layout.addWidget(self.images_input)  
        layout.addWidget(self.save_button)
        layout.addWidget(self.back_button_add)

        self.add_weapon_widget = QWidget()
        self.add_weapon_widget.setLayout(layout)

    def show_add_weapon_page(self):
        """
        This function clears the weapon ID input field and switches the current page to the "Add Weapon page.
        """
        self.weapon_id_input.clear()
        self.stacked_layout.setCurrentIndex(1)

    def add_weapon(self):
        """
        Adds a new weapon to the system.

        Validates the input fields and passes the weapon data to the presenter
        to add the weapon. If validation fails, displays a message box and 
        keeps the GUI running.

        Returns:
            None
        """
        # Validation checks for empty fields
        required_fields = {
            "Name": self.name_input.text(),
            "Type": self.type_input.text(),
            "Manufacturer": self.manufacturer_input.text(),
            "Caliber": self.caliber_input.text(),
            "Magazine Capacity": self.magazine_capacity_input.text(),
            "Fire Rate": self.fire_rate_input.text(),
            "Ammo Count": self.ammo_count_input.text(),
        }

        # Check if any required field is empty
        empty_fields = [key for key, value in required_fields.items() if not value.strip()]

        if empty_fields:
            # If there are empty fields, display a message box and exit the function
            QMessageBox.warning(self, 'Input Error', "Please fill all fields.")
            return  # Exit without adding the weapon

        # Ensure non-integer fields are properly converted to integers
        try:
            new_weapon_data = {
                "Name": self.name_input.text(),
                "Type": self.type_input.text(),
                "Manufacturer": self.manufacturer_input.text(),
                "Caliber": self.caliber_input.text(),
                "MagazineCapacity": int(self.magazine_capacity_input.text()),  # Convert to int
                "FireRate": int(self.fire_rate_input.text()),  # Convert to int
                "AmmoCount": int(self.ammo_count_input.text()),  # Convert to int
                "Images": self.images_input.text(),  
            }
            
        except ValueError:
            # If there's a conversion error, display a message box and exit the function
            QMessageBox.warning(self, 'Input Error', 'Magazine Capacity, Fire Rate, and Ammo Count must be valid integers.')
            return

        # If validation passes, add the weapon
        self.presenter.add_weapon(new_weapon_data)
        self.stacked_layout.setCurrentIndex(0)  # Return to the main page

    def display_weapon_added_message(self, weapon_id):
        """
        The function `display_weapon_added_message` displays a success message with the ID of the added
        weapon.
        
        :param weapon_id: The `weapon_id` parameter is the unique identifier or code assigned to a
        weapon that has been successfully added to a system or database. It is used to uniquely identify
        and reference the specific weapon within the system
        """
        QMessageBox.information(self, 'Success', f"Weapon added successfully with ID: {weapon_id}")


# Update region ------------------------------------------------
    def create_update_weapon_page(self):
        """
        The function creates a page for updating weapon information with input fields and buttons.
        """
        self.update_name_input = QLineEdit()
        self.update_type_input = QLineEdit()
        self.update_manufacturer_input = QLineEdit()
        self.update_caliber_input = QLineEdit()
        self.update_magazine_capacity_input = QLineEdit()
        self.update_fire_rate_input = QLineEdit()
        self.update_ammo_count_input = QLineEdit()
        self.update_images_input = QLineEdit()  # Ajout du champ Images pour la mise à jour
        self.update_save_button = QPushButton("Update")
        self.update_save_button.setStyleSheet(MyWidgetClass.button_style)
        self.back_button_update = QPushButton("Back")
        self.back_button_update.setStyleSheet(MyWidgetClass.button_style)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.update_name_input)
        layout.addWidget(QLabel("Type:"))
        layout.addWidget(self.update_type_input)
        layout.addWidget(QLabel("Manufacturer:"))
        layout.addWidget(self.update_manufacturer_input)
        layout.addWidget(QLabel("Caliber:"))
        layout.addWidget(self.update_caliber_input)
        layout.addWidget(QLabel("Magazine Capacity:"))
        layout.addWidget(self.update_magazine_capacity_input)
        layout.addWidget(QLabel("Fire Rate:"))
        layout.addWidget(self.update_fire_rate_input)
        layout.addWidget(QLabel("Ammo Count:"))
        layout.addWidget(self.update_ammo_count_input)
        layout.addWidget(QLabel("Images:"))  
        layout.addWidget(self.update_images_input)  
        layout.addWidget(self.update_save_button)
        layout.addWidget(self.back_button_update)

        self.update_weapon_widget = QWidget()
        self.update_weapon_widget.setLayout(layout)

    def show_update_weapon_page(self):
        """
        The function `show_update_weapon_page` validates a weapon ID input, checks if the weapon exists,
        loads weapon details for updating, and switches the current page to the update weapon page.
        :return: If the `weapon_id` is not valid or if the weapon with the provided ID does not exist, a
        QMessageBox warning is displayed, and the `weapon_id_input` field is cleared. If the weapon
        details are successfully loaded and the `fill_update_weapon_fields` method is called with the
        weapon details, the stacked layout is then set to display the update weapon page (index 2).
        """
        weapon_id = self.weapon_id_input.text()
        if not weapon_id or weapon_id.isdigit() is False:
            QMessageBox.warning(self, 'Error', "Please enter a valid weapon ID.")
            self.weapon_id_input.clear()
            return
        if not self.presenter.weapon_exists(int(weapon_id)):
            QMessageBox.warning(self, 'Error', f"Weapon with ID {weapon_id} does not exist.")
            self.weapon_id_input.clear()
            return
        # Load the weapon details to be updated
        if (weapon_details := self.presenter.load_weapon_details(int(weapon_id))):
            self.fill_update_weapon_fields(weapon_details)
        self.stacked_layout.setCurrentIndex(2)

    def fill_update_weapon_fields(self, weapon_details):
        """
        The function `fill_update_weapon_fields` updates the input fields with weapon details.
        
        :param weapon_details: The `fill_update_weapon_fields` method takes in a `weapon_details` object
        as a parameter. This object seems to have the following attributes:
        """
        self.update_name_input.setText(weapon_details.Name)
        self.update_type_input.setText(weapon_details.Type)
        self.update_manufacturer_input.setText(weapon_details.Manufacturer)
        self.update_caliber_input.setText(weapon_details.Caliber)
        self.update_magazine_capacity_input.setText(str(weapon_details.MagazineCapacity))
        self.update_fire_rate_input.setText(str(weapon_details.FireRate))
        self.update_ammo_count_input.setText(str(weapon_details.AmmoCount))
        self.update_images_input.setText(weapon_details.Images)  

    def update_weapon(self):  
        """
        The function `update_weapon` updates weapon data based on user input and then clears the input
        fields.
        """
        weapon_id = self.weapon_id_input.text()
        updated_weapon_data = {
            "Id": weapon_id,
            "Name": self.update_name_input.text(),
            "Type": self.update_type_input.text(),
            "Manufacturer": self.update_manufacturer_input.text(),
            "Caliber": self.update_caliber_input.text(),
            "MagazineCapacity": int(self.update_magazine_capacity_input.text()),
            "FireRate": int(self.update_fire_rate_input.text()),
            "AmmoCount": int(self.update_ammo_count_input.text()),
            "Images": self.update_images_input.text() 
        }
        self.presenter.update_weapon(int(weapon_id), updated_weapon_data)
        self.weapon_id_input.clear()
        self.stacked_layout.setCurrentIndex(0)

    def display_weapon_updated_message(self, weapon_id):
        """
        The function `display_weapon_updated_message` displays a success message with the updated weapon
        ID.
        
        :param weapon_id: The `weapon_id` parameter is the unique identifier or code that represents a
        specific weapon in the system. It is used to identify and update the specific weapon with the
        corresponding ID
        """
        QMessageBox.information(self, 'Success', f"Weapon updated successfully with ID: {weapon_id}")


# Load all region ------------------------------------------------
    def create_all_weapons_page(self):
        """
        Creates the page to display all loaded weapons with a grid layout and a scroll area.
        """
        self.all_weapons_widget = QWidget()

        # Scroll area for displaying all weapons
        self.scroll_area = QScrollArea() 
        self.scroll_area.setWidgetResizable(True)  

        # Widget for the content of the scroll area
        self.scroll_content_widget = QWidget()  
        self.scroll_layout = QGridLayout()  

        # Set the layout for the scroll content widget
        layout = QVBoxLayout() 
        layout.addWidget(self.scroll_area)  # Add scroll area

        # Back button
        self.back_button_all_weapons = QPushButton("Back")
        self.back_button_all_weapons.setStyleSheet(MyWidgetClass.button_style)
        layout.addWidget(self.back_button_all_weapons, alignment=Qt.AlignCenter)  # Center alignment
        
        # Return to main page
        self.back_button_all_weapons.clicked.connect(self.show_main_page)  

        # Set the layout for the scroll content widget
        self.scroll_content_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content_widget)  
        
        # The code is setting the layout `layout` for the widget `all_weapons_widget`
        self.all_weapons_widget.setLayout(layout)

    def show_all_weapons_page(self, weapons):
        """
        Displays all loaded weapons in the 'All Weapons' page using a single-column layout.
        """
        self.stacked_layout.setCurrentIndex(3)  # Switch to the 'All Weapons' page

        # Create a new vertical layout to avoid potential conflicts
        single_column_layout = QVBoxLayout()  

        # Iterate over the weapons and create labels for each
        for weapon in weapons:
            # Create a label with detailed information about each weapon
            weapon_label = QLabel()  
            weapon_text = (
                f"<b>ID:</b> {weapon.Id}<br>"
                f"<b>Name:</b> {weapon.Name}<br>"
                f"<b>Type:</b> {weapon.Type}<br>"
                f"<b>Manufacturer:</b> {weapon.Manufacturer}<br>"
                f"<b>Caliber:</b> {weapon.Caliber}<br>"
                f"<b>Magazine Capacity:</b> {weapon.MagazineCapacity}<br>"
                f"<b>Fire Rate:</b> {weapon.FireRate}<br>"
                f"<b>Ammo Count:</b> {weapon.AmmoCount}<br>"
                f"<b>Image URL:</b> {weapon.Images}<br>"
            )
            weapon_label.setText(weapon_text)  
            weapon_label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # Allow text selection

            # Add the label to the single-column layout
            single_column_layout.addWidget(weapon_label)  # Add the label to the layout

        # Recreate the scroll content widget to avoid conflicts
        self.scroll_content_widget = QWidget()  
        self.scroll_content_widget.setLayout(single_column_layout)  # Apply the new layout

        # Reassign the scroll content widget to the scroll area
        self.scroll_area.setWidget(self.scroll_content_widget)  # Set the new content widget

    def load_all_weapons(self):
        """
        The function `load_all_weapons` calls the `load_all_weapons` method of the `presenter` object.
        """
        self.presenter.load_all_weapons()


# Load region ------------------------------------------------
    def load_weapon(self):
        """
        The function `load_weapon` checks if a valid weapon ID is entered and loads the weapon if it
        exists.
        :return: If the weapon ID is not valid or if the weapon with the given ID does not exist, a
        QMessageBox warning is displayed and the weapon ID input field is cleared. In both cases, the
        function returns without further action. If a valid weapon ID is provided and the weapon exists,
        the function calls the `load_weapon` method of the presenter with the weapon ID as an argument.
        """
        weapon_id = self.weapon_id_input.text()
        if not weapon_id or weapon_id.isdigit() is False:
            QMessageBox.warning(self, 'Error', "Please enter a valid weapon ID.")
            self.weapon_id_input.clear()
            return
        if not self.presenter.weapon_exists(int(weapon_id)):
            QMessageBox.warning(self, 'Error', f"Weapon with ID {weapon_id} does not exist.")
            self.weapon_id_input.clear()
            return
        self.presenter.load_weapon(int(weapon_id))

    def show_weapon_details_page(self, weapon):
        """
        Displays the weapon details in the weapon details page.
        """
        self.stacked_layout.setCurrentIndex(4)  # Index of the weapon details page

        # Construct the text to display the weapon details
        details_text = (
        "<div align='center'>"
        "<h2>Weapon Details</h2>"
        f"<b>ID:</b> {weapon.Id}<br>"
        f"<b>Name:</b> {weapon.Name}<br>"
        f"<b>Type:</b> {weapon.Type}<br>"
        f"<b>Manufacturer:</b> {weapon.Manufacturer}<br>"
        f"<b>Caliber:</b> {weapon.Caliber}<br>"
        f"<b>Magazine Capacity:</b> {weapon.MagazineCapacity}<br>"
        f"<b>Fire Rate:</b> {weapon.FireRate}<br>"
        f"<b>Ammo Count:</b> {weapon.AmmoCount}<br>"
        f"<b>Image URL:</b> {weapon.Images}<br>"
        "</div>"
        )
        # Set the text to the label
        self.weapon_details_label.setText(details_text)

    def create_weapon_details_page(self):
        """
        Creates the page to display weapon details.
        """
        self.weapon_details_widget = QWidget()

        # Widgets for displaying weapon details
        self.weapon_details_label = QLabel()
        self.back_button = QPushButton("Back")
        self.back_button.setStyleSheet(MyWidgetClass.button_style)

        # Layout for the weapon details page
        layout = QVBoxLayout()
        layout.addWidget(self.weapon_details_label)
        layout.addWidget(self.back_button, alignment=Qt.AlignCenter)  # Align the back button to the center

        # Set the layout for the widget
        self.weapon_details_widget.setLayout(layout)

        # Connect the back button to the method to return to the 'Get by ID' page
        self.back_button.clicked.connect(self.show_main_page)


# Delete region ------------------------------------------------
    def delete_weapon(self):
        """
        The function `delete_weapon` in the provided Python code deletes a weapon based on the input
        weapon ID after confirming with the user.
        :return: The `delete_weapon` method returns after displaying a message box to confirm the
        deletion of a weapon. If the user confirms the deletion by clicking "Yes" in the message box,
        the method proceeds to delete the weapon using the `presenter.delete_weapon(int(weapon_id))`
        call. If the user clicks "No" or cancels the operation, the method does not delete the weapon
        and simply
        """
        weapon_id = self.weapon_id_input.text()
        if not weapon_id or weapon_id.isdigit() is False:
            QMessageBox.warning(self, 'Error', "Please enter a valid weapon ID.")
            self.weapon_id_input.clear()
            return
        if not self.presenter.weapon_exists(int(weapon_id)):
            QMessageBox.warning(self, 'Error', f"Weapon with ID {weapon_id} does not exist.")
            self.weapon_id_input.clear()
            return
        # Get the weapon details to display them in the message box
        if (weapon_details := self.presenter.load_weapon_details(int(weapon_id))):
            details_text = "\n".join([f"{attribute}: {value}" for attribute, value in weapon_details.__dict__.items()])
            confirmation = QMessageBox.question(self, 'Confirmation', f"Do you want to delete the following weapon?\n\n{details_text}", QMessageBox.Yes | QMessageBox.No)
            if confirmation == QMessageBox.Yes:
                self.presenter.delete_weapon(int(weapon_id))
        self.weapon_id_input.clear()

    def display_weapon_deleted_message(self, weapon_id):
        """
        The function `display_weapon_deleted_message` displays a success message indicating that a
        weapon has been deleted successfully with a specific ID.
        
        :param weapon_id: The `weapon_id` parameter is the unique identifier of the weapon that was
        deleted. It is used to display a message indicating that the weapon was deleted successfully
        along with its ID
        """
        QMessageBox.information(self, 'Success', f"Weapon deleted successfully with ID: {weapon_id}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    view = WeaponView()
    view.show()
    sys.exit(app.exec_())
