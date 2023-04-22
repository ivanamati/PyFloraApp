import os
import ttkbootstrap as ttk
# from ttkbootstrap.constants import *
from PIL import ImageTk, Image
from datetime import date
from PyFlora_vrijeme_api import Prognoza

###  OVAJ MODUL SADRŽI FUNKCIJE ZA CRTANJE WIDGETA I SASTAVNIH DIJELOVA ZA modul GUI APP


def prikaz_datuma_i_temperature(root, anchor, relx, rely):
    danas = date.today()
    # dd/mm/YY
    datum = danas.strftime("%d.%m.%Y.")

    temperatura = Prognoza(
        "temperatura", "celzijevci", latitude="45.82", longitude="15.959999"
    )
    prikaz_temp = temperatura.vrijednosti_s_weba(("temperature_2m"))

    print("Dohvaćena je temperatura s WEBA pomoću skripte 'PyFlora_vrijeme_api' za grad Zagreb i prikazana na pozdravnom prozoru aplikacije;")
    print(f"Možda je potrebno dulje vrijeme dohvata, no temperatura je trenutno {prikaz_temp}°C")

    label_s_anchorom(
        frame=root,
        tekst=f"Danas je {datum}, a temperatura trenutno iznosi {prikaz_temp}°C",
        font_slova=("quicksand", 10),
        stil="warning",
        anchor2="center",
        width=None,
        pozadina=None,
        anchor=anchor,
        relx=relx,
        rely=rely,
    )


def polje_za_unos_username(root, bootstyle, font, anchor, relx, rely):
    """ova metoda crta unos usernamea te
    nakon unosa username vraća username"""
    username = ttk.Entry(root, bootstyle=bootstyle, font=font)
    username.place(anchor=anchor, relx=relx, rely=rely)
    return username


def polje_za_unos_s_prikazom_postojeceg_teksta(
    root, bootstyle, font, show, anchor, relx, rely, width, detalj_za_prikaz
):
    """ova metoda crta prozor za izmjenu postojecih podataka
    te ih istovremeno prikazuje"""
    tekst = ttk.Entry(root, bootstyle=bootstyle, font=font, show=show, width=width)
    tekst.insert(0, detalj_za_prikaz)
    tekst.place(anchor=anchor, relx=relx, rely=rely)
    return tekst


def polje_za_unos(root, bootstyle, font, show, anchor, relx, rely, width):
    """ova metoda crta polja za unos teksta te
    nakon unosa vraca tekst"""
    tekst = ttk.Entry(root, bootstyle=bootstyle, font=font, show=show, width=width)
    tekst.place(anchor=anchor, relx=relx, rely=rely)
    return tekst


def glavni_prozor_aplikacije(root, ime_prozora, gumb_moj_profil):
    """ova metoda crta header i gumbe za prozor
    koji se prikazuje na svim prozorima aplikacije nakon
    sto se ulogira korisnika;
    prozor sadrzi glavnu sliku, header te gumb moj profil i gumb sinkronizacije"""
    clear_frame(root)
    pocetna_slikica(ime_slike="cvijet.png", folder_name="media")
    nacrtaj_header(root=root, tekst=ime_prozora, command_za_button=gumb_moj_profil)


def clear_frame(root):
    """ova funkcija cisti prozor od prethodnih funkcija"""
    for widget in root.winfo_children():
        widget.destroy()


# def mali_crno_bijeli_logo(frame_za_logo):
#     """ova metoda poziva i prikazuje mali crno bijeli logo"""
#     # prvo - otvorimo sliku
#     manji_image = Image.open("media\PyFlora_crno_bijela.jpg")
#     manja_slika = ImageTk.PhotoImage(manji_image.resize((65, 40)))

#     # drugo - predajemo sliku labelu (mozemo i buttonu i pozadini i...)
#     label_sa_slikom = ttk.Label(
#         frame_za_logo, image=manja_slika, relief="flat", style="warning"
#     )
#     label_sa_slikom.image = manja_slika

#     # trece - postavljamo je na ekranu; radi i place i pack
#     label_sa_slikom.place(anchor="center", relx=0.65, rely=0.5)


def logo_kao_label_u_headerima(root, slika_za_prikaz, anchor, relx, rely):
    manji_image = dohvati_sliku(
        width=75, height=50, ime_slike=slika_za_prikaz, folder_name="media"
    )

    manja_slika = ImageTk.PhotoImage(manji_image.resize((75, 50)))
    #predajemo sliku labelu (mozemo i buttonu i pozadini i...)
    label_sa_slikom = ttk.Label(root, image=manja_slika, borderwidth=0)
    label_sa_slikom.image = manja_slika
    label_sa_slikom.place(anchor=anchor, relx=relx, rely=rely)


def velika_slika_posred_ekrana(root, ime_slike, folder_name):
    """ova funkcija prikazuje veliku sliku (po izboru) na sredini prozora"""
    root.title("PyFlora Aplikacija")

    img = dohvati_sliku_u_originalu(ime_slike=ime_slike, folder_name=folder_name)
    # img = img.filter(ImageFilter.BLUR)
    slika = ImageTk.PhotoImage(img)

    label_sa_slikom = ttk.Label(root, image=slika, borderwidth=0)
    label_sa_slikom.image = slika

    label_sa_slikom.place(anchor="center", relx=0.5, rely=0.5)


def pocetna_slikica(ime_slike, folder_name):
    """ova metoda prikazuje odabranu sliku kao pozadinu prozora"""
    img = dohvati_sliku_u_originalu(ime_slike=ime_slike, folder_name=folder_name)
    slika = ImageTk.PhotoImage(img)
    label1 = ttk.Label(image=slika, borderwidth=0)
    label1.image = slika
    label1.place(anchor="w", relx=0.5, rely=0.5)


def gumb_sinkronizacije(root, command, padding, width, x, y):
    """ova metoda sada ne radi ništa;
    prije je povezivala gui s bazom;
    radi sinkronizaciju biljaka"""
    button_s_placeom(
        root=root,
        text="SYNC",
        style="warning.outline",
        command=command,
        padding=padding,
        width=width,
        x=x,
        y=y,
    )  # "warning.TButton"


def padajuci_izbornik_za_odabir_biljke(root, repozitorij, relx, rely):
    """ova funkcija crta padajuci izbornik 
    koji sadrzi sve biljke iz baze sa sadnju u posudu"""
    biljka = ttk.StringVar()
    ttk.Combobox(
        root,
        values=repozitorij.popis_imena_svih_biljaka_iz_baze(),
        width=42,
        style="warning",
        textvariable=biljka,
    ).place(
        anchor="center", relx=relx, rely=rely
    )  # relx=0.45,rely=0.35
    return biljka


def padajuci_izbornik_za_podatke_o_biljci(root, relx, rely, vrijednosti_za_prikaz):
    """ova funkcija crta padajuci izbornik 
    koji sadrzi detalje o biljci za spremanje u bazu;
    detalji se predaju kod poziva funkcije u prozoru
    u kojem se nudi dodavanje biljke u bazu"""
    tekst = ttk.StringVar()
    ttk.Combobox(
        root,
        values=vrijednosti_za_prikaz,
        width=42,
        style="warning",
        textvariable=tekst,
    ).place(
        anchor="center", relx=relx, rely=rely
    )  # relx=0.45,rely=0.35
    return tekst


def header_za_prvi_i_drugi_prozor(root, background, title):
    """ova funkcija crta prozor
    prozor samo s headerom i naslovom prozora;
    NEMA
    gumb 'moj profil' i 'sinkronizacija'"""
    clear_frame(root)
    pocetna_slikica(ime_slike="cvijet.png", folder_name="media")

    root["bg"] = background
    root.title(title)

    dodaj_frame_place(
        frame=root,
        relief="groove",
        borderwidth=1,
        width=1060,
        height=60,
        style="light",
        anchor="nw",
        relx=None,
        rely=0.9,
    )  # None

    label(
        frame=root,
        tekst="PyFlora Posuda: Prijava ",
        font_slova="warning.TLabel",
        stil="light-inverse",
        poravnanje=None,
        pozadina=None,
        anchor="nw",
        relx=0.12,
        rely=0.93,
    )  # 0.027

    # ovaj bi jos trebalo promijeniti (!!!!!)
    logo_kao_label_u_headerima(
        root=root,
        slika_za_prikaz="PyFlora_crno_zuta.jpg",
        anchor="nw",
        relx=0.005,
        rely=0.91,
    )  # 0.0085


def nacrtaj_header(root, tekst, command_za_button):
    """ova metoda crta header za glavni prozor aplikacije
    koji se prikazuje i svakom prozoru nakon sto se korisnik ulogira"""
    pocetna_slikica(ime_slike="cvijet.png", folder_name="media")

    dodaj_frame_place(
        frame=root,
        relief="groove",
        borderwidth=1,
        width=1365,
        height=60,
        style="light",
        anchor="nw",
        relx=None,
        rely=0.9,
    )

    label(
        frame=root,
        tekst=tekst,
        font_slova="warning.TLabel",
        stil="light-inverse",
        poravnanje=None,
        pozadina=None,
        anchor="nw",
        relx=0.12,
        rely=0.93,
    )  # 0.1,0.025

    logo_kao_label_u_headerima(
        root=root,
        slika_za_prikaz="PyFlora_crno_zuta.jpg",
        anchor="nw",
        relx=0.005,
        rely=0.91,
    )

    button(
        frame=root,
        style="warning.Outline.TButton",
        bootstyle=None,
        text="MENU",
        command=command_za_button,
        padding=10,
        width=16,
        anchor="nw",
        relx=0.79,
        rely=0.92,
    )

    # button_s_placeom(header_frame,"moj profil","warning.Outline.TButton",command_za_button,10,16,630,11)


def dodaj_frame(
    glavni_frame, relief, red, stupac, style, width, height, borderwidth, padx, pady
):
    """ova funkcija crta frame koristeci metodu grid
    te prima red i stupac kod prikaza biljaka
    i posuda iz baze koristeci for petlju"""
    frame = ttk.Frame(
        glavni_frame,
        relief=relief,
        width=width,
        height=height,
        borderwidth=borderwidth,
        style=style,
    )
    frame.grid(row=red, column=stupac, padx=padx, pady=pady)
    return frame


def dodaj_frame_grid(
    glavni_frame,
    relief,
    red,
    rowspan,
    stupac,
    columnspan,
    style,
    width,
    height,
    borderwidth,
    padx,
    pady,
    ipadx,
    ipady,
):
    """ova funkcija crta frame koristeci metodu grid
    te prima red i stupac, ali i column- i rowspan te ipadx i ipady
    kod prikaza biljaka i posuda iz baze koristeci for petlju"""
    frame = ttk.Frame(
        glavni_frame,
        relief=relief,
        width=width,
        height=height,
        borderwidth=borderwidth,
        style=style,
    )
    frame.grid(
        row=red,
        column=stupac,
        columnspan=columnspan,
        rowspan=rowspan,
        ipadx=ipadx,
        ipady=ipady,
        padx=padx,
        pady=pady,
    )
    return frame


def dodaj_frame_place(
    frame, relief, borderwidth, width, height, style, anchor, relx, rely
):
    """ova funkcija crta frame koristeci metodu place
    te vraca zadani frame"""
    frame = ttk.Frame(
        frame,
        relief=relief,
        borderwidth=borderwidth,
        width=width,
        height=height,
        cursor=None,
        style=style,
    )
    # frame_za_gumbe.grid(column=1, row=1, padx=5, pady=5)
    frame.place(anchor=anchor, relx=relx, rely=rely)
    return frame


def dodaj_frame_za_novu_biljku(root, redni_broj, stupac):  # broj_stupaca):
    """ova funkcija radi frame za crtanje gumba
    kojim dodajemo novu biljku u bazu biljaka
    """
    frame_za_novu_biljku = ttk.Frame(
        root, width=105, height=145, borderwidth=2, relief="raised", style="deafult"
    )  # bg='#AFE1AF'
    frame_za_novu_biljku.grid(row=redni_broj, column=stupac, padx=23, pady=20)
    # mali_crno_bijeli_logo(frame_za_novu_biljku)
    return frame_za_novu_biljku


def gumb_za_novu_biljku(root, command_button):
    # ne radi promjena pozadinske boje gumba! ZASTO???
    """ova funkcija crta gumb za dodavanje nove biljke;
    trenutno je ne koristim jer se veze za redak i stupac iz for petlje
    koja se koristi za crtanje biljaka i posuda iz baze"""
    button_nova_biljka = ttk.Button(
        root,
        text="nova biljka",
        command=command_button,  # self.dodajte_novu_biljku_iz_foldera,
        padding=10,
        width=8,
        bootstyle="warning-outline-toolbutton",
    )
    button_nova_biljka.grid(
        column=0, columnspan=3, row=1, ipadx=16, ipady=13, padx=55, pady=30
    )


def dohvati_sliku(width, height, ime_slike, folder_name="SLIKE_BILJAKA"):
    """ova funkcija dohvaca sliku prema njezinome imenu
    iz zadanoga foldera;
    najprije provjerava postoji li slika, zatim je spaja s folderom,
    a na kraju radi njezin resize te vraća samo img koji kasnije
    moramo prikazati tkinter metodom 'ImageTk.PhotoImage'"""
    if not ime_slike:
        return None

    putanja = spoji_sliku_s_folderom(ime_slike, folder_name=folder_name)
    if not os.path.exists(putanja):
        return None

    try:
        img = Image.open(putanja)
        img = img.resize((width, height))
        return img
    except FileNotFoundError:
        return None


def dohvati_sliku_u_originalu(ime_slike, folder_name):
    """ova funkcija dohvaca sliku prema njezinome imenu
    iz zadanoga foldera; najprije provjerava postoji li slika,
    zatim je spaja s folderom, vraća img u originalnoj veličini,
    koji kasnije moramo prikazati tkinter metodom
    'ImageTk.PhotoImage'"""
    if not ime_slike:
        return None

    putanja = spoji_sliku_s_folderom(ime_slike, folder_name=folder_name)
    if not os.path.exists(putanja):
        return None

    try:
        img = Image.open(putanja)
        return img
    except FileNotFoundError:
        return None


def spoji_sliku_s_folderom(photo_filename, folder_name):
    """ova funkcija provjerava postoji li datoteka s imenom photo_filename;
    ako postoji, vraća punu putanju do te datoteke;
    ako ne postoji, stvara punu putanju do mape nazvane folder_name
    i vraća punu putanju do datoteke u toj mapi."""
    if os.path.exists(photo_filename):
        return photo_filename
    #  puna putanja do foldera sa slikama koji se nalazi odmah uz ovaj file
    folder_sa_slikama = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            # folder u kojem se nalazi ovaj file
            # folder u koji ćemo spremati slike
            folder_name,
        )
    )
    slika_puna_putanja = os.path.join(folder_sa_slikama, photo_filename)
    return slika_puna_putanja


def ubaci_sliku_kao_button_u_label_posude(
    neki_frame, putanja_slike, id_slike, gui_objekt
):
    """
    ova metoda prikazuje sliku u odabranom labelu
    takoder povezuje prikazanu sliku s njezinim id-om slika je GUMB;
    klikom na njega otvara se prikazan/odabran cvijet
    """
    img = dohvati_sliku(
        width=125, height=85, ime_slike=putanja_slike, folder_name="SLIKE_POSUDA"
    )
    if img is not None:
        label_slika = ImageTk.PhotoImage(img)
        # ovim gumbom dobivamo prikaz biljke te DOHVACAMO ID biljke iz baze da prikaze podatke bas za tu biljku
        slika_u_lijevom_frameu = ttk.Button(
            neki_frame,
            image=label_slika,
            bootstyle="warning.outline",
            padding=1,
            command=lambda: gui_objekt.prozor_s_detaljima_o_posudi(id_slike=id_slike),
            cursor="hand2",
        )
        slika_u_lijevom_frameu.image = label_slika
        slika_u_lijevom_frameu.place(anchor="center", relx=0.5, rely=0.4)

    else:
        ubaci_tekst_u_label(
            neki_frame,
            f"Slika\n {putanja_slike}\n nije pronađena",
            font="quicksand, 10",
            bootsytle="warning",
            relx=0.5,
            rely=0.1,
        )


def nacrtaj_naslovnicu_aplikacije(root, gumb):
    """ova funkcija je naslovnica aplikacije
    s gumbom loga za ulaz u aplikaciju;
    ovdje samo ulazimo u aplikaciju
    """

    tekst_pozdrava = ttk.Label(
        root,
        text="PyFlora App\nZa ulazak kliknite na gumb PyFlora",
        bootstyle=("dark"),
        font="quicksand 12",
        padding=5,
        anchor="center",
        justify="center",
        borderwidth=2,
        relief="groove",
        foreground="gray",
    )
    tekst_pozdrava.place(anchor="s", relx=0.5, rely=0.7, height=60, width=800)

    manji_image = dohvati_sliku(
        width=120, height=70, ime_slike="PyFlora_crno_zuta.jpg", folder_name="media"
    )
    manja_slika = ImageTk.PhotoImage(manji_image.resize((120, 70)))

    # sad je prikazujemo na buttonu
    gumb_sa_slikom = ttk.Button(
        root,
        image=manja_slika,
        bootstyle="warning",
        command=gumb,
        padding=2,
        cursor="hand2",
    )
    gumb_sa_slikom.image = manja_slika
    gumb_sa_slikom.place(anchor="center", relx=0.5, rely=0.5)


def label(frame, tekst, font_slova, stil, poravnanje, pozadina, anchor, relx, rely):
    """ova metoda ispisuje label s place metodom te sadrzi opciju 'poravnanja'"""
    tekst_labela = ttk.Label(
        frame,
        text=tekst,
        font=font_slova,
        bootstyle=stil,
        justify=poravnanje,
        background=pozadina,
    )
    tekst_labela.place(anchor=anchor, relx=relx, rely=rely)


def label_s_anchorom(
    frame, tekst, font_slova, stil, anchor2, width, pozadina, anchor, relx, rely
):
    """ova metoda piše label, koristi place, ali ima anchor samog teksta u labelu"""
    tekst_labela = ttk.Label(
        frame,
        text=tekst,
        font=font_slova,
        bootstyle=stil,
        anchor=anchor2,
        width=width,
        background=pozadina,
    )
    tekst_labela.place(anchor=anchor, relx=relx, rely=rely)


def label_kao_slika(frame, image, bootsytle, borderwidth, relief, anchor, relx, rely):
    """ova funkcija crta label te u njemu"""
    slika_biljke = ttk.Label(
        frame,
        image=image,  # label_slika
        bootstyle=bootsytle,
        borderwidth=borderwidth,
        relief=relief,
    )
    slika_biljke.image = image  # label_slika
    slika_biljke.place(anchor=anchor, relx=relx, rely=rely)


def button(frame, style, bootstyle, text, command, padding, width, anchor, relx, rely):
    """ova funkcija crta gumb s metodom place"""
    ttk.Button(
        frame,
        style=style,
        bootstyle=bootstyle,
        text=text,
        command=command,
        padding=padding,
        width=width,
        cursor="hand2",
    ).place(anchor=anchor, relx=relx, rely=rely)


def button_s_gridom(
    frame,
    bootstyle,
    text,
    command,
    padding,
    width,
    column,
    columnspan,
    row,
    ipadx,
    ipady,
    padx,
    pady,
    sticky,
):
    """ova funkcija crta gumb s metodom grid"""
    button_ispis_synca = ttk.Button(
        frame,
        text=text,
        command=command,
        bootstyle=bootstyle,
        padding=padding,
        width=width,
        cursor="hand2",
    )
    button_ispis_synca.grid(
        column=column,
        columnspan=columnspan,
        row=row,
        ipadx=ipadx,
        ipady=ipady,
        padx=padx,
        pady=pady,
        sticky=sticky,
    )


def button_s_placeom(root, text, style, command, padding, width, x, y):
    """ova funkcija crta gumb s metodom place, ali bez opcije 'anchor'"""
    gumb_moj_profil = ttk.Button(
        root,
        text=text,
        style=style,
        command=command,
        padding=padding,
        width=width,
        cursor="hand2",
    )
    gumb_moj_profil.place(x=x, y=y)


def ubaci_tekst_u_label(frame, ime_slike, font, bootsytle, relx, rely):
    """ova funkcija upisuje tekst u odredeni label,
    a taj tekst prima u pozivu funkcije"""
    oznaka = ttk.Label(
        frame, text=f"{ime_slike}", justify="center", bootstyle=bootsytle, font=font
    )
    oznaka.place(anchor="nw", relx=relx, rely=rely)


def buttoni_za_azuriranje_i_brisanje_podataka_biljaka(
    root,
    azuriraj_izbrisi_koga,
    command_azuriraj,
    command_izbrisi,
    command_senzori,
    # command_sinkronizacija,
    command_BACK,
    anchor,
    relx,
    rely,
):
    """ova funkcija nudi mogucnost azuriranja i brisanja korisnika"""
    frame = dodaj_frame_place(
        frame=root,
        relief="raised",
        borderwidth=1,
        width=100,
        height=500,
        style="light",
        anchor=anchor,
        relx=relx,
        rely=rely,
    )  # "ne",0.98,0.35

    button_s_gridom(
        frame=frame,
        bootstyle="warning.Outline.TButton",
        text=f"ažuriraj {azuriraj_izbrisi_koga}",
        command=command_azuriraj,
        padding=10,
        width=11,
        column=1,
        columnspan=1,
        row=1,
        ipadx=10,
        ipady=1,
        padx=10,
        pady=10,
        sticky="ew",
    )

    button_s_gridom(
        frame=frame,
        bootstyle="danger-outline",
        text=f"izbriši {azuriraj_izbrisi_koga}",
        command=command_izbrisi,
        padding=10,
        width=11,
        column=2,
        columnspan=1,
        row=1,
        ipadx=10,
        ipady=1,
        padx=10,
        pady=10,
        sticky="ew",
    )

    button_s_gridom(
        frame=frame,
        bootstyle="warning-outline",
        text="SENZOR DATA",
        command=command_senzori,
        padding=10,
        width=11,
        column=3,
        columnspan=1,
        row=1,
        ipadx=10,
        ipady=1,
        padx=10,
        pady=10,
        sticky="ew",
    )

    # HTJELA sam staviti ovdje gumb SYNC medutim kada ga pokrenem prozor s prikazom svih biljaka sve se zamrzen
    # button_s_gridom(
    #     frame=frame,
    #     bootstyle="warning-outline",
    #     text="SYNC",
    #     command=command_sinkronizacija,
    #     padding=10, width=11,
    #     column=4, columnspan=1,
    #     row=1, ipadx=10, ipady=1,
    #     padx=10, pady=10, sticky="ew")

    button_s_gridom(
        frame=frame,
        bootstyle="warning-outline",
        text="BACK",
        command=command_BACK,
        padding=10,
        width=11,
        column=5,
        columnspan=1,
        row=1,
        ipadx=10,
        ipady=1,
        padx=10,
        pady=10,
        sticky="ew",
    )


def buttoni_za_azuriranje_i_brisanje_podataka_plus_senzori(
    root,
    azuriraj_izbrisi_koga,
    command_azuriraj,
    command_izbrisi,
    command_senzori,
    command_BACK,
    anchor,
    relx,
    rely,
):
    """ova funkcija nudi mogucnost azuriranja i brisanja korisnika"""
    frame = dodaj_frame_place(
        frame=root,
        relief="raised",
        borderwidth=1,
        width=100,
        height=500,
        style="light",
        anchor=anchor,
        relx=relx,
        rely=rely,
    )  # "ne",0.98,0.35

    button_s_gridom(
        frame=frame,
        bootstyle="warning.Outline.TButton",
        text=f"ažuriraj {azuriraj_izbrisi_koga}",
        command=command_azuriraj,
        padding=10,
        width=11,
        column=1,
        columnspan=1,
        row=1,
        ipadx=10,
        ipady=1,
        padx=10,
        pady=10,
        sticky="ew",
    )

    button_s_gridom(
        frame=frame,
        bootstyle="danger-outline",
        text=f"izbriši {azuriraj_izbrisi_koga}",
        command=command_izbrisi,
        padding=10,
        width=11,
        column=2,
        columnspan=1,
        row=1,
        ipadx=10,
        ipady=1,
        padx=10,
        pady=10,
        sticky="ew",
    )

    button_s_gridom(
        frame=frame,
        bootstyle="warning-outline",
        text="SENZOR DATA",
        command=command_senzori,
        padding=10,
        width=11,
        column=3,
        columnspan=1,
        row=1,
        ipadx=10,
        ipady=1,
        padx=10,
        pady=10,
        sticky="ew",
    )

    button_s_gridom(
        frame=frame,
        bootstyle="warning-outline",
        text="BACK",
        command=command_BACK,
        padding=10,
        width=11,
        column=4,
        columnspan=1,
        row=1,
        ipadx=10,
        ipady=1,
        padx=10,
        pady=10,
        sticky="ew",
    )


def buttoni_za_azuriranje_i_brisanje_podataka(
    root,
    azuriraj_izbrisi_koga,
    command_azuriraj,
    command_izbrisi,
    command_BACK,
    anchor,
    relx,
    rely,
):
    """ova funkcija nudi mogucnost azuriranja i brisanja korisnika"""
    frame = dodaj_frame_place(
        frame=root,
        relief="raised",
        borderwidth=1,
        width=100,
        height=500,
        style="light",
        anchor=anchor,
        relx=relx,
        rely=rely,
    )  # "ne",0.98,0.35

    button_s_gridom(
        frame=frame,
        bootstyle="warning.Outline.TButton",
        text=f"ažuriraj {azuriraj_izbrisi_koga}",
        command=command_azuriraj,
        padding=10,
        width=11,
        column=1,
        columnspan=1,
        row=1,
        ipadx=10,
        ipady=1,
        padx=10,
        pady=10,
        sticky="ew",
    )

    button_s_gridom(
        frame=frame,
        bootstyle="danger-outline",
        text=f"izbriši {azuriraj_izbrisi_koga}",
        command=command_izbrisi,
        padding=10,
        width=11,
        column=2,
        columnspan=1,
        row=1,
        ipadx=10,
        ipady=1,
        padx=10,
        pady=10,
        sticky="ew",
    )

    button_s_gridom(
        frame=frame,
        bootstyle="warning-outline",
        text="BACK",
        command=command_BACK,
        padding=10,
        width=11,
        column=4,
        columnspan=1,
        row=1,
        ipadx=10,
        ipady=1,
        padx=10,
        pady=10,
        sticky="ew",
    )


def labeli_i_prozori_za_spremanje_podataka_biljke(root, gui_objekt):
    """ova metoda crta labele s nazivima za spremanje nove biljke
    te prozore za unos podataka o biljci koju spremamo;
    funkcija takoder vraca unesene podatke
    koji se potom predaju funkciji za spremanje podataka"""
    # dodavanje imena biljke
    label_s_anchorom(
        root,
        "ime biljke",
        "quicksand, 14",
        "warning",
        "w",
        12,
        "#f3f6f4",
        "center",
        0.15,
        0.2,
    )
    # self.ime_nove_biljke = polje_za_unos(self.root,"warning",None,None,"center",0.35,0.2,30)
    gui_objekt.ime_nove_biljke = polje_za_unos(
        root, "warning", ("quicksand", 9), None, "center", 0.24, 0.25, 38
    )

    # dodavanje podataka o zalijevanju
    label_s_anchorom(
        root,
        "zalijevanje biljke",
        "quicksand, 14",
        "warning",
        "w",
        13,
        "#f3f6f4",
        "center",
        0.15,
        0.3,
    )
    gui_objekt.zalijevanje = padajuci_izbornik_za_podatke_o_biljci(
        root=root,
        relx=0.238,
        rely=0.35,
        vrijednosti_za_prikaz=["dnevno", "tjedno", "mjesečno"],
    )
    # padajuci_izbornik_za_zalijevanje(root,relx=0.238,rely=0.35)
    # polje_za_unos(root,"warning",('quicksand', 9),None,"center",0.225,0.35,35)

    # dodavanje podataka o mjestu biljke: treba li biti na tamnom, svijetlom, hladnom, toplom
    label_s_anchorom(
        root,
        "mjesto biljke",
        "quicksand, 14",
        "warning",
        "w",
        12,
        "#f3f6f4",
        "center",
        0.15,
        0.4,
    )
    gui_objekt.mjesto = padajuci_izbornik_za_podatke_o_biljci(
        root=root,
        relx=0.238,
        rely=0.45,
        vrijednosti_za_prikaz=[
            "toplo i tamno",
            "toplo i svijetlo",
            "hladno i tamno",
            "hladno i svijetlo",
        ],
    )
    # padajuci_izbornik_za_mjesto_biljke(root=root,relx=0.238,rely=0.45)
    # polje_za_unos(root,"warning",('quicksand', 9),None,"center",0.225,0.45,35)

    # dodavanje podataka o supstratu: da/ne
    label_s_anchorom(
        root,
        "supstrat",
        "quicksand, 14",
        "warning",
        "w",
        12,
        "#f3f6f4",
        "center",
        0.15,
        0.5,
    )
    gui_objekt.supstrat = padajuci_izbornik_za_podatke_o_biljci(
        root=root,
        relx=0.238,
        rely=0.55,
        vrijednosti_za_prikaz=["potreban", "nije potreban"],
    )
    # padajuci_izbornik_za_supstrat(root=root,relx=0.238,rely=0.55)
    # polje_za_unos(root,"warning",('quicksand', 9),None,"center",0.225,0.55,35)

    return (
        gui_objekt.ime_nove_biljke,
        gui_objekt.zalijevanje,
        gui_objekt.mjesto,
        gui_objekt.supstrat,
    )


def labeli_i_prozori_za_azuriranje_podataka_biljke(
    root, gui_objekt, ime, voda, pozicija, supstrat
):
    """ova metoda crta labele s nazivima sto se azurira
    te prozore za unos izmijenjenih podataka u kojem se
    prikazuju podaci iz baze za tu biljku koji se mogu promijeniti;
    takoder ova funkcija vraca te novo unesene podatke
    koji se potom predaju funkciji za azuriranje podataka
    pritiskom na gumb 'spremi azuriranje'"""

    label_s_anchorom(
        root,
        "ime biljke",
        "quicksand, 14",
        "warning",
        "w",
        12,
        "#f3f6f4",
        "center",
        0.15,
        0.2,
    )
    gui_objekt.novo_ime_biljke = polje_za_unos_s_prikazom_postojeceg_teksta(
        root, "warning", ("quicksand", 9), None, "center", 0.225, 0.25, 35, ime
    )

    # dodavanje podataka o zalijevanju
    label_s_anchorom(
        root,
        "zalijevanje biljke",
        "quicksand, 14",
        "warning",
        "w",
        13,
        "#f3f6f4",
        "center",
        0.15,
        0.3,
    )
    gui_objekt.novo_zalijevanje = polje_za_unos_s_prikazom_postojeceg_teksta(
        root, "warning", ("quicksand", 9), None, "center", 0.225, 0.35, 35, voda
    )

    # dodavanje podataka o mjestu biljke: treba li biti na tamnom, svijetlom, hladnom, toplom
    label_s_anchorom(
        root,
        "mjesto biljke",
        "quicksand, 14",
        "warning",
        "w",
        12,
        "#f3f6f4",
        "center",
        0.15,
        0.4,
    )
    gui_objekt.novo_mjesto = polje_za_unos_s_prikazom_postojeceg_teksta(
        root, "warning", ("quicksand", 9), None, "center", 0.225, 0.45, 35, pozicija
    )

    # dodavanje podataka o supstratu: da/ne
    label_s_anchorom(
        root,
        "supstrat",
        "quicksand, 14",
        "warning",
        "w",
        12,
        "#f3f6f4",
        "center",
        0.15,
        0.5,
    )
    gui_objekt.novi_supstrat = polje_za_unos_s_prikazom_postojeceg_teksta(
        root, "warning", ("quicksand", 9), None, "center", 0.225, 0.55, 35, supstrat
    )

    return (
        gui_objekt.novo_ime_biljke,
        gui_objekt.novo_zalijevanje,
        gui_objekt.novo_mjesto,
        gui_objekt.novi_supstrat,
    )
