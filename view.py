import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QStackedLayout
from presenter import WeaponPresenter  # Supposons que vous avez déjà le présentateur

class WeaponView(QMainWindow):
    def __init__(self):
        """
        Initializes the view for Weapon Details.

        Sets the window title, geometry, and creates instances of the WeaponPresenter class.
        Creates the pages for getting weapon details, adding a weapon, and updating a weapon.
        Sets up the stacked layout to switch between pages.
        Connects button signals to their respective slots.
        Connects presenter signals to their respective slots.
        """
        super().__init__()
        self.setWindowTitle("Weapon Details")
        self.setGeometry(1500, 1500, 1000, 600)

        self.presenter = WeaponPresenter()

        self.create_get_by_id_page()
        self.create_add_weapon_page()
        self.create_update_weapon_page()

        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.get_by_id_widget)
        self.stacked_layout.addWidget(self.add_weapon_widget)
        self.stacked_layout.addWidget(self.update_weapon_widget)

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

        self.presenter.weapon_loaded.connect(self.update_weapon_details)
        self.presenter.all_weapons_loaded.connect(self.display_all_weapons_table)
        self.presenter.error_occurred.connect(self.display_error)
        self.presenter.weapon_added.connect(self.display_weapon_added_message)
        self.presenter.weapon_deleted.connect(self.display_weapon_deleted_message)
        self.presenter.weapon_updated.connect(self.display_weapon_updated_message)

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
        self.weapon_details_label = QLabel("Weapon Details:")
        self.table = QTableWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.weapon_id_input)
        layout.addWidget(self.load_button)
        layout.addWidget(self.add_button)
        layout.addWidget(self.load_all_button)
        layout.addWidget(self.update_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.weapon_details_label)
        layout.addWidget(self.table)

        self.get_by_id_widget = QWidget()
        self.get_by_id_widget.setLayout(layout)

    def validate_weapon_id(self, weapon_id):
        """
        Validates the given weapon ID.

        Args:
            weapon_id (int): The ID of the weapon to validate.

        Returns:
            bool: True if the weapon ID is valid, False otherwise.
        """
        if not weapon_id:
            self.display_error("Please enter a valid weapon ID.")
            return False
        try:
            weapon_id = int(weapon_id)
        except ValueError:
            self.display_error("Please enter a valid numeric weapon ID.")
            return False
        if self.presenter.weapon_exists(weapon_id):
            return True
        self.display_error(f"Weapon with ID {weapon_id} does not exist.")
        return False

    def display_error(self, error_message):
        print(f"Error: {error_message}")

    def create_add_weapon_page(self):
        self.name_input = QLineEdit()
        self.type_input = QLineEdit()
        self.manufacturer_input = QLineEdit()
        self.caliber_input = QLineEdit()
        self.magazine_capacity_input = QLineEdit()
        self.fire_rate_input = QLineEdit()
        self.ammo_count_input = QLineEdit()
        self.save_button = QPushButton("Add")

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

        self.add_weapon_widget = QWidget()
        self.add_weapon_widget.setLayout(layout)

    def show_add_weapon_page(self):
        self.stacked_layout.setCurrentIndex(1)

    def add_weapon(self):
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

    def load_weapon(self):
        weapon_id = self.weapon_id_input.text()
        if not weapon_id:
            self.display_error("Please enter a valid weapon ID.")
            return
        self.presenter.load_weapon(int(weapon_id))

    def load_all_weapons(self):
        self.presenter.load_all_weapons()

    def display_all_weapons_table(self, weapons):
        self.table.setRowCount(len(weapons))
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Type", "Manufacturer", "Caliber", "Magazine Capacity", "Fire Rate", "Ammo Count"])
        for row, weapon in enumerate(weapons):
            self.set_table_item_values(row, weapon)

    def set_table_item_values(self, row, weapon):
        self.set_table_item(row, 0, str(weapon.Id))
        self.set_table_item(row, 1, weapon.Name)
        self.set_table_item(row, 2, weapon.Type)
        self.set_table_item(row, 3, weapon.Manufacturer)
        self.set_table_item(row, 4, weapon.Caliber)
        self.set_table_item(row, 5, str(weapon.MagazineCapacity))
        self.set_table_item(row, 6, str(weapon.FireRate))
        self.set_table_item(row, 7, str(weapon.AmmoCount))

    def set_table_item(self, row, column, value):
        self.table.setItem(row, column, QTableWidgetItem(value))

    def create_update_weapon_page(self):
        self.update_name_input = QLineEdit()
        self.update_type_input = QLineEdit()
        self.update_manufacturer_input = QLineEdit()
        self.update_caliber_input = QLineEdit()
        self.update_magazine_capacity_input = QLineEdit()
        self.update_fire_rate_input = QLineEdit()
        self.update_ammo_count_input = QLineEdit()
        self.update_save_button = QPushButton("Update")

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

        self.update_weapon_widget = QWidget()
        self.update_weapon_widget.setLayout(layout)

    def show_update_weapon_page(self):
        weapon_id = self.weapon_id_input.text()
        if not self.validate_weapon_id(weapon_id):
            return
        # Chargez les détails de l'arme à mettre à jour
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
            "Id": weapon_id,  # Ajoutez l'ID de l'arme à mettre à jour dans les données mises à jour
            "Name": self.update_name_input.text(),
            "Type": self.update_type_input.text(),
            "Manufacturer": self.update_manufacturer_input.text(),
            "Caliber": self.update_caliber_input.text(),
            "MagazineCapacity": int(self.update_magazine_capacity_input.text()),
            "FireRate": int(self.update_fire_rate_input.text()),
            "AmmoCount": int(self.update_ammo_count_input.text())
        }
        self.presenter.update_weapon(int(weapon_id), updated_weapon_data)
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
    def delete_weapon(self):
        weapon_id = self.weapon_id_input.text()
        if not self.validate_weapon_id(weapon_id):
            return
        confirmation = QMessageBox.question(self, 'Confirmation', f"Do you want to delete weapon with ID {weapon_id}?", QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            self.presenter.delete_weapon(int(weapon_id))

    def display_weapon_deleted_message(self, weapon_id):
        QMessageBox.information(self, 'Success', f"Weapon deleted successfully with ID: {weapon_id}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = WeaponView()
    view.show()
    sys.exit(app.exec_())