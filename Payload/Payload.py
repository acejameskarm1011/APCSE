class Payload:
    def __init__(self, mass) -> None:
        self.mass = mass
    def Ejectable(self, bool):
        if bool:
            self.ejectable = True
        else:
            self.ejectable = False
    def Eject(self):
        if self.ejectable:
            self.mass = 0