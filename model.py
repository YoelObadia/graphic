# The class `Weapon` in Python defines attributes for a weapon object including ID, name, type,
# manufacturer, caliber, magazine capacity, fire rate, ammo count, and optional images.
class Weapon:
    def __init__(self, Id, Name, Type, Manufacturer, Caliber, MagazineCapacity, FireRate, AmmoCount, Images):
        self.Id = Id
        self.Name = Name
        self.Type = Type
        self.Manufacturer = Manufacturer
        self.Caliber = Caliber
        self.MagazineCapacity = MagazineCapacity
        self.FireRate = FireRate
        self.AmmoCount = AmmoCount
        self.Images = Images  
