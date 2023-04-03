# from sqlalchemy import TextClause
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import ImageTk, Image, ImageFilter
from tkinter.messagebox import showerror, showinfo
from tkinter import filedialog
from time import strftime
from datetime import datetime,date

# u ovom fileu se nalaze funkcije koje crtaju odredene dijelove GUI-a

def prikaz_datuma(root,):
    danas = date.today()
    # dd/mm/YY
    datum = danas.strftime("%d.%m.%Y.")
    vrijeme = strftime("%H:%M:%S")

    label_s_anchorom(root,f"{datum}",('quicksand',10),"primary","center",None,None,"center",0.5,0.1)

def polje_za_unos_username(root,bootstyle,font,anchor,relx,rely):
    """ ova metoda crta unos usernamea te 
    nakon unosa username vraća username """
    username = ttk.Entry(root, bootstyle=bootstyle, font = font)
    username.place(anchor=anchor,relx=relx,rely=rely)
    return username

def polje_za_unos(root,bootstyle,font,show,anchor,relx,rely,width):
    """ ova metoda crta unos lozinke te 
    nakon unosa vraca password """
    password = ttk.Entry(root, bootstyle=bootstyle,font=font,show=show,width=width)
    password.place(anchor=anchor,relx=relx,rely=rely)
    return password

def glavni_prozor_aplikacije(root, ime_prozora, gumb_moj_profil):
    """ ova metoda crta header i gumbe za prozor 
    koji se prikazuje na svim prozorima aplikacije nakon 
    sto se ulogira korisnika;
    prozor sadrzi glavnu sliku, header te gumb moj profil i gumb sinkronizacije"""
    clear_frame(root)
    pocetna_slikica()
    nacrtaj_header(root,tekst = ime_prozora,command_za_button=gumb_moj_profil)

def clear_frame(root):
    """ova funkcija cisti prozor od prethodnih funkcija"""
    for widget in root.winfo_children():
        widget.destroy()

def mali_crno_bijeli_logo(frame_za_logo):
    """ova metoda poziva i prikazuje mali crno bijeli logo"""
    manji_image = Image.open("media\PyFlora_crno_bijela.jpg")
    manja_slika = ImageTk.PhotoImage(manji_image.resize((65,40)))
    # drugo - predajemo sliku labelu (mozemo i buttonu i pozadini i...)
    label_sa_slikom = ttk.Label(frame_za_logo, image=manja_slika,relief='flat',style="warning")
    label_sa_slikom.image = manja_slika
    #label_sa_slikom.place(anchor="center",relx=0.5,rely=0.5)
    # trece - postavljamo je na ekranu; radi i place i pack
    label_sa_slikom.place(anchor="center", relx = 0.65,rely=0.5)

def velika_slika_posred_ekrana(root,slika):
    """ova funkcija prikazuje veliku sliku (po izboru) na sredini prozora"""
    root.title('PyFlora Aplikacija')
    img = Image.open(slika)
    #img = img.filter(ImageFilter.BLUR)
    slika = ImageTk.PhotoImage(img)
    
    label_sa_slikom = ttk.Label(root, image=slika, borderwidth=0)
    label_sa_slikom.image = slika
    # trece - postavljamo je na ekranu; radi i place i pack
    #label_sa_slikom.pack(anchor ="center", fill=Y, expand=YES)
    label_sa_slikom.place(anchor="center",relx=0.5,rely=0.5)  #rely=0.55

def pocetna_slikica():
    """ ova metoda prikazuje odabranu sliku kao pozadinu prozora """
    slika = ImageTk.PhotoImage(Image.open("media\cvijet.png"))
    label1 = ttk.Label(image = slika, borderwidth=0)
    label1.image = slika
    label1.place(anchor='w', relx=0.5, rely=0.5)

def gumb_sinkronizacije(root):
    """ ova metoda sada ne radi ništa;
        prije je povezivala gui s bazom;
        radi sinkronizaciju biljaka """
    pocetna_slikica()
    button_s_placeom(root,"sinkronizacija","warning.TButton",None,10,16,830,70)

def header_za_prvi_i_drugi_prozor(root,background,title):
    """ ova funkcija crta prozor 
        prozor samo s headerom i naslovom prozora; 
        NEMA
        gumb 'moj profil' i 'sinkronizacija' """
    clear_frame(root)
    pocetna_slikica()
    #nacrtaj_header_prijava(root)
    root['bg']= background
    root.title(title)
    header_frame=dodaj_frame_place(root,'groove',1,1060,60,None,"light","nw",None,None)
    label(root,'PyFlora Posuda: Prijava ',"warning.TLabel","light-inverse",None,None,"nw",0.1,0.025)

    # prvo - otvorimo sliku
    manji_image = Image.open("media\PyFlora_crno_zuta.jpg")
    manja_slika = ImageTk.PhotoImage(manji_image.resize((75,50)))
    # drugo - predajemo sliku labelu (mozemo i buttonu i pozadini i...)
    label_sa_slikom = ttk.Label(root, image=manja_slika,borderwidth=0)
    label_sa_slikom.image = manja_slika
    # trece - postavljamo je na ekranu; radi i place i pack
    label_sa_slikom.place(anchor="nw", relx = 0.005,rely=0.0085)

def nacrtaj_header(root, tekst, command_za_button):
    """ova metoda crta header za glavni prozor aplikacije
    koji se prikazuje i svakom prozoru nakon sto se korisnik ulogira"""
    pocetna_slikica()
    gumb_sinkronizacije(root)

    header_frame = dodaj_frame_place(root,'groove',1,1060,60,None,"light","nw",None,None)
    label(root,tekst,"warning.TLabel","light-inverse",None,None,"nw",0.1,0.025)

    manji_image = Image.open("media\PyFlora_crno_zuta.jpg")
    manja_slika = ImageTk.PhotoImage(manji_image.resize((75,50)))
    # drugo - predajemo sliku labelu (mozemo i buttonu i pozadini i...)
    label_sa_slikom = ttk.Label(root, image=manja_slika,borderwidth=0)
    label_sa_slikom.image = manja_slika
    # trece - postavljamo je na ekranu; radi i place i pack
    label_sa_slikom.place(anchor="nw", relx = 0.005,rely=0.0085)

    button_s_placeom(header_frame,"moj profil","warning.Outline.TButton",command_za_button,10,16,830,11)

def dodaj_redak(root, redni_broj, stupac, broj_stupaca):
    """ova se funkcija ne koristi"""
    #frame_pape = tk.Frame(self.root, width=250, height=150, bd=1, relief="solid")
    frame_pape  =  ttk.Frame(
        root,  width=300,  height=250, borderwidth=3, 
        relief='raised', style="dark")
    frame_pape.grid(
        row=redni_broj, 
        column=stupac, 
        columnspan=broj_stupaca, 
        padx=31, pady=110
    )
    return frame_pape

def dodaj_frame(parent_frame, relief,red,stupac,style,width,height,borderwidth,padx,pady):
    """ova funkcija crta frame koristeci metodu grid
    te prima red i stupac kod prikaza biljaka i posuda iz baze koristeci
    for petlju"""
    frame_child = ttk.Frame(
        parent_frame, relief=relief,
        width=width, height=height, borderwidth=borderwidth, style=style
        )
    frame_child.grid(row=red, column=stupac,padx=padx,pady=pady)
    return frame_child

def dodaj_frame_place(frame,relief,borderwidth,width,height,cursor,style,anchor,relx,rely):
    """ova funkcija crta frame koristeci metodu place
    te vraca zadani frame"""
    frame_za_gumbe = ttk.Frame(
    frame, relief=relief, borderwidth=borderwidth, 
    width=width,height=height,cursor=cursor,style=style)
    #frame_za_gumbe.grid(column=1, row=1, padx=5, pady=5)
    frame_za_gumbe.place(anchor=anchor, relx=relx, rely=rely)
    return frame_za_gumbe

def dodaj_frame_za_novu_biljku(root,redni_broj,stupac):# broj_stupaca):
    """ ova funkcija radii frame za crtanje gumba
    kojim dodajemo novu biljku u bazu biljaka 
    """
    frame_za_novu_biljku = ttk.Frame(
        root,  width=50,  height=50, 
        borderwidth=2, relief='raised', style="deafult") #bg='#AFE1AF'
    frame_za_novu_biljku.grid(row=redni_broj, column=stupac, 
        #columnspan=broj_stupaca, 
        padx=10, pady=70)
    #mali_crno_bijeli_logo(frame_za_novu_biljku)
    return frame_za_novu_biljku

   
def gumb_za_novu_biljku(root, command_button): # ne radi promjena pozadinske boje gumba! ZASTO???
    """ova funkcija crta gumb za dodavanje nove biljke;
    trenutno je ne koristim jer se veze za redak i stupac iz for petlje
    koja se koristi za crtanje biljaka i posuda iz baze"""
    button_nova_biljka = ttk.Button(root,text="nova biljka", 
        command= command_button, #self.dodajte_novu_biljku_iz_foldera,
        padding=5,width=8,bootstyle="warning-outline-toolbutton") 
    button_nova_biljka.grid(column=0, columnspan=3, row=1, ipadx=16, ipady=13, padx=55, pady=30)

def nacrtaj_naslovnicu_aplikacije(root,gumb):
    """ ova funkcija je naslovnica aplikacije
            s gumbom loga za ulaz u aplikaciju; 
            ovdje samo ulazimo u aplikaciju
    """
    tekst_pozdrava = ttk.Label(root,
            text="Dobrodošli u aplikaciju PyFlora.\nZa ulazak kliknite na cvijetak",
            bootstyle=('dark'),font="quicksand 14",padding=5, anchor="center")
    tekst_pozdrava.place(anchor="s", relx=0.5,rely=0.7,width=800)

    manji_image = Image.open("media\PyFlora_crno_zuta.jpg")
    manja_slika = ImageTk.PhotoImage(manji_image.resize((120,70)))

    # sad je prikazujemo na buttonu
    gumb_sa_slikom = ttk.Button(root, 
    image=manja_slika, 
    bootstyle='warning',
    command=gumb,#prozor_ulaska_login_ili_registracija,
    padding=2)

    gumb_sa_slikom.image = manja_slika
    gumb_sa_slikom.place(anchor="center", relx=0.5,rely=0.35)

def dodajmo_novu_biljku_na_listu(root,redak,stupac,command_za_button):
    """ ova funkcija crta okvir i 
        gumb za dodavanje nove biljke u bazu
        iz foldera koji ce odabrati korisnik"""
    novi_frame = dodaj_frame_za_novu_biljku(root,redak,stupac)
    gumb_za_novu_biljku(novi_frame,command_button=command_za_button)


def label(frame,tekst,font_slova,stil,poravnanje,pozadina,anchor,relx,rely):
    """ ova metoda ispisuje automatski zadan label i radi place"""
    tekst_labela = ttk.Label(
        frame, text=tekst, font=font_slova, 
        bootstyle=stil,justify=poravnanje, 
        background=pozadina)
    tekst_labela.place(anchor=anchor,relx=relx, rely=rely)

def label_s_anchorom(frame,tekst,font_slova,stil,anchor2,width,pozadina,anchor,relx,rely):
    """ ova metoda ispisuje automatski zadan label i radi place"""
    tekst_labela = ttk.Label(
        frame, text=tekst, font=font_slova, 
        bootstyle=stil,anchor=anchor2, width=width,
        background=pozadina)
    tekst_labela.place(anchor=anchor,relx=relx, rely=rely)

def button(frame,style,bootstyle,text,command,padding,width,anchor,relx,rely):
    """ova funkcija crta gumb s metodom place"""
    button = ttk.Button(
        frame, style=style, bootstyle=bootstyle, 
        text =text, command=command, padding=padding, width=width
        ).place(anchor=anchor,relx=relx,rely=rely)

def button_s_gridom(frame,bootstyle,text,command,padding,width,
                    column,columnspan,row,ipadx,ipady,padx,pady,sticky):
    """ova funkcija crta gumb s metodom grid"""
    button_ispis_synca = ttk.Button(frame, text=text, 
        command=command,bootstyle=bootstyle,padding=padding, width=width)
    button_ispis_synca.grid(
        column=column, columnspan=columnspan, row=row, 
        ipadx=ipadx, ipady=ipady, padx=padx, pady=pady, sticky=sticky)
    
def button_s_placeom(root,text,style,command,padding,width,x,y):
    """ova funkcija crta gumb s metodom place, ali bez opcije 'anchor'"""
    gumb_moj_profil = ttk.Button(root,
                        text=text, 
                        #bootstyle= "warning-outline-toolbutton",
                        style=style,
                        command= command, padding=padding, width=width)
        #                       nacrtaj_treci_prozor_moj_profil
    gumb_moj_profil.place(x=x,y=y)#relwidth=0.3)


def ubaci_tekst_u_label(frame,ime_slike,font,bootsytle,relx,rely):
    """ova funkcija upisuje tekst u odredeni label,
    a taj tekst prima u pozivu funkcije"""
    oznaka = ttk.Label(
        frame, 
        text=f'{ime_slike}',
        justify='center',bootstyle=bootsytle, font=font) #font="quicksand, 10"  # svijetlo zuta - FFE890
    oznaka.place(anchor ='nw', relx=relx,rely=rely)#relx=0.05,rely=0.1)


def buttoni_za_azuriranje_i_brisanje_podataka(root,azuriraj_izbrisi_koga,command_azuriraj,command_izbrisi,command_BACK):
    """ova funkcija nudi mogucnost azuriranja i brisanja korisnika"""
    frame = dodaj_frame_place(root,"raised",1,50,500,"heart","light","ne",0.98,0.35)

    button_s_gridom(frame,"warning.Outline.TButton",f"ažuriraj {azuriraj_izbrisi_koga}",command_azuriraj,10,11,
                    column=3,columnspan=3,row=2,ipadx=10,ipady=3,padx=15,pady=10,sticky="ew")
    button_s_gridom(frame,"danger-outline",f"izbriši {azuriraj_izbrisi_koga}",
                    command_izbrisi,10,11, column=3,columnspan=3,row=3,ipadx=10,ipady=3,padx=15,pady=10,sticky="ew")
    button_s_gridom(frame,"warning-outline","BACK",command_BACK,10,11,
                    column=3,columnspan=3,row=5,ipadx=10,ipady=3,padx=15,pady=10,sticky="ew")
    
