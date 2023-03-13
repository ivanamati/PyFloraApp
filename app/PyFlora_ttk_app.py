#from sqlalchemy import TextClause
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import Style
from PIL import ImageTk, Image, ImageFilter
from tkinter.messagebox import showerror, showinfo
from tkinter import filedialog

from gui_repozitorij_prozora import *
from gui_baza_i_dohvacanje import *

from SQLAlchemy_seminarski_repo import SQLAlchemyRepozitorij, Korisnik, Biljke, spoji_se_na_bazu


class PyFlora:

    def __init__(self, repozitorij):
        # DIO ZA root ELEMENT
        self.root = ttk.Window(themename="flatly")
        self.root.title('PyFlora - PRIJAVA')
        self.width = 960
        self.height = 640
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
      
    def unos_korisnicko_ime_i_lozinka(self):
        """ 
        ova metoda piše labele korisnicko ime i lozinka
        te polja za upis korisnickog imena i lozinke 
        """
        label(self.root,'username','quicksand, 14',"warning",None,'#f3f6f4',"center",0.2,0.3)
        self.username = ttk.Entry(self.root, bootstyle="warning", font = ('quicksand' , 9))
        self.username.place(anchor="center",relx=0.4,rely=0.3)

        label(self.root,'password','quicksand, 14',"warning",None,'#f3f6f4',"center",0.2,0.4)
        self.password = ttk.Entry(self.root, bootstyle="warning",show="*")
        self.password.place(anchor="center",relx=0.4,rely=0.4,width=154)

    def provjeri_korisnika(self):
        """ 
        ova metoda provjerava postoji li korisnik u bazi 
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
            self.prozor_ulaska_login_ili_registracija()
            
    def nacrtaj_naslovnicu_aplikacije(self):
        """ 
        ova metoda je naslovnica aplikacije s gumbom loga za ulaz u aplikaciju; 
        ovdje samo ulazimo u aplikaciju 
        """
        clear_frame(self.root)
        #self.root.title('PyFlora Aplikacija')
        velika_slika_posred_ekrana(self.root,"media\cvijet.png")
        naslovnica(self.root,self.prozor_ulaska_login_ili_registracija)

    def prozor_ulaska_login_ili_registracija(self):
        """ 
        ova metoda ispisuje prozor 
        koji nudi korisniku opciju LOGINA 
        ili upisa NOVOG korisnika u obliku gumba
        """
        clear_frame(self.root)
        self.root.title('PyFlora Aplikacija')
        self.root["bg"]="white"
        velika_slika_posred_ekrana(self.root,'media\PyFlora_crno_zuta.jpg')
        
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
        glavni_prozor_aplikacije(self.root, "PyFlora: dodajmo novog korisnika",self.nacrtaj_treci_prozor_moj_profil)
        spremi_korisnika_korisnicko_ime_i_lozinka(self.root,repozitorij) 
        self.root['bg']= '#f3f6f4'
        button(self.root,'warning.Outline.TButton',None,'pogledaj korisnike',
               self.prozor_prikaz_korisnika,10,30,"center",0.3,0.7)

    def nacrtaj_prvi_prozor_login(self): 
        """ 
        ova metoda crta prvi prozor aplikacije u kojem se 
        postojeci korisnik
        LOGIRA u aplikaciju PyFlora
        """
        header_za_prvi_i_drugi_prozor(self.root,"#f3f6f4",None)
        self.unos_korisnicko_ime_i_lozinka()
        button(self.root,'warning.Outline.TButton',"warning-outline",'login',
               self.provjeri_korisnika,10,30,"center",0.3,0.5)
 
    def nacrtaj_drugi_prozor(self, username):
        """ 
        ova metoda crta prozor u kojem pozdravljamo
        korisnika koji se uspjesno ulogirao 
        i sadrzi gumb za nastavak 
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

        frame_za_gumbe = ttk.Frame(
            self.root, relief="raised", borderwidth=1, 
            width=250,height=600,cursor="heart",style="warning")
        frame_za_gumbe.place(anchor='ne', relx=0.6, rely=0.17)
        #frame_za_gumbe.grid(column=1, row=1, padx=5, pady=5)
       
        button_s_gridom(frame_za_gumbe,"warning-outline","popis korisnika",self.prozor_prikaz_korisnika,10,30,
                        column=3,columnspan=3,row=2,ipadx=10,ipady=3,padx=15,pady=10,sticky="ew")

        button_s_gridom(frame_za_gumbe,"warning-outline","pogledaj svoje biljke",self.prozor_prikaz_biljaka_PyPosuda,10,30,
                        column=3,columnspan=3,row=3,ipadx=10,ipady=3,padx=10,pady=10,sticky="ew")
        
        button_s_gridom(frame_za_gumbe,"warning-outline","pogledaj svoje posude",#self.prozor_prikaz_posuda_PyPosuda,
                        None,10,30,
                        column=3,columnspan=3,row=4,ipadx=10,ipady=3,padx=10,pady=10,sticky="ew")
        
        button_s_gridom(frame_za_gumbe,"warning-outline","moji podaci",None,10,30,
                        3,3,5,10,3,10,10,"ew")
        
        button_s_gridom(frame_za_gumbe,"warning-outline","dodaj novog korisnika",self.prozor_za_dodavanje_novog_korisnika,
                        10,30,3,3,6,10,3,10,10,"ew")

        button_s_gridom(frame_za_gumbe,"warning-outline","vrati se na pocetak",self.nacrtaj_naslovnicu_aplikacije,
                        10,30,3,3,7,10,3,10,10,"ew")
        
        button_s_gridom(frame_za_gumbe,"danger-outline","IZLAZ",self.root.destroy,
                        10,30,3,3,8,10,3,10,10,"ew")

    def dodajte_novu_biljku_iz_foldera(self):
        """ 
        ova metoda dodaje i sprema NOVU biljku na gumbu gumb_za_novu_biljku 
        """
        glavni_prozor_aplikacije(self.root,'PyFlora Posuda: Nova biljka',self.nacrtaj_treci_prozor_moj_profil)
        
        label(self.root,'ime biljke','quicksand, 14',"warning",None,'#f3f6f4',"center",0.2,0.3)
        self.ime_nove_biljke = ttk.Entry(self.root, bootstyle="warning")
        self.ime_nove_biljke.place(anchor="center",relx=0.4,rely=0.3)

        label(self.root,'odaberite sliku','quicksand, 14',"warning",None,'#f3f6f4',"center",0.2,0.4)

        # gumb koji ce otvoriti prozor za odabir slike te je spremiti nakon odabira
        button(self.root,None,"warning-outline","odaberi sliku biljke",
               lambda:otvori_i_spremi_sliku_biljke_od_korisnika(repozitorij,self.ime_nove_biljke),
               10,20,"center",0.4,0.4)

        #gumb koji ce nas opet odvesti na listu s biljkama
        button(self.root,None,"warning",'POGLEDAJ SVOJE BILJKE',self.prozor_prikaz_biljaka_PyPosuda,10,30,
               "center",0.4,0.6)
        
    def ubaci_sliku_u_label(self, neki_frame, putanja_slike, id_slike):
        """ 
        ova metoda prikazuje sliku u odabranom labelu
        takoder povezuje prikazanu sliku s njezinim id-om
        slika je GUMB;
        klikom na njega otvara se prikazan/odabran cvijet
        """
        img= dohvati_sliku(width=115, height=75,ime_slike=putanja_slike)
        if img is not None:
            label_slika = ImageTk.PhotoImage(img)

            # ovim gumbom dobivamo prikaz biljke te DOHVACAMO ID biljke iz baze da prikaze podatke bas za tu biljku  
            slika_u_lijevom_frameu = ttk.Button(
                neki_frame,
                image=label_slika,
                bootstyle="warning",
                padding=2,
                command=lambda:self.prozor_s_detaljima_o_biljci(id_slike=id_slike)
            )   # ovo sam pronasla na internetu
            slika_u_lijevom_frameu.image = label_slika
            slika_u_lijevom_frameu.place(anchor='center', relx=0.5, rely=0.5)
        else:
            ubaci_tekst_u_label(neki_frame, f"Slika\n {putanja_slike}\n nije pronađena",font="quicksand, 10",bootsytle="warning")

    def prozor_prikaz_biljaka_PyPosuda(self):
        """
        ova metoda crta prozor u kojem su prikazane
        sve biljke iz baze te sadrži i gumb za dodavanje nove biljke
        """
        self.root.title ("PyFlora Posuda: ovo su vaše biljke")
        glavni_prozor_aplikacije(self.root,"PyFlora Posuda: Biljke",self.nacrtaj_treci_prozor_moj_profil)

        baza_biljaka=session.execute("SELECT * FROM biljke")#TextClause("SELECT * FROM biljke") 
        stupac = 0
        redak = 0
        
        for biljka in baza_biljaka: 
            # frameovi
            glavni_frame  =  ttk.Frame(self.root,  width=300,  height=200, borderwidth=1, relief='raised', style="deafult")
            glavni_frame.grid(row=redak, column=stupac, padx=31, pady=70) #pady=110
            # pape = self.dodaj_redak(redak,stupac*2,1)
            lijevi_frame = dodaj_frame(glavni_frame,redak,0,"warning")    # svijetlo zuta - FFE890
            desni_frame = dodaj_frame(glavni_frame,redak,1,"default")   # svijetlo zuta - FFE890
            
            self.ubaci_sliku_u_label(lijevi_frame, putanja_slike=biljka.slika_biljke, id_slike=biljka.id) 
            ubaci_tekst_u_label(desni_frame, biljka.ime_biljke,font="quicksand, 10",bootsytle="warning")

            status_biljke = ttk.Label(desni_frame, text='Status: ',font="quicksand, 8", bootstyle= "default", justify='left')   # svijetlo zuta - FFE890
            status_biljke.place(anchor ='s',relx=0.2,rely=0.95)
            
            stupac += 1
                     
            if stupac >= 2:
                redak +=1
                stupac = 0 
        dodajmo_novu_biljku_na_listu(self.root,redak,stupac,self.dodajte_novu_biljku_iz_foldera)

    def prozor_s_detaljima_o_biljci(self, id_slike):
        """ 
        ova metoda crta prozor 
        na kojem se prikazuju detalji o  
        odabranoj biljci prema id iz baze 
        """
        self.root.title ("PyFlora Posuda: Biljke")
        glavni_prozor_aplikacije(self.root,"PyFlora Posuda: Biljka",self.nacrtaj_treci_prozor_moj_profil)

        frame_za_tekst = ttk.Frame(self.root, width=350,height=300,padding=2,borderwidth=0)
        frame_za_tekst.place(anchor="center",relx=0.6,rely=0.5)

        label(frame_za_tekst,"Karakteristika 1:\n\nKarakteristika 2:\n\nKarakteristika 3:",
              ('Quicksand',10),"dark",None,None,"nw",0.02,0.5)
        prikaz_biljke_prema_id_u_bazi(self.root,frame_za_tekst,session,id_slike)
        button(self.root,"warning.TButton.Outline",None,"BACK",self.prozor_prikaz_biljaka_PyPosuda,10,16,
               "center",0.875,0.22)
             
    def prozor_prikaz_korisnika(self):
        """ 
        ova metoda crta prozor na kojem se prikazuju
        korisnici apliakcije s njihovim id-om i lozinkom 
        """
        glavni_prozor_aplikacije(self.root,"PyFlora: Popis korisnika aplikacije",self.nacrtaj_treci_prozor_moj_profil)
        # frame za prikaz korisnika
        prvi_frame = ttk.Frame(self.root, style="warning", borderwidth=2, width=250,height=200,cursor="heart")
        #prvi_frame.grid(column=1, row=0, padx=10, pady=10)
        prvi_frame.place(anchor='center', relx= 0.3,rely=0.5)
        prikaz_korisnika(prvi_frame,session)
       
    def pokreni(self):
        #self.prikaz_korisnika()
        #self.nacrtaj_naslovnicu_aplikacije()
        # self.root.mainloop()
        pass
        
session = spoji_se_na_bazu("SQL_PyFlora_Baza.sqlite")
repozitorij = SQLAlchemyRepozitorij(session)

# if __name__ == "__main__":
#     gui_program = PyFlora(repozitorij=repozitorij)
#     gui_program.pokreni()