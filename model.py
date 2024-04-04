class Weapon:
    def __init__(self, Id, Name, Type, Manufacturer, Caliber, MagazineCapacity, FireRate, AmmoCount, Images=None):
        self.Id = Id
        self.Name = Name
        self.Type = Type
        self.Manufacturer = Manufacturer
        self.Caliber = Caliber
        self.MagazineCapacity = MagazineCapacity
        self.FireRate = FireRate
        self.AmmoCount = AmmoCount
        self.Images = Images  
