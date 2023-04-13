from ctypes import resize
import random
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from gui_repozitorij_prozora import *

# u ovom se modulu nalaze klase za simulaciju senzora PyPosuda
# modul sadrzi i funkcije za crtanje grafova prema dohvacenim podacima iz posude
# te funkcije za prikaz dohvacenih podataka sa senzora u GUI aplikaciji

class SabirnicaSenzora:         # OVO JE HUB (neka vrsta sabirnica)
    def __init__(self, senzori):
        self.senzori = senzori

    def get_data(self):
        data = []
        for senzor in self.senzori:
            data.append(senzor.dohvati_podatke()) #dohvati_podatke
            # ovdje smo se mi obvezali sto ce se dogoditi i sto ce se vracati, 
            # takoder da ce senzori postojati
            # i da ce senzori biti lista
            # senzor smo dobili instanciranjem klase SenzoriZaRaspberyyPi
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
        podaci_sa_senzora = PodaciSaSenzora(self.name, vrijednost,self.mjerna_jedinica,self.vrijeme_dohvata.strftime("%Y-%m-%d %H:%M"))
        return podaci_sa_senzora

senzor_temperature = SenzoriZaRaspberryPi(
    ime_senzora="TEMPERATURA", max_vrijednost=100, min_vrijednost=-40, mjerna_jedinica="°C"
)

senzor_vlage = SenzoriZaRaspberryPi(
    ime_senzora="VLAŽNOST ZEMLJE", max_vrijednost=100, min_vrijednost=0, mjerna_jedinica="%"
)

senzor_kiselosti = SenzoriZaRaspberryPi(
    ime_senzora="KISELOST", max_vrijednost=14, min_vrijednost=0, mjerna_jedinica="pH" 
) #7 je neutralno

senzor_saliniteta = SenzoriZaRaspberryPi(
    ime_senzora="SALINITET", max_vrijednost=15, min_vrijednost=0, mjerna_jedinica="dS/m" #deciSiemens po metru
)

senzor_svjetlosti = SenzoriZaRaspberryPi(
    ime_senzora="SVJETLOST", max_vrijednost=150, min_vrijednost=0, mjerna_jedinica="lx"
)

raspberry_pi_stara_jagodica = SabirnicaSenzora([senzor_temperature, senzor_vlage])

# ovo je raspberry pi za senzore PyFlora posude koji sadrzi senzore za vlaznost zemlje, ph, salinitet zemlje te razinu svjetlosti
raspberry_pi = SabirnicaSenzora([senzor_vlage,senzor_kiselosti,senzor_saliniteta,senzor_svjetlosti])


# SENZORI koje sadrzi PyPosuda:
# - vlažnosti zemlje (postoci)
# - pH vrijednosti i saliniteta zemlje (ph i dS/m)
# - razine svjetla koje dopire do biljke (lux)

def dohvati_podatke_sa_senzora():
    """Funkcija dohvati_podatke_sa_senzora() je funkcija u Pythonu koja vraća listu podataka s senzora. 
    Funkcija poziva metodu get_data() objekta nazvanog raspberry_pi 
    i proširuje listu podataka s podacima koji su vraćeni. 
    Metoda extend() dodaje elemente liste koji su predani kao argument .
    Metoda json.dumps() je metoda u Pythonu koja pretvara objekt u JSON niz. 
    Metoda prihvaća objekt kao argument i vraća JSON niz ."""
    podaci = []
    for i in range(100): #1000
        podaci.extend(raspberry_pi.get_data())
    return podaci

def ocitanje_vrijednosti(ime_senzora, max_vrijednost, min_vrijednost, mjerna_jedinica):
    senzor = SenzoriZaRaspberryPi(ime_senzora, max_vrijednost, min_vrijednost, mjerna_jedinica)
    return senzor.dohvati_podatke()["vrijednost"]

def dohvati_podatke_rezultata_mjerenja(ime_senzora, max_vrijednost, min_vrijednost, mjerna_jedinica):
    # ova funkcija dohvaca rezultate mjerenja
    # pomocu metode koja vraca podatke sa senzora u obliku klase "PodaciSaSenzora"
    rezultat_mjerenja = SenzoriZaRaspberryPi(ime_senzora, max_vrijednost, min_vrijednost, mjerna_jedinica)
    return rezultat_mjerenja.dohvati_podatke_klase()

# def prikaz_svih_senzora_u_gui_s_dohvacenim_podacima(frame,gui_objekt,id_slike):
#     """ova funkcija dohvaca podatke sa simulatora senzora
#     te ih prikazuje najprije u cetiri mala prozorcica pored biljke;
#     u frameu ispod njih ispisuje status biljke, odnosno treba li zaliti biljku,
#     dodati supstrat ili nesto drugo s obzirom na vrijednosti sa senzora;
#     na dnu podataka nudi gumb sink koji azurira podatke sa senzora"""
#     # podaci dohvaceni sa simulatora senzora za vlaznost, kiselost i salinitet zemlje te svijetlost
#     # spremljeni u varijable za prikaz na ekranu kod odabrane biljke iz baze
#     podaci = dohvati_podatke_sa_senzora() #ovo je lista dictova!
#     vlaznost_zemlje = f'{podaci[0]["vrijednost"]} %'
#     kiselost = f'{podaci[1]["vrijednost"]} pH'
#     salinitet = f'{podaci[2]["vrijednost"]} dS/m'
#     svijetlost = f'{podaci[3]["vrijednost"]} lx'
    
#     frame_za_vlaznost=dodaj_frame_place(frame,"raised",1,90,85,"heart",None,"center",0.77,0.16)
#     # prikaz vlage izmjerene simulatorom senzora na ekranu
#     label(frame_za_vlaznost,f'VLAGA\n\n{vlaznost_zemlje}',('Quicksand',10),"dark","center",None,"center",0.5,0.5)

#     frame_za_kiselost=dodaj_frame_place(frame,"raised",1,90,85,"heart",None,"center",0.63,0.16)
#     label(frame_za_kiselost,f'KISELOST\n\n{kiselost}',('Quicksand',10),"dark","center",None,"center",0.5,0.5)

#     frame_za_salinitet = dodaj_frame_place(frame,"raised",1,90,85,"heart",None,"center",0.77,0.33)
#     label(frame_za_salinitet,f'SALINITET\n\n{salinitet}',('Quicksand',10),"dark","center",None,"center",0.5,0.5)

#     frame_za_svijetlost = dodaj_frame_place(frame,"raised",1,90,85,"heart",None,"center",0.63,0.33)
#     label(frame_za_svijetlost,f'SVIJETLO\n\n{svijetlost}',('Quicksand',10),"dark","center",None,"center",0.5,0.5)

#     frame_za_status_biljke=dodaj_frame_place(frame,None,0,270,150,"heart",None,"center",0.7,0.59)
#     kiselina = podaci[1]["vrijednost"]
#     vlaga = podaci[0]["vrijednost"]
#     slanost = podaci[2]["vrijednost"]
#     osvijetljenje  = podaci[3]["vrijednost"]

#     if kiselina > 7:
#         label(frame_za_status_biljke,
#             tekst="dodaj supstrat",font_slova=('Quicksand',10),stil="dark",
#             poravnanje="center",pozadina=None,anchor="center",relx=0.5,rely=0.2)
#     else:
#         label(frame_za_status_biljke,
#             tekst="kiselost je u redu",font_slova=('Quicksand',10),stil="dark",
#             poravnanje="center",pozadina=None,anchor="center",relx=0.5,rely=0.2)

#     if vlaga < 50:
#         label(frame_za_status_biljke,
#             tekst="zalijte biljku",font_slova=('Quicksand',10),stil="dark",
#             poravnanje="center",pozadina=None,anchor="center",relx=0.5,rely=0.35)

#     else:
#         label(frame_za_status_biljke,
#             tekst="zalijevanje nije potrebno",font_slova=('Quicksand',10),stil="dark",
#             poravnanje="center",pozadina=None,anchor="center",relx=0.5,rely=0.35)

#     if slanost > 8:
#         label(frame_za_status_biljke,
#             tekst="slanost je umjerena",font_slova=('Quicksand',10),stil="dark",
#             poravnanje="center",pozadina=None,anchor="center",relx=0.5,rely=0.5)
#     else:
#         label(frame_za_status_biljke,
#             tekst="slanost je niska",font_slova=('Quicksand',10),stil="dark",
#             poravnanje="center",pozadina=None,anchor="center",relx=0.5,rely=0.5)
        
#     if osvijetljenje < 75:
#         label(frame_za_status_biljke,
#             tekst="premijestite biljku na svijetlo",font_slova=('Quicksand',10),stil="dark",
#             poravnanje="center",pozadina=None,anchor="center",relx=0.5,rely=0.65)
#     else:
#         label(frame_za_status_biljke,
#             tekst="maknite biljku s izravne svijetlosti",font_slova=('Quicksand',10),stil="dark",
#             poravnanje="center",pozadina=None,anchor="center",relx=0.5,rely=0.65)
        
#     gumb_sinkronizacije(frame_za_status_biljke,lambda:gui_objekt.prozor_s_detaljima_o_biljci(id_slike,command_za_button_BACK=None),
#                             padding=8,width=32,x=0,y=115)

# def prikaz_statusa_biljke_prema_podacima_sa_senzora(frame_za_tekst_statusa,anchor,relx,rely):
#     """ ova funkcija u prozoru gdje se nalaze sve biljke
#     prikazuje je li potrebno napraviti nesto 
#     s biljkom prije otvaranja prozora s detaljima od biljke"""
#     # podaci dohvaceni sa simulatora senzora za vlaznost, kiselost i salinitet zemlje te svijetlost
#     # spremljeni u varijable za prikaz na ekranu kod odabrane biljke iz baze
#     podaci = dohvati_podatke_sa_senzora() 
#     kiselost = podaci[1]["vrijednost"]
#     vlaga = podaci[0]["vrijednost"]
#     # slanost = podaci[2]["vrijednost"]
#     osvijetljenje  = podaci[3]["vrijednost"]

#     if kiselost > 7:
#         label(frame_za_tekst_statusa,
#             tekst="dodaj supstrat",font_slova=('Quicksand',10),stil="dark",
#             poravnanje="center",pozadina=None,anchor=anchor,relx=relx,rely=rely)
#     elif vlaga < 50:
#         label(frame_za_tekst_statusa,
#             tekst="zalijte biljku",font_slova=('Quicksand',10),stil="dark",
#             poravnanje="center",pozadina=None,anchor=anchor,relx=relx,rely=rely)
#     elif osvijetljenje < 75:
#         label(frame_za_tekst_statusa,
#             tekst="premijestite biljku na svijetlo",font_slova=('Quicksand',10),stil="dark",
#             poravnanje="center",pozadina=None,anchor=anchor,relx=relx,rely=rely)
#     elif osvijetljenje > 75:
#         label(frame_za_tekst_statusa,
#             tekst="maknite biljku sa svijetlosti",font_slova=('Quicksand',10),stil="dark",
#             poravnanje="center",pozadina=None,anchor=anchor,relx=relx,rely=rely)
#     else:
#         label(frame_za_tekst_statusa,
#             tekst="sve OK",font_slova=('Quicksand',10),stil="dark",
#             poravnanje="center",pozadina=None,anchor=anchor,relx=relx,rely=rely)

# def obradi_i_pivotiraj_podatke():
#     """ova funkcija dohvaca podatke sa senzora 
#     te ih pivotira prema dohvatu vremena za obradu i prikaz grafova;
#     funkcija vraca te pivotirane podatke"""

#     podaci = dohvati_podatke_sa_senzora()
#     df = pd.DataFrame(podaci)
#     df["vrijeme dohvata"] = pd.to_datetime(df["vrijeme dohvata"], format="%Y-%m-%d %H:%M")
#     pivoted_df = df.pivot(index="vrijeme dohvata", columns="ime senzora", values="vrijednost")
#     return pivoted_df

# def obradi_dohvacene_podatke_i_nacrtaj_line_chart_graf(root, title):
#         """ ova se funkcija koristi u gui_app za obradu podataka dobivenih s rasberry_pi
#         te crtanje grada bas u samom GUI prozoru"""
#         pivoted_df=obradi_i_pivotiraj_podatke()

#         # Stvaranje figur4
#         fig = Figure(figsize=(6, 6), dpi=80)
#         # Dodavanje subplot-a na figure
#         plot1 = fig.add_subplot(132)
#         # Prikazivanje podataka na subplot-u
#         pivoted_df.plot(kind="area",ax=plot1, subplots=True, title=title, ylabel="vrijednost")
#         # Stvaranje canvas-a za tkinter
#         canvas = FigureCanvasTkAgg(fig, master=root)  
#         canvas.draw()
#         # Prikazivanje canvas-a
#         canvas.get_tk_widget().place(anchor="center",relx=0.5,rely=0.4)

# def obradi_dohvacene_podatke_i_nacrtaj_graf_histogram(root, title):
#         """ ova se funkcija koristi u gui_app za obradu podataka dobivenih s rasberry_pi
#         te crtanje grada bas u samom GUI prozoru"""
             
#         pivoted_df=obradi_i_pivotiraj_podatke()

#         # Stvaranje figur4
#         fig = Figure(figsize=(6, 5), dpi=90, layout='compressed')
#         # Dodavanje subplot-a na figure
#         plot1 = fig.add_subplot(132)
#         # Prikazivanje podataka na subplot-u
#         pivoted_df.plot(ax=plot1, subplots=True, title=title)

#         plot2 = fig.add_subplot(131)
#         pivoted_df.hist(ax=plot2)
#         # Stvaranje canvas-a za tkinter
#         canvas = FigureCanvasTkAgg(fig, master=root)  
#         canvas.draw()

#         # Prikazivanje canvas-a
#         canvas.get_tk_widget().place(anchor="center",relx=0.5,rely=0.4)

# def obradi_dohvacene_podatke_i_nacrtaj_treci_graf(root, title):
#         """ ova se funkcija koristi u gui_app za obradu podataka dobivenih s rasberry_pi
#         te crtanje grada bas u samom GUI prozoru"""
#         pivoted_df=obradi_i_pivotiraj_podatke()

#         # Stvaranje figur4
#         fig = Figure(figsize=(6.5, 4), dpi=90,layout="compressed")
#         # Dodavanje subplot-a na figure
#         plot1 = fig.add_subplot(132)
#         # Prikazivanje podataka na subplot-u
#         pivoted_df.plot(kind="box",ax=plot1, subplots=True, title=title)
#         # Stvaranje canvas-a za tkinter
#         canvas = FigureCanvasTkAgg(fig, master=root)  
#         canvas.draw()
#         # Prikazivanje canvas-a
#         canvas.get_tk_widget().place(anchor="center",relx=0.5,rely=0.4)


# # ovo je poziv funkcije kojoj predajem vrijednosti atributa klase "SenzoriZaRasberryPi"
# # i od nje dobivam objekt te pozivam metodu klase "PodaciSaSenzora":
# #dohvati_podatke_rezultata_mjerenja("temperatura",100,-50,"C").lijepi_ispis()

# # pozivam funkciju koja mi vraca podatke sa senzora prema vrijednostima atributa:
# #ocitanje_vrijednosti(ime_senzora="temperatura",max_vrijednost= 35,min_vrijednost= -40,mjerna_jedinica="C")

