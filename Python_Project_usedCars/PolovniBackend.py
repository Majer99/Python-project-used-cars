

class Automobil:
    def __init__(self, marka, model, godiste, cena):
        self.marka = marka
        self.model = model
        self.godiste = godiste
        self.cena = cena

    def __str__(self):
        return f"Marka: {self.marka} Model: {self.model} Godiste: {self.godiste} Cena: {self.cena}"
