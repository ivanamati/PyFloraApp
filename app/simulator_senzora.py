from ctypes import resize
import random
from datetime import datetime, timedelta

        # ZADATAK: koristiti klasu, a ne dict. 
        # Klasa mora biti ista kao i u simulator senzora SensorZaRaspberryPi.dohvati_podatke
        # napomena: tu će biti 3 objekta, ne 1

        # osmisliti klasu umjesto dicta iz dohvati_podatke
        # u klasi nam teba biti kojeg je tipa senzor i koja je vrijednost i dodati jedinicu
# DODAJ class Jagodica iz Učinog koda

class Jagodica:
    def __init__(self, senzori):
        self.senzori = senzori

    def get_data(self):
        data = []
        for senzor in self.senzori:
            data.append(senzor.dohvati_podatke()) #dohvati_podatke
        return data


class PodaciSaSenzora:
    def __init__(self, ime_senzora, vrijednost, mjerna_jedinica,vrijeme_dohvata):
        self.ime_senzora = ime_senzora
        self.vrijednost = vrijednost 
        self.mjerna_jedinica = mjerna_jedinica
        self.vrijeme_dohvata = vrijeme_dohvata

    def lijepi_ispis(self):
        print(f"Vrijednost {self.ime_senzora} mjerenja je {self.vrijednost}{self.mjerna_jedinica}, a vrijeme {self.vrijeme_dohvata}")

    def metoda_za_usporedivanje(self, drugi_objekt):
        if self.ime_senzora == drugi_objekt.ime_senzora:
            return self.vrijednost == drugi_objekt.vrijednost
        return False

       
class SenzoriZaRaspberryPi:
    def __init__(self,ime_senzora, max_vrijednost, min_vrijednost, mjerna_jedinica):
        self.name = ime_senzora
        self.max_vrijednost = max_vrijednost
        self.min_vrijednost = min_vrijednost
        self.mjerna_jedinica = mjerna_jedinica
        # ovo dodajem iz Učinog koda
        self.value = 0
        self.vrijeme_dohvata = datetime.now()

    # def generiraj_vrijednost(self):
    # ovo vise ne koristimo
    #     self.vrijeme_dohvata += timedelta(minutes=15)
    #     return random.randint(self.min_vrijednost, self.max_vrijednost)
    
    def generiraj_vrijednost(self):
        self.vrijeme_dohvata += timedelta(minutes=15)
        if self.value:
            return random.randint(self.value-10, self.value+10)
        return random.randint(self.min_vrijednost, self.max_vrijednost)
    
    def dohvati_podatke(self):
        # vraca podatke sa senzra,
        # ali kao dict 
        self.vrijednost = self.generiraj_vrijednost()
        return {
            "ime senzora":self.name,
            "vrijednost": self.vrijednost,
            "mjerna jedinica": self.mjerna_jedinica,
            "vrijeme dohvata": self.vrijeme_dohvata.strftime("%Y-%m-%d %H:%M")
        }

    def dohvati_podatke_klase(self):
        # vraca podatke sa senzora,
        # ali kao klasu umjesto dicta iz prethodne metode
        vrijednost = self.generiraj_vrijednost()
        podaci_sa_senzora = PodaciSaSenzora(self.name, vrijednost,self. mjerna_jedinica,self.vrijeme_dohvata.strftime("%Y-%m-%d %H:%M"))
        return podaci_sa_senzora

senzor_temperature = SenzoriZaRaspberryPi(
    ime_senzora="TEMPERATURA", max_vrijednost=100, min_vrijednost=-40, mjerna_jedinica="°C"
)

senzor_tlaka = SenzoriZaRaspberryPi(
    ime_senzora="TLAK", max_vrijednost=1300, min_vrijednost=900, mjerna_jedinica="hPa"
)

senzor_vlage = SenzoriZaRaspberryPi(
    ime_senzora="VLAGA", max_vrijednost=100, min_vrijednost=0, mjerna_jedinica="%"
)

raspberry_pi = Jagodica([senzor_temperature, senzor_tlaka, senzor_vlage])



def ocitanje_vrijednosti(ime_senzora, max_vrijednost, min_vrijednost, mjerna_jedinica):
    senzor = SenzoriZaRaspberryPi(ime_senzora, max_vrijednost, min_vrijednost, mjerna_jedinica)
    return senzor.dohvati_podatke()["vrijednost"]

def dohvati_podatke_rezultata_mjerenja(ime_senzora, max_vrijednost, min_vrijednost, mjerna_jedinica):
    # ova funkcija dohvaca rezultate mjerenja
    # pomocu metode koja vraca podatke sa senzora u obliku klase "PodaciSaSenzora"
    rezultat_mjerenja = SenzoriZaRaspberryPi(ime_senzora, max_vrijednost, min_vrijednost, mjerna_jedinica)
    return rezultat_mjerenja.dohvati_podatke_klase()


# ovo je poziv funkcije kojoj predajem vrijednosti atributa klase "SenzoriZaRasberryPi"
# i od nje dobivam objekt te pozivam metodu klase "PodaciSaSenzora":
#dohvati_podatke_rezultata_mjerenja("temperatura",100,-50,"C").lijepi_ispis()

# pozivam funkciju koja mi vraca podatke sa senzora prema vrijednostima atributa:
#ocitanje_vrijednosti(ime_senzora="temperatura",max_vrijednost= 35,min_vrijednost= -40,mjerna_jedinica="C")

