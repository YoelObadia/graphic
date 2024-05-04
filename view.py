import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QScrollArea, QMessageBox, QStackedLayout, QHBoxLayout, QGridLayout, QGroupBox, QTableWidgetItem
from PyQt5.QtCore import Qt
from presenter import WeaponPresenter
import qdarkstyle

class WeaponView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weapon Details")
        self.setGeometry(150, 150, 800, 600)

        self.presenter = WeaponPresenter()

        self.create_get_by_id_page()
        self.create_add_weapon_page()
        self.create_update_weapon_page()
        self.create_all_weapons_page()
        self.create_weapon_details_page()
        self.create_search_page()
        self.create_openai_page()

        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.get_by_id_widget)
        self.stacked_layout.addWidget(self.add_weapon_widget)
        self.stacked_layout.addWidget(self.update_weapon_widget)
        self.stacked_layout.addWidget(self.all_weapons_widget)
        self.stacked_layout.addWidget(self.weapon_details_widget)
        self.stacked_layout.addWidget(self.search_widget)
        self.stacked_layout.addWidget(self.openai_widget)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.central_widget)

        self.openai_button.clicked.connect(self.openai)
        self.load_button.clicked.connect(self.load_weapon)
        self.load_all_button.clicked.connect(self.load_all_weapons)
        self.add_button.clicked.connect(self.show_add_weapon_page)
        self.update_button.clicked.connect(self.show_update_weapon_page)
        self.save_button.clicked.connect(self.add_weapon)
        self.delete_button.clicked.connect(self.delete_weapon)
        self.update_save_button.clicked.connect(self.update_weapon)
        self.back_button_add.clicked.connect(self.show_get_by_id_page)
        self.back_button_update.clicked.connect(self.show_get_by_id_page)
        self.search_button.clicked.connect(self.search_keyword)
        self.presenter.weapon_loaded.connect(self.show_weapon_details_page)
        self.presenter.all_weapons_loaded.connect(self.show_all_weapons_page)
        self.presenter.error_occurred.connect(self.display_error)
        self.presenter.weapon_added.connect(self.display_weapon_added_message)
        self.presenter.weapon_deleted.connect(self.display_weapon_deleted_message)
        self.presenter.weapon_updated.connect(self.display_weapon_updated_message)
        self.presenter.keyword_founded.connect(self.show_search_page)
        self.presenter.openai_founded.connect(self.show_openai_page)

        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    def create_get_by_id_page(self):
        """
        Creates the 'Get by ID' page of the view.

        This method initializes the necessary widgets and layout for the 'Get by ID' page.
        It creates a QLineEdit for entering the weapon ID, QPushButton for various actions,
        QLabel for displaying weapon details, and a QTableWidget for displaying a table of weapons.

        Returns:
            None
        """
        self.get_by_id_widget = QWidget()  # Create the widget for this page
        main_layout = QVBoxLayout()  # Use a vertical layout

        # Group box for ID input and related actions
        id_groupbox = QGroupBox("Load, Update, Delete Weapon by ID")  # Title of the group box
        id_layout = QHBoxLayout()  # Use a horizontal layout
        
        self.weapon_id_input = QLineEdit()  # Input field for weapon ID
        self.weapon_id_input.setPlaceholderText("Enter Weapon ID")  # Placeholder text
        self.weapon_id_input.setToolTip("Enter the ID of the weapon to load, update, or delete.")  # Tooltip

        # Buttons for various actions
        self.load_button = QPushButton("Load")
        self.load_button.setToolTip("Load weapon details by ID.")  # Tooltip for the button
        self.update_button = QPushButton("Update")
        self.update_button.setToolTip("Update weapon details by ID.")  # Tooltip
        self.delete_button = QPushButton("Delete")
        self.delete_button.setToolTip("Delete weapon by ID.")  # Tooltip

        # Add widgets to the ID layout
        id_layout.addWidget(QLabel("Weapon ID:"))  # Label for the ID input
        id_layout.addWidget(self.weapon_id_input)  # Input field
        id_layout.addWidget(self.load_button)  # Load button
        id_layout.addWidget(self.update_button)  # Update button
        id_layout.addWidget(self.delete_button)  # Delete button

        id_groupbox.setLayout(id_layout)  # Set the layout for the group box

        # Group box for additional actions
        actions_groupbox = QGroupBox("Additional Actions")  # Title for the group box
        actions_layout = QVBoxLayout()  # Use a vertical layout
        
        self.add_button = QPushButton("Add Weapon")
        self.add_button.setToolTip("Add a new weapon to the system.")  # Tooltip for adding weapons
        self.load_all_button = QPushButton("Load All Weapons")
        self.load_all_button.setToolTip("Load all weapons in the system.")  # Tooltip for loading all weapons

        # Add buttons to the actions layout
        actions_layout.addWidget(self.add_button)
        actions_layout.addWidget(self.load_all_button)

        actions_groupbox.setLayout(actions_layout)  # Set the layout for the group box

        # Group box for keyword search and OpenAI interaction
        search_groupbox = QGroupBox("Search and OpenAI")  # Title for the group box
        search_layout = QVBoxLayout()  # Vertical layout for the search and OpenAI interaction
        
        self.keyword_input = QLineEdit()  # Keyword search input
        self.keyword_input.setPlaceholderText("Search by keyword")  # Placeholder text
        self.search_button = QPushButton("Search")  # Search button
        self.search_button.setToolTip("Search for weapons by keyword.")  # Tooltip

        self.prompt_input = QLineEdit()  # Input for OpenAI
        self.prompt_input.setPlaceholderText("Enter OpenAI prompt")  # Placeholder text
        self.openai_button = QPushButton("OpenAI")  # OpenAI button
        self.openai_button.setToolTip("Send a prompt to OpenAI.")  # Tooltip

        # Add widgets to the search layout
        search_layout.addWidget(QLabel("Search weapons by Keyword:"))  # Label for the keyword input
        search_layout.addWidget(self.keyword_input)  # Input field for keywords
        search_layout.addWidget(self.search_button)  # Search button
        search_layout.addWidget(QLabel("OpenAI:"))  # Label for OpenAI
        search_layout.addWidget(self.prompt_input)  # Input field for OpenAI
        search_layout.addWidget(self.openai_button)  # OpenAI button

        search_groupbox.setLayout(search_layout)  # Set the layout for the group box

        # Add the group boxes to the main layout
        main_layout.addWidget(id_groupbox)  # Group box for ID-related actions
        main_layout.addWidget(actions_groupbox)  # Group box for additional actions
        main_layout.addWidget(search_groupbox)  # Group box for search and OpenAI interaction

        # Set the layout for the 'Get by ID' widget
        self.get_by_id_widget.setLayout(main_layout)

    def show_get_by_id_page(self):
        self.weapon_id_input.clear()
        self.stacked_layout.setCurrentIndex(0)

    def display_error(self, error_message):
        print(f"Error: {error_message}")
        

# OpenAI region ------------------------------------------------

    def create_openai_page(self):
        self.openai_widget = QWidget()
        layout = QVBoxLayout()
        self.openai_widget.setLayout(layout)
        self.result_label = QLabel()
        layout.addWidget(self.result_label)
        back_to_main_button = QPushButton("Back to Main")
        layout.addWidget(back_to_main_button)
        back_to_main_button.clicked.connect(self.show_get_by_id_page)
        
    def openai(self):
        prompt = self.prompt_input.text()
        self.prompt_input.clear()
        self.presenter.search_openai(prompt)
    
    def show_openai_page(self, result):
        self.result_label.setText(result)
        self.stacked_layout.setCurrentIndex(6)


# Search region ------------------------------------------------

    def search_keyword(self):
        keyword = self.keyword_input.text()
        self.keyword_input.clear()
        self.presenter.search_keyword(keyword)

    def create_search_page(self):
        self.search_widget = QWidget()
        layout = QVBoxLayout()  # Disposition verticale
        self.search_widget.setLayout(layout)

        # Utilisation d'une zone de défilement pour afficher plusieurs armes
        self.result_scroll_area = QScrollArea()
        self.result_scroll_area.setWidgetResizable(True)  # Autoriser le redimensionnement
        self.result_widget = QWidget()  # Widget pour afficher les résultats
        self.result_layout = QVBoxLayout()  # Disposition des résultats
        self.result_widget.setLayout(self.result_layout)
        self.result_scroll_area.setWidget(self.result_widget)  # Ajouter le widget de résultats à la zone de défilement

        # Ajouter le résultat et le bouton de retour
        layout.addWidget(self.result_scroll_area)
        back_to_main_button = QPushButton("Back to Main")
        layout.addWidget(back_to_main_button)
        back_to_main_button.clicked.connect(self.show_get_by_id_page)  # Retour à la page principale

    def show_search_page(self, result):
        try:
            # Effacer le layout actuel
            for i in reversed(range(self.result_layout.count())):
                self.result_layout.itemAt(i).widget().deleteLater()

            # Convertir le JSON reçu en liste d'armes
            weapons_list = json.loads(result)

            # Pour chaque arme, créer un label avec ses détails
            for weapon in weapons_list:
                # Construire une chaîne de texte avec tous les attributs
                weapon_info = "<b>Weapon Details:</b><br>"
                for key, value in weapon.items():
                    weapon_info += f"<b>{key}:</b> {value}<br>"

                # Créer un label avec tous les détails
                weapon_label = QLabel()
                weapon_label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # Permet de sélectionner le texte
                weapon_label.setText(weapon_info)

                # Ajouter le label au layout
                self.result_layout.addWidget(weapon_label)

            # Afficher la page de recherche
            self.stacked_layout.setCurrentIndex(5)
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            error_label = QLabel(error_message)
            self.result_layout.addWidget(error_label)
    
# Add region ------------------------------------------------
    def create_add_weapon_page(self):
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
        self.back_button_add = QPushButton("Back")

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
        self.weapon_id_input.clear()
        self.stacked_layout.setCurrentIndex(1)

    def add_weapon(self):
        """
        Adds a new weapon to the view.

        Retrieves the weapon data from the input fields and passes it to the presenter
        to add the weapon. After adding the weapon, it clears the input fields and
        switches the current index of the stacked layout to 0.

        Returns:
            None
        """
        new_weapon_data = {
            "Name": self.name_input.text(),
            "Type": self.type_input.text(),
            "Manufacturer": self.manufacturer_input.text(),
            "Caliber": self.caliber_input.text(),
            "MagazineCapacity": int(self.magazine_capacity_input.text()),
            "FireRate": int(self.fire_rate_input.text()),
            "AmmoCount": int(self.ammo_count_input.text()),
            "Images": self.images_input.text()  # Ajout des images
        }
        self.presenter.add_weapon(new_weapon_data)
        self.clear_add_weapon_fields()
        self.stacked_layout.setCurrentIndex(0)

    def clear_add_weapon_fields(self):
        self.name_input.clear()
        self.type_input.clear()
        self.manufacturer_input.clear()
        self.caliber_input.clear()
        self.magazine_capacity_input.clear()
        self.fire_rate_input.clear()
        self.ammo_count_input.clear()
        self.images_input.clear()  # Nettoyer le champ des images

    def display_weapon_added_message(self, weapon_id):
        QMessageBox.information(self, 'Success', f"Weapon added successfully with ID: {weapon_id}")


# Update region ------------------------------------------------
    def create_update_weapon_page(self):
        self.update_name_input = QLineEdit()
        self.update_type_input = QLineEdit()
        self.update_manufacturer_input = QLineEdit()
        self.update_caliber_input = QLineEdit()
        self.update_magazine_capacity_input = QLineEdit()
        self.update_fire_rate_input = QLineEdit()
        self.update_ammo_count_input = QLineEdit()
        self.update_images_input = QLineEdit()  # Ajout du champ Images pour la mise à jour
        self.update_save_button = QPushButton("Update")
        self.back_button_update = QPushButton("Back")

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
        layout.addWidget(QLabel("Images:"))  # Ajout du label pour Images
        layout.addWidget(self.update_images_input)  # Ajout du champ Images pour la mise à jour
        layout.addWidget(self.update_save_button)
        layout.addWidget(self.back_button_update)

        self.update_weapon_widget = QWidget()
        self.update_weapon_widget.setLayout(layout)

    def show_update_weapon_page(self):
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
        self.update_name_input.setText(weapon_details.Name)
        self.update_type_input.setText(weapon_details.Type)
        self.update_manufacturer_input.setText(weapon_details.Manufacturer)
        self.update_caliber_input.setText(weapon_details.Caliber)
        self.update_magazine_capacity_input.setText(str(weapon_details.MagazineCapacity))
        self.update_fire_rate_input.setText(str(weapon_details.FireRate))
        self.update_ammo_count_input.setText(str(weapon_details.AmmoCount))
        self.update_images_input.setText(weapon_details.Images)  # Remplir le champ Images

    def update_weapon(self):  
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
            "Images": self.update_images_input.text()  # Ajout des images pour la mise à jour
        }
        self.presenter.update_weapon(int(weapon_id), updated_weapon_data)
        self.clear_update_weapon_fields()
        self.stacked_layout.setCurrentIndex(0)

    def clear_update_weapon_fields(self):
        self.update_name_input.clear()
        self.update_type_input.clear()
        self.update_manufacturer_input.clear()
        self.update_caliber_input.clear()
        self.update_magazine_capacity_input.clear()
        self.update_fire_rate_input.clear()
        self.update_ammo_count_input.clear()
        self.update_images_input.clear()  # Nettoyer le champ des images

    def display_weapon_updated_message(self, weapon_id):
        QMessageBox.information(self, 'Success', f"Weapon updated successfully with ID: {weapon_id}")


# Load all region ------------------------------------------------
    def create_all_weapons_page(self):
        """
        Creates the page to display all loaded weapons with a grid layout and a scroll area.
        """
        self.all_weapons_widget = QWidget()

        # Scroll area for displaying all weapons
        self.scroll_area = QScrollArea()  # Permet l'ajout de barres de défilement
        self.scroll_area.setWidgetResizable(True)  # Autorise le redimensionnement du widget interne

        # Widget pour le contenu du scroll area
        self.scroll_content_widget = QWidget()  # Widget contenant le layout avec des lignes et des colonnes
        self.scroll_layout = QGridLayout()  # Grid layout pour organiser les armes

        # Disposition pour la page des armes
        layout = QVBoxLayout()  # Disposition verticale pour tout contenir
        layout.addWidget(self.scroll_area)  # Ajouter le scroll area

        # Bouton de retour
        self.back_button_all_weapons = QPushButton("Back")
        layout.addWidget(self.back_button_all_weapons, alignment=Qt.AlignCenter)  # Bouton de retour aligné au centre
        self.back_button_all_weapons.clicked.connect(self.show_get_by_id_page)  # Retour à la page 'Get by ID'

        # Mise en place du scroll content widget avec son layout
        self.scroll_content_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content_widget)  # Assignation du widget de contenu au scroll area

        # Appliquer la disposition principale au widget
        self.all_weapons_widget.setLayout(layout)

    def show_all_weapons_page(self, weapons):
        """
        Displays all loaded weapons in the all weapons page using a grid layout.
        """
        self.stacked_layout.setCurrentIndex(3)  # Index de la page des armes

        # Nettoyer le layout pour éviter la duplication de widgets
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().deleteLater()

        # Ajouter les armes au grid layout
        for index, weapon in enumerate(weapons):
            # Créer des étiquettes pour chaque attribut
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
                f"<b>Images:</b> {weapon.Images}<br>"
            )
            weapon_label.setText(weapon_text)
            weapon_label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # Pour sélectionner le texte

            # Placement dans le grid layout (colonnes de 2 armes par ligne)
            row = index // 2  # Ligne
            col = index % 2  # Colonne
            self.scroll_layout.addWidget(weapon_label, row, col)  # Ajout au layout


    def load_all_weapons(self):
        self.presenter.load_all_weapons()


# Load region ------------------------------------------------
    def load_weapon(self):
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
        details_text = "<h2>Weapon Details</h2>"
        details_text += f"<b>ID:</b> {weapon.Id}<br>"
        details_text += f"<b>Name:</b> {weapon.Name}<br>"
        details_text += f"<b>Type:</b> {weapon.Type}<br>"
        details_text += f"<b>Manufacturer:</b> {weapon.Manufacturer}<br>"
        details_text += f"<b>Caliber:</b> {weapon.Caliber}<br>"
        details_text += f"<b>Magazine Capacity:</b> {weapon.MagazineCapacity}<br>"
        details_text += f"<b>Fire Rate:</b> {weapon.FireRate}<br>"
        details_text += f"<b>Ammo Count:</b> {weapon.AmmoCount}<br>"
        details_text += f"<b>Images:</b> {weapon.Images}<br>"  # Afficher les images
        self.weapon_details_label.setText(details_text)

    def create_weapon_details_page(self):
        """
        Creates the page to display weapon details.
        """
        self.weapon_details_widget = QWidget()

        # Widgets for displaying weapon details
        self.weapon_details_label = QLabel()
        self.back_button = QPushButton("Back")

        # Layout for the weapon details page
        layout = QVBoxLayout()
        layout.addWidget(self.weapon_details_label)
        layout.addWidget(self.back_button, alignment=Qt.AlignCenter)  # Align the back button to the center

        # Set the layout for the widget
        self.weapon_details_widget.setLayout(layout)

        # Connect the back button to the method to return to the 'Get by ID' page
        self.back_button.clicked.connect(self.show_get_by_id_page)


# Delete region ------------------------------------------------
    def delete_weapon(self):
        weapon_id = self.weapon_id_input.text()
        if not weapon_id or weapon_id.isdigit() is False:
            QMessageBox.warning(self, 'Error', "Please enter a valid weapon ID.")
            self.weapon_id_input.clear()
            return
        if not self.presenter.weapon_exists(int(weapon_id)):
            QMessageBox.warning(self, 'Error', f"Weapon with ID {weapon_id} does not exist.")
            self.weapon_id_input.clear()
            return
        # Obtenir les détails de l'arme pour afficher dans le message
        if (weapon_details := self.presenter.load_weapon_details(int(weapon_id))):
            details_text = "\n".join([f"{attribute}: {value}" for attribute, value in weapon_details.__dict__.items()])
            confirmation = QMessageBox.question(self, 'Confirmation', f"Do you want to delete the following weapon?\n\n{details_text}", QMessageBox.Yes | QMessageBox.No)
            if confirmation == QMessageBox.Yes:
                self.presenter.delete_weapon(int(weapon_id))
        self.weapon_id_input.clear()

    def display_weapon_deleted_message(self, weapon_id):
        QMessageBox.information(self, 'Success', f"Weapon deleted successfully with ID: {weapon_id}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    view = WeaponView()
    view.show()
    sys.exit(app.exec_())
