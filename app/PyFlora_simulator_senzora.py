from ctypes import resize
import random
from datetime import datetime, timedelta
from gui_repozitorij_prozora import *

### OVAJ MODUL SADRŽI KLASE ZA SIMULACIJU SENZORA PYPOSUDA 


class SabirnicaSenzora:  # OVO JE HUB (neka vrsta sabirnica)
    def __init__(self, senzori):
        self.senzori = senzori

    def get_data(self):
        data = []
        for senzor in self.senzori:
            data.append(senzor.dohvati_podatke())  # dohvati_podatke
            # ovdje smo se mi obvezali sto ce se dogoditi i sto ce se vracati,
            # takoder da ce senzori postojati
            # i da ce senzori biti lista
            # senzor smo dobili instanciranjem klase SenzoriZaRaspberyyPi
        return data


class PodaciSaSenzora:
    def __init__(self, ime_senzora, vrijednost, mjerna_jedinica, vrijeme_dohvata):
        self.ime_senzora = ime_senzora
        self.vrijednost = vrijednost
        self.mjerna_jedinica = mjerna_jedinica
        self.vrijeme_dohvata = vrijeme_dohvata

    def lijepi_ispis(self):
        print(
            f"Vrijednost {self.ime_senzora} mjerenja je {self.vrijednost}{self.mjerna_jedinica}, a vrijeme {self.vrijeme_dohvata}"
        )

    def metoda_za_usporedivanje(self, drugi_objekt):
        if self.ime_senzora == drugi_objekt.ime_senzora:
            return self.vrijednost == drugi_objekt.vrijednost
        return False


class SenzoriZaRaspberryPi:
    """ovu sam klasu napravila kako bi podaci sa senzora bili
    klasa, a ne dict; 
    to je bilo za vjezbu odnosno domacu zadacu"""
    def __init__(self, ime_senzora, max_vrijednost, min_vrijednost, mjerna_jedinica):
        self.name = ime_senzora
        self.max_vrijednost = max_vrijednost
        self.min_vrijednost = min_vrijednost
        self.mjerna_jedinica = mjerna_jedinica
        # ovo dodajem iz Učinog koda
        self.value = 0
        self.vrijeme_dohvata = datetime.now()

    def generiraj_vrijednost(self):
        self.vrijeme_dohvata -= timedelta(minutes=5)
        if self.value:
            return random.randint(self.value - 10, self.value + 10)
        return random.randint(self.min_vrijednost, self.max_vrijednost)

    def dohvati_podatke(self):
        # vraca podatke sa senzra,
        # ali kao dict
        self.vrijednost = self.generiraj_vrijednost()
        return {
            "ime senzora": self.name,
            "vrijednost": self.vrijednost,
            "mjerna jedinica": self.mjerna_jedinica,
            "vrijeme dohvata": self.vrijeme_dohvata.strftime("%Y-%m-%d %H:%M"),
        }

    def dohvati_podatke_klase(self):
        # vraca podatke sa senzora,
        # ali kao klasu umjesto dicta iz prethodne metode
        vrijednost = self.generiraj_vrijednost()
        podaci_sa_senzora = PodaciSaSenzora(
            self.name,
            vrijednost,
            self.mjerna_jedinica,
            self.vrijeme_dohvata.strftime("%Y-%m-%d %H:%M"),
        )
        return podaci_sa_senzora


senzor_temperature = SenzoriZaRaspberryPi(
    ime_senzora="TEMPERATURA",
    max_vrijednost=100,
    min_vrijednost=-40,
    mjerna_jedinica="°C",
)

senzor_vlage = SenzoriZaRaspberryPi(
    ime_senzora="VLAŽNOST ZEMLJE",
    max_vrijednost=100,
    min_vrijednost=0,
    mjerna_jedinica="%",
)

senzor_kiselosti = SenzoriZaRaspberryPi(
    ime_senzora="KISELOST", 
    max_vrijednost=14, 
    min_vrijednost=0, 
    mjerna_jedinica="pH"
)  # 7 je neutralno

senzor_saliniteta = SenzoriZaRaspberryPi(
    ime_senzora="SALINITET",
    max_vrijednost=15,
    min_vrijednost=0,
    mjerna_jedinica="dS/m",  # deciSiemens po metru
)

senzor_svjetlosti = SenzoriZaRaspberryPi(
    ime_senzora="SVJETLOST", 
    max_vrijednost=150, 
    min_vrijednost=0, 
    mjerna_jedinica="lx"
)

raspberry_pi_stara_jagodica = SabirnicaSenzora([senzor_temperature, senzor_vlage])

# ovo je raspberry pi za senzore PyFlora posude koji sadrzi senzore za vlaznost zemlje, ph, salinitet zemlje te razinu svjetlosti
raspberry_pi = SabirnicaSenzora(
    [senzor_vlage, senzor_kiselosti, senzor_saliniteta, senzor_svjetlosti]
)

def dohvati_podatke_sa_senzora():
    """Funkcija dohvati_podatke_sa_senzora() je funkcija u Pythonu koja vraća listu podataka s senzora.
    Funkcija poziva metodu get_data() objekta nazvanog raspberry_pi
    i proširuje listu podataka s podacima koji su vraćeni.
    Metoda extend() dodaje elemente liste koji su predani kao argument .
    Metoda json.dumps() je metoda u Pythonu koja pretvara objekt u JSON niz.
    Metoda prihvaća objekt kao argument i vraća JSON niz ."""
    podaci = []
    for i in range(100):  # 1000
        podaci.extend(raspberry_pi.get_data())
    return podaci


def ocitanje_vrijednosti(ime_senzora, max_vrijednost, min_vrijednost, mjerna_jedinica):
    senzor = SenzoriZaRaspberryPi(
        ime_senzora, max_vrijednost, min_vrijednost, mjerna_jedinica
    )
    return senzor.dohvati_podatke()["vrijednost"]


def dohvati_podatke_rezultata_mjerenja(
    ime_senzora, max_vrijednost, min_vrijednost, mjerna_jedinica
):
    # ova funkcija dohvaca rezultate mjerenja
    # pomocu metode koja vraca podatke sa senzora u obliku klase "PodaciSaSenzora"
    rezultat_mjerenja = SenzoriZaRaspberryPi(
        ime_senzora, max_vrijednost, min_vrijednost, mjerna_jedinica
    )
    return rezultat_mjerenja.dohvati_podatke_klase()

