import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QStackedLayout
from presenter import WeaponPresenter  # Supposons que vous avez déjà le présentateur

class WeaponView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weapon Details")
        self.setGeometry(1500, 1500, 1000, 600)

        # Création du présentateur
        self.presenter = WeaponPresenter()

        # Création des pages
        self.create_get_by_id_page()
        self.create_add_weapon_page()
        self.create_update_weapon_page()  # Nouvelle méthode pour créer la page de mise à jour

        # Création du stacked layout
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.get_by_id_widget)
        self.stacked_layout.addWidget(self.add_weapon_widget)
        self.stacked_layout.addWidget(self.update_weapon_widget)  # Ajout de la page de mise à jour

        # Widget contenant le stacked layout
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.central_widget)

        # Connexion des signaux des boutons aux slots correspondants
        self.load_button.clicked.connect(self.load_weapon)
        self.load_all_button.clicked.connect(self.load_all_weapons)
        self.add_button.clicked.connect(self.show_add_weapon_page)
        self.update_button.clicked.connect(self.show_update_weapon_page)  # Connexion du bouton à la méthode show_update_weapon_page
        self.save_button.clicked.connect(self.add_weapon)
        self.delete_button.clicked.connect(self.delete_weapon)
        self.update_save_button.clicked.connect(self.update_weapon)  # Connexion du bouton "Update" à la méthode update_weapon

        # Connexion des signaux du présentateur aux méthodes de mise à jour de l'interface utilisateur
        self.presenter.weapon_loaded.connect(self.update_weapon_details)
        self.presenter.all_weapons_loaded.connect(self.display_all_weapons_table)
        self.presenter.error_occurred.connect(self.display_error)
        self.presenter.weapon_added.connect(self.display_weapon_added_message)
        self.presenter.weapon_deleted.connect(self.display_weapon_deleted_message)
        self.presenter.weapon_updated.connect(self.display_weapon_updated_message)  # Connexion du signal de mise à jour

    def create_get_by_id_page(self):
        # Création des widgets de la page de chargement d'une arme par son ID
        self.weapon_id_input = QLineEdit()
        self.load_button = QPushButton("Load Weapon")
        self.add_button = QPushButton("Add Weapon")
        self.load_all_button = QPushButton("Load All Weapons")
        self.update_button = QPushButton("Update Weapon")
        self.delete_button = QPushButton("Delete Weapon")
        self.weapon_details_label = QLabel("Weapon Details:")
        self.table = QTableWidget()

        # Layout vertical pour la page de chargement d'une arme par son ID
        layout = QVBoxLayout()
        layout.addWidget(self.weapon_id_input)
        layout.addWidget(self.load_button)
        layout.addWidget(self.add_button)
        layout.addWidget(self.load_all_button)
        layout.addWidget(self.update_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.weapon_details_label)
        layout.addWidget(self.table)

        # Widget contenant le layout vertical de la page de chargement d'une arme par son ID
        self.get_by_id_widget = QWidget()
        self.get_by_id_widget.setLayout(layout)
        
    def validate_weapon_id(self, weapon_id):
        if not weapon_id:
            self.display_error("Please enter a valid weapon ID.")
            return False
        try:
            weapon_id = int(weapon_id)
        except ValueError:
            self.display_error("Please enter a valid numeric weapon ID.")
            return False
        for row in range(self.table.rowCount()):
            if int(self.table.item(row, 0).text()) == weapon_id:
                return True
        self.display_error(f"Weapon with ID {weapon_id} does not exist.")
        return False

    def create_add_weapon_page(self):
        # Création des widgets de la page d'ajout d'une arme
        self.name_input = QLineEdit()
        self.type_input = QLineEdit()
        self.manufacturer_input = QLineEdit()
        self.caliber_input = QLineEdit()
        self.magazine_capacity_input = QLineEdit()
        self.fire_rate_input = QLineEdit()
        self.ammo_count_input = QLineEdit()
        self.save_button = QPushButton("Add")

        # Layout vertical pour la page d'ajout d'une arme
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

        # Widget contenant le layout vertical de la page d'ajout d'une arme
        self.add_weapon_widget = QWidget()
        self.add_weapon_widget.setLayout(layout)

    def create_update_weapon_page(self):
        # Création des widgets de la page de mise à jour d'une arme
        self.update_name_input = QLineEdit()
        self.update_type_input = QLineEdit()
        self.update_manufacturer_input = QLineEdit()
        self.update_caliber_input = QLineEdit()
        self.update_magazine_capacity_input = QLineEdit()
        self.update_fire_rate_input = QLineEdit()
        self.update_ammo_count_input = QLineEdit()
        self.update_save_button = QPushButton("Update")

        # Layout vertical pour la page de mise à jour d'une arme
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

        # Widget contenant le layout vertical de la page de mise à jour d'une arme
        self.update_weapon_widget = QWidget()
        self.update_weapon_widget.setLayout(layout)

    def load_weapon(self):
        weapon_id = self.weapon_id_input.text()
        if not weapon_id:
            self.display_error("Please enter a valid weapon ID.")
            return
        self.presenter.load_weapon(int(weapon_id))

    def load_all_weapons(self):
        self.presenter.load_all_weapons()

    def show_add_weapon_page(self):
        self.stacked_layout.setCurrentIndex(1)  # Afficher la page d'ajout d'une arme

    def show_update_weapon_page(self):
        weapon_id = self.weapon_id_input.text()
        if not self.validate_weapon_id(weapon_id):
            return
        self.stacked_layout.setCurrentIndex(2)

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
        self.stacked_layout.setCurrentIndex(0)  # Revenir à la page de chargement par ID

    def update_weapon(self):
        weapon_id = self.weapon_id_input.text()
        
        updated_weapon_data = {
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
        self.stacked_layout.setCurrentIndex(0)  # Revenir à la page de chargement par ID

    def delete_weapon(self):
        weapon_id = self.weapon_id_input.text()
        if not self.validate_weapon_id(weapon_id):
            return
        confirmation = QMessageBox.question(self, 'Confirmation', f"Do you want to delete weapon with ID {weapon_id}?", QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            self.presenter.delete_weapon(int(weapon_id))

    def update_weapon_details(self, weapon):
        details_text = f"Name: {weapon.Name}\nType: {weapon.Type}\nManufacturer: {weapon.Manufacturer}\nCaliber: {weapon.Caliber}\nMagazine Capacity: {weapon.MagazineCapacity}\nFire Rate: {weapon.FireRate}\nAmmo Count: {weapon.AmmoCount}"
        self.weapon_details_label.setText(details_text)

    def display_all_weapons_table(self, weapons):
        self.table.setRowCount(len(weapons))
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Type", "Manufacturer", "Caliber", "Magazine Capacity", "Fire Rate", "Ammo Count"])
        for row, weapon in enumerate(weapons):
            self.table.setItem(row, 0, QTableWidgetItem(str(weapon.Id)))
            self.table.setItem(row, 1, QTableWidgetItem(weapon.Name))
            self.table.setItem(row, 2, QTableWidgetItem(weapon.Type))
            self.table.setItem(row, 3, QTableWidgetItem(weapon.Manufacturer))
            self.table.setItem(row, 4, QTableWidgetItem(weapon.Caliber))
            self.table.setItem(row, 5, QTableWidgetItem(str(weapon.MagazineCapacity)))
            self.table.setItem(row, 6, QTableWidgetItem(str(weapon.FireRate)))
            self.table.setItem(row, 7, QTableWidgetItem(str(weapon.AmmoCount)))

    def display_error(self, error_message):
        print(f"Error: {error_message}")

    def display_weapon_added_message(self, weapon_id):
        QMessageBox.information(self, 'Success', f"Weapon added successfully with ID: {weapon_id}")

    def display_weapon_deleted_message(self, weapon_id):
        QMessageBox.information(self, 'Success', f"Weapon deleted successfully with ID: {weapon_id}")
        
    def display_weapon_updated_message(self, weapon_id):
        QMessageBox.information(self, 'Success', f"Weapon updated successfully with ID: {weapon_id}")

    def clear_add_weapon_fields(self):
        self.name_input.clear()
        self.type_input.clear()
        self.manufacturer_input.clear()
        self.caliber_input.clear()
        self.magazine_capacity_input.clear()
        self.fire_rate_input.clear()
        self.ammo_count_input.clear()

    def clear_update_weapon_fields(self):
        self.update_name_input.clear()
        self.update_type_input.clear()
        self.update_manufacturer_input.clear()
        self.update_caliber_input.clear()
        self.update_magazine_capacity_input.clear()
        self.update_fire_rate_input.clear()
        self.update_ammo_count_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = WeaponView()
    view.show()
    sys.exit(app.exec_())
