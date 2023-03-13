#from sqlalchemy import TextClause
import ttkbootstrap as ttk
from tkinter import Button, Label
from ttkbootstrap.constants import *
from ttkbootstrap import Style
from PIL import ImageTk, Image, ImageFilter
from tkinter.messagebox import showerror, showinfo
from tkinter import filedialog

from SQLAlchemy_seminarski_repo import Biljke, Korisnik,spoji_se_na_bazu


import os

# u ovom fileu se nalaze funkcije koje omogucuju rad izmedu GUI i BAZE

def prikaz_korisnika(frame,session):
    """ ova funkcija u bazi odabire sve korisnike
        te ih ispisuje u obliku tablice prikazujuci njihov
        id, ime i lozinku """
    
    tablica_korisnika=session.execute("SELECT * FROM Korisnici") #TextClause
    e=ttk.Label(frame,width=10,text='userid',
        font="quicksand, 10",borderwidth=2, anchor='center',bootstyle="warning-inverse") #foreground='#0c4f4e', background='#f3f6f4'
    e.grid(row=0,column=0)
    e=ttk.Label(frame,width=10,text='IME',
        font="quicksand, 10",borderwidth=2, anchor='center',bootstyle="warning-inverse")
    e.grid(row=0,column=1)
    e=ttk.Label(frame,width=10,text='LOZINKA',
        font="quicksand, 10",borderwidth=2, anchor='center',bootstyle="warning-inverse")
    e.grid(row=0,column=2)
    i=1
    #i=0 
    for user in tablica_korisnika: 
        for j in range(len(user)):
            prikaz_korisnika = ttk.Label(
                frame, width=15, font="comicsans, 10",
                text=user[j], foreground='gray', borderwidth=2, border=8,
                relief='ridge', anchor="center", bootstyle="light-inverse",background='white')
                
            prikaz_korisnika.grid(row=i, column=j) 
            #e.insert(END, student[j])
        i=i+1

def prikaz_biljke_prema_id_u_bazi(frame,frame_za_tekst,session,id_slike):
    baza_biljaka=session.execute(f"SELECT * FROM biljke where id = {id_slike}") #TextClause # sada uzme id i onda prema njemu otvori biljku
        
    for biljka in baza_biljaka:
        img = dohvati_sliku(width=250, height=165,ime_slike=biljka.slika_biljke)
        if img is not None:
            label_slika = ImageTk.PhotoImage(img)
            slika_biljke = ttk.Label(frame, image=label_slika,bootstyle="light-inverse",borderwidth=0)
            slika_biljke.image = label_slika
            slika_biljke.place(anchor='center', relx=0.2, rely=0.5)
            ubaci_tekst_u_label(frame_za_tekst,ime_slike=biljka.ime_biljke,font="quicksand, 15",bootsytle="dark")

# def provjeri_lozinku(lozinka):
#     """ ova funkcija provjerava duljinu lozinke;
#     trenutno je ne koristim """
#     # ZADATAK dodati metodu za provjeru duljinu lozinke i kompleksnost
#     #print(f"Duljina lozinke je: {len(self.password.get())} znakova")
#     if len(lozinka) < 6:
#         showinfo(title="UPS!", message=f"Duljina vaše lozinke je {len(lozinka)}, \na mora sadržavati najmanje 6 znakova")
#         #print(f"Duljina lozinke je: {len(lozinka)} znakova, a mora biti minimalno 6.")
#     else:
#         return lozinka
    
def dohvati_sliku(width, height,ime_slike):
    if not ime_slike:
        return None
        
    putanja = spoji_sliku_s_folderom(ime_slike)
    if not os.path.exists(putanja):
        return None

    try:
        img = Image.open(putanja) 
        img = img.resize((width, height))
        return img
    except FileNotFoundError:
        return None
    
def spoji_sliku_s_folderom(photo_filename):
    if os.path.exists(photo_filename):
        return photo_filename
    #  puna putanja do foldera sa slikama koji se nalazi odmah uz ovaj file
    folder_sa_slikama = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),   # folder u kojem se nalazi ovaj file
            "SLIKE_BILJAKA"              # folder u koji ćemo spremati slike
        )
    )
    slika_puna_putanja = os.path.join(
        folder_sa_slikama, 
        photo_filename
    )
    return slika_puna_putanja

def ubaci_tekst_u_label(frame,ime_slike,font,bootsytle):
    oznaka = ttk.Label(
        frame, 
        text=f'{ime_slike}',
        justify='left',bootstyle=bootsytle, font=font) #font="quicksand, 10"  # svijetlo zuta - FFE890
    oznaka.place(anchor ='nw', relx=0.05,rely=0.2)

def otvori_i_spremi_sliku_biljke_od_korisnika(repozitorij,ime_nove_biljke):
    """ ova metoda otvara biljku iz foldera korisnika 
        i sprema je u isti folder 
        s imenom koje je korisnik odabrao """
    # otvaranje slike iz foldera
    photo_filename = filedialog.askopenfilename(title ='Open image')
    img = Image.open(str(photo_filename))
    img = img.resize((150, 110))
    label_slika = ImageTk.PhotoImage(img)
    
    # spremanje slike i putanje u folder
    putanja_slike = f'{ime_nove_biljke.get()}.jpg'

    if img:
            nova_slika = f'{ime_nove_biljke.get()}.jpg'
            
            putanja_do_slike = spoji_sliku_s_folderom(nova_slika)
            # na disk spremamo sa punom putanjom da se ne spremi 
            # u folderu iz kjeg je pozvana aplikacija
            img.save(putanja_do_slike)
            img.close()
    else:
            nova_slika = ""
        # u bazu putanju do slike spremamo samo ime slike
    repozitorij.spremi_biljku(Biljke(
                ime_biljke=ime_nove_biljke.get(),
                slika_biljke=nova_slika)
            )
    showinfo(title="YES!", message=f"Slika '{putanja_slike}' uspješno spremljena!")

def provjeri_lozinku(lozinka):
    """ ova funkcija provjerava duljinu lozinke;
    trenutno je ne koristim """
    # ZADATAK dodati metodu za provjeru duljinu lozinke i kompleksnost
    #print(f"Duljina lozinke je: {len(self.password.get())} znakova")
    if len(lozinka) < 6:
        showinfo(title="UPS!", message=f"Duljina vaše lozinke je {len(lozinka)}, \na mora sadržavati najmanje 6 znakova")
        #print(f"Duljina lozinke je: {len(lozinka)} znakova, a mora biti minimalno 6.")
    else:
        return lozinka
    
def spremi_korisnika_korisnicko_ime_i_lozinka(root,repozitorij):
    """ ova metoda piše labele korisnicko ime i lozinka
        te polja za upis korisnickog imena i lozinke """
    oznaka_username = ttk.Label(
        root, text='username', 
        font='quicksand, 14',bootstyle="warning",background='#f3f6f4')
    oznaka_username.place(anchor="center",relx=0.2,rely=0.3)
    
    username = ttk.Entry(root, bootstyle="warning", font = ('quicksand' , 9))
    username.place(anchor="center",relx=0.4,rely=0.3)

    oznaka_lozinka = ttk.Label(
        root, text='password', 
        font="quicksand, 14",bootstyle="warning",background='#f3f6f4')
    oznaka_lozinka.place(anchor="center",relx=0.2,rely=0.4)

    password = ttk.Entry(root, bootstyle="warning",show="*")
    password.place(anchor="center",relx=0.4,rely=0.4,width=154)

    button_ulogiraj = ttk.Button(root, text='registriraj korisnika',
    style='warning.Outline.TButton',
    bootstyle="warning-outline", 
    command=lambda:spremi_korisnika(repozitorij,username,password),
    padding=10, width=30
    ).place(anchor="center",relx=0.3,rely=0.6)


def spremi_korisnika(repozitorij,username,password):
    """ ova metoda prima username i password koji je unio korisnik
        u Entry, provjera postoji li user,
        a ako ga nema sprema ga u bazu"""
    print(f"Username: {username.get()}")
    print(f"Password: {password.get()}")
    username = username.get()
    password = password.get()
    korisnik = repozitorij.get_user_by_username(username)
    if korisnik: 
        showinfo(f"Korisnik {username} već postoji.")
        # PROMISLI SVE OPCIJE LOGINA !
        # user postoji, uđi
        # user postoji, kriva lozinka
        # user ne postoji, upiši ga
        # user ne postoji, krivi login
    else:
        # ZADATAK: Tu dodati provjeru duljine lozinke i/ili kompleksnosti 
        repozitorij.create_user(Korisnik(username=username, password=password))
        provjeri_lozinku(password)
        showinfo(title="Registracija", message=f"Korisnik '{username}' je uspješno spremljen!")
        #self.prikaz_korisnika()
