import requests
from datetime import datetime
from time import strftime

### OVAJ MODUL SADRZI KLASU Prognoza TE SE KORISTI ZA DOBIVANJE AKTUALNE TEMPERATURE


class Prognoza:
    def __init__(self, tip_vrijednosti, mjerna_jedinica, latitude, longitude):
        self.tip_vrijednosti = tip_vrijednosti
        self.mjerna_jedninica = mjerna_jedinica
        self.latitude = latitude
        self.longitude = longitude

    def dohvati_prognozu_s_meteo_api(self):
        """ova metoda dohvaca podatke s weba"""
        url = f"https://api.open-meteo.com/v1/forecast?latitude={self.latitude}&longitude={self.longitude}&hourly=temperature_2m,relativehumidity_2m,surface_pressure&daily=temperature_2m_max,temperature_2m_min&current_weather=true&timezone=auto"
        prognoza = {}
        try:
            response = requests.get(url)
            if response.status_code == requests.codes.ok:
                # dobili smo listu dictova
                prognoza = response.json()
            else:
                prognoza = {}
        except Exception as e:
            print(f"Ooooops!!!  {e}")
        return prognoza

    def vrijednosti_s_weba(
        self, vrijednost_koju_zelimo_ocitati
    ):  # ovo su vrijednosti koje sam citala: "temperature_2m", "relativehumidity_2m","surface_pressure"
        index = self.aktualni_sat()
        vrijednost_api = self.dohvati_prognozu_s_meteo_api()["hourly"][
            vrijednost_koju_zelimo_ocitati
        ][index]
        return vrijednost_api

    def aktualni_sat(self):
        sati = self.dohvati_prognozu_s_meteo_api()["hourly"]["time"]
        sada = datetime.now()
        iso_puni_sat = sada.strftime("%Y-%m-%dT%H:00")
        index_json = sati.index(iso_puni_sat)
        # return index_json
        return index_json


objekt = Prognoza("temperatura", "celzijevci", latitude="45.82", longitude="15.959999")
# ->
# print("Trenutna temp je:")
objekt.vrijednosti_s_weba(("temperature_2m"))

# print("Trenutna vlaga je:")
# objekt.vrijednosti_s_weba(("relativehumidity_2m"))
# print("Trenutni tlak je:")
# objekt.vrijednosti_s_weba(("surface_pressure"))

# funkcija koja prima lat i long i vraca json prognoza klasa
# ->
# def funkcija_koja_vraca_prognozu_s_weba():
#     prognoza = Prognoza()
#     return prognoza
