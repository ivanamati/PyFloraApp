import tkinter as tk
#from sqlalchemy import TextClause
import ttkbootstrap as ttk
from tkinter import Button, Label
from ttkbootstrap.constants import *
from ttkbootstrap import Style
from PIL import ImageTk, Image, ImageFilter
from tkinter.messagebox import showerror, showinfo
from tkinter import filedialog


import os
from SQLAlchemy_seminarski_repo import SQLAlchemyRepozitorij, Korisnik, Biljke, spoji_se_na_bazu
from seminarsi_dohvati_podatke_weba import *


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


class PyFlora:

    def __init__(self, repozitorij):
        # DIO ZA root ELEMENT
        #self.root = tk.Tk()
        self.root = ttk.Window(themename="flatly")
        self.root.title('PyFlora - PRIJAVA')
        self.width = 960
        self.height = 640
        self.root.geometry(f'{self.width}x{self.height}')
        #self.root.geometry('960x540')
        self.root['bg']= '#f3f6f4'
        #self.root['bg']= 'white'
        self.repozitorij = repozitorij

        self.style = ttk.Style()
        #gumb sinkronizacije
        self.style.configure('warning.TButton', font=('Quicksand', 10), borderwidth=0)
        #gumb moj profil 
        self.style.configure('warning.Outline.TButton', font=('Quicksand', 10), borderwidth=0)
        #label u headeru
        self.style.configure('warning.TLabel',font=('Quicksand', 1))
      


    def provjeri_korisnika(self):
        """ 
        ova metoda provjerava postoji li korisnik 
        (u dictu) uskoro u bazi 
        """
        korisnik = self.repozitorij.get_user_by_username(self.username.get())
        if korisnik:
            if self.password.get() == korisnik.password:
                #return True
                print(f"Korisnik {self.username.get()} postoji u bazi. Ulaz slobodan.")
                self.nacrtaj_drugi_prozor(korisnik.username) 
            else: 
                #self.korisnik_postoji_kriva_lozinka()
                showinfo(title="Registracija", message=f"Korisnik '{korisnik.username}' postoji.\n lozinka je neispravna!")
                print(f'Korisnička lozinka je neispravna')
            return True
        else:
            #self.korisnik_ne_postoji()
            showinfo(title="Registracija", message=f"Korisnik '{korisnik.username}' ne postoji!")
            print(f'Korisnik ne postoji')
            #self.prozor_ulaska_login_ili_registracija()
            
    def spremi_korisnika(self):
        print(f"Username: {self.username.get()}")
        print(f"Password: {self.password.get()}")
        username = self.username.get()
        password = self.password.get()
        korisnik = self.repozitorij.get_user_by_username(username)
        if korisnik: 
            showinfo(f"Korisnik {username} već postoji.")
            # PROMISLI SVE OPCIJE LOGINA !
            # user postoji, uđi
            # user postoji, kriva lozinka
            # user ne postoji, upiši ga
            # user ne postoji, krivi login
        else:
            # ZADATAK: Tu dodati provjeru duljine lozinke i/ili kompleksnosti 
            self.repozitorij.create_user(Korisnik(username=username, password=password))
            provjeri_lozinku(password)
            showinfo(title="Registracija", message=f"Korisnik '{username}' je uspješno spremljen!")
            self.prikaz_korisnika()

    def korisnik_postoji_kriva_lozinka(self):
        """ 
            ova metoda se pokrece kada uneseni korisnik postoji,
            ali je unesena i kriva lozinka;
            prikazuje obavijest o krivom unosu 
            i nudi mogucnost povratka na prvi prozor
        """
        self.clear_frame()
        self.pocetna_slikica()
        self.root.title('PyFlora NEUSPJELA PRIJAVA')
        
        prikaz_lozinke = ttk.Label(
            self.root, text=f'Korisnik postoji, ali je unešena pogrešna lozinka. \nPokušajte ponovo!', 
            font="quicksand, 14",bootstyle="warning",background='#f3f6f4'
            )
        prikaz_lozinke.grid(column=2, row=15, padx=45, pady=5)

        frm_action_buttons = ttk.Frame(self.root).grid(
            column=0, columnspan=3, row=4, ipadx=0, ipady=20, padx=10, pady=10
        )
        button_ulogiraj = ttk.Button(
            frm_action_buttons, text='login again', 
            font="quicksand, 14",bootstyle="warning",background='#f3f6f4',
            command=self.nacrtaj_prvi_prozor_login)
        button_ulogiraj.grid(column=0, columnspan=3, row=25, ipadx=15, ipady=10, padx=15, pady=10)

    def korisnik_ne_postoji(self):
        """ 
            ova metoda se pokrece kada uneseni korisnik ne postoji;
            prikazuje obavijest o krivom unosu
            i nudi mogucnost povratka na prvi prozor
        """
        self.clear_frame()
        self.pocetna_slikica()
        self.root.title('PyFlora NEUSPJELA PRIJAVA')
        
        prikaz_lozinke = ttk.Label(
            self.root, text='Korisnik ne postoji. \nPokušajte ponovo!', 
            font="quicksand, 14",bootstyle="warning",background='#f3f6f4'
            ) #forground = boja fonta!
        prikaz_lozinke.grid(column=2, row=15, padx=45, pady=5)

        frm_action_buttons = ttk.Frame(self.root).grid(
            column=0, columnspan=3, row=4, ipadx=0, ipady=20, padx=10, pady=10
        )
        button_ulogiraj = ttk.Button(
            frm_action_buttons, text='login again', 
            font="quicksand, 14",bootstyle="warning",background='#f3f6f4',
            command=self.nacrtaj_prvi_prozor_login)
        button_ulogiraj.grid(column=0, columnspan=3, row=25, ipadx=15, ipady=10, padx=15, pady=10)

    def ispis_neispravne_lozinke(self, lozinka):
        """ 
            ZA SADA NE KORISTIM
            ova metoda ispisuje neispravnu lozinku, 
            ako je manja od 6 znakova;
            sad je ne koristim; 
            korisstila sam je kada nisam imala korisnika
        """
        self.clear_frame()
        self.pocetna_slikica()
        self.root.title('PyFlora - NEUSPJELA PRIJAVA')
        
        prikaz_lozinke = ttk.Label(self.root, text='Pogrešna lozinka! \nVaša lozinka mora sadržavati minimalno 6 znakova.', font=("Times", 12, "italic"), fg='#0c4f4e')
        prikaz_lozinke.grid(column=2, row=15, padx=45, pady=5)
        prikaz_lozinke['bg']='#f3f6f4'
        frm_action_buttons = ttk.Frame(self.root).grid(
            column=0, columnspan=3, row=4, ipadx=0, ipady=20, padx=10, pady=10
        )
        button_ulogiraj = ttk.Button(
            frm_action_buttons, text='login again', font=("Times", 15, "italic"), fg='#0c4f4e',
            command=self.nacrtaj_prvi_prozor)
        button_ulogiraj.grid(column=0, columnspan=3, row=25, ipadx=15, ipady=10, padx=15, pady=10)
        button_ulogiraj['bg']='#b6d7a8'

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def unos_korisnicko_ime_i_lozinka(self):
        """ ova metoda piše labele korisnicko ime i lozinka
            te polja za upis korisnickog imena i lozinke """
        oznaka_username = ttk.Label(
            self.root, text='username', 
            font='quicksand, 14',bootstyle="warning",background='#f3f6f4')
        oznaka_username.place(anchor="center",relx=0.2,rely=0.3)
        
        self.username = ttk.Entry(self.root, bootstyle="warning", font = ('quicksand' , 9))
        self.username.place(anchor="center",relx=0.4,rely=0.3)

        oznaka_lozinka = ttk.Label(
            self.root, text='password', 
            font="quicksand, 14",bootstyle="warning",background='#f3f6f4')
        oznaka_lozinka.place(anchor="center",relx=0.2,rely=0.4)


        self.password = ttk.Entry(self.root, bootstyle="warning",show="*")
        self.password.place(anchor="center",relx=0.4,rely=0.4,width=154)

    def nacrtaj_naslovnicu_aplikacije(self):
        """ ova metoda je naslovnica aplikacije
            s gumbom loga za ulaz u aplikaciju; 
            ovdje samo ulazimo u aplikaciju
        """
        self.clear_frame()
        #self.root.title('PyFlora Aplikacija')
        self.velika_slika_posred_ekrana("media\cvijet.png")

        tekst_pozdrava = ttk.Label(self.root,
                text="Dobrodošli u aplikaciju PyFlora.\nZa ulazak kliknite na cvijetak",
                bootstyle=('dark'),font="quicksand 14",padding=5, anchor="center")
        tekst_pozdrava.place(anchor="s", relx=0.5,rely=0.7,width=800)
        #tekst_pozdrava.pack(fill=X, anchor = "e", expand=YES, padx=5,)

        #labelframe = ttk.LabelFrame(self.root,bootstyle="warning")

        manji_image = Image.open("media\PyFlora_crno_zuta.jpg")
        manja_slika = ImageTk.PhotoImage(manji_image.resize((120,70)))

        # sad je prikazujemo na buttonu
        gumb_sa_slikom = ttk.Button(self.root, 
        image=manja_slika, 
        bootstyle='warning',
        command=self.prozor_ulaska_login_ili_registracija,padding=2)

        gumb_sa_slikom.image = manja_slika
        gumb_sa_slikom.place(anchor="center", relx=0.5,rely=0.35)

    def prozor_ulaska_login_ili_registracija(self):
        """ ova metoda ispisuje prozor 
            koji nudi korisniku opciju LOGINA 
            ili upisa NOVOG korisnika 
            u obliku gumba
        """
        self.clear_frame()
        self.root.title('PyFlora Aplikacija')
        self.root["bg"]="white"
        self.velika_slika_posred_ekrana('media\PyFlora_crno_zuta.jpg')
        
        tekst_pozdrava = ttk.Label(self.root, 
                text="Dobrodošli u aplikaciju PyFlora",
               font=("quicksand", 15, "normal"),
               bootstyle='succes', anchor="center")#, image=self.mali_crno_bijeli_logo(self.root))
        tekst_pozdrava.place(anchor="center", relx=0.5,rely=0.15)

        button_ulogiraj = ttk.Button(
            self.root, style='warning.TButton',
            bootstyle="warning-outline-toolbutton", 
            text ='ulogiraj me', command=self.nacrtaj_prvi_prozor_login, padding=10, width=30
            )
        button_ulogiraj.place(anchor="center",relx=0.5,rely=0.75)

        button_novi_korisnik = ttk.Button(
            self.root, style='warning.Outline.TButton',
            bootstyle="warning-toolbutton",
            text='dodaj novog korisnika',
            command=self.prozor_za_dodavanje_novog_korisnika, padding=10,width=30
            )
        button_novi_korisnik.place(anchor="center",relx=0.5,rely=0.83)
        
    def prozor_za_dodavanje_novog_korisnika(self):
        """
        ova metoda crta prozor u kojem cemo registriati NOVOG korisnika
        upisom korisnickog imena i lozinke
        te ce ga spremiti u bazu
        """
        self.clear_frame()
        self.pocetna_slikica()
        self.nacrtaj_header()
        self.unos_korisnicko_ime_i_lozinka()
        self.root['bg']= '#f3f6f4'

        button_ulogiraj = ttk.Button(
            self.root, text='registriraj korisnika', style='warning.Outline.TButton',bootstyle="warning-toolbutton", 
            command=self.spremi_korisnika,padding=10, width=30)#, bd=3, fg='#0c4f4e',padx=45, pady=10
    
        button_ulogiraj.place(anchor="center",relx=0.3,rely=0.6)

    def nacrtaj_prvi_prozor_login(self): 
        """ 
        ova metoda crta prvi prozor aplikacije u kojem se 
        postojeci korisnik
        LOGIRA u aplikaciju PyFlora
        """
        self.clear_frame()
        self.pocetna_slikica()
        self.nacrtaj_header_prijava()
        self.root['bg']= '#f3f6f4'
        self.unos_korisnicko_ime_i_lozinka()

        button_ulogiraj = ttk.Button(
            self.root, text='login', 
            style='warning.Outline.TButton',
            bootstyle="warning-outline", 
            command=self.dohvati_podatke, padding=10, width=30
            ).place(anchor="center",relx=0.3,rely=0.6)
 
    def nacrtaj_drugi_prozor(self, username):
        """ ova metoda crta prozor u kojem pozdravljamo
            korisnika koji se uspjesno ulogirao 
            i sadrzi gumb za nastavak """
        self.clear_frame()
        self.pocetna_slikica()
        self.nacrtaj_header_prijava()
        self.root.title('PyFlora - Ulaz u PyFlora aplikaciju')
        self.root['bg']= '#f3f6f4'

        # username = self.username.get() - možemo i ovako i onda ne predajemo username u pozivu metode "nacrtaj_drugi_prozor"
        button_za_nastavak = ttk.Button(
            self.root, text="let's go!", style='warning.TButton', bootstyle="warning-outline", 
            command = self.nacrtaj_treci_prozor_moj_profil,padding=10, width=30)
        button_za_nastavak.place(anchor='center',relx=0.5,rely=0.6)

        korisnicko_ime = ttk.Label(
            self.root, 
            text=f'Pozdrav \n{username.capitalize()}!', 
            font="quicksand, 20", bootstyle="light-inverse",background="#f3f6f4"
            )
        korisnicko_ime.place(anchor='center',relx=0.5,rely=0.4)

    def nacrtaj_treci_prozor_moj_profil(self):
        self.clear_frame()
        self.pocetna_slikica()
        self.nacrtaj_header('PyFlora Posuda: Moj Profil')

        # naslov prozora:
        self.root.title ("PyFlora Posuda")

        frame_za_gumbe = ttk.Frame(
            self.root, relief="raised", borderwidth=1, 
            width=250,height=600,cursor="heart",style="warning")
        #frame_za_gumbe.grid(column=1, row=1, padx=5, pady=5)
        frame_za_gumbe.place(anchor='ne', relx=0.6, rely=0.2)

        button_ispis_synca = ttk.Button(frame_za_gumbe, text="popis korisnika", 
            command=self.prikaz_korisnika,bootstyle="warning-outline",padding=10, width=30)
        button_ispis_synca.grid(column=3, columnspan=3, row=2, ipadx=10, ipady=3, padx=15, pady=10, sticky="ew")

        button_prikaz_biljaka = ttk.Button(frame_za_gumbe, text="pogledaj svoje biljke", 
            command=self.prikaz_liste_PyPosuda, bootstyle="warning-outline",padding=10, width=30)
        button_prikaz_biljaka.grid(column=3, columnspan=3, row=3, ipadx=10, ipady=3,padx=10, pady=10, sticky="ew")

        button_podaci = ttk.Button(frame_za_gumbe,text='moji podaci', 
            bootstyle="warning-outline", padding=10, width=30) # nedostaje jos command = ?
        button_podaci.grid(column=3, columnspan=3, row=4, ipadx=10, ipady=3,padx=10, pady=10, sticky="ew")

        button_novi_korisnik = ttk.Button(frame_za_gumbe, text='dodaj novog korisnika', 
            command=self.prozor_za_dodavanje_novog_korisnika, bootstyle="warning-outline", padding=10, width=30)
        button_novi_korisnik.grid(column=3, columnspan=3, row=5, ipadx=10, ipady=3,padx=10, pady=10, sticky="ew")

        button_pocetak = ttk.Button(frame_za_gumbe, text='vrati se na pocetak', 
            command=self.nacrtaj_naslovnicu_aplikacije, bootstyle="warning-outline", padding=10, width=30)
        button_pocetak.grid(column=3, columnspan=3, row=6, ipadx=10, ipady=3,padx=10, pady=10, sticky="ew")

        button_logout = ttk.Button(frame_za_gumbe, text='IZLAZ', 
             command=self.root.destroy, bootstyle="danger-outline", padding=10, width=30)
        button_logout.grid(column=3, columnspan=3, row=7, ipadx=10, ipady=3,padx=10, pady=10, sticky="ew")

    def dodajte_novu_biljku_iz_foldera(self):
        """ ova metoda dodaje i sprema NOVU biljku na gumbu gumb_za_novu_biljku """

        self.clear_frame()
        self.pocetna_slikica()
        self.nacrtaj_header('PyFlora Posuda: Nova biljka')

        ime_nove_biljke = ttk.Label(self.root, text='ime biljke', 
        font='quicksand, 14',bootstyle="warning",background='#f3f6f4')
        #font="quicksand, 13",bootstyle="light-inverse")
        ime_nove_biljke.place(anchor="center",relx=0.2,rely=0.3)
        
        self.ime_nove_biljke = ttk.Entry(self.root, bootstyle="warning")
        self.ime_nove_biljke.place(anchor="center",relx=0.4,rely=0.3)

        slika_nove_biljke = ttk.Label(self.root, text='odaberite sliku',
        font='quicksand, 14',bootstyle="warning",background='#f3f6f4') 
        #font="quicksand, 13",bootstyle="light-inverse" )
        slika_nove_biljke.place(anchor="center",relx=0.2,rely=0.4)

        button_dodaj_novu_sliku= ttk.Button(
            self.root, text='odaberi sliku biljke',  
            command=self.otvori_i_spremi_sliku_biljke_od_korisnika, bootstyle="warning-outline", padding=10, width=20)
        button_dodaj_novu_sliku.place(anchor="center",relx=0.4,rely=0.4)

        #gumb koji ce nas opet povezati na listu s biljkama
        button_prikazi_listu_PyFlora_posuda= ttk.Button(
            self.root, text='POGLEDAJ SVOJE BILJKE',  
            command=self.prikaz_liste_PyPosuda,  bootstyle="warning", padding=10, width=30)
        button_prikazi_listu_PyFlora_posuda.place(anchor="center",relx=0.4,rely=0.6)
        
    def otvori_i_spremi_sliku_biljke_od_korisnika(self):
        """ ova metoda otvara biljku iz foldera korisnika 
            i sprema je u isti folder 
            s imenom koje je korisnik odabrao """
        # otvaranje slike iz foldera
        photo_filename = filedialog.askopenfilename(title ='Open image')
        img = Image.open(str(photo_filename))
        img = img.resize((150, 110))
        label_slika = ImageTk.PhotoImage(img)
        
        # spremanje slike i putanje u folder
        putanja_slike = f'{self.ime_nove_biljke.get()}.jpg'

        if img:
                nova_slika = f'{self.ime_nove_biljke.get()}.jpg'
                
                putanja_do_slike = spoji_sliku_s_folderom(nova_slika)
                # na disk spremamo sa punom putanjom da se ne spremi 
                # u folderu iz kjeg je pozvana aplikacija
                img.save(putanja_do_slike)
                img.close()
        else:
                nova_slika = ""
            # u bazu putanju do slike spremamo samo ime slike
        self.repozitorij.spremi_biljku(Biljke(
                    ime_biljke=self.ime_nove_biljke.get(),
                    slika_biljke=nova_slika)
                )
        showinfo(title="YES!", message=f"Slika '{putanja_slike}' uspješno spremljena!")

    def spremi_novu_biljku_u_bazu(self, ime_nove_biljke, odabrana_slika):
        """ 
            ne koristim za sada:
            ova metoda sprema sliku iz GUI-a u  bazu;
            odabrana slika bi trebala biti ona odabrana slika iz  filea, 
            a ime nove biljke self.ime_nove_biljke.get()
        """
        moja_nova_biljka = Biljke(ime_biljke = ime_nove_biljke, slika_biljke= odabrana_slika)
        self.repozitorij.spremi_biljku(moja_nova_biljka)
        pass

    def gumb_sinkronizacije(self):
        """ ova metoda sada ne radi ništa;
            prije je povezivala gui s bazom;
            radi sinkronizaciju biljaka """
        self.pocetna_slikica()

        gumb_sinkronizacije = ttk.Button(self.root,
                        text="sinkronizacija", 
                        #command=main(ime_baze="SQLite_Baza_PyFlora.sqlite"),
                        style="warning.TButton",
                        padding=10, width=16)
        gumb_sinkronizacije.place(x=766,y=70)


    def nacrtaj_header(self, tekst):
        self.pocetna_slikica()
        self.gumb_sinkronizacije()

        header  =  ttk.Frame(self.root,  width=1060,  height=60, relief='groove', borderwidth= 1,style="light")
        header.place(anchor='nw')
        tekst = ttk.Label(self.root, 
                text= tekst,
                font="warning.TLabel",
                bootstyle="light-inverse")
        #tekst['bg']='#d9ead3' #background color
        tekst.place(anchor="nw",relx = 0.1, rely=0.025)

        manji_image = Image.open("media\PyFlora_crno_zuta.jpg")
        manja_slika = ImageTk.PhotoImage(manji_image.resize((75,50)))
        # drugo - predajemo sliku labelu (mozemo i buttonu i pozadini i...)
        label_sa_slikom = ttk.Label(self.root, image=manja_slika,borderwidth=0)
        label_sa_slikom.image = manja_slika
        # trece - postavljamo je na ekranu; radi i place i pack
        label_sa_slikom.place(anchor="nw", relx = 0.005,rely=0.0085)

        gumb_moj_profil = ttk.Button(header,
                        text="moj profil", 
                        #bootstyle= "warning-outline-toolbutton",
                        style='warning.Outline.TButton',
                        command= self.nacrtaj_treci_prozor_moj_profil, padding=10, width=16)
        gumb_moj_profil.place(x=766,y=11)#relwidth=0.3)
   
    def nacrtaj_header_prijava(self):
        self.pocetna_slikica()
        #self.root['bg']= '#f3f6f4'
        
        header  =  ttk.Frame(self.root,  width=1060,  height=60, relief='groove', borderwidth= 1,style="light")
        header.place(anchor='nw')
        tekst = ttk.Label(self.root, 
                text='PyFlora Posuda: Prijava ',
                font="warning.TLabel",
                bootstyle="light-inverse")
        #tekst['bg']='#d9ead3' #background color
        tekst.place(anchor="nw",relx = 0.1, rely=0.025)

        manji_image = Image.open("media\PyFlora_crno_zuta.jpg")
        manja_slika = ImageTk.PhotoImage(manji_image.resize((75,50)))
        # drugo - predajemo sliku labelu (mozemo i buttonu i pozadini i...)
        label_sa_slikom = ttk.Label(self.root, image=manja_slika,borderwidth=0)
        label_sa_slikom.image = manja_slika
        # trece - postavljamo je na ekranu; radi i place i pack
        label_sa_slikom.place(anchor="nw", relx = 0.005,rely=0.0085)

    def dohvati_sliku(self, width, height,ime_slike):
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

    def ubaci_sliku_u_label(self, neki_frame, putanja_slike):
        img= self.dohvati_sliku(width=115, height=75,ime_slike=putanja_slike)
        if img is not None:
            label_slika = ImageTk.PhotoImage(img)
            #slika_livo = ttk.Label(neki_frame, image=label_slika,bootstyle="light-inverse",borderwidth=0)
            # da gumb bude ovdje?!
            slika_livo = ttk.Button(neki_frame,image=label_slika,bootstyle="warning",
                                    padding=2,command=self.prikaz_detalja_o_biljci) 
            slika_livo.image = label_slika
            slika_livo.place(anchor='center', relx=0.5, rely=0.5)
        else:
            self.ubaci_tekst_u_label(neki_frame, f"Slika\n {putanja_slike}\n nije pronađena",font="quicksand, 10",bootsytle="warning")

    def ubaci_tekst_u_label(self, neki_frame,ime_slike,font,bootsytle):
        oznaka = ttk.Label(
            neki_frame, 
            text=f'{ime_slike}',
            justify='left',bootstyle=bootsytle, font=font) #font="quicksand, 10"  # svijetlo zuta - FFE890
        oznaka.place(anchor ='nw', relx=0.05,rely=0.2)



    def dodaj_redak(self, redni_broj, stupac, broj_stupaca):
        #frame_pape = tk.Frame(self.root, width=250, height=150, bd=1, relief="solid")
        frame_pape  =  ttk.Frame(
            self.root,  width=300,  height=250, borderwidth=3, 
            relief='raised', style="dark")
        frame_pape.grid(
            row=redni_broj, 
            column=stupac, 
            columnspan=broj_stupaca, 
            padx=31, pady=110,
        )
        return frame_pape

    def dodaj_frame(self, parent_frame,  red, stupac, style):
        frame_child = ttk.Frame(
            parent_frame, 
            width=125, height=175, borderwidth=0, relief="flat", style=style
            )
        frame_child.grid(row=red, column=stupac)
        return frame_child

    def prikaz_liste_PyPosuda(self):

        self.root.title ("PyFlora Posuda: ovo su vaše biljke")
        self.clear_frame()
        self.pocetna_slikica()
        self.nacrtaj_header("PyFlora Posuda: Biljke") 

        baza_biljaka=session.execute("SELECT * FROM biljke")#(TextClause("SELECT * FROM biljke"))
        stupac = 0
        redak = 0
        
        for biljka in baza_biljaka: 
            # frameovi
            glavni_frame  =  ttk.Frame(self.root,  width=300,  height=200, borderwidth=1, relief='raised', style="deafult")
            glavni_frame.grid(row=redak, column=stupac, padx=31, pady=70) #pady=110
            # pape = self.dodaj_redak(redak,stupac*2,1)
            lijevi_frame = self.dodaj_frame(glavni_frame,redak,0,"warning")    # svijetlo zuta - FFE890
            desni_frame = self.dodaj_frame(glavni_frame,redak,1,"default")   # svijetlo zuta - FFE890
            
            self.ubaci_sliku_u_label(lijevi_frame, putanja_slike=biljka.slika_biljke) 
            self.ubaci_tekst_u_label(desni_frame, biljka.ime_biljke,font="quicksand, 10",bootsytle="warning")
            

            #PITANJE ZA UCU
            # kako dohvatiti podatke bas od te biljke? 
            # kako to povezati s bazom? treba li gumb staviti kada dohvacamo prvi  put biljke?
            
            # gumb_info_livo = ttk.Button(dite_livo,text="INFO",bootstyle="warning",
            #                         padding=2,command=self.prikaz_detalja_o_biljci) 
            # gumb_info_livo.place(anchor="center",relx=0.5,rely=0.85)
            status_biljke = ttk.Label(desni_frame, text='Status: ',font="quicksand, 8", bootstyle= "default", justify='left')   # svijetlo zuta - FFE890
            status_biljke.place(anchor ='s',relx=0.3,rely=0.95)
            
            stupac += 1
                     
            if stupac >= 2:
                redak +=1
                stupac = 0 
        self.dodajmo_novu_biljku_na_listu(redak,stupac)

    def dodajmo_novu_biljku_na_listu(self,redak,stupac):
        """ ova metoda crta okvir i 
            gumb za dodavanje nove biljke u bazu
            iz foldera koji ce odabrati korisnik"""
        novi_frame = self.dodaj_frame_za_novu_biljku(redak,stupac)
        self.gumb_za_novu_biljku(novi_frame)

    def dodaj_frame_za_novu_biljku(self,redni_broj,stupac):# broj_stupaca):
        frame_za_novu_biljku = ttk.Frame(
            self.root,  width=280,  height=180, 
            borderwidth=2, relief='raised', style="deafult") #bg='#AFE1AF'
        frame_za_novu_biljku.grid(row=redni_broj, column=stupac, 
            #columnspan=broj_stupaca, 
            padx=10, pady=70)
        self.mali_crno_bijeli_logo(frame_za_novu_biljku)
        return frame_za_novu_biljku
    
    def gumb_za_novu_biljku(self, frame): # ne radi promjena pozadinske boje gumba! ZASTO???
        button_nova_biljka = ttk.Button(frame,text="nova biljka", 
            command=self.dodajte_novu_biljku_iz_foldera,
            padding=10,width=10,bootstyle="warning-outline-toolbutton") 
        button_nova_biljka.grid(column=0, columnspan=3, row=1, ipadx=16, ipady=13, padx=70, pady=55)

    def prikaz_detalja_o_biljci(self):
        """ ova metoda crta prozor 
            na kojem se prikazuju detalji o biljci """
        
        self.root.title ("PyFlora Posuda: Biljke")
        self.clear_frame()
        self.pocetna_slikica()
        self.nacrtaj_header("PyFlora Posuda: Biljka") 

        frame_za_tekst = ttk.Frame(self.root, width=90,height=40,padding=2,borderwidth=0)
        frame_za_tekst.place(anchor="center",relx=0.2,rely=0.2)
        # kako spojiti odabranu sliku klikom na gumb s bazom i detaljima o biljci???
        baza_biljaka=session.execute("SELECT * FROM biljke")#(TextClause("SELECT * FROM biljke"))
        
        for biljka in baza_biljaka:
            img = self.dohvati_sliku(width=250, height=165,ime_slike=biljka.slika_biljke)
            if img is not None:
                label_slika = ImageTk.PhotoImage(img)
                slika_biljke = ttk.Label(self.root, image=label_slika,bootstyle="light-inverse",borderwidth=0)
                slika_biljke.image = label_slika
                slika_biljke.place(anchor='center', relx=0.2, rely=0.5)
                self.ubaci_tekst_u_label(frame_za_tekst,ime_slike=biljka.ime_biljke,font="quicksand, 15",bootsytle="dark")


    def mali_crno_bijeli_logo(self,frame_za_logo):
        manji_image = Image.open("media\PyFlora_crno_bijela.jpg")
        manja_slika = ImageTk.PhotoImage(manji_image.resize((75,50)))
        # drugo - predajemo sliku labelu (mozemo i buttonu i pozadini i...)
        label_sa_slikom = ttk.Label(frame_za_logo, image=manja_slika,relief='flat',style="warning")
        label_sa_slikom.image = manja_slika
        #label_sa_slikom.place(anchor="center",relx=0.5,rely=0.5)
        # trece - postavljamo je na ekranu; radi i place i pack
        label_sa_slikom.place(anchor="nw", relx = 0.65,rely=0.005)
 
    def prikaz_korisnika(self):

        self.clear_frame()
        self.pocetna_slikica()
        self.nacrtaj_header("PyFlora: Popis korisnika aplikacije")
        # frame za prikaz korisnika
        prvi_frame = ttk.Frame(self.root, style="warning", borderwidth=2, width=250,height=200,cursor="heart")
        #prvi_frame.grid(column=1, row=0, padx=10, pady=10)
        prvi_frame.place(anchor='center', relx= 0.3,rely=0.5)
       
        tablica_korisnika=session.execute("SELECT * FROM Korisnici")
        e=ttk.Label(prvi_frame,width=10,text='userid',
            font="quicksand, 10",borderwidth=2, anchor='center',bootstyle="warning-inverse") #foreground='#0c4f4e', background='#f3f6f4'
        e.grid(row=0,column=0)
        e=ttk.Label(prvi_frame,width=10,text='IME',
            font="quicksand, 10",borderwidth=2, anchor='center',bootstyle="warning-inverse")
        e.grid(row=0,column=1)
        e=ttk.Label(prvi_frame,width=10,text='LOZINKA',
            font="quicksand, 10",borderwidth=2, anchor='center',bootstyle="warning-inverse")
        e.grid(row=0,column=2)
        i=1
        #i=0 
        for user in tablica_korisnika: 
            for j in range(len(user)):
                prikaz_korisnika = ttk.Label(
                    prvi_frame, width=15, font="comicsans, 10",
                    text=user[j], foreground='gray', borderwidth=2, border=8,
                    relief='ridge', anchor="center", bootstyle="light-inverse",background='white')
                    
                prikaz_korisnika.grid(row=i, column=j) 
             #e.insert(END, student[j])
            i=i+1
        #frame za gumbe za povratak i login
        # frame_za_gumbe = ttk.Frame(self.root, 
        #     relief="raised", borderwidth=0, style="light", 
        #     width=250,height=200,cursor="heart")
        # #frame_za_gumbe.grid(column=1, row=1, padx=5, pady=5)
        # frame_za_gumbe.place(anchor='ne', relx=0.55, rely=0.7)

        # button_povratak = ttk.Button(self.root, text="vrati se", 
        #     padding=10,width=10,bootstyle="warning-toolbutton",
        #     command=self.nacrtaj_treci_prozor_moj_profil,)
        # button_povratak.place(x=400,y=500)
        #button_povratak.grid(column=0, columnspan=3, row=8, ipadx=38, ipady=3, padx=10, pady=10)


    def dohvati_podatke(self):
        """ ispisati podatke iz username-a i lozinke"""
        print(f"Username: {self.username.get()}")
        print(f"Password: {self.password.get()}")
        #self.provjeri_lozinku(self.password.get())
        # if provjeri_lozinku(self.password.get()):
        #     self.nacrtaj_drugi_prozor()
        # else:
        #     self.ispis_neispravne_lozinke(lozinka=self.password.get())
        self.provjeri_korisnika()

    def pocetna_slikica(self):
        """ ova metoda prikazuje odabranu sliku kao pozadinu prozora """
        slika = ImageTk.PhotoImage(Image.open("media\cvijet.png"))
        label1 = ttk.Label(image = slika, borderwidth=0)
        label1.image = slika
        label1.place(anchor='w', relx=0.5, rely=0.5)

    def velika_slika_posred_ekrana(self,slika):
        self.root.title('PyFlora Aplikacija')
        img = Image.open(slika)
        #img = img.filter(ImageFilter.BLUR)
        slika = ImageTk.PhotoImage(img)
        
        label_sa_slikom = ttk.Label(self.root, image=slika, borderwidth=0)
        label_sa_slikom.image = slika
        # trece - postavljamo je na ekranu; radi i place i pack
        #label_sa_slikom.pack(anchor ="center", fill=Y, expand=YES)
        label_sa_slikom.place(anchor="center",relx=0.5,rely=0.5)  #rely=0.55

    def nacrtaj_biljku_i_tekst(self):
        """ ova metoda je samo za probu i vjezbu crtanja framova sa slikom i tekstom iz baze"""
        self.clear_frame()
        # PRVA BILJKA S TEKSTOM
        frame_pape=ttk.Frame(self.root,width=250, height=150, bd=1, relief="flat", bg="#b6d7a8")
        frame_pape.grid(row=1,column=0,columnspan=2)

        frame_dite_lite = ttk.Frame(self.root,width=125, height=150, bd=1, relief="ridge", bg="gray")
        frame_dite_lite.grid(row=1,column=0,padx=5,pady=5)

        frame_dite_desno=ttk.Frame(self.root,width=125, height=150, bd=1, relief="ridge", bg="white")
        frame_dite_desno.grid(row=1,column=1,padx=5,pady=5)

        # manji_image = ImageTk.PhotoImage(Image.open("cvijet_mali.png"))
        
        # dohvatila sam imena slika iz baze
        tablica_biljke=session.execute("SELECT * FROM biljke")
        #ispisujem ime slike iz baze, 
        # ali sad je u svakom frameu isti naziv i ispisuje samo zadnje dodanu sliku...
        for red in tablica_biljke: 
            print(red)
            ime_slike = red[1]
            putanja_slike = red[2]

            oznaka = ttk.Label(
                frame_dite_desno, 
                text=f'{ime_slike}',
                font=("calibre", 10, "normal"), 
                fg='#0c4f4e')
            oznaka.place(anchor ='center', relx=0.5, rely=0.5)

            
            # slika u lijevom dijelu frame
            manji_image = Image.open(putanja_slike)
            #manji_image = Image.open()
            #manji_image = Image.open(repozitorij.slika_biljke())
            manja_slika = ImageTk.PhotoImage(manji_image.resize((100,75)))

            label_sa_slikom = ttk.Label(frame_dite_lite, image=manja_slika)
            label_sa_slikom.image = manja_slika
            label_sa_slikom.place(anchor="center", relx=0.5, rely=0.5)

            #tekst u desnom dijelu framea
            tekst = ttk.Label(frame_dite_desno, text='biljka 1',font=("calibre", 10, "normal"), fg='#0c4f4e')#padx=10,pady=10)
            tekst['bg']='#f3f6f4' #background color
            tekst.place(anchor="center",relx=0.5, rely=0.5) # polozaj teksta
   
    def pokreni(self):
        #self.nacrtaj_naslovnicu_aplikacije()
        #self.prikaz_korisnika()
        #self.proba_bootstrap()
        #self.nacrtaj_naslovnicu_aplikacije()
        #self.prozor_ulaska_login_ili_registracija()
        #self.prozor_za_dodavanje_novog_korisnika()
        #self.nacrtaj_prvi_prozor_login()
        #self.nacrtaj_treci_prozor_moj_profil()
        #self.nacrtaj_cetvrti_prozor()
        self.prikaz_liste_PyPosuda()
        #self.moj_profil_opcije()
        #self.dodajte_novu_biljku_iz_foldera()
        #self.prikaz_sadrzaja_synca_autori()
        #self.nacrtaj_prozor_s_biljkama()
        #self.nacrtaj_biljku_i_tekst() # ovo je samo proba!
        self.root.mainloop()
        

session = spoji_se_na_bazu("SQLite_Baza_PyFlora.sqlite")
repozitorij = SQLAlchemyRepozitorij(session)

if __name__ == "__main__":
    gui_program = PyFlora(repozitorij=repozitorij)
    gui_program.pokreni()



