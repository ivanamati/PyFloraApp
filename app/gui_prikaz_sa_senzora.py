from gui_repozitorij_prozora import *
from simulator_senzora import dohvati_podatke_sa_senzora

def prikaz_svih_senzora_u_gui_s_dohvacenim_podacima(frame,gui_objekt,id_slike):
    """ova funkcija dohvaca podatke sa simulatora senzora
    te ih prikazuje najprije u cetiri mala prozorcica pored biljke;
    u frameu ispod njih ispisuje status biljke, odnosno treba li zaliti biljku,
    dodati supstrat ili nesto drugo s obzirom na vrijednosti sa senzora;
    na dnu podataka nudi gumb sink koji azurira podatke sa senzora"""
    # podaci dohvaceni sa simulatora senzora za vlaznost, kiselost i salinitet zemlje te svijetlost
    # spremljeni u varijable za prikaz na ekranu kod odabrane biljke iz baze
    podaci = dohvati_podatke_sa_senzora() #ovo je lista dictova!
    vlaznost_zemlje = f'{podaci[0]["vrijednost"]} %'
    kiselost = f'{podaci[1]["vrijednost"]} pH'
    salinitet = f'{podaci[2]["vrijednost"]} dS/m'
    svijetlost = f'{podaci[3]["vrijednost"]} lx'
    
    frame_za_vlaznost=dodaj_frame_place(frame,"raised",1,90,85,"heart",None,"center",0.77,0.16)
    # prikaz vlage izmjerene simulatorom senzora na ekranu
    label(frame_za_vlaznost,f'VLAGA\n\n{vlaznost_zemlje}',('Quicksand',10),"dark","center",None,"center",0.5,0.5)

    frame_za_kiselost=dodaj_frame_place(frame,"raised",1,90,85,"heart",None,"center",0.63,0.16)
    label(frame_za_kiselost,f'KISELOST\n\n{kiselost}',('Quicksand',10),"dark","center",None,"center",0.5,0.5)

    frame_za_salinitet = dodaj_frame_place(frame,"raised",1,90,85,"heart",None,"center",0.77,0.33)
    label(frame_za_salinitet,f'SALINITET\n\n{salinitet}',('Quicksand',10),"dark","center",None,"center",0.5,0.5)

    frame_za_svijetlost = dodaj_frame_place(frame,"raised",1,90,85,"heart",None,"center",0.63,0.33)
    label(frame_za_svijetlost,f'SVIJETLO\n\n{svijetlost}',('Quicksand',10),"dark","center",None,"center",0.5,0.5)

    frame_za_status_biljke=dodaj_frame_place(frame,None,0,270,150,"heart",None,"center",0.7,0.59)
    kiselina = podaci[1]["vrijednost"]
    vlaga = podaci[0]["vrijednost"]
    slanost = podaci[2]["vrijednost"]
    osvijetljenje  = podaci[3]["vrijednost"]

    if kiselina > 7:
        label(frame_za_status_biljke,
            tekst="dodaj supstrat",font_slova=('Quicksand',10),stil="dark",
            poravnanje="center",pozadina=None,anchor="center",relx=0.5,rely=0.2)
    else:
        label(frame_za_status_biljke,
            tekst="kiselost je u redu",font_slova=('Quicksand',10),stil="dark",
            poravnanje="center",pozadina=None,anchor="center",relx=0.5,rely=0.2)

    if vlaga < 50:
        label(frame_za_status_biljke,
            tekst="zalijte biljku",font_slova=('Quicksand',10),stil="dark",
            poravnanje="center",pozadina=None,anchor="center",relx=0.5,rely=0.35)

    else:
        label(frame_za_status_biljke,
            tekst="zalijevanje nije potrebno",font_slova=('Quicksand',10),stil="dark",
            poravnanje="center",pozadina=None,anchor="center",relx=0.5,rely=0.35)

    if slanost > 8:
        label(frame_za_status_biljke,
            tekst="slanost je umjerena",font_slova=('Quicksand',10),stil="dark",
            poravnanje="center",pozadina=None,anchor="center",relx=0.5,rely=0.5)
    else:
        label(frame_za_status_biljke,
            tekst="slanost je niska",font_slova=('Quicksand',10),stil="dark",
            poravnanje="center",pozadina=None,anchor="center",relx=0.5,rely=0.5)
        
    if osvijetljenje < 75:
        label(frame_za_status_biljke,
            tekst="premijestite biljku na svijetlo",font_slova=('Quicksand',10),stil="dark",
            poravnanje="center",pozadina=None,anchor="center",relx=0.5,rely=0.65)
    else:
        label(frame_za_status_biljke,
            tekst="maknite biljku s izravne svijetlosti",font_slova=('Quicksand',10),stil="dark",
            poravnanje="center",pozadina=None,anchor="center",relx=0.5,rely=0.65)
        
    gumb_sinkronizacije(frame_za_status_biljke,lambda:gui_objekt.prozor_s_detaljima_o_biljci(id_slike,command_za_button_BACK=None),
                            padding=8,width=32,x=0,y=115)

def prikaz_statusa_biljke_prema_podacima_sa_senzora(frame_za_tekst_statusa,anchor,relx,rely):
    """ ova funkcija u prozoru gdje se nalaze sve biljke
    prikazuje je li potrebno napraviti nesto 
    s biljkom prije otvaranja prozora s detaljima od biljke"""
    # podaci dohvaceni sa simulatora senzora za vlaznost, kiselost i salinitet zemlje te svijetlost
    # spremljeni u varijable za prikaz na ekranu kod odabrane biljke iz baze
    podaci = dohvati_podatke_sa_senzora() 
    kiselost = podaci[1]["vrijednost"]
    vlaga = podaci[0]["vrijednost"]
    # slanost = podaci[2]["vrijednost"]
    osvijetljenje  = podaci[3]["vrijednost"]

    if kiselost > 7:
        label(frame_za_tekst_statusa,
            tekst="dodaj supstrat",font_slova=('Quicksand',10),stil="dark",
            poravnanje="center",pozadina=None,anchor=anchor,relx=relx,rely=rely)
    elif vlaga < 50:
        label(frame_za_tekst_statusa,
            tekst="zalijte biljku",font_slova=('Quicksand',10),stil="dark",
            poravnanje="center",pozadina=None,anchor=anchor,relx=relx,rely=rely)
    elif osvijetljenje < 75:
        label(frame_za_tekst_statusa,
            tekst="premijestite biljku na svijetlo",font_slova=('Quicksand',10),stil="dark",
            poravnanje="center",pozadina=None,anchor=anchor,relx=relx,rely=rely)
    elif osvijetljenje > 75:
        label(frame_za_tekst_statusa,
            tekst="maknite biljku sa svijetlosti",font_slova=('Quicksand',10),stil="dark",
            poravnanje="center",pozadina=None,anchor=anchor,relx=relx,rely=rely)
    else:
        label(frame_za_tekst_statusa,
            tekst="sve OK",font_slova=('Quicksand',10),stil="dark",
            poravnanje="center",pozadina=None,anchor=anchor,relx=relx,rely=rely)
