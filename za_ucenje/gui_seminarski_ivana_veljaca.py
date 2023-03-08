import tkinter as tk
from PIL import ImageTk, Image, ImageFilter
from tkinter.messagebox import showerror, showinfo
from tkinter import filedialog
import requests
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
        self.root = tk.Tk()
        self.root.title('PyFlora - PRIJAVA')
        self.width = 960
        self.height = 640
        self.root.geometry(f'{self.width}x{self.height}')
        #self.root.geometry('960x540')
        self.root['bg']= '#f3f6f4'
        #self.root['bg']= 'white'
        self.repozitorij = repozitorij



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
                self.korisnik_postoji_kriva_lozinka()
                print(f'Korisnička lozinka je neispravna')
            return True
        else:
            self.korisnik_ne_postoji()
            print(f'Korisnik ne postoji')
            
    def spremi_korisnika(self):
        print(f"Username: {self.username.get()}")
        print(f"Password: {self.password.get()}")
        username = self.username.get()
        password = self.password.get()
        korisnik = self.repozitorij.get_user_by_username(username)
        if korisnik: 
            showinfo(f"Korisnik {username} već postoji.")
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
        self.root.title('PyFlora - NEUSPJELA PRIJAVA')
        
        prikaz_lozinke = tk.Label(
            self.root, text=f'Korisnik postoji, ali je unešena pogrešna lozinka. \nPokušajte ponovo!', 
            font=("Times", 12, "italic"), fg='#0c4f4e'
            )
        prikaz_lozinke.grid(column=2, row=15, padx=45, pady=5)
        prikaz_lozinke['bg']='#f3f6f4'
        frm_action_buttons = tk.Frame(self.root).grid(
            column=0, columnspan=3, row=4, ipadx=0, ipady=20, padx=10, pady=10
        )
        button_ulogiraj = tk.Button(
            frm_action_buttons, text='login again', font=("Times", 15, "italic"), fg='#0c4f4e',
            command=self.nacrtaj_prvi_prozor)
        button_ulogiraj.grid(column=0, columnspan=3, row=25, ipadx=15, ipady=10, padx=15, pady=10)
        button_ulogiraj['bg']='#b6d7a8'

    def korisnik_ne_postoji(self):
        """ 
            ova metoda se pokrece kada uneseni korisnik ne postoji;
            prikazuje obavijest o krivom unosu
            i nudi mogucnost povratka na prvi prozor
        """
        self.clear_frame()
        self.pocetna_slikica()
        self.root.title('PyFlora - NEUSPJELA PRIJAVA')
        
        prikaz_lozinke = tk.Label(
            self.root, text='Korisnik ne postoji. \nPokušajte ponovo!', 
            font=("quicksand", 12, "italic"),fg='#0c4f4e'
            )
        prikaz_lozinke.grid(column=2, row=15, padx=45, pady=5)
        prikaz_lozinke['bg']='#f3f6f4'
        frm_action_buttons = tk.Frame(self.root).grid(
            column=0, columnspan=3, row=4, ipadx=0, ipady=20, padx=10, pady=10
        )
        button_ulogiraj = tk.Button(
            frm_action_buttons, text='login again', font=("quicksand", 15, "italic"), fg='#0c4f4e',
            command=self.nacrtaj_prvi_prozor)
        button_ulogiraj.grid(column=0, columnspan=3, row=25, ipadx=15, ipady=10, padx=15, pady=10)
        button_ulogiraj['bg']='#b6d7a8'

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
        
        prikaz_lozinke = tk.Label(self.root, text='Pogrešna lozinka! \nVaša lozinka mora sadržavati minimalno 6 znakova.', font=("Times", 12, "italic"), fg='#0c4f4e')
        prikaz_lozinke.grid(column=2, row=15, padx=45, pady=5)
        prikaz_lozinke['bg']='#f3f6f4'
        frm_action_buttons = tk.Frame(self.root).grid(
            column=0, columnspan=3, row=4, ipadx=0, ipady=20, padx=10, pady=10
        )
        button_ulogiraj = tk.Button(
            frm_action_buttons, text='login again', font=("Times", 15, "italic"), fg='#0c4f4e',
            command=self.nacrtaj_prvi_prozor)
        button_ulogiraj.grid(column=0, columnspan=3, row=25, ipadx=15, ipady=10, padx=15, pady=10)
        button_ulogiraj['bg']='#b6d7a8'

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def nacrtaj_naslovnicu_aplikacije(self):
        """ ova metoda je naslovnica aplikacije
            s gumbom loga za ulaz u aplikaciju 
        """
            
        self.root.title('PyFlora Aplikacija')
        self.velika_slika_posred_ekrana("cvijet.png")

        tekst_pozdrava = tk.Label(self.root, 
                text="Dobrodošli u aplikaciju PyFlora.\nZa ulazak kliknite na cvijetak",
                fg="#312520", font=("quicksand", 15, "normal"),bg="white")
        tekst_pozdrava.place(anchor="center", relx=0.5,rely=0.7)

        manji_image = Image.open("PyFlora_crno_zuta.jpg")
        manja_slika = ImageTk.PhotoImage(manji_image.resize((100,55)))

        # sad je prikazujemo na buttonu
        gumb_sa_slikom = tk.Button(self.root, image=manja_slika, command=self.prozor_ulaska_login)
        gumb_sa_slikom.image = manja_slika
        gumb_sa_slikom.place(anchor="center", relx=0.5,rely=0.45)

    def prozor_ulaska_login(self):
        """ ova metoda ispisuje prozor 
            koji nudi korisniku opciju LOGINA 
            ili upisa NOVOG korisnika 
            u obliku gumba
        """

        self.clear_frame()
        self.root.title('PyFlora Aplikacija')
        self.root["bg"]="white"
        self.velika_slika_posred_ekrana('PyFlora_crno_zuta.jpg')
        
        tekst_pozdrava = tk.Label(self.root, 
                text="Dobrodošli u aplikaciju PyFlora",
                fg="#312520", font=("quicksand", 15, "normal"),bg="white")#, image=self.mali_crno_bijeli_logo(self.root))
        tekst_pozdrava.place(anchor="center", relx=0.5,rely=0.2)

        manji_image = Image.open("PyFlora_crno_zuta.jpg")
        manja_slika = ImageTk.PhotoImage(manji_image.resize((100,55)))

        button_ulogiraj = tk.Button(
            self.root, text='ulogiraj me', font=("quicksand", 12, "normal"), 
            command=self.nacrtaj_prvi_prozor, bd=3, fg='#0c4f4e',padx=45, pady=3
            )
        button_ulogiraj.place(anchor="center",relx=0.5,rely=0.71)
        button_ulogiraj["bg"]="#FFE890"
        # svijetlo narancasta boja
        # button_ulogiraj['bg']='#FFCF79'

        button_novi_korisnik = tk.Button(
            self.root, text='dodaj novog korisnika', font=("quicksand", 12, "normal"), 
            command=self.prozor_za_dodavanje_novog_korisnika, bd=3, fg='#0c4f4e',padx=45, pady=2
            )
        button_novi_korisnik.place(anchor="center",relx=0.5,rely=0.8)
        button_novi_korisnik["bg"]="#FFCF79"

    def prozor_za_dodavanje_novog_korisnika(self):
        """
        ova metoda crta prozor u kojem cemo registriati NOVOG korisnika
        upisom korisnickog imena i lozinke
        te ce ga spremiti u bazu
        """
        self.clear_frame()
        self.pocetna_slikica()
        self.nacrtaj_header_prijava()
        # self.root['bg']= '#f3f6f4'

        oznaka_username = tk.Label(self.root, text='username', font=("quicksand", 15, "normal"),fg='#0c4f4e')
        oznaka_username.place(anchor="center",relx=0.2,rely=0.3)
        oznaka_username['bg']='#f3f6f4'
        
        self.username = tk.Entry(self.root, bd=3, relief="ridge", fg='#312520')
        self.username.place(anchor="center",relx=0.4,rely=0.3)
        self.username['bg']='#d9ead3'

        oznaka_lozinka = tk.Label(self.root, text='password', font=("quicksand", 15, "normal"), fg='#0c4f4e')
        oznaka_lozinka.place(anchor="center",relx=0.2,rely=0.4)
        oznaka_lozinka['bg']='#f3f6f4'

        self.password = tk.Entry(self.root, bd=3, relief="ridge", show="*",)
        self.password.place(anchor="center",relx=0.4,rely=0.4)
        self.password['bg']='#d9ead3'

        button_ulogiraj = tk.Button(
            self.root, text='registriraj korisnika', font=("quicksand", 12, "normal"), 
            command=self.spremi_korisnika, bd=3, fg='#0c4f4e',padx=45, pady=10
            )
        button_ulogiraj.place(anchor="center",relx=0.3,rely=0.6)
        button_ulogiraj["bg"]="#FFE890"
        # svijetlo narancasta boja
        # button_ulogiraj['bg']='#FFCF79'

        # button_novi_korisnik = tk.Button(
        #     self.root, text='novi korisnik', font=("quicksand", 12, "normal"), 
        #     command=self.spremi_korisnika, bd=3, fg='#0c4f4e',padx=45, pady=10
        #     )
        # button_novi_korisnik.place(anchor="center",relx=0.3,rely=0.7)
        # button_novi_korisnik["bg"]="#FFCF79"

    def nacrtaj_prvi_prozor(self): 
        """ 
        ova metoda crta prvi prozor aplikacije u kojem se 
        postojeci korisnik
        LOGIRA u aplikaciju PyFlora
        """
        self.clear_frame()
        self.pocetna_slikica()
        self.nacrtaj_header_prijava()
        # self.root['bg']= '#f3f6f4'

        oznaka_username = tk.Label(self.root, text='username', font=("quicksand", 15, "normal"),fg='#0c4f4e')
        oznaka_username.place(anchor="center",relx=0.2,rely=0.3)
        oznaka_username['bg']='#f3f6f4'
        
        self.username = tk.Entry(self.root, bd=3, relief="ridge", fg='#312520')
        self.username.place(anchor="center",relx=0.4,rely=0.3)
        self.username['bg']='#d9ead3'

        oznaka_lozinka = tk.Label(self.root, text='password', font=("quicksand", 15, "normal"), fg='#0c4f4e')
        oznaka_lozinka.place(anchor="center",relx=0.2,rely=0.4)
        oznaka_lozinka['bg']='#f3f6f4'

        self.password = tk.Entry(self.root, bd=3, relief="ridge", show="*",)
        self.password.place(anchor="center",relx=0.4,rely=0.4)
        self.password['bg']='#d9ead3'

        button_ulogiraj = tk.Button(
            self.root, text='login', font=("quicksand", 12, "normal"), 
            command=self.dohvati_podatke, bd=3, fg='#0c4f4e',padx=45, pady=10
            )
        button_ulogiraj.place(anchor="center",relx=0.3,rely=0.6)
        button_ulogiraj["bg"]="#FFE890"
        # svijetlo narancasta boja
        # button_ulogiraj['bg']='#FFCF79'

        # manji_image = Image.open("cvijet_mali.png")
        # manja_slika = ImageTk.PhotoImage(manji_image.resize((75,50)))

        # gumb_sa_slikom = tk.Button(frame, image=manji_image)
        # gumb_sa_slikom.image = manja_slika
        # gumb_sa_slikom.pack()
        
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
        button_za_nastavak = tk.Button(
            self.root, text="let's go!", 
            font=("quicksand", 12, "normal"), fg='#0c4f4e',
            command=self.nacrtaj_treci_prozor,padx=45,pady=10)
        #button_povratak.grid(column=0, columnspan=3, row=15, ipadx=15, ipady=10, padx=25,pady=20)
        button_za_nastavak.place(anchor='center',relx=0.5,rely=0.6)
        button_za_nastavak['bg']='#FFE890'

        korisnicko_ime = tk.Label(
            self.root, text=f'Pozdrav \n{username.capitalize()}!', 
            font=("quicksand", 25, "normal"), fg='#0c4f4e', padx=10,pady=10
            )
        #oznaka = tk.Label(self.root, text='Drugi prozor', font=("Times", 15, "italic"))
        korisnicko_ime['bg']='#f3f6f4'
        korisnicko_ime.place(anchor='center',relx=0.5,rely=0.4)
        #korisnicko_ime.grid(column=2, row=10, padx=5, pady=5)

    def nacrtaj_treci_prozor(self):
        self.clear_frame()
        self.pocetna_slikica()
        self.nacrtaj_header('PyFlora Posuda: Biljke')

        # naslov prozora:
        self.root.title ("PyFlora Posuda              Biljke")

        frame_za_gumbe = tk.Frame(self.root,bg='#f3f6f4',relief="raised", borderwidth=1, width=250,height=200,cursor="heart")
        #frame_za_gumbe.grid(column=1, row=1, padx=5, pady=5)
        frame_za_gumbe.place(anchor='ne', relx=0.55, rely=0.35)


        button_ispis_synca = tk.Button(frame_za_gumbe, text="popis korisnika", 
            font=("quicksand", 12, "normal"), fg='#0c4f4e', command=self.prikaz_korisnika)
        button_ispis_synca.grid(column=3, columnspan=3, row=2, ipadx=10, ipady=3, padx=15, pady=10, sticky="ew")
        button_ispis_synca['bg']='#FFE890'


        button_prikaz_biljaka = tk.Button(frame_za_gumbe, text="pogledaj svoje biljke", 
            font=("quicksand", 12, "normal"), fg='#0c4f4e', command=self.prikaz_liste_PyPosuda)
        button_prikaz_biljaka.grid(column=3, columnspan=3, row=10, ipadx=10, ipady=3,padx=10, pady=10, sticky="ew")
        button_prikaz_biljaka['bg']='#FFE890'

    def nacrtaj_cetvrti_prozor(self): 
        """ ova metoda za sada ne radi NISTA """
        self.root.title ("PyFlora Posuda: ovo su vaše biljke")
        self.clear_frame()
        self.pocetna_slikica()
        self.nacrtaj_header('PyFlora Posuda: Biljke')

    def upisi_novu_biljku(self):
        """ NE KORISTIMO !!!!!!!!
        ova metoda dodaje i sprema NOVU biljku na gumbu gumb_za_novu_biljku """

        self.clear_frame()
        self.pocetna_slikica()
        self.nacrtaj_header('PyFlora Posuda: Nova biljka')

        ime_nove_biljke = tk.Label(self.root, text='imenujte biljku', font=("quicksand", 15, "normal"),fg='#0c4f4e')
        ime_nove_biljke.place(anchor="center",relx=0.2,rely=0.3)
        ime_nove_biljke['bg']='#f3f6f4'
        
        self.ime_nove_biljke = tk.Entry(self.root, bd=3, relief="ridge", fg='#312520')
        self.ime_nove_biljke.place(anchor="center",relx=0.4,rely=0.3)
        self.ime_nove_biljke['bg']='#d9ead3'

        button_odaberi_i_dodaj_novu_sliku= tk.Button(
            self.root, text='odaberi sliku za prikaz \ncvijeta', font=("quicksand", 10, "normal"), 
            command=self.otvori_i_spremi_sliku_biljke_od_korisnika, bd=3, fg='#0c4f4e',padx=45, pady=10
            )
        button_odaberi_i_dodaj_novu_sliku.place(anchor="center",relx=0.3,rely=0.5)
        button_odaberi_i_dodaj_novu_sliku['bg']='#b6d7a8'


    def dodajte_novu_biljku_iz_foldera(self):
        """ ova metoda dodaje i sprema NOVU biljku na gumbu gumb_za_novu_biljku """

        self.clear_frame()
        self.pocetna_slikica()
        self.nacrtaj_header('PyFlora Posuda: Nova biljka')

        ime_nove_biljke = tk.Label(self.root, text='ime biljke', font=("quicksand", 15, "normal"),fg='#0c4f4e')
        ime_nove_biljke.place(anchor="center",relx=0.2,rely=0.3)
        ime_nove_biljke['bg']='#f3f6f4'
        
        self.ime_nove_biljke = tk.Entry(self.root, bd=3, relief="ridge", fg='#312520')
        self.ime_nove_biljke.place(anchor="center",relx=0.4,rely=0.3)
        self.ime_nove_biljke['bg']='#d9ead3'

        slika_nove_biljke = tk.Label(self.root, text='odaberite sliku', font=("quicksand", 15, "normal"), fg='#0c4f4e')
        slika_nove_biljke.place(anchor="center",relx=0.2,rely=0.4)
        slika_nove_biljke['bg']='#f3f6f4'

        # self.slika_nove_biljke = tk.Entry(self.root, bd=3, relief="ridge")
        # self.slika_nove_biljke.place(anchor="center",relx=0.4,rely=0.4)
        # self.slika_nove_biljke['bg']='#d9ead3'

        button_dodaj_novu_sliku= tk.Button(
            self.root, text='odaberi sliku biljke', font=("quicksand", 10, "normal"), 
            command=self.otvori_i_spremi_sliku_biljke_od_korisnika, bd=3, fg='#0c4f4e',padx=45, pady=10
            )
        button_dodaj_novu_sliku.place(anchor="center",relx=0.4,rely=0.4)
        button_dodaj_novu_sliku['bg']='#b6d7a8'

        # ovdje treba dodati gumb koji ce nas opet povezati na listu s biljkama

        button_prikazi_listu_PyFlora_posuda= tk.Button(
            self.root, text='POGLEDAJ SVOJE BILJKE', font=("quicksand", 10, "normal"), 
            command=self.prikaz_liste_PyPosuda, bd=3, fg='#0c4f4e',padx=45, pady=10
            )
        button_prikazi_listu_PyFlora_posuda.place(anchor="center",relx=0.4,rely=0.6)
        button_prikazi_listu_PyFlora_posuda['bg']='#b6d7a8'
        

    def otvori_i_spremi_sliku_biljke_od_korisnika(self):
        """ 
            ova metoda otvara biljku iz foldera korisnika 
            i sprema je u isti folder 
            s imenom koje je korisnik odabrao
        """
        # otvaranje slike iz foldera
        photo_filename = filedialog.askopenfilename(title ='Open image')
        img = Image.open(str(photo_filename))
        img = img.resize((150, 110))
        label_slika = ImageTk.PhotoImage(img)
        

        # spremanje slike i putanje u folder
        putanja_slike = f'{self.ime_nove_biljke.get()}.jpg'

        # folder_sa_slikama = os.path.abspath(
        #     os.path.join(
        #         os.path.dirname(__file__),
        #         "SLIKE_BILJAKA"))  
        
        # spremi_sliku_u_folder = os.path.join(folder_sa_slikama, putanja_slike)
        # ime_slike_u_direktoriju = img.save(spremi_sliku_u_folder)

        if img:
                nova_slika = f'{self.ime_nove_biljke.get()}.jpg'
                #profilna_slika_ime= f"profilna_slika_{username}.jpg"
                putanja_do_slike = spoji_sliku_s_folderom(nova_slika)
                # na disk spremamo sa punom putanjom da se ne spremi 
                # u folderu iz kjeg je pozvana aplikacija
                img.save(putanja_do_slike)
                img.close()
        else:
                nova_slika = ""
            # u bazu putanju do slike spremamo samo ime slike
        self.repozitorij.spremi_biljku(
                Biljke(
                    ime_biljke=self.ime_nove_biljke.get(),
                    slika_biljke=nova_slika)
                )
            

        # spremanje slike u BAZU
        #self.spremi_novu_biljku_u_bazu(self.ime_nove_biljke.get(), putanja_slike)   #spremi_sliku_u_folder
        showinfo(title="Wohooo!", message=f"Slika {putanja_slike} uspješno spremljena!")

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
        self.pocetna_slikica()
        #self.root.wm_attributes('-transparentcolor','green') - stvaranje transparentnog prozora
        # header  =  tk.Frame(self.root,  width=1060,  height=63, relief='raised', bg='black')
        # header.place(anchor='nw')
        gumb_sinkronizacije = tk.Button(self.root,
                        text="sinkronizacija", 
                        font=("quicksand", 10, "normal"), 
                        fg='#0c4f4e',padx=35, pady=3, command=main(ime_baze="SQLite_Baza_PyFlora.sqlite") )
        gumb_sinkronizacije.place(x=765,y=70)
        gumb_sinkronizacije['bg']='#FFE890'
        
    def nacrtaj_header(self, tekst):
        self.pocetna_slikica()
        self.gumb_sinkronizacije()
        header  =  tk.Frame(self.root,  width=1400,  height=60, relief='groove', borderwidth= 2, bg='#d9ead3')
        header.place(anchor='nw')
        tekst = tk.Label(self.root, 
                text=tekst, #'PyFlora Posuda: Biljke ',
                font=("quicksand", 15, "normal"), 
                fg='#0c4f4e', 
                padx=90,pady=3)
        tekst['bg']='#d9ead3' #background color
        tekst.place(anchor="nw",rely=0.015)

        gumb_moj_profil = tk.Button(header,
                        text="moj profil", 
                        font=("quicksand", 10, "normal"), 
                        fg='#0c4f4e', padx=25, pady=3, command= self.moj_profil_opcije)
        gumb_moj_profil.place(x=766,y=11,relwidth=0.115)
        gumb_moj_profil['bg']='#FFE890' #FFE890

        manji_image = Image.open("PyFlora_crno_zuta.jpg")
        manja_slika = ImageTk.PhotoImage(manji_image.resize((75,50)))
        # drugo - predajemo sliku labelu (mozemo i buttonu i pozadini i...)
        label_sa_slikom = tk.Label(self.root, image=manja_slika)
        label_sa_slikom.image = manja_slika
        # trece - postavljamo je na ekranu; radi i place i pack
        label_sa_slikom.place(anchor="nw", relx = 0.005,rely=0.005)

    def moj_profil_opcije(self):
        """ u ovoj metodi dodaj sto zelis imati u mom profilu
        mozda: moji podaci; izbrisi korisnika; logout; """
        self.clear_frame()
        self.velika_slika_posred_ekrana("PyFlora_crno_zuta.jpg")

        button_podaci = tk.Button(
            self.root, text='moji podaci', font=("quicksand", 12, "normal"), 
            bd=3, fg='#0c4f4e',padx=45, pady=3
            ) # nedostaje jos command = ?
        button_podaci.place(anchor="center",relx=0.5,rely=0.2)
        button_podaci["bg"]="#FFE890"
        # svijetlo narancasta boja: button_ulogiraj['bg']='#FFCF79'
        # svijetlo zuta boja: button_podaci["bg"]="#FFE890"

        button_moje_biljke = tk.Button(
            self.root, text='pogledaj svoje bilje', font=("quicksand", 12, "normal"), 
            command=self.prikaz_liste_PyPosuda, bd=3, fg='#0c4f4e',padx=45, pady=2
            )
        button_moje_biljke.place(anchor="center",relx=0.5,rely=0.3)
        button_moje_biljke["bg"]="#FFCF79"

        button_svi_korisnici = tk.Button(
            self.root, text='pogledaj sve korisnike', font=("quicksand", 12, "normal"), 
            command=self.prikaz_korisnika, bd=3, fg='#0c4f4e',padx=45, pady=2
            )
        button_svi_korisnici.place(anchor="center",relx=0.5,rely=0.4)
        button_svi_korisnici["bg"]="#FFCF79"

        button_novi_korisnik = tk.Button(
            self.root, text='dodaj novog korisnika', font=("quicksand", 12, "normal"), 
            command=self.prozor_za_dodavanje_novog_korisnika, bd=3, fg='#0c4f4e',padx=45, pady=2
            )
        button_novi_korisnik.place(anchor="center",relx=0.5,rely=0.5)
        button_novi_korisnik["bg"]="#FFCF79"

        button_pocetak = tk.Button(
            self.root, text='vrati se na pocetak', font=("quicksand", 12, "normal"), 
            command=self.nacrtaj_naslovnicu_aplikacije, bd=3, fg='#0c4f4e',padx=45, pady=2
            )
        button_pocetak.place(anchor="center",relx=0.5,rely=0.6)
        button_pocetak["bg"]="#FFCF79"
   
    def nacrtaj_header_prijava(self):
        self.pocetna_slikica()
        self.root['bg']= '#f3f6f4'
        
        header  =  tk.Frame(self.root,  width=1060,  height=60, relief='groove', borderwidth= 2, bg='#d9ead3')
        header.place(anchor='nw')
        tekst = tk.Label(self.root, 
                text='PyFlora Posuda: Prijava ',
                font=("quicksand", 15, "normal"), 
                fg='#0c4f4e', 
                padx=90,pady=3)
        tekst['bg']='#d9ead3' #background color
        tekst.place(anchor="nw",rely=0.015)

        manji_image = Image.open("PyFlora_crno_zuta.jpg")
        manja_slika = ImageTk.PhotoImage(manji_image.resize((75,50)))
        # drugo - predajemo sliku labelu (mozemo i buttonu i pozadini i...)
        label_sa_slikom = tk.Label(self.root, image=manja_slika)
        label_sa_slikom.image = manja_slika
        # trece - postavljamo je na ekranu; radi i place i pack
        label_sa_slikom.place(anchor="nw", relx = 0.005,rely=0.005)

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
            slika_livo = tk.Label(neki_frame, image=label_slika,bg='#d9ead3')
            slika_livo.image = label_slika
            slika_livo.place(anchor='center', relx=0.5, rely=0.5)
        else:
            self.ubaci_tekst_u_label(neki_frame, f"Slika\n {putanja_slike}\n nije pronađena")

    def ubaci_tekst_u_label(self, neki_frame,ime_slike):

        oznaka = tk.Label(
            neki_frame, 
            text=f'{ime_slike}',
            font=("quicksand", 10, "normal"), 
            fg='#0c4f4e',bg="#d9ead3", justify='left')   # svijetlo zuta - FFE890
        oznaka.place(anchor ='center', relx=0.3, rely=0.2)

        status_biljke = tk.Label(
            neki_frame, 
            text='Status: \nVlažnost tla: \nSvjetlost: ',
            font=("quicksand", 8, "normal"), 
            fg='#0c4f4e', bg="#d9ead3", justify='left')   # svijetlo zuta - FFE890
        status_biljke.place(anchor ='s',relx=0.3,rely=0.95)

    def dodaj_redak(self, redni_broj, stupac, broj_stupaca):
        #frame_pape = tk.Frame(self.root, width=250, height=150, bd=1, relief="solid")
        frame_pape  =  tk.Frame(self.root,  width=300,  height=250, bd=3, relief='raised', bg='lightgrey')
        frame_pape.grid(
            row=redni_broj, 
            column=stupac, 
            columnspan=broj_stupaca, 
            padx=31, pady=110,
        )
        return frame_pape

    def dodaj_frame(self, parent_frame,  red, stupac, background_color):
        frame_child = tk.Frame(
            parent_frame, 
            width=125, height=175, bd=0, relief="flat", bg=background_color
            )
        frame_child.grid(row=red, column=stupac)
        return frame_child

    def prikaz_liste_PyPosuda(self):

        self.root.title ("PyFlora Posuda: ovo su vaše biljke")
        self.clear_frame()
        self.pocetna_slikica()
        self.nacrtaj_header("PyFlora Posuda: Biljke") 

        baza_biljaka=session.execute("SELECT * FROM biljke")
        stupac = 0
        redak = 0
        
        for biljka in baza_biljaka: 
            # frameovi

            pape  =  tk.Frame(self.root,  width=300,  height=200, bd=1, relief='flat', bg='#d9ead3')
            pape.grid(row=redak, column=stupac, padx=31, pady=70) #pady=110
            # pape = self.dodaj_redak(redak,stupac*2,1)

            dite_livo = self.dodaj_frame(pape,redak,0,"#d9ead3")    # svijetlo zuta - FFE890
            dite_desno = self.dodaj_frame(pape,redak,1,"#d9ead3")   # svijetlo zuta - FFE890
            # dite_livo=tk.Frame(pape, width=125,  height=150, bg='#b6d7a8')
            # dite_livo.grid(row=0,  column=0,  padx=5, pady=5)
            # dite_desno=tk.Frame(pape, width=125,  height=150, bg='white')
            # dite_desno.grid(row=0,  column=1,  padx=5, pady=5)
            
            self.ubaci_sliku_u_label(dite_livo, putanja_slike=biljka.slika_biljke) # ovdje umjesto red[2] bi trebala biti putanja slike
            self.ubaci_tekst_u_label(dite_desno, biljka.ime_biljke)# ovo prikazuje ime, ali ovo iznad ne i sliku...
            
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
        frame_za_novu_biljku = tk.Frame(self.root,  width=300,  height=200, bd=2, relief='raised', bg='white') #bg='#AFE1AF'
        frame_za_novu_biljku.grid(
            row=redni_broj, 
            column=stupac, 
            #columnspan=broj_stupaca, 
            padx=10, pady=80
        )
        self.mali_crno_bijeli_logo(frame_za_novu_biljku)
        return frame_za_novu_biljku
    
    def gumb_za_novu_biljku(self, frame): # ne radi promjena pozadinske boje gumba! ZASTO???
        button_nova_biljka = tk.Button(frame,text="nova biljka", bg='white',
            font=("quicksand", 10, "normal"),fg="#0c4f4e",command=self.dodajte_novu_biljku_iz_foldera) #fg='#0c4f4e'
        # button_nova_biljka = tk.Button(frame, text="nova biljka", 
        #     font=("calibre", 10, "normal"), fg='#0c4f4e',command=self.upisi_novu_biljku)
        button_nova_biljka.grid(column=0, columnspan=3, row=1, ipadx=20, ipady=20, padx=70, pady=55)
        button_nova_biljka['bg']='#FFCF79'    

    def mali_crno_bijeli_logo(self,frame_za_logo):
        manji_image = Image.open("PyFlora_crno_bijela.jpg")
        manja_slika = ImageTk.PhotoImage(manji_image.resize((75,50)))
        # drugo - predajemo sliku labelu (mozemo i buttonu i pozadini i...)
        label_sa_slikom = tk.Label(frame_za_logo, image=manja_slika,relief='flat', bg='white')
        label_sa_slikom.image = manja_slika
        #label_sa_slikom.place(anchor="center",relx=0.5,rely=0.5)
        # trece - postavljamo je na ekranu; radi i place i pack
        label_sa_slikom.place(anchor="nw", relx = 0.65,rely=0.005)


 
    def prikaz_korisnika(self):

        self.clear_frame()
        self.pocetna_slikica()
        self.nacrtaj_header("PyFlora: Korisnici")
        # frame za prikaz korisnika
        prvi_frame = tk.Frame(self.root,bg="#f3f6f4", borderwidth=2, width=250,height=200,cursor="dotbox")
        #prvi_frame.grid(column=1, row=0, padx=10, pady=10)
        prvi_frame.place(anchor='nw', relx= 0.04,rely=0.25)
       
        tablica_korisnika=session.execute("SELECT * FROM Korisnici")
        e=tk.Label(prvi_frame,width=10,text='userid',font=("calibre", 10, "normal"),fg='#0c4f4e',borderwidth=2, anchor='center',bg='#f3f6f4')
        e.grid(row=0,column=0)
        e=tk.Label(prvi_frame,width=10,text='IME',font=("calibre", 10, "normal"),fg='#0c4f4e',borderwidth=2,anchor='center',bg='#f3f6f4')
        e.grid(row=0,column=1)
        e=tk.Label(prvi_frame,width=10,text='LOZINKA',font=("calibre", 10, "normal"),fg='#0c4f4e',borderwidth=2,anchor='center',bg='#f3f6f4')
        e.grid(row=0,column=2)
        i=1
        #i=0 
        for user in tablica_korisnika: 
            for j in range(len(user)):
                prikaz_korisnika = tk.Label(
                    prvi_frame, width=10, font=("quicksand", 9, "normal"), 
                    text=user[j], fg='#0c4f4e', borderwidth=2,
                    relief='ridge', anchor="center"
                    ) 
                prikaz_korisnika.grid(row=i, column=j) 
                prikaz_korisnika['bg']='white'
                
                #e.insert(END, student[j])
            i=i+1

        # frame za prikaz teksta: za sada ne koristim!
        # frame_za_tekst = tk.Frame(self.root, bg='#f3f6f4', borderwidth=1, width=150,height=200,cursor="dotbox")
        # #frame_za_tekst.grid(column=0, row=1, padx=5, pady=40)
        # frame_za_tekst.place(anchor='center', relx=0.2, rely=0.8)
        # tekst_u_frameu_za_prostor = tk.Label(
        #     frame_za_tekst, 
        #     text='Ovo je popis korisnika aplikacije PyFlora \n\nza povratak odaberite "go back!"\nza ponovno logiranje odaberite "go to login"', 
        #     font=("Times", 12, "italic"), 
        #     fg='#0c4f4e',
        #     justify='left'
        #     )
        # tekst_u_frameu_za_prostor.grid(column=0, row=0, padx=15, pady=5)
        # tekst_u_frameu_za_prostor['bg']='#f3f6f4'

        #frame za gumbe za povratak i login
        frame_za_gumbe = tk.Frame(self.root,bg='#f3f6f4',relief="raised", borderwidth=0, width=250,height=200,cursor="dotbox")
        #frame_za_gumbe.grid(column=1, row=1, padx=5, pady=5)
        frame_za_gumbe.place(anchor='ne', relx=0.55, rely=0.35)

        button_povratak = tk.Button(frame_za_gumbe, text="vrati se", 
            font=("quicksand", 11, "normal"), fg='#0c4f4e', command=self.nacrtaj_treci_prozor)
        button_povratak.grid(column=0, columnspan=3, row=8, ipadx=38, ipady=3, padx=10, pady=10)
        button_povratak['bg']='#FFE890'


        button_poceteak = tk.Button(frame_za_gumbe, text="vrati se na login", 
            font=("quicksand", 11, "normal"), fg='#0c4f4e', command=self.prozor_ulaska_login)
        button_poceteak.grid(column=0, columnspan=3, row=10, ipadx=10, ipady=3, padx=10, pady=10)
        button_poceteak['bg']='#FFE890'

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
        slika = ImageTk.PhotoImage(Image.open("cvijet.png"))
        label1 = tk.Label(image = slika)
        label1.image = slika
        label1.place(anchor='w', relx=0.5, rely=0.5)

    def velika_slika_posred_ekrana(self,slika):
        self.root.title('PyFlora Aplikacija')
        img = Image.open(slika)
        #img = img.filter(ImageFilter.BLUR)
        slika = ImageTk.PhotoImage(img)
        
        label_sa_slikom = tk.Label(self.root, image=slika,relief="flat")
        label_sa_slikom.image = slika
        # trece - postavljamo je na ekranu; radi i place i pack
        label_sa_slikom.place(anchor="center",relx=0.5,rely=0.5)  #rely=0.55



    def prikaz_sadrzaja_synca_autori(self):
        # skinuto s neta
        self.clear_frame()
        self.pocetna_slikica()
        tablica_korisnika=session.execute("SELECT * FROM autor")
        e=tk.Label(self.root,width=10,text='autorid',font=("calibre", 10, "normal"),fg='#0c4f4e',borderwidth=2, anchor='center',bg='#f3f6f4')
        e.grid(row=0,column=0)
        e=tk.Label(self.root,width=10,text='NAME',font=("calibre", 10, "normal"),fg='#0c4f4e',borderwidth=2,anchor='center',bg='#f3f6f4')
        e.grid(row=0,column=1)
        e=tk.Label(self.root,width=10,text='EMAIL',font=("calibre", 10, "normal"),fg='#0c4f4e',borderwidth=2,anchor='center',bg='#f3f6f4')
        e.grid(row=0,column=2)

        i=1
        for user in tablica_korisnika: 
            for j in range(len(user)):
                prikaz_korisnika = tk.Label(
                    self.root, width=20, font=("calibre", 10, "normal"), 
                    text=user[j], fg='#0c4f4e', borderwidth=2,
                    relief='ridge', anchor="center"
                    ) 
                prikaz_korisnika.grid(row=i, column=j) 
                    
            i=i+1
        button_povratak = tk.Button(self.root, text="go back", 
                font=("calibre", 12, "normal"), fg='#0c4f4e', command=self.nacrtaj_treci_prozor)
        button_povratak.grid(column=0, columnspan=3, row=15, ipadx=10, ipady=3) #padx=10, pady=10)
        button_povratak['bg']='#b6d7a8'

        button_poceteak = tk.Button(self.root, text="go to login", 
            font=("calibre", 12, "normal"), fg='#0c4f4e', command=self.nacrtaj_prvi_prozor)
        button_poceteak.grid(column=0, columnspan=3, row=20, ipadx=10, ipady=3, padx=10, pady=10)
        button_poceteak['bg']='#b6d7a8'

    def nacrtaj_prozor_s_biljkama(self): 
        """ ova metoda je samo proba i prikaz kako sve mozemo prikazivati slike na GUI """
        self.clear_frame()
        self.root.title(f'PyFlora')
        self.pocetna_slikica() 

        oznaka = tk.Label(self.root, text='Vaše biljke...', font=("calibre", 12, "normal"), fg='#0c4f4e', padx=30,pady=20)   
        oznaka['bg']='#f3f6f4'
        oznaka.grid(column=0, row=0, padx=5, pady=5)
       
        # Frame 1
        frame1 = tk.Frame(self.root,relief="raised", bg="#b6d7a8", borderwidth=1, width=250,height=200,cursor="heart")
        frame1.grid(column=0, row=1, padx=5, pady=5)

        # Frame 2
        frame2 = tk.Frame(self.root,bg="white",relief="raised", borderwidth=1, width=250,height=200,cursor="circle")
        frame2.grid(column=0, row=2, padx=5, pady=5)

        # Frame 3
        frame3 = tk.Frame(self.root,bg="white",relief="raised", borderwidth=1, width=250,height=200,cursor="dotbox")
        frame3.grid(column=1, row=1, padx=5, pady=5)

        # Frame 4
        frame3 = tk.Frame(self.root,bg="white",relief="raised", borderwidth=1, width=250,height=200,cursor="plus")
        frame3.grid(column=1, row=2, padx=5, pady=5)


        # PRIKAZ SLIKA:
        # prvo - ovdje otvaramo sliku koju smo odrabrali
        image = Image.open("cvijet_mali.png")
        slika = ImageTk.PhotoImage(image)
        # moze i ovako krace: 
        # slika = ImageTk.PhotoImage(Image.open("cvijet_mali.png"))

        # drugo - predajemo sliku labelu (mozemo i buttonu i pozadini i...)
        label_sa_slikom = tk.Label(frame1, image=slika)
        label_sa_slikom.image = slika
        # trece - postavljamo je na ekranu; radi i place i pack
        label_sa_slikom.place(anchor="nw", rely=0.03)
        #label.pack()
        
        #ako zelimo manju sliku za button, mozemo je resizeati
        manji_image = Image.open("cvijet_voda.png")
        manja_slika = ImageTk.PhotoImage(manji_image.resize((150,100)))

        # sad je prikazujemo na buttonu
        gumb_sa_slikom = tk.Button(frame2, image=manja_slika)
        gumb_sa_slikom.image = manja_slika
        gumb_sa_slikom.pack()

        # slika u trecem frameu:
        image = Image.open("cvijet_orhideja.png")
        slika_treci_frame = ImageTk.PhotoImage(image.resize((80,50)))
        label_sa_slikom = tk.Label(frame3, image=slika_treci_frame, cursor="dot")
        label_sa_slikom.image = slika_treci_frame
        label_sa_slikom.place(relx=0.35)

        # tekst ispod slike u trecem frameu
        tekst_ispod_slike = tk.Label(
            frame3, text='orhideja vulgaris', 
            font=("calibre", 10, "normal"), borderwidth=2,
        fg='#0c4f4e', padx=30,pady=20)   
        tekst_ispod_slike['bg']='white'
        tekst_ispod_slike.grid(column=0, row=1, padx=45, pady=65)

    def nacrtaj_biljku_i_tekst(self):
        """ ova metoda je samo za probu i vjezbu crtanja framova sa slikom i tekstom iz baze"""
        self.clear_frame()
        # PRVA BILJKA S TEKSTOM
        frame_pape=tk.Frame(self.root,width=250, height=150, bd=1, relief="flat", bg="#b6d7a8")
        frame_pape.grid(row=1,column=0,columnspan=2)

        frame_dite_lite = tk.Frame(self.root,width=125, height=150, bd=1, relief="ridge", bg="gray")
        frame_dite_lite.grid(row=1,column=0,padx=5,pady=5)

        frame_dite_desno=tk.Frame(self.root,width=125, height=150, bd=1, relief="ridge", bg="white")
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

            oznaka = tk.Label(
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

            label_sa_slikom = tk.Label(frame_dite_lite, image=manja_slika)
            label_sa_slikom.image = manja_slika
            label_sa_slikom.place(anchor="center", relx=0.5, rely=0.5)

            #tekst u desnom dijelu framea
            tekst = tk.Label(frame_dite_desno, text='biljka 1',font=("calibre", 10, "normal"), fg='#0c4f4e')#padx=10,pady=10)
            tekst['bg']='#f3f6f4' #background color
            tekst.place(anchor="center",relx=0.5, rely=0.5) # polozaj teksta
    
    def pokreni(self):
        #self.nacrtaj_naslovnicu_aplikacije()
        #self.prikaz_korisnika()
        self.nacrtaj_naslovnicu_aplikacije()
        #self.prozor_ulaska_login()
        #self.nacrtaj_prvi_prozor()
        #self.nacrtaj_treci_prozor()
        #self.nacrtaj_cetvrti_prozor()
        #self.prikaz_liste_PyPosuda()
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


# DOMACA ZADACA
# da se ispise u dva reda (prem kodu od uce)
# pokusaj dodati biljke kroz GUI u bazu


# photoshop file  - button - open - taj dio prouciti kako se moze otvoriti dijalog s otvaranjem diska
# prouci - tu je djelomicno odgovor na pitanje za domacu zadacu



# ZADATAK:

# 1. korištenjem primjer SQLAlchemy _repo.py napraviti repozitorij za
# dohvat korisnika iz baze
# 1. a) korisnik more imati ID, username i password
#       username mora biti jedinstven
# 1. b) repozitorij mora imati najmanje 2 metode:
# get_user_by_username
# i
# get_all_users

# 2. umjesto provjeri_lozinku koristiti poziv repozitorija koji će to napraviti
# 2. a) proširiti PyFlora __init__ tako da prima ime baze
# 2. b) provjeri_lozinku neka bude metoda PyFlora klase koja će:
#    primiti username i password
#    pokušati dohvatiti prema usernameu korisnika iz baze
#    ako koirnsik postoji provjeriti lozinku
#    vraća True ako je sve uspjelo
#    ako korisnik nije pronađen ili lozinka ne odgovara vraća False
#
# 3. Na sljedecem ekranu (nacrtaj drugi prozor) u nekom objektu po zelji
#    labela i tome nešto slično 
#    prikaži korisničko ime


