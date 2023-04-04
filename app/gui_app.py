import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import ImageTk, Image, ImageFilter
from tkinter.messagebox import showerror, showinfo
#from tkinter import filedialog
from gui_repozitorij_prozora import *
from gui_dohvacanje_iz_baze import *
from prikaz_grafovlja import dohvati_podatke_sa_senzora, obradi_dohvacene_podatke_i_nacrtaj_graf

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from prikaz_grafovlja import dohvati_podatke_sa_senzora

from PYFlora_baza_repozitorij import SQLAlchemyRepozitorij, Korisnik, Biljke, spoji_se_na_bazu


class PyFlora:

    def __init__(self, repozitorij):
        # DIO ZA root ELEMENT
        self.root = ttk.Window(themename="flatly")
        self.root.title('PyFlora')
        self.width = 800
        self.height = 600
        self.root.geometry(f'{self.width}x{self.height}')
        self.root['bg']= '#f3f6f4'
        self.repozitorij = repozitorij

        self.style = ttk.Style()
        #gumb sinkronizacije
        self.style.configure('warning.TButton', font=('Quicksand', 10), borderwidth=0)
        #gumb moj profil 
        self.style.configure('warning.Outline.TButton', font=('Quicksand', 10), borderwidth=0)
        #label u headeru
        self.style.configure('warning.TLabel',font=('Quicksand', 1))
      
           
    def naslovnica(self):
        """ 
        ova metoda je naslovnica aplikacije s gumbom loga za ulaz u aplikaciju; 
        ovdje samo ulazimo u aplikaciju 
        """
        clear_frame(self.root)
        velika_slika_posred_ekrana(self.root,"media\cvijet.png")
        nacrtaj_naslovnicu_aplikacije(self.root,self.prozor_ulaska_login_ili_registracija)  

    def prozor_ulaska_login_ili_registracija(self):
        """
        ova metoda ispisuje prozor 
        koji nudi korisniku opciju LOGINA ili upisa NOVOG korisnika u obliku gumba
        """
        clear_frame(self.root)
        self.root.title('PyFlora Aplikacija')
        self.root["bg"]="white"
        velika_slika_posred_ekrana(self.root,'media\PyFlora_crno_zuta.jpg')
        prikaz_datuma(self.root)
        
        label(self.root,tekst="Dobrodošli u aplikaciju PyFlora",font_slova=("quicksand", 15, "normal"),
            stil='succes',poravnanje=None,pozadina="white",anchor="center",relx=0.5,rely=0.15)

        button(self.root, style='warning.TButton',
            bootstyle="warning-outline-toolbutton", 
            text ='ulogiraj me', command=self.nacrtaj_prvi_prozor_login, padding=10, width=30,anchor="center",relx=0.5,rely=0.75)

        button(self.root, style='warning.Outline.TButton',
            bootstyle="warning-outline-toolbutton", 
            text ='dodaj novog korisnika', command=self.prozor_za_dodavanje_novog_korisnika, padding=10, width=30,
            anchor="center",relx=0.5,rely=0.83)
        
    def prozor_za_dodavanje_novog_korisnika(self):
        """
        ova metoda crta prozor u kojem cemo registriati NOVOG korisnika
        upisom korisnickog imena i lozinke te ce ga spremiti u bazu
        """
        header_za_prvi_i_drugi_prozor(self.root,None,"PyFlora: dodajmo novog korisnika")
        #glavni_prozor_aplikacije(self.root, "PyFlora: dodajmo novog korisnika",self.nacrtaj_treci_prozor_moj_profil)
        spremi_korisnika_korisnicko_ime_i_lozinka(self.root,repozitorij,gui_objekt=self) 
        self.root['bg']= '#f3f6f4'
        button(self.root,'warning.Outline.TButton',None,'pogledaj korisnike',
               self.prozor_prikaz_korisnika,10,30,"center",0.3,0.7)

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
               lambda:provjeri_korisnika_postoji_li_u_bazi(repozitorij,gui_objekt=self),10,30,"center",0.3,0.5)
 
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
        glavni_prozor_aplikacije(self.root,'PyFlora Posuda: Moj Profil',self.nacrtaj_treci_prozor_moj_profil)
        # naslov prozora:
        self.root.title ("PyFlora Posuda")

        frame = dodaj_frame_place(self.root,"raised",1,250,600,"heart","warning","ne",0.7,0.1)
        button_s_gridom(frame,"warning-outline","popis korisnika",self.prozor_prikaz_korisnika,10,30,
                        column=3,columnspan=3,row=2,ipadx=10,ipady=3,padx=15,pady=10,sticky="ew")
        button_s_gridom(frame,"warning-outline","pogledaj svoje biljke",self.prozor_prikaz_biljaka_PyPosuda,10,30,
                        column=3,columnspan=3,row=3,ipadx=10,ipady=3,padx=10,pady=10,sticky="ew")
        button_s_gridom(frame,"warning-outline","pogledaj svoje posude",self.prozor_prikaz_posuda_PyPosuda,
                        10,30,column=3,columnspan=3,row=4,ipadx=10,ipady=3,padx=10,pady=10,sticky="ew")
        button_s_gridom(frame,"warning-outline","ažuriraj podatke korisnika",self.prozor_prikaz_korisnika,10,30,
                        3,3,5,10,3,10,10,"ew")
        button_s_gridom(frame,"warning-outline","dodaj novog korisnika",self.prozor_za_dodavanje_novog_korisnika,
                        10,30,3,3,6,10,3,10,10,"ew")
        button_s_gridom(frame,"warning-outline","vrati se na pocetak",self.naslovnica,
                        10,30,3,3,7,10,3,10,10,"ew")
        button_s_gridom(frame,"danger-outline","IZLAZ",self.root.destroy,
                        10,30,3,3,8,10,3,10,10,"ew")
        
    def dodajte_novu_biljku_iz_foldera(self):
        """ 
        ova metoda crta prozor u kojem se dodaje i sprema nova biljku na gumbu nova biljka;
        prikazani su labeli i polja za unos podataka za novu biljku (ime,slika,zalijevanje,mjesto i supstrat) 
        """
        # VAZNO potrebno urediti da se dodaju detalji i o njezi biljke!!!
        glavni_prozor_aplikacije(self.root,'PyFlora Posuda: Nova biljka',self.nacrtaj_treci_prozor_moj_profil)
        #dodavanje imena biljke
        label_s_anchorom(self.root,'ime biljke','quicksand, 14',"warning","w",12,'#f3f6f4',"center",0.15,0.2)
        #self.ime_nove_biljke = polje_za_unos(self.root,"warning",None,None,"center",0.35,0.2,30)
        self.ime_nove_biljke = polje_za_unos(self.root,"warning",None,None,"center",0.225,0.25,45)
        
        #dodavanje podataka o zalijevanju
        label_s_anchorom(self.root,'zalijevanje biljke','quicksand, 14',"warning","w",13,'#f3f6f4',"center",0.15,0.3)
        #self.zalijevanje = polje_za_unos(self.root,"warning",None,None,"center",0.35,0.3,30)
        self.zalijevanje = polje_za_unos(self.root,"warning",None,None,"center",0.225,0.35,45)

        #dodavanje podataka o mjestu biljke: treba li biti na tamnom, svijetlom, hladnom, toplom
        label_s_anchorom(self.root,'mjesto biljke','quicksand, 14',"warning","w",12,'#f3f6f4',"center",0.15,0.4)
        #self.mjesto = polje_za_unos(self.root,"warning",None,None,"center",0.35,0.4,30)
        self.mjesto = polje_za_unos(self.root,"warning",None,None,"center",0.225,0.45,45)

        #dodavanje podataka o supstratu: da/ne
        label_s_anchorom(self.root,'supstrat','quicksand, 14',"warning","w",12,'#f3f6f4',"center",0.15,0.5)
        #self.supstrat = polje_za_unos(self.root,"warning",None,None,"center",0.35,0.5,30)
        self.supstrat = polje_za_unos(self.root,"warning",None,None,"center",0.225,0.55,45)

        # dodavanje slike za novu biljku
        label_s_anchorom(self.root,'odaberite sliku','quicksand, 14',"warning","w",12,'#f3f6f4',"center",0.15,0.6)
        # gumb koji ce otvoriti prozor za odabir slike te je spremiti nakon odabira
        button(self.root,None,"warning-outline","odaberi sliku biljke",
            lambda:otvori_i_spremi_sliku_biljke_od_korisnika(
            repozitorij,self.ime_nove_biljke,self.zalijevanje,self.mjesto,self.supstrat
            ),10,20,"center",0.17,0.66)

        #gumb koji ce nas opet odvesti na listu s biljkama da vidimo sto smo spremili
        button(self.root,None,"warning",'POGLEDAJ SVOJE BILJKE',self.prozor_prikaz_biljaka_PyPosuda,10,30,
               "center",0.5,0.8)
        
    def prozor_azuriraj_biljku_iz_baze(self,id_biljke):
        """ 
        ova metoda crta prozor u kojem se ažurira postojeća biljka biljku na gumbu 'ažuriraj biljku';
        prikazani su labeli i polja za unos podataka za novu biljku (ime,slika,zalijevanje,mjesto i supstrat) 
        """
        glavni_prozor_aplikacije(self.root,'PyFlora Posuda: Ažuriranje biljke',self.nacrtaj_treci_prozor_moj_profil)

        label_s_anchorom(self.root,'ime biljke','quicksand, 14',"warning","w",12,'#f3f6f4',"center",0.15,0.2)
        self.novo_ime_biljke = polje_za_unos(self.root,"warning",None,None,"center",0.225,0.25,45)
        
        #dodavanje podataka o zalijevanju
        label_s_anchorom(self.root,'zalijevanje biljke','quicksand, 14',"warning","w",13,'#f3f6f4',"center",0.15,0.3)
        self.novo_zalijevanje = polje_za_unos(self.root,"warning",None,None,"center",0.225,0.35,45)

        #dodavanje podataka o mjestu biljke: treba li biti na tamnom, svijetlom, hladnom, toplom
        label_s_anchorom(self.root,'mjesto biljke','quicksand, 14',"warning","w",12,'#f3f6f4',"center",0.15,0.4)
        self.novo_mjesto = polje_za_unos(self.root,"warning",None,None,"center",0.225,0.45,45)

        #dodavanje podataka o supstratu: da/ne
        label_s_anchorom(self.root,'supstrat','quicksand, 14',"warning","w",12,'#f3f6f4',"center",0.15,0.5)
        self.novi_supstrat = polje_za_unos(self.root,"warning",None,None,"center",0.225,0.55,45)

        # gumb koji ce spremiti azurirane podatke
        button(self.root,None,"warning-outline","spremi ažurirane podakte",
            lambda:azuriraj_biljku_u_bazu(id_biljke,session,repozitorij,
                                          self.novo_ime_biljke,
                                          self.novo_zalijevanje,
                                          self.novo_mjesto,
                                          self.novi_supstrat),10,20,"center",0.17,0.66)

        #gumb koji ce nas opet odvesti na listu s biljkama da vidimo sto smo spremili
        button(self.root,None,"warning",'POGLEDAJ SVOJE BILJKE',self.prozor_prikaz_biljaka_PyPosuda,10,30,
               "center",0.5,0.8)
        
    def prozor_prikaz_biljaka_PyPosuda(self):
        """
        ova metoda crta prozor u kojem su prikazane
        sve biljke iz baze te sadrži i gumb za dodavanje nove biljke
        """
        self.root.title ("PyFlora Posuda: ovo su vaše biljke")
        glavni_prozor_aplikacije(self.root,"PyFlora Posuda: Biljke",self.nacrtaj_treci_prozor_moj_profil)

        dohvati_sve_biljke_iz_baze_i_nacrtaj_u_gui(self.root,session,gui_objekt=self)

        frame = dodaj_frame_place(self.root,"raised",1,50,500,"heart","warning","ne",0.98,0.75)
        button_s_gridom(frame,"warning-outline","dodaj biljku",self.dodajte_novu_biljku_iz_foldera,10,10,
                        column=3,columnspan=3,row=2,ipadx=10,ipady=3,padx=15,pady=10,sticky="ew")

    def prozor_s_detaljima_o_biljci(self, id_slike):
        """ 
        ova metoda crta prozor 
        na kojem se prikazuju detalji o  
        odabranoj biljci prema id iz baze 
        """
        self.root.title ("PyFlora Posuda: Biljke")
        glavni_prozor_aplikacije(self.root,"PyFlora Posuda: Biljka",self.nacrtaj_treci_prozor_moj_profil)

        # ovo je frame u kojem se ispisuju podaci o biljci koje smo dohvatili iz baze pomocu 
        # funkcije nize: 'prikaz_biljke_prema_id_u_bazi'
        frame_za_tekst=dodaj_frame_place(self.root,None,0,270,150,"heart",None,"center",0.3,0.59)

        # slika biljke i podaci o biljci u 'frame_za_tekst'
        prikaz_biljke_prema_id_u_bazi(self.root,frame_za_tekst,session,id_slike)

        # podaci dohvaceni sa simulatora senzora za vlaznost, kiselost i salinitet zemlje te svijetlost
        # spremljeni u varijable za prikaz na ekranu kod odabrane biljke iz baze
        podaci = dohvati_podatke_sa_senzora()
        vlaznost_zemlje = f'{podaci[0]["vrijednost"]} %'
        kiselost = f'{podaci[1]["vrijednost"]} pH'
        salinitet = f'{podaci[2]["vrijednost"]} dS/m'
        svijetlost = f'{podaci[3]["vrijednost"]} lx'
        
        # frame za vrijednost vlage
        frame_za_vlaznost=dodaj_frame_place(self.root,"raised",1,90,85,"heart",None,"center",0.75,0.16)
        # prikaz vlage izmjerene simulatorom senzora na ekranu
        label(frame_za_vlaznost,f'VLAGA\n\n{vlaznost_zemlje}',('Quicksand',10),"dark","center",None,"center",0.5,0.5)

        frame_za_kiselost=dodaj_frame_place(self.root,"raised",1,90,85,"heart",None,"center",0.61,0.16)
        label(frame_za_kiselost,f'KISELOST\n\n{kiselost}',('Quicksand',10),"dark","center",None,"center",0.5,0.5)

        frame_za_salinitet = dodaj_frame_place(self.root,"raised",1,90,85,"heart",None,"center",0.75,0.33)
        label(frame_za_salinitet,f'SALINITET\n\n{salinitet}',('Quicksand',10),"dark","center",None,"center",0.5,0.5)

        frame_za_svijetlost = dodaj_frame_place(self.root,"raised",1,90,85,"heart",None,"center",0.61,0.33)
        label(frame_za_svijetlost,f'SVIJETLO\n\n{svijetlost}',('Quicksand',10),"dark","center",None,"center",0.5,0.5)


        buttoni_za_azuriranje_i_brisanje_podataka(self.root,"biljku",
            command_azuriraj=lambda:self.prozor_azuriraj_biljku_iz_baze(id_biljke=id_slike),
            command_izbrisi=lambda:izbrisi_biljku_iz_baze(repozitorij,id_biljke=id_slike,gui_objekt=self),
            command_BACK=self.prozor_prikaz_biljaka_PyPosuda,anchor="center",relx=0.5,rely=0.81) #relx=0.7,rely=0.71

        gumb_sinkronizacije(self.root,lambda:self.prozor_s_detaljima_o_biljci(id_slike),440,280)

    def prozor_prikaz_posuda_PyPosuda(self):
        """
        ova metoda crta prozor u kojem su prikazane
        sve PyPosude iz baze
        """
        self.root.title ("PyFlora Posuda: ovo su vaše pametne posude")
        glavni_prozor_aplikacije(self.root,"PyFlora Posuda: PyPosude",self.nacrtaj_treci_prozor_moj_profil)
        dohvati_sve_posude_iz_baze_i_nacrtaj_u_gui(session,self.root,gui_objekt=self)

    def prozor_s_detaljima_o_posudi(self,id_slike):
        """ 
        ova metoda crta prozor na kojem se prikazuju detalji o  
        odabranoj biljci prema id iz baze; takoder prikazuje graf 
        s podacima dohvacenima sa senzora
        """
        self.root.title ("PyFlora Posuda: Biljke")
        glavni_prozor_aplikacije(self.root,"PyFlora Posuda: Posuda",self.nacrtaj_treci_prozor_moj_profil)

        #frame_za_graf=dodaj_frame_place(self.root,None,0,200,250,"heart","#f3f6f4","center",0.335,0.65)

        #ovo je frame u kojem se prikazuje ime posude te ime biljke u posudi
        frame_s_tekstom=dodaj_frame_place(self.root,None,0,270,150,"heart",None,"center",0.5,0.59)

        prikaz_posude_prema_id_u_bazi(self.root,frame_s_tekstom,session,id_slike)

        # button_za_prikaz_grafa = button(frame_za_graf, "warning", None, "PODACI SA SENZORA",
        #                                 graf_podataka_sa_senzora,20,20,"center",0.8,0.6)
        
        # ovo je gumb kojim dobivamo prikaz grafa na idućem prozoru
        button(
            self.root, "warning", None, "PODACI SA SENZORA",
            self.prikazi_graf,20,18,"center",0.5,0.57) # ime varijable kao komentar (!!!!!!!!!!!)
        
        # label(frame_za_graf,
        #       "za više informacija o prikupljenim podacima sa senzora\nodaberite gumb niže",
        #       ("quicksand",10),"warning","right",None,"w",0.3,0.3)

        buttoni_za_azuriranje_i_brisanje_podataka(self.root,"posudu",
            command_azuriraj=lambda:self.prozor_azuriraj_posudu(id_slike),
            command_izbrisi=lambda:izbrisi_posudu_iz_baze(repozitorij,id_posude=id_slike,gui_objekt=self)
            ,command_BACK=self.prozor_prikaz_posuda_PyPosuda,anchor="center",relx=0.5,rely=0.81)

    def prikazi_graf(self):
        glavni_prozor_aplikacije(self.root,"PyFlora: Podaci sa senzora",gumb_moj_profil=self.nacrtaj_treci_prozor_moj_profil)
            
        podaci = dohvati_podatke_sa_senzora()
        obradi_dohvacene_podatke_i_nacrtaj_graf(self.root,podaci=podaci, title="Podaci sa senzora")


        frame = dodaj_frame_place(self.root,"raised",1,50,500,"heart","warning","ne",0.98,0.18)
        button_s_gridom(frame,"warning-outline","BACK",self.prozor_prikaz_posuda_PyPosuda,10,10,
                        column=3,columnspan=3,row=2,ipadx=10,ipady=3,padx=15,pady=10,sticky="ew")


    def prozor_azuriraj_posudu(self,id_slike):
        """ 
        ova metoda crta prozor u kojem su gumbovi za:
        brisanje biljke iz posude;
        zamjenu biljke u posudi;
        dodavanje biljke u posudu
        """
        glavni_prozor_aplikacije(self.root,'PyFlora Posuda: Ažuriranje posude',self.nacrtaj_treci_prozor_moj_profil)
        frame_s_tekstom=dodaj_frame_place(self.root,None,0,270,150,"heart",None,"center",0.5,0.59)
        #frame_za_tekst=dodaj_frame_place(self.root,None,0,350,300,"heart",None,"center",0.6,0.5)

        prikaz_posude_prema_id_u_bazi(self.root,frame_s_tekstom,session,id_slike)
        #prikaz_posude_za_azuriranje_prema_id_u_bazi(self.root,frame_za_tekst,session,id_slike)

        frame = dodaj_frame_place(self.root,"raised",1,50,500,"heart","light","center",0.5,0.81)
        button_s_gridom(frame,"warning.Outline.TButton",f"zamijeni biljku",None,10,11,
                        column=1,columnspan=1,row=1,ipadx=10,ipady=1,padx=10,pady=10,sticky="ew")
        button_s_gridom(frame,"danger-outline",f"isprazni posudu",
                        None,10,11, column=2,columnspan=1,row=1,ipadx=10,ipady=1,padx=10,pady=10,sticky="ew")
        button_s_gridom(frame,"warning-outline","dodaj biljku",None,10,11,
                        column=3,columnspan=1,row=1,ipadx=10,ipady=1,padx=10,pady=10,sticky="ew")
        button_s_gridom(frame,"warning-outline","BACK",lambda:self.prozor_s_detaljima_o_posudi(id_slike),10,11,
                        column=4,columnspan=1,row=1,ipadx=10,ipady=1,padx=10,pady=10,sticky="ew")

        # ovaj gumb vraća na prozor u kojem su prikazane sve posude iz baze
        #button(self.root,None,"warning",'POGLEDAJ SVOJE POSUDE',self.prozor_prikaz_posuda_PyPosuda,10,30,"center",0.5,0.57)


    def prozor_prikaz_korisnika(self):
        """ 
        ova metoda crta prozor na kojem se prikazuju
        korisnici aplikacije kao button (pomocu funkcije prikaz korisnika)
        """
        glavni_prozor_aplikacije(self.root,"PyFlora: Popis korisnika aplikacije",self.nacrtaj_treci_prozor_moj_profil)
        # frame za prikaz korisnika

        frame_za_tekst = dodaj_frame_place(self.root,None,2,250,200,"heart","warning","center",0.5,0.5)
        prikaz_korisnika(frame_za_tekst,session,gui_objekt=self)

    def prozor_s_detaljima_o_korisniku(self,uhvaceni_korisnik):
        print(uhvaceni_korisnik)
        glavni_prozor_aplikacije(self.root,"PyFlora: Moji podaci",self.nacrtaj_treci_prozor_moj_profil)
        buttoni_za_azuriranje_i_brisanje_podataka(self.root,"korisnika",
            command_azuriraj=None,
            command_izbrisi=None,
            command_BACK=self.nacrtaj_treci_prozor_moj_profil, 
            anchor="center",relx=0.5,rely=0.82)
        
        frame_za_tekst=dodaj_frame_place(self.root,None,0,450,400,"heart",None,"center",0.5,0.4)
        prikaz_korisnika_prema_id_iz_baze(frame_za_tekst,session,uhvaceni_korisnik)
       

    def pokreni(self):
        # self.prikaz_korisnika()
        # self.root.mainloop()
        pass
        
session = spoji_se_na_bazu("SQL_PyFlora_Baza.sqlite")
repozitorij = SQLAlchemyRepozitorij(session)

