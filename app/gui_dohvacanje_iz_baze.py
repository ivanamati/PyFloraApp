from sqlalchemy import TextClause
from sqlalchemy.orm import sessionmaker
import sqlalchemy as db
import ttkbootstrap as ttk
from tkinter import Button, Label
from ttkbootstrap.constants import *
from PIL import ImageTk, Image, ImageFilter
from tkinter.messagebox import showerror, showinfo
from tkinter import filedialog
import pandas as pd
from PYFlora_baza_repozitorij import PyPosude
from gui_repozitorij_prozora import *


from PYFlora_baza_repozitorij import Biljke, Korisnik, spoji_se_na_bazu,PyPosude


import os

# u ovom fileu se nalaze funkcije koje omogucuju rad izmedu GUI i BAZE

def lista_podataka_iz_baze_biljke(session):
    """ 
    ova funkcija povlaci sve biljke iz baze te vraca listu biljaka sa svim njezinim podacima
    """

    baza_biljaka=session.execute(TextClause("SELECT * FROM biljke"))
    return baza_biljaka

def lista_podataka_iz_baze_posude(session):
    """ 
    ova funkcija povlaci sve biljke iz baze te vraca listu biljaka sa svim njezinim podacima
    """
    baza_posuda=session.execute(TextClause("SELECT * FROM pyposude"))
    return baza_posuda

def biljka_iz_baze_prema_idu(session,id_biljke):
    """ 
    ova funkcija povlaci biljku iz baze prema njezino idu i vraća baš tu biljku
    """
    biljka_iz_baze=session.execute(TextClause(f"SELECT * FROM biljke where id = {id_biljke}"))
    return biljka_iz_baze

def posuda_iz_baze_prema_idu(session,id_posude):
    """ 
    ova funkcija povlaci posudu iz baze prema njezino idu i vraća baš tu posudu
    """
    posuda_iz_baze=session.execute(TextClause(f"SELECT * FROM pyposude where id = {id_posude}"))
    return posuda_iz_baze

def dohvati_sve_biljke_iz_baze_i_nacrtaj_u_gui(root,session,gui_objekt):
    """ ova metoda dohvaća sve biljke s njihovim podacima iz baze
    te crta jednu po jednu u zaseban frame preko petlje u gui;
    dodan joj je argument SELF, kako bi radila LAMBDA iz funkcije 
    'ubaci_sliku_u_label' preko koja dohvaćamo ID slike biljke na koju smo kliknuli;
    taj self je objekt tipa PyFlora za prikaz na GUI-u 
    """
    baza_biljaka = lista_podataka_iz_baze_biljke(session)
    stupac = 0
    redak = 0
    
    for biljka in baza_biljaka: 
        glavni_frame  = dodaj_frame(root,'raised',redak,stupac,"white",110,145,1,23,20) 
        lijevi_frame = dodaj_frame(glavni_frame,"flat",redak,0,"white",width=110,height=145,borderwidth=0,padx=None,pady=None)    # svijetlo zuta - FFE890
        desni_frame = dodaj_frame(glavni_frame,"flat",redak,1,"default",width=100,height=145,borderwidth=0,padx=None,pady=None)   # svijetlo zuta - FFE890
        
        ubaci_sliku_kao_button_u_label_biljke(glavni_frame, putanja_slike=biljka.slika_biljke,id_slike=biljka.id,gui_objekt=gui_objekt,repozitorij=gui_objekt.repozitorij) 
        ubaci_tekst_u_label(lijevi_frame, biljka.ime_biljke,font="quicksand, 10",bootsytle="warning",relx=0.5,rely=0.8)

        zalijevanje = biljka.zalijevanje
        mjesto = biljka.mjesto
        supstrat = biljka.supstrat

        label(
            glavni_frame,f"'{biljka.ime_biljke}'\nZalijevanje je potrebno jednom {zalijevanje},\npoželjno mjesto je {mjesto}.\nSupstrat:{supstrat}",
              "quicksand, 8","dark","center",None,"center",0.5,0.75)
      
        stupac += 1      
        if stupac >= 3:
            redak +=1
            stupac = 0 
        
        # metodu za dodavanje biljke vise ne koristim jer sam umjesto frame i velikog gumba koji se ispisuje
        # prema retku nakon svih biljaka dodala obicni gumb ispod sinkronizacije za dodavanje
        # nove biljke
        # ali se metoda moze iskoristiti za prikaz POSUDA, 
        # odnosno kao opcija za dodavanje NOVE posude:
        # dodajmo_novu_biljku_na_listu(self.root,redak,stupac,self.dodajte_novu_biljku_iz_foldera)

def ubaci_sliku_kao_button_u_label_biljke(neki_frame, putanja_slike, id_slike,gui_objekt,repozitorij):
        """ 
        ova metoda prikazuje sliku u odabranom labelu
        takoder povezuje prikazanu sliku s njezinim id-om slika je GUMB;
        klikom na njega otvara se prikazan/odabran cvijet
        """
        img= dohvati_sliku(width=105, height=65,ime_slike=putanja_slike)
        if img is not None:
            label_slika = ImageTk.PhotoImage(img)
            # ovim gumbom dobivamo prikaz biljke te DOHVACAMO ID biljke iz baze da prikaze podatke bas za tu biljku  
            slika_u_lijevom_frameu = ttk.Button(
                neki_frame,
                image=label_slika,
                bootstyle="warning.outline",
                padding=1,
                command=lambda:gui_objekt.prozor_s_detaljima_o_biljci(id_slike=id_slike)
            )   
            slika_u_lijevom_frameu.image = label_slika
            slika_u_lijevom_frameu.place(anchor='center', relx=0.5, rely=0.26)
            return id_slike
        else:
            button_s_gridom(neki_frame,"danger-outline",f"izbriši biljku",
                    lambda:izbrisi_biljku_iz_baze(repozitorij=repozitorij,id_biljke=id_slike,gui_objekt=gui_objekt),
                    10,11, column=3,columnspan=3,row=5,ipadx=1,ipady=3,padx=20,pady=20,sticky="ew")
            label(neki_frame,"Slika nije pronađena",('quicksand',8),"warning",None,None,
                  "center",0.5,0.9)
            #ubaci_tekst_u_label(neki_frame, "Slika nije pronađena",font="quicksand, 10",bootsytle="warning",relx=0.1,rely=0.1)    

def prikaz_korisnika(frame,session,gui_objekt):
    """ ova funkcija u bazi odabire sve korisnike
        te ih ispisuje u obliku tablice prikazujuci njihov
        id, ime i lozinku;
        imena se ispisuju kao gumbi koji potom prikazuju pojedinog korisnika """
    
    tablica_korisnika=session.execute(TextClause("SELECT * FROM Korisnici"))
    e=ttk.Label(frame,width=20,text='IME KORISNIKA\nodaberite ime korisnika',
        font="quicksand, 10",borderwidth=2, anchor='center',bootstyle="warning-inverse",justify="center")
    e.grid(row=0,column=0)

    red=1
    
    #i=0 
    for user in tablica_korisnika: 
        user_id = user.id
        #print(user_id)
        ttk.Button(
            frame, width=30, padding=10,
            text=user.username,
            bootstyle="warning.outline",
            #command=lambda:prikaz_korisnika_prema_id_iz_baze(frame,session,uhvaceni_korisnik=user.id,gui_objekt=gui_objekt,root=gui_objekt.root)
            command=lambda:gui_objekt.prozor_s_detaljima_o_korisniku(uhvaceni_korisnik=user_id)
            # ova lambda ne radi dobro i stalno vraca posljednjeg korisnika iz baze!!!
        ).grid(row=red, column=0)   #column=stupac
        red=red+1

def prikaz_korisnika_prema_id_iz_baze(frame,session,uhvaceni_korisnik):
    #gui_objekt.prozor_s_detaljima_o_korisniku(uhvaceni_korisnik)

    tablica_korisnika=session.execute(TextClause(f"SELECT * FROM Korisnici WHERE id = {uhvaceni_korisnik}"))

    for user in tablica_korisnika: 
        ime_korisnika = user.username
        lozinka = user.password

    label(frame,f"Bok, {ime_korisnika}!",("quicksand",14), "warning",None,None,"nw",0.4,0.1)
    label(frame,f"Tvoje korisničko ime je: {ime_korisnika}",("quicksand",12), "warning",None,None,"center",0.5,0.3)
    label(frame,f"Tvoja lozinka je: {lozinka}",("quicksand",12), "warning",None,None,"center",0.5,0.4)
    label(frame,
          "Za ažuriranje podataka odaberi gumb 'ažuriraj korisnika'\nZa brisanja korisnika odaberi gumb 'izbriši korisnika'\nZa povratak odaberite gumb 'BACK'",
          ("quicksand",10), "primary","center",None,"center",0.5,0.7)

def prikaz_biljke_prema_id_u_bazi(frame,frame_za_tekst,session,id_slike):
    """ ova funkcija nakon klika na gumb biljke
    dohvaca biljku prema njezinom ID-u iz baze
    te daje prikaz njezinih podataka iz baze """

    baza_biljaka=session.execute(TextClause(f"SELECT * FROM biljke where id = {id_slike}"))  
    for biljka in baza_biljaka:
        img = dohvati_sliku(width=250, height=165,ime_slike=biljka.slika_biljke)
        if img is not None:
            label_slika = ImageTk.PhotoImage(img)
            slika_biljke = ttk.Label(frame, image=label_slika,bootstyle="light-inverse",borderwidth=15,relief="groove")
            slika_biljke.image = label_slika
            # ovom place metodom se prikazuje slika na zeljenoj poziciji na prozoru GUI-a
            slika_biljke.place(anchor='center', relx=0.3, rely=0.25)
            # ova funckija ispisuje samo ime biljke iz baze
            ubaci_tekst_u_label(frame_za_tekst,ime_slike=biljka.ime_biljke,font="quicksand, 15",bootsytle="dark",relx=0.2,rely=0.1)

            zalijevanje = biljka.zalijevanje
            mjesto = biljka.mjesto
            supstrat = biljka.supstrat

    # ovdje se ispisuju karakteristike biljaka vezane za NJEGU
    label(frame_za_tekst,
            f"Zalijevanje: jednom {zalijevanje}\n\nMjesto u stanu: {mjesto}\n\nZahtjeva supstrat: {supstrat}",
            ('Quicksand',10),"dark",None,None,"nw",0.02,0.3)
        
def dohvati_sliku(width, height,ime_slike,folder_name="SLIKE_BILJAKA"):
    if not ime_slike:
        return None
        
    putanja = spoji_sliku_s_folderom(ime_slike,folder_name=folder_name)
    if not os.path.exists(putanja):
        return None

    try:
        img = Image.open(putanja) 
        img = img.resize((width, height))
        return img
    except FileNotFoundError:
        return None
    
def spoji_sliku_s_folderom(photo_filename,folder_name):
    if os.path.exists(photo_filename):
        return photo_filename
    #  puna putanja do foldera sa slikama koji se nalazi odmah uz ovaj file
    folder_sa_slikama = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),   # folder u kojem se nalazi ovaj file
            #"SLIKE_BILJAKA"              # folder u koji ćemo spremati slike
            folder_name
        )
    )
    slika_puna_putanja = os.path.join(
        folder_sa_slikama, 
        photo_filename
    )
    return slika_puna_putanja

def azuriraj_biljku_u_bazu(id_biljke,session,repozitorij,novo_ime_biljke,novo_zalijevanje,novo_mjesto,novi_supstrat):
    """ ova se funkcija pokrece pritiskom na gumb u prozoru 'prozor_azuriraj_biljku_iz_baze'
        te azurira odabranu biljku iz baze novim podacima;
        novi podaci o biljci dohvacaju se s prozora 'prozor_azuriraj_biljku_iz_baze'
        za biljku koju smo odabrali preko njezinog id;
        potom se ova funkcija spaja na bazu i izvodi se UPDATE prema njezinom idu s novim podacima"""
    #print(f"mijenjamo: {id_biljke}") #- ovo je tocan id biljke iz baze!!!

    biljka_iz_baze=biljka_iz_baze_prema_idu(session,id_biljke)
    for biljka in biljka_iz_baze:        
        # provjera
        # print(f"mijenjamo: {biljka.ime_biljke}, {biljka.zalijevanje}, {biljka.mjesto}, {biljka.supstrat}")

        ime_biljke = novo_ime_biljke.get()
        slika_biljke = biljka.slika_biljke
        zalijevanje = novo_zalijevanje.get()
        mjesto = novo_mjesto.get()
        supstrat = novi_supstrat.get()

        # ovo je kljucni dio ove funkcije
        # na ovaj se nacin azurira biljka u bazi preko metode 'update_biljka' iz repozitorija metoda nad klasama za baze
        repozitorij.azuriraj_biljku("SQLalchemy_PyFlora_Baza.sqlite",ime_biljke,zalijevanje,mjesto,supstrat,id_biljke)

    showinfo(title="OK!", message="Podaci uspješno spremljeni!")

                
def otvori_i_spremi_sliku_biljke_od_korisnika(repozitorij,ime_nove_biljke,zalijevanje,mjesto,supstrat):
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
            
            putanja_do_slike = spoji_sliku_s_folderom(nova_slika,folder_name="SLIKE_BILJAKA")
            # na disk spremamo sa punom putanjom da se ne spremi 
            # u folderu iz kjeg je pozvana aplikacija
            img.save(putanja_do_slike)
            img.close()
    else:
            nova_slika = ""
        # u bazu putanju do slike spremamo samo ime slike
    repozitorij.spremi_biljku(Biljke(
                ime_biljke=ime_nove_biljke.get(),
                slika_biljke=nova_slika,
                zalijevanje = zalijevanje.get(),
                mjesto = mjesto.get(),
                supstrat = supstrat.get())
            )
    showinfo(title="YES!", message=f"Slika '{putanja_slike}' uspješno spremljena!")


# !!! NOVA METODA
def otvori_i_spremi_posudu_od_korisnika(repozitorij,ime_nove_posude,posadena_biljka):
    """ ova metoda otvara posudu iz foldera korisnika 
        i sprema je u isti folder 
        s imenom koje je korisnik odabrao """
    # otvaranje slike iz foldera
    photo_filename = filedialog.askopenfilename(title ='Open image')
    img = Image.open(str(photo_filename))
    img = img.resize((150, 110))
    label_slika = ImageTk.PhotoImage(img)
    
    # spremanje slike i putanje u folder
    putanja_slike = f'{ime_nove_posude.get()}.jpg'

    if img:
            nova_slika = f'{ime_nove_posude.get()}.jpg'
            
            putanja_do_slike = spoji_sliku_s_folderom(nova_slika,folder_name="SLIKE_POSUDA")
            # na disk spremamo sa punom putanjom da se ne spremi 
            # u folderu iz kjeg je pozvana aplikacija
            img.save(putanja_do_slike)
            img.close()
    else:
            nova_slika = ""
        # u bazu putanju do slike spremamo samo ime slike
    repozitorij.spremi_posudu(PyPosude(
                ime_posude=ime_nove_posude.get(),
                slika_posude=nova_slika,
                posadena_biljka = posadena_biljka.get()
                )
            )
    showinfo(title="YES!", message=f"Posuda '{putanja_slike}' uspješno spremljena!")


def izbrisi_biljku_iz_baze(repozitorij,id_biljke,gui_objekt):
    repozitorij.delete_biljka(id=id_biljke)
    showinfo(title="OK", message=f"Biljka je uspješno izbrisana!")
    gui_objekt.prozor_prikaz_biljaka_PyPosuda()

def izbrisi_posudu_iz_baze(repozitorij,id_posude,gui_objekt):
    repozitorij.delete_posuda(id=id_posude)
    showinfo(title="OK", message="Posuda je uspješno izbrisana!")
    gui_objekt.prozor_prikaz_posuda_PyPosuda()

def provjeri_lozinku(lozinka):
    """ ova funkcija provjerava duljinu lozinke;
    trenutno je ne koristim """
    if len(lozinka) < 3:
        showinfo(title="UPS!", message=f"Duljina vaše lozinke je {len(lozinka)}, \na mora sadržavati najmanje 3 znaka")
    else:
        return lozinka
    
def provjeri_korisnika_u_bazi(repozitorij,username):
    korisnik = repozitorij.get_user_by_username(username.get())
    return korisnik
    
def spremi_korisnika_korisnicko_ime_i_lozinka(root,repozitorij,gui_objekt):
    """ ova metoda piše labele korisnicko ime i lozinka;
    polja za upis korisnickog imena i lozinke 
    te gumb za spremanje novog korisnika"""

    label(root,'username','quicksand, 14',"warning",None,'#f3f6f4',"center",0.2,0.3)
    username = polje_za_unos_username(root,"warning",('quicksand' , 9),"center",0.4,0.3)

    label(root,'password','quicksand, 14',"warning",None,'#f3f6f4',"center",0.2,0.4)
    password = polje_za_unos(root,"warning",('quicksand',9),"*","center",0.4,0.4,20)

    ttk.Button(root, text='registriraj korisnika',
    style='warning.Outline.TButton',
    bootstyle="warning-outline", 
    command=lambda:spremi_korisnika(root,repozitorij,username,password,gui_objekt),
    padding=10, width=30
    ).place(anchor="center",relx=0.3,rely=0.6)

def spremi_korisnika(root,repozitorij,username,password,gui_objekt):
    """ ova metoda prima username i password koji je unio korisnik
        u Entry, provjera postoji li user;
        ako user postoji, nudi ponovni unos novog korisnika,
        a ako je usera nema u bazi, sprema ga"""
    print(f"Username: {username.get()}")
    print(f"Password: {password.get()}")
    username = username.get()
    password = password.get()
    korisnik = repozitorij.get_user_by_username(username)
    if korisnik: 
        showinfo(title="Registracija",message=f"Korisnik {username} već postoji.")
        spremi_korisnika_korisnicko_ime_i_lozinka(root=root,repozitorij=repozitorij,gui_objekt=gui_objekt)
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
        gui_objekt.prozor_prikaz_korisnika()

def provjeri_korisnika_postoji_li_u_bazi(repozitorij, gui_objekt):
    """
    ova metoda provjerava postoji li na GUI uneseni username
    i lozinka u bazi korisnika;
    ako postoji prikazuje pozdravni prozor za korisnika,
    ako ne postoji vraća na ponovni odabir login ili registracija,
    a ako postoji, ali je pogresna lozinka daje tu obavijest te nudi ponovni unos
    """
    korisnik = provjeri_korisnika_u_bazi(repozitorij,username=gui_objekt.username)
    if korisnik:
        if gui_objekt.password.get() == korisnik.password:

            print(f"Korisnik {gui_objekt.username.get()} postoji u bazi. Ulaz slobodan.")
            gui_objekt.nacrtaj_drugi_prozor(korisnik.username) 
        else: 
            showinfo(title="Registracija", message=f"Korisnik '{korisnik.username}' postoji.\n lozinka je neispravna! Pokušaj ponovo!")
            gui_objekt.nacrtaj_prvi_prozor_login()
            print(f'Korisnička lozinka je neispravna')
    else:
        showinfo(title="Registracija", message=f"Korisnik {gui_objekt.username.get()} ne postoji!")
        print(f'Korisnik ne postoji')
        gui_objekt.prozor_ulaska_login_ili_registracija()

def ubaci_sliku_kao_button_u_label_posude(neki_frame, putanja_slike, id_slike,gui_objekt):
        """ 
        ova metoda prikazuje sliku u odabranom labelu
        takoder povezuje prikazanu sliku s njezinim id-om slika je GUMB;
        klikom na njega otvara se prikazan/odabran cvijet
        """
        img= dohvati_sliku(width=125, height=85,ime_slike=putanja_slike,folder_name="SLIKE_POSUDA")
        if img is not None:
            label_slika = ImageTk.PhotoImage(img)
            # ovim gumbom dobivamo prikaz biljke te DOHVACAMO ID biljke iz baze da prikaze podatke bas za tu biljku  
            slika_u_lijevom_frameu = ttk.Button(
                neki_frame,
                image=label_slika,
                bootstyle="warning.outline",
                padding=1,
                command=lambda:gui_objekt.prozor_s_detaljima_o_posudi(id_slike=id_slike)
            )   
            slika_u_lijevom_frameu.image = label_slika
            slika_u_lijevom_frameu.place(anchor='center', relx=0.5, rely=0.4)

        else:
            ubaci_tekst_u_label(neki_frame, f"Slika\n {putanja_slike}\n nije pronađena",
                                font="quicksand, 10",bootsytle="warning",relx=0.5,rely=0.1)    

def dohvati_sve_posude_iz_baze_i_nacrtaj_u_gui(session,frame,gui_objekt):
    """ova funkcija dohvaca sve posude iz baze u obliku liste 
    te prikazuje postojece posude u posebnim frameovima
    pomocu for petlje pri cemu je slika posude gumb koji prikazuje
    podatke o odabranoj posudi"""

    baza_posuda=lista_podataka_iz_baze_posude(session)
    stupac = 0
    redak = 0
                
    for posuda in baza_posuda: 
        # frameovi

        glavni_frame  =  ttk.Frame(frame,  width=10,  height=50, borderwidth=1, relief='raised', style="deafult")
        glavni_frame.grid(row=redak, column=stupac, padx=23, pady=20) #pady=110
        # pape = self.dodaj_redak(redak,stupac*2,1)
        lijevi_frame = dodaj_frame(glavni_frame,None,redak,0,"white",150,145,None,None,None)    # svijetlo zuta - FFE890
        desni_frame = dodaj_frame(glavni_frame,None,redak,1,"default",150,145,None,None,None)   # svijetlo zuta - FFE890
        
        ubaci_sliku_kao_button_u_label_posude(lijevi_frame, putanja_slike=posuda.slika_posude,id_slike=posuda.id,gui_objekt=gui_objekt) 
        ubaci_tekst_u_label(lijevi_frame, posuda.ime_posude,font="quicksand, 10",bootsytle="warning",relx=0.5,rely=0.8)

        posadena_biljka = posuda.posadena_biljka
        posadena_biljka = ttk.Label(desni_frame, text=f'BILJKA:\n{posadena_biljka}',font="quicksand, 8", bootstyle= "default", justify='left')   # svijetlo zuta - FFE890
        posadena_biljka.place(anchor ='s',relx=0.3,rely=0.95)

        # VAZNO ovdje napraviti prikaz informacija o odabranoj posudi
        # prikaz_biljke_prema_id_u_bazi(self.root,frame_za_tekst,session,id_slike)
        
        stupac += 1
                    
        if stupac >= 2:
            redak +=1
            stupac = 0 

def prikaz_posude_prema_id_u_bazi(frame,frame_za_tekst,session,id_slike):
    """ ova funkcija nakon klika na gumb posude
    dohvaca posudu prema njezinom ID-u iz baze
    te daje prikaz njezinih podataka iz baze """

    baza_posuda=posuda_iz_baze_prema_idu(session,id_posude=id_slike)

    for posuda in baza_posuda:
        img = dohvati_sliku(width=250, height=165,ime_slike=posuda.slika_posude,folder_name="SLIKE_POSUDA")
        if img is not None:
            label_slika = ImageTk.PhotoImage(img)
            label_kao_slika(
                frame=frame,
                image=label_slika,
                bootsytle="light_inverse",
                borderwidth=15,
                relief="groove",
                anchor="center",
                relx=0.5,
                rely=0.25
            )
            ubaci_tekst_u_label(frame_za_tekst,ime_slike=posuda.ime_posude,font="quicksand, 15",bootsytle="dark",relx=0.5,rely=0.1)

        ime_posude = posuda.ime_posude
        posadena_biljka = posuda.posadena_biljka


    # ovdje se ispisuje ime posude i koja se biljka nalazi u posudi
    label(frame_za_tekst,f"Posuda: '{ime_posude}'\nBiljka u posudi: {posadena_biljka}",
            ('Quicksand',10),"warning",None,None,"nw",0.1,0.7)

    
def prikaz_posude_za_azuriranje_prema_id_u_bazi(frame,frame_za_tekst,session,id_slike):
    """ ova funkcija nakon klika na gumb posude
    dohvaca posudu prema njezinom ID-u iz baze
    te daje prikaz njezinih podataka iz baze """

    baza_posuda=session.execute(TextClause(f"SELECT * FROM pyposude where id = {id_slike}"))  
    for posuda in baza_posuda:
        img = dohvati_sliku(width=250, height=165,ime_slike=posuda.slika_posude, folder_name="SLIKE_POSUDA")
        if img is not None:
            label_slika = ImageTk.PhotoImage(img)
            label_kao_slika(
                frame=frame,
                image=label_slika,
                bootsytle="light_inverse",
                borderwidth=15,
                relief="groove",
                anchor="center",
                relx=0.5,
                rely=0.5
            )
            ubaci_tekst_u_label(frame_za_tekst,ime_slike=posuda.ime_posude,font="quicksand, 15",bootsytle="dark",relx=0.5,rely=0.1)

            ime_posude = posuda.ime_posude
            posadena_biljka = posuda.posadena_biljka

    # ovdje se ispisuju karakteristike biljaka vezane za NJEGU
    label(frame_za_tekst,f"Posuda: '{ime_posude}'\n\n Biljka u posudi: {posadena_biljka}",
            ('Quicksand',10),"dark",None,None,"nw",0.1,0.7)
    
    
def proba_prikaza_podataka_o_biljci_iz_baze(ime_baze):
    session = spoji_se_na_bazu(ime_baze)    
    ime_tablice_iz_baze = "biljke"  # ovo je ime tablice u SQL_PyFlora_Baza.sqlite
                                # mora biti ime tablice jer koristim funkciju "read_sql_table" iz pandasa
                                # ako mijenjam ime tablice dobijem podatke iz svih tih drugih
    connection = session.connection()
    biljka = pd.read_sql_table(table_name=ime_tablice_iz_baze, con=connection)
    print(biljka)
