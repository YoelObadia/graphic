import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QTableWidgetItem, QMessageBox, QStackedLayout
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

        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.get_by_id_widget)
        self.stacked_layout.addWidget(self.add_weapon_widget)
        self.stacked_layout.addWidget(self.update_weapon_widget)
        self.stacked_layout.addWidget(self.all_weapons_widget)
        self.stacked_layout.addWidget(self.weapon_details_widget)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.central_widget)

        self.load_button.clicked.connect(self.load_weapon)
        self.load_all_button.clicked.connect(self.load_all_weapons)
        self.add_button.clicked.connect(self.show_add_weapon_page)
        self.update_button.clicked.connect(self.show_update_weapon_page)
        self.save_button.clicked.connect(self.add_weapon)
        self.delete_button.clicked.connect(self.delete_weapon)
        self.update_save_button.clicked.connect(self.update_weapon)
        self.back_button_add.clicked.connect(self.show_get_by_id_page)
        self.back_button_update.clicked.connect(self.show_get_by_id_page)
        self.presenter.weapon_loaded.connect(self.show_weapon_details_page)
        self.presenter.all_weapons_loaded.connect(self.show_all_weapons_page)
        self.presenter.error_occurred.connect(self.display_error)
        self.presenter.weapon_added.connect(self.display_weapon_added_message)
        self.presenter.weapon_deleted.connect(self.display_weapon_deleted_message)
        self.presenter.weapon_updated.connect(self.display_weapon_updated_message)

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
        self.weapon_id_input = QLineEdit()
        self.load_button = QPushButton("Load Weapon")
        self.add_button = QPushButton("Add Weapon")
        self.load_all_button = QPushButton("Load All Weapons")
        self.update_button = QPushButton("Update Weapon")
        self.delete_button = QPushButton("Delete Weapon")

        layout = QVBoxLayout()
        layout.addWidget(self.weapon_id_input)
        layout.addWidget(self.load_button)
        layout.addWidget(self.add_button)
        layout.addWidget(self.load_all_button)
        layout.addWidget(self.update_button)
        layout.addWidget(self.delete_button)

        self.get_by_id_widget = QWidget()
        self.get_by_id_widget.setLayout(layout)

    def show_get_by_id_page(self):
        self.weapon_id_input.clear()
        self.stacked_layout.setCurrentIndex(0)

    def display_error(self, error_message):
        print(f"Error: {error_message}")


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
            "AmmoCount": int(self.ammo_count_input.text())
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

    def display_weapon_added_message(self, weapon_id):
        QMessageBox.information(self, 'Success', f"Weapon added successfully with ID: {weapon_id}")



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

        # Set the text to the label to display the details
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



# Load all region ------------------------------------------------
    def create_all_weapons_page(self):
        """
        Creates the page to display all loaded weapons.
        """
        self.all_weapons_widget = QWidget()

        # Widgets for displaying all loaded weapons
        self.all_weapons_label = QLabel()
        self.back_button_all_weapons = QPushButton("Back")

        # Layout for the all weapons page
        layout = QVBoxLayout()
        layout.addWidget(self.all_weapons_label)
        layout.addWidget(self.back_button_all_weapons, alignment=Qt.AlignCenter)  # Align the back button to the center

        # Set the layout for the widget
        self.all_weapons_widget.setLayout(layout)

        # Connect the back button to the method to return to the 'Get by ID' page
        self.back_button_all_weapons.clicked.connect(self.show_get_by_id_page)

    def show_all_weapons_page(self, weapons):
        """
        Displays all loaded weapons in the all weapons page.
        """
        self.stacked_layout.setCurrentIndex(3)  # Index of the all weapons page

        # Construct the text to display all loaded weapons
        weapons_text = "<h2>All Loaded Weapons</h2>"
        for weapon in weapons:
            weapons_text += f"<b>ID:</b> {weapon.Id}<br>"
            weapons_text += f"<b>Name:</b> {weapon.Name}<br>"
            weapons_text += f"<b>Type:</b> {weapon.Type}<br>"
            weapons_text += f"<b>Manufacturer:</b> {weapon.Manufacturer}<br>"
            weapons_text += f"<b>Caliber:</b> {weapon.Caliber}<br>"
            weapons_text += f"<b>Magazine Capacity:</b> {weapon.MagazineCapacity}<br>"
            weapons_text += f"<b>Fire Rate:</b> {weapon.FireRate}<br>"
            weapons_text += f"<b>Ammo Count:</b> {weapon.AmmoCount}<br>"
            weapons_text += "<hr>"  # Add a horizontal line between weapons

        # Set the text to the label to display all loaded weapons
        self.all_weapons_label.setText(weapons_text)

    def load_all_weapons(self):
        self.presenter.load_all_weapons()

    #def display_all_weapons_table(self, weapons):
    #    self.table.setRowCount(len(weapons))
    #    self.table.setColumnCount(8)
    #    self.table.setHorizontalHeaderLabels(["ID", "Name", "Type", "Manufacturer", "Caliber", "Magazine Capacity", "Fire Rate", "Ammo Count"])
    #    for row, weapon in enumerate(weapons):
    #        self.set_table_item_values(row, weapon)
#
    #def set_table_item_values(self, row, weapon):
    #    self.set_table_item(row, 0, str(weapon.Id))
    #    self.set_table_item(row, 1, weapon.Name)
    #    self.set_table_item(row, 2, weapon.Type)
    #    self.set_table_item(row, 3, weapon.Manufacturer)
    #    self.set_table_item(row, 4, weapon.Caliber)
    #    self.set_table_item(row, 5, str(weapon.MagazineCapacity))
    #    self.set_table_item(row, 6, str(weapon.FireRate))
    #    self.set_table_item(row, 7, str(weapon.AmmoCount))
#
    #def set_table_item(self, row, column, value):
    #    self.table.setItem(row, column, QTableWidgetItem(value))



# Update region ------------------------------------------------
    def create_update_weapon_page(self):
        self.update_name_input = QLineEdit()
        self.update_type_input = QLineEdit()
        self.update_manufacturer_input = QLineEdit()
        self.update_caliber_input = QLineEdit()
        self.update_magazine_capacity_input = QLineEdit()
        self.update_fire_rate_input = QLineEdit()
        self.update_ammo_count_input = QLineEdit()
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
            "AmmoCount": int(self.update_ammo_count_input.text())
        }
        success = self.presenter.update_weapon(int(weapon_id), updated_weapon_data)
        #if success:
        #    QMessageBox.information(self, 'Success', f"Weapon updated successfully with ID: {weapon_id}")
        #else:
        #    QMessageBox.warning(self, 'Error', f"Failed to update weapon with ID: {weapon_id}")
        self.clear_update_weapon_fields()
        self.stacked_layout.setCurrentIndex(0)

    def update_weapon_details(self, weapon):
        details_text = f"Id:{weapon.Id} \nName: {weapon.Name}\nType: {weapon.Type}\nManufacturer: {weapon.Manufacturer}\nCaliber: {weapon.Caliber}\nMagazine Capacity: {weapon.MagazineCapacity}\nFire Rate: {weapon.FireRate}\nAmmo Count: {weapon.AmmoCount}"
        self.weapon_details_label.setText(details_text)

    def clear_update_weapon_fields(self):
        self.update_name_input.clear()
        self.update_type_input.clear()
        self.update_manufacturer_input.clear()
        self.update_caliber_input.clear()
        self.update_magazine_capacity_input.clear()
        self.update_fire_rate_input.clear()
        self.update_ammo_count_input.clear()

    def display_weapon_updated_message(self, weapon_id):
        QMessageBox.information(self, 'Success', f"Weapon updated successfully with ID: {weapon_id}")



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
