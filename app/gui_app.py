import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from gui_repozitorij_prozora import *
from gui_rad_s_bazom import *
from PyFlora_simulator_senzora import * 
from gui_prikaz_sa_senzora import *
from gui_prikaz_grafova import *
from PYFlora_baza_repozitorij import SQLAlchemyRepozitorij, spoji_se_na_bazu

### OVAJ MODUL SADRZI KLASU PYLORA APLIKACIJE s METODAMA ZA CRTANJE APLIKACIJE
class PyFlora:

    def __init__(self, repozitorij):
        # DIO ZA root ELEMENT
        self.root = ttk.Window(themename="flatly")
        self.root.title('PyFlora')
        self.width = 800
        self.height = 610
        self.root.geometry(f'{self.width}x{self.height}')
        self.root['bg']= '#f3f6f4'
        self.repozitorij = repozitorij

        self.style = ttk.Style()
        #gumb moj profil 
        self.style.configure('warning.Outline.TButton', font=('Quicksand', 10), borderwidth=0)
        #label u headeru
        self.style.configure('warning.TLabel',font=('Quicksand', 1))
      
           
    # METODE ZA KORISNIKE:

    def prozor_za_dodavanje_novog_korisnika(self):
        """
        ova metoda crta prozor u kojem cemo registriati NOVOG korisnika
        upisom korisnickog imena i lozinke te ce ga pritiskom na gumb
        spremiti u bazu; prozor takoder nudi opciju povratka na prethodni prozor
        """
        self.root['bg']= '#f3f6f4'
        header_za_prvi_i_drugi_prozor(root=self.root, background=None, title="PyFlora: dodajmo novog korisnika")
        
        #spremi_korisnika_korisnicko_ime_i_lozinka(root=self.root,repozitorij=repozitorij,gui_objekt=self) 

        label(
            self.root,
            "username",
            "quicksand, 14",
            "warning",
            None,
            "#f3f6f4",
            "center",
            0.2,
            0.3,
        )
        self.username = polje_za_unos_username(self.root, "warning", ("quicksand", 9), "center", 0.4, 0.3
        )

        label(
            self.root,
            "password",
            "quicksand, 14",
            "warning",
            None,
            "#f3f6f4",
            "center",
            0.2,
            0.4,
        )
        self.password = polje_za_unos(self.root, "warning", ("quicksand", 9), "*", "center", 0.4, 0.4, 20
        )

        # gumbi za akcije te frame za gumbe
        frame = dodaj_frame_place(self.root,"raised",1,50,500,"light","center",0.5,0.81)
        button_s_gridom(frame,bootstyle="warning-outline",text="spremi novog korisnika",
                        command=lambda:spremi_korisnika(
                            repozitorij=repozitorij,
                            username=self.username.get(),
                            password=self.password.get(),
                            gui_objekt=self
                        ),
                        padding=10, width=18, column=1, columnspan=1,
                        row=1,ipadx=10,ipady=1,padx=10,pady=10,sticky="ew")
        button_s_gridom(frame,bootstyle="warning-outline",text="BACK",
                        command=self.prozor_ulaska_login_ili_registracija, 
                        padding=10,width=12,column=2,columnspan=1,row=1,
                        ipadx=10,ipady=1,padx=10,pady=10,sticky="ew")

    def prozor_prikaz_korisnika(self):
        """ 
        ova metoda crta prozor na kojem se prikazuju
        korisnici aplikacije kao button (pomocu funkcije prikaz korisnika)
        """
        glavni_prozor_aplikacije(root=self.root, 
                                 ime_prozora="PyFlora: Popis korisnika aplikacije",
                                 gumb_moj_profil=self.nacrtaj_treci_prozor_moj_profil)
        # frame za prikaz korisnika

        frame_za_tekst = dodaj_frame_place(frame=self.root,
                                           relief=None, borderwidth=2, 
                                           width=250, height=20,
                                           style="warning",
                                           anchor="center", relx= 0.5, rely=0.5)
        prikaz_korisnika(frame=frame_za_tekst,repozitorij=repozitorij,gui_objekt=self)

    def prozor_s_detaljima_o_korisniku(self,uhvaceni_korisnik):
        """
        ova metoda crta prozor na kojem se prikazuju
        detalji uhvacenog korisnika prema njegovom idu;
        na prozoru su i gumbi za azuriranje i brisanje korisnika iz baze
        te gumb za povratak na prethodn prozor 
        """
        glavni_prozor_aplikacije(self.root,"PyFlora: Moji podaci",self.nacrtaj_treci_prozor_moj_profil)
        
        frame_za_tekst=dodaj_frame_place(self.root,None,0,450,400,None,"center",0.5,0.4)
        prikaz_korisnika_prema_id_iz_baze(frame_za_tekst,repozitorij,uhvaceni_korisnik)

        buttoni_za_azuriranje_i_brisanje_podataka(
            root=self.root,
            azuriraj_izbrisi_koga="korisnika",
            command_azuriraj=lambda:self.prozor_za_azuriranje_korisnika(uhvaceni_korisnik=uhvaceni_korisnik),
            command_izbrisi=lambda:repozitorij.izbrisi_korisnika(id=uhvaceni_korisnik,gui_objekt=self),
            command_BACK=self.prozor_prikaz_korisnika, 
            anchor="center",relx=0.5,rely=0.82)
        
    def prozor_za_azuriranje_korisnika(self,uhvaceni_korisnik):
        """ova metoda crta prozor u kojem azuriramo korisnika"""
        glavni_prozor_aplikacije(self.root,"PyFlora: Ažuriraj moje podatke",self.nacrtaj_treci_prozor_moj_profil)

        korisnik = repozitorij.dohvati_korisnika_prema_id(id=uhvaceni_korisnik)
        if korisnik: 
            korisnicko_ime = korisnik.username
            lozinka = korisnik.password
        frame_za_tekst=dodaj_frame_place(self.root,None,0,450,400,None,"center",0.5,0.4)

        # pozdravni tekst
        label(
        frame_za_tekst,
        f"Bok, {(korisnicko_ime).capitalize()}!",
        ("quicksand", 14),
        "warning",
        None,
        None,
        "center",
        0.5,
        0.1)

        # korisnicko ime i polje za izmjenu imena
        label_s_anchorom(frame_za_tekst,'korisničko ime',("quicksand", 12),"warning","w",12,None,"center",0.2,0.6)
        self.novi_username = polje_za_unos_s_prikazom_postojeceg_teksta(
            frame_za_tekst,"warning",('quicksand', 9),None,
            "center",0.63,0.6,35,korisnicko_ime)
        
        # lozinka i polje za izmjenu lozinke
        label_s_anchorom(frame_za_tekst,'lozinka',("quicksand", 12),"warning","w",12,None,"center",0.2,0.75)
        self.novi_password = polje_za_unos_s_prikazom_postojeceg_teksta(
            frame_za_tekst,"warning",('quicksand', 9),None,
            "center",0.63,0.75,35,lozinka)
        
        # opis aktivnosti na stranici za azuriranje podataka
        label(
        frame_za_tekst,
        "Ovdje možeš ažurirati svoje podatke.\nZa spremanje ažuriranja odaberi gumb 'spremi ažuriranje'\nZa brisanja korisnika odaberi gumb 'izbriši korisnika'\nZa povratak odaberite gumb 'BACK'",
        ("quicksand", 10),
        "primary",
        "center",
        None,
        "center",
        0.5,
        0.3)
        
        # gumbi za akcije te frame za gumbe
        frame = dodaj_frame_place(self.root,"raised",1,50,500,"light","center",0.5,0.81)
        button_s_gridom(frame,"warning-outline",f"spremi ažuriranje",
                        lambda:repozitorij.azuriraj_korisnika(
                        id=uhvaceni_korisnik,
                        korisnicko_ime=self.novi_username.get(),
                        lozinka=self.novi_password.get(),
                        gui_objekt=self),
                        padding=10, width=15, column=1, columnspan=1,
                        row=1,ipadx=10,ipady=1,padx=10,pady=10,sticky="ew")
        button_s_gridom(frame,bootstyle="danger-outline",text="izbriši korisnika",
                        command=lambda:repozitorij.izbrisi_korisnika(id=uhvaceni_korisnik,gui_objekt=self), 
                        padding=10,width=12,column=2,columnspan=1,row=1,
                        ipadx=10,ipady=1,padx=10,pady=10,sticky="ew")
        button_s_gridom(frame,"warning-outline","BACK",
                        lambda:self.prozor_s_detaljima_o_korisniku(uhvaceni_korisnik=uhvaceni_korisnik),
                        padding=10, width=12,
                        column=3,columnspan=1,row=1,
                        ipadx=10,ipady=1,padx=10,pady=10,sticky="ew")
     
    # METODE ZA POCETNE PROZORE i MENU:

    def naslovnica(self):
        """ 
        ova metoda je naslovnica aplikacije s gumbom loga za ulaz u aplikaciju; 
        ovdje samo ulazimo u aplikaciju 
        """
        clear_frame(self.root)

        velika_slika_posred_ekrana(self.root,'cvijet.png',folder_name="media")

        nacrtaj_naslovnicu_aplikacije(self.root,self.prozor_ulaska_login_ili_registracija)  

    def prozor_ulaska_login_ili_registracija(self):
        """
        ova metoda ispisuje prozor 
        koji nudi korisniku opciju LOGINA ili upisa NOVOG korisnika u obliku gumba
        """
        clear_frame(self.root)
        self.root.title('PyFlora Aplikacija')
        self.root["bg"]="white"
        velika_slika_posred_ekrana(self.root,ime_slike='PyFlora_crno_zuta.jpg',folder_name="media")
        prikaz_datuma_i_temperature(self.root,anchor="center", relx=0.5, rely=0.72)
        
        label(self.root,tekst="Dobrodošli u aplikaciju PyFlora",
            font_slova=("quicksand", 15, "bold"),
            stil='dark',poravnanje=None,pozadina="white",anchor="center",relx=0.5,rely=0.1)
        
        label(self.root,tekst="Za ulazak u app odaberite 'ulogiraj me',\nili 'registriraj me' ako niste registrirani",
            font_slova=("quicksand", 10),
            stil='dark',poravnanje="center",pozadina="white",anchor="center",relx=0.5,rely=0.17) #0.72

        button(self.root, style='warning.Outline.TButton',
            bootstyle="warning.outline",
            text ='ulogiraj me', command=self.nacrtaj_prvi_prozor_login, padding=10, width=30,
            anchor="center",relx=0.5,rely=0.79)

        button(self.root, style='warning.Outline.TButton',
            bootstyle="warning-outline-toolbutton", 
            text ='registriraj me', command=self.prozor_za_dodavanje_novog_korisnika, padding=10, width=30,
            anchor="center",relx=0.5,rely=0.87)
    
    def nacrtaj_prvi_prozor_login(self): 
        """ 
        ova metoda crta prvi prozor aplikacije u kojem se 
        postojeci korisnik LOGIRA u aplikaciju PyFlora
        """
        header_za_prvi_i_drugi_prozor(self.root,"#f3f6f4",None)

        #provjeri_korisnika_postoji_li_u_bazi(self.root,repozitorij,gui_objekt=self)
        label(self.root,'username','quicksand, 14',"warning",None,'#f3f6f4',"center",0.2,0.3)
        self.username = polje_za_unos_username(self.root,"warning",('quicksand',9),"center",0.4,0.3)

        label(self.root,'password','quicksand, 14',"warning",None,'#f3f6f4',"center",0.2,0.4)
        self.password = polje_za_unos(self.root,"warning",('quicksand',9),"*","center",0.4,0.4,20)
        # #self.unos_korisnicko_ime_i_lozinka()

        button(self.root,'warning.Outline.TButton',"warning-outline",'login',
               lambda:provjeri_korisnika_postoji_li_u_bazi(repozitorij,gui_objekt=self),10,30,"center",0.32,0.5)
 
    def nacrtaj_drugi_prozor(self, username):
        """ 
        ova metoda crta prozor u kojem pozdravljamo
        korisnika koji se uspjesno ulogirao i sadrzi gumb za nastavak 
        """
        header_za_prvi_i_drugi_prozor(self.root,"#f3f6f4",'PyFlora - Ulaz u PyFlora aplikaciju')
        # username = self.username.get() - možemo i ovako i onda ne predajemo username u pozivu metode "nacrtaj_drugi_prozor"
        button(self.root,'warning.TButton','warning-outline',"let's go!",self.nacrtaj_treci_prozor_moj_profil,
               10,30,'center',0.5,0.6)
        label(self.root,f'Pozdrav \n{username.capitalize()}!',('quicksand',20),'light-inverse',
              None,"#f3f6f4",'center',0.5,0.4)

    def nacrtaj_treci_prozor_moj_profil(self):
        """
        ova metoda crta prozor u kojem su prikazani svi gumbi 
        s opcijama aplikacije PyFlora
        """
        glavni_prozor_aplikacije(self.root,'PyFlora Posuda: MENU',self.nacrtaj_treci_prozor_moj_profil)
        # naslov prozora:
        self.root.title ("PyFlora Posuda")

        frame = dodaj_frame_place(self.root,"raised",1,250,600,"warning","ne",0.7,0.14)
        button_s_gridom(frame,"warning-outline","popis korisnika",self.prozor_prikaz_korisnika,10,30,
                        column=3,columnspan=3,row=2,ipadx=10,ipady=3,padx=15,pady=10,sticky="ew")
        button_s_gridom(frame,"warning-outline","pogledaj svoje biljke",self.prozor_prikaz_biljaka_PyPosuda,10,30,
                        column=3,columnspan=3,row=3,ipadx=10,ipady=3,padx=10,pady=10,sticky="ew")
        button_s_gridom(frame,"warning-outline","pogledaj svoje posude",self.prozor_prikaz_posuda_PyPosuda,
                        10,30,column=3,columnspan=3,row=4,ipadx=10,ipady=3,padx=10,pady=10,sticky="ew")
        button_s_gridom(frame,"warning-outline","dodaj novog korisnika",self.prozor_za_dodavanje_novog_korisnika,
                        10,30,3,3,5,10,3,10,10,"ew")
        button_s_gridom(frame,"warning-outline","vrati se na pocetak",self.naslovnica,
                        10,30,3,3,6,10,3,10,10,"ew")
        button_s_gridom(frame,"danger-outline","IZLAZ",self.root.destroy,
                        10,30,3,3,7,10,3,10,10,"ew")
        
    # METODE ZA BILJKE:

    def prozor_za_dodavanje_nove_biljke_u_bazu(self):
        """ 
        ova metoda crta prozor u kojem se dodaje i sprema nova biljku;
        prikazani su labeli i polja za unos podataka za novu biljku (ime,slika,zalijevanje,mjesto i supstrat),
        od kojih su neki padajući izbornici
        """
        glavni_prozor_aplikacije(self.root,'PyFlora Posuda: Nova biljka',self.nacrtaj_treci_prozor_moj_profil)

        # prikaz prozora za unos podataka o novoj biljci
        labeli_i_prozori_za_spremanje_podataka_biljke(self.root,gui_objekt=self)

        # dodavanje slike za novu biljku
        label_s_anchorom(self.root,'odaberite sliku','quicksand, 14',"warning","w",12,'#f3f6f4',"center",0.15,0.6)
        # gumb koji ce otvoriti prozor za odabir slike te je spremiti nakon odabira
        button(self.root,None,"warning-outline","odaberi sliku biljke",
            lambda:otvori_sliku_biljke_koju_cemo_spremiti_u_bazu(
            ime_nove_biljke=self.ime_nove_biljke),10,20,"center",0.18,0.66)

        # Frame za gumbe za spremanje nove biljku u bazu i za povratak/odustajanje
        frame = dodaj_frame_place(frame=self.root,relief="raised",
                                  borderwidth=1,width=50,height=500,style="light",
                                  anchor="center", relx=0.5, rely=0.81)
        button_s_gridom(frame,bootstyle="warning-outline",text="spremi biljku",
                        command=lambda:repozitorij.spremi_biljku(
                            Biljke(
                                ime_biljke=self.ime_nove_biljke.get(),
                                slika_biljke=f"{self.ime_nove_biljke.get()}.jpg",
                                zalijevanje=self.zalijevanje.get(),
                                mjesto=self.mjesto.get(),
                                supstrat=self.supstrat.get(),
                                ),
                                gui_objekt=self),
                        padding=10,width=20,column=2,columnspan=1,row=1,
                        ipadx=10,ipady=1,padx=10,pady=10,sticky="ew")
        button_s_gridom(frame,"warning-outline","ODUSTANI",self.prozor_prikaz_biljaka_PyPosuda,10,11,
                        column=3,columnspan=1,row=1,ipadx=10,ipady=1,padx=10,pady=10,sticky="ew")

        
    def prozor_azuriraj_biljku_iz_baze(self,id_biljke):
        """ 
        ova metoda crta prozor u kojem se ažurira postojeća biljka biljku na gumbu 'ažuriraj biljku';
        prikazani su labeli i polja za unos podataka za novu biljku (ime,slika,zalijevanje,mjesto i supstrat) 
        """
        glavni_prozor_aplikacije(self.root,'PyFlora Posuda: Ažuriranje biljke',self.nacrtaj_treci_prozor_moj_profil)

        # ovu petlju koristim kako bih u poljima za azuriranje biljke ispisala postojece podatke iz baze
        # te podatke mogu promijeniti novim unosim te spremiti gumbom "spremi ažuriranje"
        biljka = repozitorij.dohvati_biljku_prema_idu_u_bazi(id=id_biljke)
        if biljka:   
            ime = biljka.ime_biljke
            voda = biljka.zalijevanje
            pozicija = biljka.mjesto
            supstrat = biljka.supstrat

        labeli_i_prozori_za_azuriranje_podataka_biljke(self.root,gui_objekt=self,ime=ime,
                                                        voda=voda,pozicija=pozicija,supstrat=supstrat)
        button(self.root,None,"warning-outline","spremi ažuriranje",
               lambda:repozitorij.azuriraj_biljku(
                    ime_biljke=self.novo_ime_biljke.get(),
                    zalijevanje=self.novo_zalijevanje.get(), 
                    mjesto=self.novo_mjesto.get(),
                    supstrat=self.novi_supstrat.get(),
                    id_biljke=id_biljke,
                    gui_objekt=self
                    ),
                    10,23,"center",0.19,0.66)
        
        #gumb koji ce nas opet odvesti na listu s biljkama da vidimo sto smo spremili
        button(self.root,None,"warning",'ODUSTANI/BACK',self.prozor_prikaz_biljaka_PyPosuda,10,30,
               "center",0.5,0.8)
        
    def prozor_prikaz_biljaka_PyPosuda(self):
        """
        ova metoda crta prozor u kojem su prikazane
        sve biljke iz baze te sadrži i gumb za dodavanje nove biljke
        """
        self.root.title ("PyFlora Posuda: ovo su vaše biljke")
        glavni_prozor_aplikacije(self.root,"PyFlora Posuda: Biljke",self.nacrtaj_treci_prozor_moj_profil)

        dohvati_sve_biljke_iz_baze_i_nacrtaj_u_gui(self.root,repozitorij,gui_objekt=self)

        frame = dodaj_frame_place(self.root,"raised",1,50,500,"warning","ne",0.98,0.75)

        button_s_gridom(frame,"warning-outline","dodaj biljku",
                        command=self.prozor_za_dodavanje_nove_biljke_u_bazu,
                        padding=10, width=15,
                        column=3,columnspan=3,row=2,ipadx=10,ipady=3,padx=15,pady=10,sticky="ew")

    def prozor_s_detaljima_o_biljci(self, id_slike,command_za_button_BACK=prozor_prikaz_biljaka_PyPosuda):
        """ 
        ova metoda crta prozor 
        na kojem se prikazuju detalji o  
        odabranoj biljci prema id iz baze 
        """
        self.root.title ("PyFlora Posuda: Biljke")
        glavni_prozor_aplikacije(self.root,"PyFlora Posuda: Biljka",self.nacrtaj_treci_prozor_moj_profil)

        # ovo je frame u kojem se ispisuju podaci o biljci koje smo dohvatili iz baze pomocu 
        # funkcije nize: 'prikaz_biljke_prema_id_u_bazi'
        frame_za_tekst=dodaj_frame_place(self.root,None,0,270,150,None,"center",0.5,0.59)

        # slika biljke i podaci o biljci u 'frame_za_tekst'
        prikaz_biljke_prema_id_u_bazi(self.root,frame_za_tekst,repozitorij,id_slike)

        buttoni_za_azuriranje_i_brisanje_podataka_biljaka(self.root,"biljku",
            command_azuriraj=lambda:self.prozor_azuriraj_biljku_iz_baze(id_biljke=id_slike),
            command_izbrisi=lambda:izbrisi_biljku_iz_baze(repozitorij,id_biljke=id_slike,gui_objekt=self),
            command_senzori=self.glavni_prozor_za_grafove,
            # PROBLEM: kada ovdje dodam funkciju - program ne radi, smrzne se!
            #command_sinkronizacija=self.prozor_s_detaljima_o_biljci(id_slike),
            # preveliki broj rekurzija
            command_BACK=command_za_button_BACK,
            anchor="center",relx=0.5,rely=0.81) #relx=0.7,rely=0.71

    # METODE ZA PYPOSUDE:

    def prozor_prikaz_posuda_PyPosuda(self):
        """
        ova metoda crta prozor u kojem su prikazane
        sve PyPosude iz baze
        """
        self.root.title ("PyFlora Posuda: ovo su vaše pametne posude")
        glavni_prozor_aplikacije(self.root,"PyFlora Posuda: PyPosude",self.nacrtaj_treci_prozor_moj_profil)
        dohvati_sve_posude_iz_baze_i_nacrtaj_u_gui(repozitorij,self.root,gui_objekt=self)
        
        # novo dodani gumb za dodavanje nove PyPosude (5.4.2023.)
        frame = dodaj_frame_place(self.root,"raised",1,50,500,"warning","ne",0.98,0.75)
        button_s_gridom(frame,"warning-outline","dodaj PyPosudu",self.prozor_za_dodavanje_nove_posude,10,15,
                        column=3,columnspan=3,row=2,ipadx=10,ipady=3,padx=15,pady=10,sticky="ew")

    def prozor_za_dodavanje_nove_posude(self):
        """ 
        ova metoda crta prozor u kojem se dodaje i sprema nova posuda na gumbu 'dodaj pyposudu';
        prikazani su labeli i polja za unos podataka za novu posudu kao i
        padajući izbornik za biljku koju želimo posaditi
        """
        glavni_prozor_aplikacije(self.root,'PyFlora Posuda: Nova posuda',self.nacrtaj_treci_prozor_moj_profil)

        #dodavanje imena nova posude
        label_s_anchorom(self.root,'ime posude','quicksand, 14',"warning","w",12,'#f3f6f4',"center",0.15,0.2)
        self.ime_nove_posude = polje_za_unos(self.root,"warning",None,None,"center",0.45,0.2,45)
        
        # ovo je label za posaditi biljku pomocu izbora iz padajuceg izbornika
        label_s_anchorom(self.root,'posadi biljku','quicksand, 14',"warning","w",13,'#f3f6f4',"center",0.15,0.35)
        self.posadena_biljka = padajuci_izbornik_za_odabir_biljke(self.root,repozitorij,relx=0.45,rely=0.35)
        
        # dodavanje slike za novu PyPosudu
        label_s_anchorom(self.root,'odaberite sliku','quicksand, 14',"warning","w",12,'#f3f6f4',"center",0.15,0.5)
        button(self.root,None,"warning-outline","odaberi sliku PyPosude",
            lambda:otvori_sliku_posude_od_korisnika(self.ime_nove_posude),
            10,25,"center",0.415,0.5)
      
        # Frame i gumbi za spremanje biljke i povratak na prethodnu stranicu
        frame = dodaj_frame_place(frame=self.root,relief="raised",
                                  borderwidth=1,width=50,height=500,style="light",
                                  anchor="center", relx=0.5, rely=0.81)
        button_s_gridom(frame,bootstyle="warning-outline",text="spremi PyPosudu",
                        command=lambda:repozitorij.spremi_posudu_preko_imena(
                        ime_posude=self.ime_nove_posude.get(),
                        slika_posude=f"{self.ime_nove_posude.get()}.jpg",
                        ime_biljke=self.posadena_biljka.get(),
                        gui_objekt=self),
                        padding=10,width=20,column=2,columnspan=1,row=1,
                        ipadx=10,ipady=1,padx=10,pady=10,sticky="ew"),
        button_s_gridom(frame,"warning-outline","ODUSTANI",self.prozor_prikaz_posuda_PyPosuda,10,11,
                        column=3,columnspan=1,row=1,ipadx=10,ipady=1,padx=10,pady=10,sticky="ew")

    def prozor_s_detaljima_o_posudi(self,id_slike):
        """ 
        ova metoda crta prozor na kojem se prikazuju detalji o  
        odabranoj biljci prema id iz baze; takoder prikazuje graf 
        s podacima dohvacenima sa senzora
        """
        self.root.title ("PyFlora Posuda: Biljke")
        glavni_prozor_aplikacije(self.root,"PyFlora Posuda: Posuda",self.nacrtaj_treci_prozor_moj_profil)
        
        #ovo je frame u kojem se prikazuje ime posude te ime biljke u posudi
        frame_s_tekstom=dodaj_frame_place(
            frame=self.root,
            relief=None,
            borderwidth=0,
            width=270,
            height=150,
            style=None,
            anchor="center",
            relx=0.3, 
            rely=0.59)

        #prikaz svih posuda iz baze s njihovom slikom i imenom biljke
        prikaz_posude_prema_id_u_bazi(frame=self.root,frame_za_tekst=frame_s_tekstom,
                                      repozitorij=repozitorij,id_slike=id_slike,gui_objekt=self,relx=0.3,rely=0.25)

        #ovaj gumb je povezan s biljkom u posudi i vodi na profil biljke s njezinim podacima
        gumb_kojim_dohvacamo_detalje_o_biljci_iz_baze(root=self.root,
                                                      session=session,
                                                      id_slike=id_slike,
                                                      gui_objekt=self)

        buttoni_za_azuriranje_i_brisanje_podataka_plus_senzori(
            root=self.root,
            azuriraj_izbrisi_koga="posudu",
            command_azuriraj=lambda:self.prozor_azuriraj_posudu(id_slike),
            command_izbrisi=lambda:izbrisi_posudu_iz_baze(repozitorij, id_posude=id_slike, gui_objekt=self),
            command_senzori=self.glavni_prozor_za_grafove,
            command_BACK=self.prozor_prikaz_posuda_PyPosuda,
            anchor="center", relx=0.5, rely=0.81)
    
    def prozor_azuriraj_posudu(self,id_slike):
        """ 
        ova metoda crta prozor u kojem su gumbovi za:
        brisanje biljke iz posude;
        zamjenu biljke u posudi;
        dodavanje biljke u posudu
        """
        glavni_prozor_aplikacije(self.root,'PyFlora Posuda: Ažuriranje posude',self.nacrtaj_treci_prozor_moj_profil)
        frame_s_tekstom=dodaj_frame_place(self.root,None,0,270,150,None,"center",0.5,0.59)

        prikaz_posude_prema_id_u_bazi_za_azuriranje(self.root,frame_s_tekstom,
                                      repozitorij=repozitorij,id_slike=id_slike,
                                      relx=0.5,rely=0.25)

        #frame za akcijske gumbe praznjenja posude i povratka na prethodni prozor
        frame = dodaj_frame_place(self.root,"raised",1,50,500,"light","center",0.5,0.81)

        button_s_gridom(frame=frame,bootstyle="danger-outline",
                        text=f"isprazni posudu",
                        command=lambda:izbrisi_biljku_iz_posude(repozitorij,id_slike,gui_objekt=self),
                        padding=10,width=11, 
                        column=1,columnspan=1,row=1,ipadx=10,ipady=1,padx=10,pady=10,sticky="ew")
        button_s_gridom(frame=frame,bootstyle="warning.outline",text="dodaj/zamijeni biljku",
                        command=lambda:self.prozor_za_dodavanje_ili_zamjenu_biljke(id_slike), padding=10,width=15,
                        column=2,columnspan=1,row=1,ipadx=10,ipady=1,padx=10,pady=10,sticky="ew"),
        button_s_gridom(frame=frame,
                        bootstyle="warning-outline",text="BACK",command=lambda:self.prozor_s_detaljima_o_posudi(id_slike),
                        padding=10,width=11,
                        column=3,columnspan=1,row=1,ipadx=10,ipady=1,padx=10,pady=10,sticky="ew")

    def prozor_za_dodavanje_ili_zamjenu_biljke(self,id_slike):
        """ova metoda crta prozor u kojem se prikazuje slika posude koju azuriramo;
        nudi se upis novog imena posude te odabir nove biljke;
        na dnu su opcije za spremanje izmjena te za odustajanje"""
        glavni_prozor_aplikacije(self.root,'PyFlora Posuda: Nova posuda',self.nacrtaj_treci_prozor_moj_profil)
        
        prikaz_slike_posude_prema_id_u_bazi(frame=self.root,repozitorij=repozitorij,id_slike=id_slike,relx=0.5,rely=0.25)
        ime_posude = repozitorij.dohvati_ime_posude(id=id_slike)

        #dodavanje imena nova posude i prikaz postojeceg imena u Entry-u
        label_s_anchorom(frame=self.root,tekst='ime posude',font_slova='quicksand, 14',
                         stil="warning", anchor2="w",
                         width=12, pozadina='#f3f6f4',
                         anchor="center", relx=0.3, rely=0.5)
        self.novo_ime_posude = polje_za_unos_s_prikazom_postojeceg_teksta(
            root=self.root,
            bootstyle="warning",
            font=('quicksand', 9),show =None,
            anchor="center",relx=0.55,rely=0.5,
            width=38, detalj_za_prikaz=ime_posude)
        
        # sadnja biljke prilikom dodavanja nove posude
        # ovo je label za posaditi biljku pomocu izbora iz padajuceg izbornika
        label_s_anchorom(frame=self.root,tekst='posadi biljku',font_slova='quicksand, 14',
                         stil="warning",anchor2="w",
                         width=13,pozadina='#f3f6f4',
                         anchor="center", relx=0.3, rely=0.65)
        self.nova_posadena_biljka = padajuci_izbornik_za_odabir_biljke(self.root,repozitorij,relx=0.55,rely=0.65)

        frame = dodaj_frame_place(frame=self.root,relief="raised",
                                  borderwidth=1,width=50,height=500,style="light",
                                  anchor="center", relx=0.5, rely=0.81)
        # spremanje izmjena za odabranu PyPosudu
        button_s_gridom(frame,bootstyle="warning-outline",text="spremi izmjene PyPosude",
                        command=lambda:
                        repozitorij.azuriraj_pyposudu_u_bazi(
                                id_posude=id_slike,
                                ime_posude=self.novo_ime_posude.get(),
                                posadena_biljka=self.nova_posadena_biljka.get(),
                                gui_objekt=self),
                                padding=10,width=20,column=2,columnspan=1,row=1,
                                ipadx=10,ipady=1,padx=10,pady=10,sticky="ew"),
        #gumb odustani od akcije spremanja azuriranja posude
        button_s_gridom(frame,"warning-outline","ODUSTANI",lambda:self.prozor_s_detaljima_o_posudi(id_slike),10,11,
                        column=3,columnspan=1,row=1,ipadx=10,ipady=1,padx=10,pady=10,sticky="ew")
  

    # METODE ZA GRAFOVE:   

    def glavni_prozor_za_grafove(self):
        """ ova funkcija pri pozivu s gumba crta prozor u kojem se automatski
        daje prikaz linijskog prikaza dohvacenih podataka sa senzora;
        takoder nudi mogucnost da se pomocu gumbova na donjem dijelu ekrana
        prikaze histagram te da se vratimo na biljke i posude u bazi """
        glavni_prozor_aplikacije(self.root,"PyFlora: Podaci sa senzora",gumb_moj_profil=self.nacrtaj_treci_prozor_moj_profil)

        # IDEJA:
        # prikazati jedan prikaz podataka sa senzora
        # i omoguciti druge prikaze gumbovima

        # linijski graf podataka sa senzora
        obradi_dohvacene_podatke_i_nacrtaj_line_chart_graf(self.root,title="Podaci sa senzora")

        # frame za gumbe za prikaz drugih vrsta grafova
        frame = dodaj_frame_place(self.root,"raised",1,50,500,"light","center",0.5,0.84)
        button_s_gridom(frame=frame,
                        bootstyle="warning-outline",
                        text="histagram",
                        command=self.prozor_za_histagram_graf,
                        padding=8,
                        width=10,
                        column=1,columnspan=1,row=1,ipadx=10,ipady=3,padx=10,pady=10,sticky="ew")
        button_s_gridom(frame=frame,
                        bootstyle="warning-outline",
                        text="box",
                        command=self.prozor_za_treci_graf,
                        padding=8,
                        width=10,
                        column=2,columnspan=1,row=1,ipadx=10,ipady=3,padx=10,pady=10,sticky="ew")
        # gumbi za povratak na prikaz biljaka i prikaz posuda
        button_s_gridom(frame=frame,
                        bootstyle="warning-outline",
                        text="PyPosude",
                        command=self.prozor_prikaz_posuda_PyPosuda,
                        padding=8,
                        width=10,
                        column=3,columnspan=1,row=1,ipadx=10,ipady=3,padx=15,pady=10,sticky="ew")
        button_s_gridom(frame=frame,
                        bootstyle="warning-outline",
                        text="PyBiljke",
                        command=self.prozor_prikaz_biljaka_PyPosuda,
                        padding=8,
                        width=10,
                        column=4,columnspan=1,row=1,ipadx=10,ipady=3,padx=15,pady=10,sticky="ew")

    def prozor_za_histagram_graf(self):
        """ ova funkcija pri pozivu s gumba crta prozor u kojem dobijemo
        prikaz histagrama dohvacenih podataka sa senzora;
        takoder nudi mogucnost da se pomocu gumbova na donjem dijelu ekrana
        prikaze linijski graf te da se vratimo na biljke i posude u bazi """
        glavni_prozor_aplikacije(self.root,ime_prozora="PyFlora: Podaci sa senzora",gumb_moj_profil=self.nacrtaj_treci_prozor_moj_profil)
        obradi_dohvacene_podatke_i_nacrtaj_graf_histogram(root=self.root,title="Podaci sa senzora")
        
        frame = dodaj_frame_place(self.root,"raised",1,50,500,"light","center",0.5,0.84)
        button_s_gridom(frame=frame,
                        bootstyle="warning-outline",
                        text="line chart",
                        command=self.glavni_prozor_za_grafove,
                        padding=8,
                        width=10,
                        column=1,columnspan=1,row=1,ipadx=10,ipady=3,padx=10,pady=10,sticky="ew")
        button_s_gridom(frame=frame,
                        bootstyle="warning-outline",
                        text="box",
                        command=self.prozor_za_treci_graf,
                        padding=8,
                        width=10,
                        column=2,columnspan=1,row=1,ipadx=10,ipady=3,padx=10,pady=10,sticky="ew")
        # gumbi za povratak na prikaz biljaka i prikaz posuda
        button_s_gridom(frame=frame,
                        bootstyle="warning-outline",
                        text="PyPosude",
                        command=self.prozor_prikaz_posuda_PyPosuda,
                        padding=8,
                        width=10,
                        column=3,columnspan=1,row=1,ipadx=10,ipady=3,padx=15,pady=10,sticky="ew")
        button_s_gridom(frame=frame,
                        bootstyle="warning-outline",
                        text="PyBiljke",
                        command=self.prozor_prikaz_biljaka_PyPosuda,
                        padding=8,
                        width=10,
                        column=4,columnspan=1,row=1,ipadx=10,ipady=3,padx=15,pady=10,sticky="ew")
        
    def prozor_za_treci_graf(self):
        """ ova funkcija pri pozivu s gumba crta prozor u kojem dobijemo
        prikaz histagrama dohvacenih podataka sa senzora;
        takoder nudi mogucnost da se pomocu gumbova na donjem dijelu ekrana
        prikaze linijski graf te da se vratimo na biljke i posude u bazi """
        glavni_prozor_aplikacije(self.root,ime_prozora="PyFlora: Podaci sa senzora",gumb_moj_profil=self.nacrtaj_treci_prozor_moj_profil)
        obradi_dohvacene_podatke_i_nacrtaj_treci_graf(root=self.root,title="Podaci sa senzora")
        
        frame = dodaj_frame_place(self.root,"raised",1,50,500,"light","center",0.5,0.84)
        button_s_gridom(frame=frame,
                        bootstyle="warning-outline",
                        text="line chart",
                        command=self.glavni_prozor_za_grafove,
                        padding=8,
                        width=10,
                        column=1,columnspan=1,row=1,ipadx=10,ipady=3,padx=10,pady=10,sticky="ew")
        button_s_gridom(frame=frame,bootstyle="warning-outline",text="histagram",
                        command=self.prozor_za_histagram_graf,
                        padding=8,
                        width=10,
                        column=2,columnspan=1,row=1,ipadx=10,ipady=3,padx=10,pady=10,sticky="ew")
        # gumbi za povratak na prikaz biljaka i prikaz posuda
        button_s_gridom(frame=frame,
                        bootstyle="warning-outline",
                        text="PyPosude",
                        command=self.prozor_prikaz_posuda_PyPosuda,
                        padding=8,
                        width=10,
                        column=3,columnspan=1,row=1,ipadx=10,ipady=3,padx=15,pady=10,sticky="ew")
        button_s_gridom(frame=frame,bootstyle="warning-outline",text="PyBiljke",
                        command=self.prozor_prikaz_biljaka_PyPosuda,
                        padding=8,
                        width=10,
                        column=4,columnspan=1,row=1,ipadx=10,ipady=3,padx=15,pady=10,sticky="ew")


    # METODA ZA POKRETANJE APLIKACIJE

    def pokreni(self):
        # self.prikaz_korisnika()
        # self.root.mainloop()
        pass
        
session = spoji_se_na_bazu("SQLalchemy_PyFlora_Baza.sqlite")
repozitorij = SQLAlchemyRepozitorij(session)

