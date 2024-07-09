class ProductionUnit:
    def __init__(self, energyConsumtion, position):
        self.energyConsumtion = energyConsumtion
        self.position = position

    def beschreibung(self):
        return f"{self.marke} {self.modell}"
    
    def informAboutError():
        return "Error was sent to "

'''The Hub or Core is the main component of the machine. It also defines the position of all other production units.'''
class HUB(ProductionUnit):

    def __init__(self, marke, modell, ip_address, port):
        super().__init__(marke, modell, ip_address, port)
        self.coordinates = [0,0,0]

    def beschreibung(self):
        return f"{self.marke} {self.modell}, coordinates {self.coordinates}"

class AssamblyStation(ProductionUnit):
    def __init__(self, marke, modell, coordinates):
        super().__init__(marke, modell)
        self.coordinates = coordinates

    def beschreibung(self):
        return f"{self.marke} {self.modell}, coordinates {self.coordinates}"





'''
class CNC(ProductionUnit):
    def __init__(self, marke, modell, coordinates):
        super().__init__(marke, modell)
        self.coordinates = coordinates

    def beschreibung(self):
        return f"{self.marke} {self.modell}, coordinates {self.coordinates}"


class SimpleLab(ProductionUnit):
    def __init__(self, marke, modell, coordinates):
        super().__init__(marke, modell)
        self.coordinates = coordinates

    def beschreibung(self):
        return f"{self.marke} {self.modell}, coordinates {self.coordinates}"

class GrowStation(ProductionUnit):
    def __init__(self, marke, modell, coordinates):
        super().__init__(marke, modell)
        self.coordinates = coordinates

    def beschreibung(self):
        return f"{self.marke} {self.modell}, coordinates {self.coordinates}"
       

class Printer3D(ProductionUnit):
    def __init__(self, marke, modell, coordinates):
        super().__init__(marke, modell)
        self.coordinates = coordinates

    def beschreibung(self):
        return f"{self.marke} {self.modell}, coordinates {self.coordinates}"
    
class StorageUnit(ProductionUnit):
    def __init__(self, marke, modell, coordinates):
        super().__init__(marke, modell)
        self.coordinates = coordinates

    def beschreibung(self):
        return f"{self.marke} {self.modell}, coordinates {self.coordinates}"
    
class TransportUnit(ProductionUnit):
    def __init__(self, marke, modell, coordinates):
        super().__init__(marke, modell)
        self.coordinates = coordinates

    def beschreibung(self):
        return f"{self.marke} {self.modell}, coordinates {self.coordinates}"
    
class InspectionUnit(ProductionUnit):
    def __init__(self, marke, modell, coordinates):
        super().__init__(marke, modell)
        self.coordinates = coordinates

    def beschreibung(self):
        return f"{self.marke} {self.modell}, coordinates {self.coordinates}"

'''