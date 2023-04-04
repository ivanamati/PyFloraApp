import json
from tokenize import group
from turtle import color
import pandas as pd
import ttkbootstrap as ttk

# ovaj import nam služi za crtanje grafova
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from simulator_senzora import raspberry_pi
#from weather_api import base_url,dohvati_prognozu,obradi_prognozu


# ovo je super dokumentacija za početnike
# https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html

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

# probe za dohvacanje podataka sa senzora i prikaz u aplikaciji kod podataka o biljci
podaci = dohvati_podatke_sa_senzora()
#print(podaci)
vlažnost_zemlje = f'{podaci[0]["vrijednost"]} %'
#print(vlažnost_zemlje)

# podaci = raspberry_pi.get_data()
# for i in range(10):
#     podaci.extend(raspberry_pi.get_data())

# def dohvati_podatke_sa_prognoze():
#     return obradi_prognozu(dohvati_prognozu(url=base_url, latitude=48.99, longitude=19.56))

def obradi_podatke(podaci):
    """ Metoda pd.DataFrame() u Pythonu stvara DataFrame objekt iz različitih vrsta podataka, 
    uključujući liste, rječnike i nizove. Metoda prihvaća podatke kao argument 
    i vraća DataFrame objekt. 
    Metoda df.plot() u Pythonu koristi se za stvaranje grafova iz DataFrame objekta. 
    Metoda prihvaća različite argumente koji se koriste za prilagođavanje grafa."""
    df = pd.DataFrame(podaci)
    #print(df)
    #df.plot()
    return df

def konvertiraj_vrijeme(df, format="%Y-%m-%dT%H:%M"):
    """ova funkcija se koristi da pretvorimo vrijednost iz stringa u pravi datime objekt
    koristeci pd.to_datime za spomenutu konverziju"""
    # kako bi pretvorili vrijednost iz stringa "2023-03-28 19:52" u pravi datetime objekt
    # format nam je isti kao u simulator_senzora :
    #     "vrijeme_dohvata": self.vrijeme_dohvata.strftime("%Y-%m-%d %H:%M")

    # koristimo pd.to_datetime za konverziju
    df["vrijeme dohvata"] = pd.to_datetime(df["vrijeme dohvata"], format=format)

def pivotiraj_podatke(df):
    """ova funkcija iz tablice podataka 'df' uzima 3 podatka
    i to tako da index po kojemu idu podaci u seriji bude vrijeme dohvata
    i uz to imamo još 3 kolone koje uzimamo iz kolone "ime" iz originalnog data framea """
    return df.pivot(index="vrijeme dohvata", columns="ime senzora", values="vrijednost")

def nacrtaj_jednostavni_graf_samo_za_temperaturu(pivoted_df):
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel("Vrijeme dohvata")
    plt.ylabel("TEMPERATURA") #"Vrijednosti TEMPERATURA"
    plt.plot(pivoted_df.index.strftime("%H:%M"), pivoted_df.TEMPERATURA)

def nacrtaj_jednostavni_graf_samo_za_tlak(pivoted_df):
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel("Vrijeme dohvata")
    plt.ylabel("TLAK") #"Vrijednosti TLAK"
    plt.plot(pivoted_df.index.strftime("%H:%M"), pivoted_df.TLAK)

def nacrtaj_jednostavni_graf_samo_za_vlagu(pivoted_df):
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel("Vrijeme dohvata")
    plt.ylabel("VLAGA") #"Vrijednosti VLAGA"
    plt.plot(pivoted_df.index.strftime("%H:%M"), pivoted_df.VLAGA)

def nacrtaj_lijepi_graf(pivoted_df):
    # tu crtamo lijepe grafove
    ax1 = plt.gca() # get current axes

    ax1.set_xlabel("Vrijeme dohvata")
    ax1.set_ylabel("Tlak", color="red")

    ax1.plot(pivoted_df.index.strftime("%H:%M"), pivoted_df.TLAK, "r.-")

    ax2 = ax1.twinx() # crerate another axis which shares same x-axis

    ax2.set_ylabel("Temparatura/Vlaga", color="blue")
    ax2.set_ylabel("Temparatura", color="blue")

    ax2.plot(pivoted_df.index.strftime("%H:%M"), pivoted_df.TEMPERATURA, "b.-")
    ax2.plot(pivoted_df.index.strftime("%H:%M"), pivoted_df.VLAGA, "g-.")

    #ax1.grid()
    #ax2.grid()

def obradi_podatke_i_nacrtaj_graf(podaci, title):
    """ovu funkciju NE koristim"""
    df = obradi_podatke(podaci=podaci)
    #print(df)
    konvertiraj_vrijeme(df=df, format="%Y-%m-%dT%H:%M")
    pivoted_df = pivotiraj_podatke(df=df)
    #print(pivoted_df)
        
    # prikaži vrijednosti u 3 grafa koji dijele istu X os
    # bez korištenja dodatnih funkcije koje smo gore definirali!
    pivoted_df.plot(subplots=True, title=title)

def obradi_dohvacene_podatke_i_nacrtaj_graf(root,podaci, title):
        """ ova se funkcija koristi u gui_app za obradu podataka dobivenih s rasberry_pi
        te crtanje grada bas u samom GUI prozoru"""
        df = pd.DataFrame(podaci)
        df["vrijeme dohvata"] = pd.to_datetime(df["vrijeme dohvata"], format="%Y-%m-%d %H:%M")
        pivoted_df = df.pivot(index="vrijeme dohvata", columns="ime senzora", values="vrijednost")

        # Stvaranje figure
        fig = Figure(figsize=(5, 4), dpi=110)

        # Dodavanje subplot-a na figure
        plot1 = fig.add_subplot(111)

        # Prikazivanje podataka na subplot-u
        pivoted_df.plot(ax=plot1, subplots=True, title=title)

        # Stvaranje canvas-a za tkinter
        canvas = FigureCanvasTkAgg(fig, master=root)  
        canvas.draw()

        # Prikazivanje canvas-a
        canvas.get_tk_widget().place(anchor="center",relx=0.5,rely=0.5)

# def graf_podataka_sa_senzora():
#     podaci = dohvati_podatke_sa_senzora()
#     obradi_podatke_i_nacrtaj_graf(podaci=podaci, title="Podaci sa senzora")
#     plt.show()


# def obradi_podatke_i_nacrtaj_graf(podaci, title):
#             df = pd.DataFrame(podaci)
#             df["vrijeme dohvata"] = pd.to_datetime(df["vrijeme dohvata"], format="%Y-%m-%d %H:%M")
#             pivoted_df = df.pivot(index="vrijeme dohvata", columns="ime senzora", values="vrijednost")

#             # Stvaranje figure
#             fig = Figure(figsize=(5, 4), dpi=100)

#             # Dodavanje subplot-a na figure
#             plot1 = fig.add_subplot(111)

#             # Prikazivanje podataka na subplot-u
#             pivoted_df.plot(ax=plot1, subplots=True, title=title)

#             # Stvaranje canvas-a za tkinter
#             canvas = FigureCanvasTkAgg(fig, master=self.root)  
#             canvas.draw()

#             # Prikazivanje canvas-a
#             canvas.get_tk_widget().pack()