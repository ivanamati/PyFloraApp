import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import ImageTk, Image, ImageFilter
from tkinter.messagebox import showerror, showinfo
from tkinter import filedialog
import pandas as pd
from gui_repozitorij_prozora import *
from PYFlora_baza_repozitorij import Biljke, Korisnik, spoji_se_na_bazu, PyPosude
from gui_prikaz_grafova import *
from gui_prikaz_sa_senzora import *

### OVAJ SE MODUL SE KORISTI ZA RAD S BAZOM U GUI-u


# FUNKCIJE ZA RAD S BILJKAMA


def dohvati_sve_biljke_iz_baze_i_nacrtaj_u_gui(root, repozitorij, gui_objekt):
    """ova metoda dohvaća sve biljke s njihovim podacima iz baze
    te crta jednu po jednu u zaseban frame preko petlje u gui;
    dodan joj je argument SELF, kako bi radila LAMBDA iz funkcije
    'ubaci_sliku_u_label' preko koja dohvaćamo ID slike biljke na koju smo kliknuli;
    taj self je objekt tipa PyFlora za prikaz na GUI-u
    """
    biljke = repozitorij.dohvati_sve_biljke_iz_baze()
    stupac = 0
    redak = 0

    for biljka in biljke:
        glavni_frame = dodaj_frame(
            root, "raised", redak, stupac, "white", 110, 145, 1, 23, 20
        )
        lijevi_frame = dodaj_frame(
            glavni_frame,
            "flat",
            redak,
            0,
            "white",
            width=105,
            height=145,
            borderwidth=0,
            padx=None,
            pady=None,
        )  # svijetlo zuta - FFE890
        desni_frame = dodaj_frame(
            glavni_frame,
            "flat",
            redak,
            1,
            "white",
            width=105,
            height=145,
            borderwidth=3,
            padx=None,
            pady=None,
        )  # svijetlo zuta - FFE890

        ubaci_sliku_kao_button_u_label_biljke(
            glavni_frame,
            putanja_slike=biljka.slika_biljke,
            id_slike=biljka.id,
            gui_objekt=gui_objekt,
            repozitorij=gui_objekt.repozitorij,
        )
        # ubaci_tekst_u_label(
        #     lijevi_frame,
        #     biljka.ime_biljke,
        #     font="quicksand, 10",
        #     bootsytle="warning",
        #     relx=0.15,
        #     rely=0.55,
        # )

        zalijevanje = biljka.zalijevanje
        mjesto = biljka.mjesto
        supstrat = biljka.supstrat

        label(
            glavni_frame,
            f"'{biljka.ime_biljke}'\nZalijevanje je potrebno jednom {zalijevanje},\npoželjno mjesto je {mjesto}.\nSupstrat:{supstrat}",
            "quicksand, 8",
            "dark",
            "center",
            None,
            "center",
            0.5,
            0.75,
        )

        stupac += 1
        if stupac >= 3:
            redak += 1
            stupac = 0


def ubaci_sliku_kao_button_u_label_biljke(
    neki_frame, putanja_slike, id_slike, gui_objekt, repozitorij
):
    """
    ova metoda prikazuje sliku u odabranom labelu
    takoder povezuje prikazanu sliku s njezinim id-om slika je GUMB;
    klikom na njega otvara se prikazan/odabran cvijet
    """
    img = dohvati_sliku(width=105, height=65, ime_slike=putanja_slike)
    if img is not None:
        label_slika = ImageTk.PhotoImage(img)
        # ovim gumbom dobivamo prikaz biljke te DOHVACAMO ID biljke iz baze da prikaze podatke bas za tu biljku
        slika_u_lijevom_frameu = ttk.Button(
            neki_frame,
            image=label_slika,
            bootstyle="warning.outline",
            padding=1,
            command=lambda: gui_objekt.prozor_s_detaljima_o_biljci(
                id_slike=id_slike,
                command_za_button_BACK=gui_objekt.prozor_prikaz_biljaka_PyPosuda,
            ),
        )
        slika_u_lijevom_frameu.image = label_slika
        slika_u_lijevom_frameu.place(anchor="center", relx=0.5, rely=0.26)
        return id_slike
    else:
        button_s_gridom(
            neki_frame,
            "danger-outline",
            f"izbriši biljku",
            lambda: izbrisi_biljku_iz_baze(
                repozitorij=repozitorij, id_biljke=id_slike, gui_objekt=gui_objekt
            ),
            10,
            11,
            column=3,
            columnspan=3,
            row=5,
            ipadx=1,
            ipady=3,
            padx=20,
            pady=20,
            sticky="ew",
        )
        label(
            neki_frame,
            "Slika nije pronađena",
            ("quicksand", 8),
            "warning",
            None,
            None,
            "center",
            0.5,
            0.9,
        )
        # ubaci_tekst_u_label(neki_frame, "Slika nije pronađena",font="quicksand, 10",bootsytle="warning",relx=0.1,rely=0.1)


def prikaz_biljke_prema_id_u_bazi(frame, frame_za_tekst, repozitorij, id_slike):
    """ova funkcija nakon klika na gumb biljke
    dohvaca biljku prema njezinom ID-u iz baze
    te daje prikaz njezinih podataka iz baze"""

    biljka = repozitorij.dohvati_biljku_prema_idu_u_bazi(id=id_slike)

    if biljka:
        img = dohvati_sliku(width=250, height=165, ime_slike=biljka.slika_biljke)
        if img is not None:
            label_slika = ImageTk.PhotoImage(img)
            slika_biljke = ttk.Label(
                frame,
                image=label_slika,
                bootstyle="light-inverse",
                borderwidth=15,
                relief="groove",
            )
            slika_biljke.image = label_slika
            # ovom place metodom se prikazuje slika na zeljenoj poziciji na prozoru GUI-a
            slika_biljke.place(anchor="center", relx=0.5, rely=0.25)
            # ova funckija ispisuje samo ime biljke iz baze
            ubaci_tekst_u_label(
                frame_za_tekst,
                ime_slike=biljka.ime_biljke,
                font="quicksand, 15",
                bootsytle="dark",
                relx=0.2,
                rely=0.1,
            )

            zalijevanje = biljka.zalijevanje
            mjesto = biljka.mjesto
            supstrat = biljka.supstrat

    # ovdje se ispisuju karakteristike biljaka vezane za NJEGU
    label(
        frame_za_tekst,
        f"Zalijevanje: jednom {zalijevanje}\n\nMjesto u stanu: {mjesto}\n\nSupstrat: {supstrat}",
        ("Quicksand", 10),
        "dark",
        None,
        None,
        "nw",
        0.02,
        0.3,
    )


def otvori_sliku_biljke_koju_cemo_spremiti_u_bazu(ime_nove_biljke):
    """ova metoda otvara biljku iz foldera korisnika
    i sprema je u isti folder
    s imenom koje je korisnik odabrao"""
    # otvaranje slike iz foldera
    photo_filename = filedialog.askopenfilename(title="Open image")
    img = Image.open(str(photo_filename))
    img = img.resize((150, 110))
    label_slika = ImageTk.PhotoImage(img)

    # spremanje slike i putanje u folder
    putanja_slike = f"{ime_nove_biljke.get()}.jpg"

    if img:
        nova_slika = f"{ime_nove_biljke.get()}.jpg"

        putanja_do_slike = spoji_sliku_s_folderom(
            nova_slika, folder_name="SLIKE_BILJAKA"
        )
        # na disk spremamo sa punom putanjom da se ne spremi
        # u folderu iz kjeg je pozvana aplikacija
        img.save(putanja_do_slike)
        img.close()
    else:
        nova_slika = ""
    # u bazu putanju do slike spremamo samo ime slike


def izbrisi_biljku_iz_baze(repozitorij, id_biljke, gui_objekt):
    repozitorij.delete_biljka(id=id_biljke,gui_objekt=gui_objekt)


# FUNKCIJE ZA KORISNIKA/E


def provjeri_korisnika_u_bazi(repozitorij, username):
    korisnik = repozitorij.get_user_by_username(username.get())
    return korisnik


def spremi_korisnika(repozitorij, username, password, gui_objekt):
    """ova metoda prima username i password koji je unio korisnik
    u Entry, provjera postoji li user;
    ako user postoji, nudi ponovni unos novog korisnika,
    a ako je usera nema u bazi, sprema ga"""
    print(f"Username: {username}")
    print(f"Password: {password}")

    korisnik = repozitorij.get_user_by_username(username)

    if korisnik:
        showinfo(title="Registracija", message=f"Korisnik {(username).capitalize()} već postoji.")

    else:
        repozitorij.create_user(Korisnik(username=username, password=password))

        showinfo(
            title="Registracija",
            message=f"Korisnik '{(username).capitalize()}' je uspješno spremljen!",
        )
        gui_objekt.prozor_prikaz_korisnika()


def provjeri_korisnika_postoji_li_u_bazi(repozitorij, gui_objekt):
    """
    ova metoda provjerava postoji li na GUI uneseni username
    i lozinka u bazi korisnika;
    ako postoji prikazuje pozdravni prozor za korisnika,
    ako ne postoji vraća na ponovni odabir login ili registracija,
    a ako postoji, ali je pogresna lozinka daje tu obavijest te nudi ponovni unos
    """
    korisnik = provjeri_korisnika_u_bazi(repozitorij, username=gui_objekt.username)
    if korisnik:
        if gui_objekt.password.get() == korisnik.password:
            print(
                f"Korisnik {gui_objekt.username.get()} postoji u bazi. Ulaz slobodan."
            )
            gui_objekt.nacrtaj_drugi_prozor(korisnik.username)
        else:
            showinfo(
                title="Registracija",
                message=f"Korisnik '{korisnik.username}' postoji.\n lozinka je neispravna! Pokušaj ponovo!",
            )
            gui_objekt.nacrtaj_prvi_prozor_login()
            print(f"Korisnička lozinka je neispravna")
    else:
        showinfo(
            title="Registracija",
            message=f"Korisnik {gui_objekt.username.get()} ne postoji!",
        )
        print(f"Korisnik ne postoji")
        gui_objekt.prozor_ulaska_login_ili_registracija()


def prikaz_korisnika(frame, repozitorij, gui_objekt):
    """ova funkcija u bazi odabire sve korisnike
    te ih ispisuje u obliku tablice prikazujuci njihov
    id, ime i lozinku;
    imena se ispisuju kao gumbi koji potom prikazuju pojedinog korisnika"""

    korisnici = repozitorij.dohvati_sve_korisnike()
    e = ttk.Label(
        frame,
        width=20,
        text="IME KORISNIKA\nodaberite ime korisnika",
        font="quicksand, 10",
        borderwidth=2,
        anchor="center",
        bootstyle="warning-inverse",
        justify="center",
    )
    e.grid(row=0, column=0)

    red = 1
    for korisnik in korisnici:
        button_s_gridom(
            frame,
            bootstyle="warning.outline",
            text=korisnik.username,
            command=lambda id_korisnika=korisnik.id: gui_objekt.prozor_s_detaljima_o_korisniku(
                uhvaceni_korisnik=id_korisnika
            ),
            padding=8,
            width=25,
            column=0,
            columnspan=1,
            row=red,
            ipadx=5,
            ipady=5,
            padx=10,
            pady=10,
            sticky="nw",
        )
        red = red + 1

        # ttk.Button(
        #     frame, width=30, padding=10,
        #     text=korisnik.username,
        #     bootstyle="warning.outline",
        #     command=lambda id_korisnika=korisnik.id:gui_objekt.prozor_s_detaljima_o_korisniku(uhvaceni_korisnik=id_korisnika)
        # ).grid(row=red, column=0)
        # red=red+1


def prikaz_korisnika_prema_id_iz_baze(frame, repozitorij, uhvaceni_korisnik):
    """ova funkcija dohvaca korisnika iz baze prema njegovom idu
    te ispisuje njegove podatke na gui-u,
    takoder ispisuje tekst s uputama sto rade gumbi na ekranu"""
    korisnik = repozitorij.dohvati_korisnika_prema_id(id=uhvaceni_korisnik)
    # session.query(Korisnik).filter_by(id=uhvaceni_korisnik).first()
    if korisnik:
        # print("ovo je proba dohvata korisnika pomocu sqlalchemy")
        # print(korisnik.username)
        ime_korisnika = korisnik.username
        lozinka = korisnik.password

    label(
        frame,
        f"Bok, {(ime_korisnika).capitalize()}!",
        ("quicksand", 14),
        "warning",
        None,
        None,
        "center",
        0.5,
        0.1,
    )
    label(
        frame,
        f"Tvoje korisničko ime je: {ime_korisnika}",
        ("quicksand", 12),
        "warning",
        None,
        None,
        "center",
        0.5,
        0.3,
    )
    label(
        frame,
        f"Tvoja lozinka je: {lozinka}",
        ("quicksand", 12),
        "warning",
        None,
        None,
        "center",
        0.5,
        0.4,
    )
    label(
        frame,
        "Za ažuriranje podataka odaberi gumb 'ažuriraj korisnika'\nZa brisanja korisnika odaberi gumb 'izbriši korisnika'\nZa povratak odaberite gumb 'BACK'",
        ("quicksand", 10),
        "primary",
        "center",
        None,
        "center",
        0.5,
        0.7,
    )


# FUNKCIJE ZA PYPOSUDU/E:


def dohvati_sve_posude_iz_baze_i_nacrtaj_u_gui(repozitorij, frame, gui_objekt):
    """ova funkcija dohvaca sve posude iz baze u obliku liste
    te prikazuje postojece posude u posebnim frameovima
    pomocu for petlje pri cemu je slika posude gumb koji prikazuje
    podatke o odabranoj posudi; ako posuda sadrzi biljku tada se ispisuju i
    potrebne akcije za biljku prema dohvacenim podacima sa senzora,
    no ako je posuda prazna NEMA prikaza potrebnih aktivnosti;
    ovdje je to definiramo if/else statementima"""

    pyposude_iz_baze = repozitorij.dohvati_sve_posude_iz_baze()

    stupac = 0
    redak = 0

    for pyposuda in pyposude_iz_baze:
        # frameovi
        glavni_frame = ttk.Frame(
            frame, width=10, height=50, borderwidth=1, relief="raised", style="deafult"
        )
        glavni_frame.grid(row=redak, column=stupac, padx=23, pady=20)  # pady=110

        lijevi_frame = dodaj_frame(
            glavni_frame, None, redak, 0, "white", 150, 145, None, None, None
        )  # svijetlo zuta - FFE890
        desni_frame = dodaj_frame(
            glavni_frame, None, redak, 1, "default", 160, 145, None, None, None
        )  # svijetlo zuta - FFE890

        ubaci_sliku_kao_button_u_label_posude(
            lijevi_frame,
            putanja_slike=pyposuda.slika_posude,
            id_slike=pyposuda.id,
            gui_objekt=gui_objekt,
        )
        ubaci_tekst_u_label(
            lijevi_frame,
            pyposuda.ime_posude,
            font="quicksand, 10",
            bootsytle="warning",
            relx=0.2,
            rely=0.8,
        )

        posadena_biljka = pyposuda.ime_posadjene_biljke()
        if posadena_biljka is not None:
            label(
                frame=desni_frame,
                tekst=f"BILJKA:\n{posadena_biljka}",
                font_slova=("quicksand", 10),
                stil="dark",
                poravnanje="left",
                pozadina=None,
                anchor="nw",
                relx=0.15,
                rely=0.2,
            )
            prikaz_statusa_biljke_prema_podacima_sa_senzora(
                desni_frame, "nw", 0.15, 0.6
            )
        else:
            posadena_biljka = "PyPosuda je prazna"
            label(
                frame=desni_frame,
                tekst="PyPosuda\nje prazna",
                font_slova=("quicksand", 9),
                stil="dark",
                poravnanje="left",
                pozadina=None,
                anchor="nw",
                relx=0.15,
                rely=0.4,
            )

        stupac += 1

        if stupac >= 2:
            redak += 1
            stupac = 0


def prikaz_posude_prema_id_u_bazi(
    frame, frame_za_tekst, repozitorij, id_slike, gui_objekt, relx, rely
):
    """ova funkcija nakon klika na gumb posude
    dohvaca posudu prema njezinom ID-u iz baze
    te daje prikaz njezinih podataka iz baze;
    ako posuda sadrzi biljku tada se ispisuju i podaci senzora,
    no ako je posuda prazna NEMA prikaza podataka sa senzora;
    ovdje je to definiramo if/else statementima;
    u ovoj funkciji reguliram crtanje gumba sync i njegovog framea"""

    pyposuda = repozitorij.dohvati_posudu_prema_idu_sqlalchemy_query(id=id_slike)

    if pyposuda:
        img = dohvati_sliku(
            width=250,
            height=165,
            ime_slike=pyposuda.slika_posude,
            folder_name="SLIKE_POSUDA",
        )
        if img is not None:
            label_slika = ImageTk.PhotoImage(img)
            label_kao_slika(
                frame=frame,
                image=label_slika,
                bootsytle="light_inverse",
                borderwidth=15,
                relief="groove",
                anchor="center",
                relx=relx,  # o3
                rely=rely,  # 025
            )
            ubaci_tekst_u_label(
                frame_za_tekst,
                ime_slike=pyposuda.ime_posude,
                font="quicksand, 15",
                bootsytle="dark",
                relx=0.28,
                rely=0.1,
            )

        ime_posude = pyposuda.ime_posude
        posadena_biljka = pyposuda.ime_posadjene_biljke()

        if posadena_biljka is not None:
            frame_za_status_biljke = dodaj_frame_place(
                frame, None, 0, 270, 150, None, "center", 0.7, 0.59
            )
            prikaz_svih_senzora_u_gui_s_dohvacenim_podacima(
                frame, frame_za_status_biljke
            )
            gumb_sinkronizacije(
                frame_za_status_biljke,
                lambda: gui_objekt.prozor_s_detaljima_o_posudi(id_slike),
                padding=8,
                width=32,
                x=0,
                y=115,
            )
        else:
            posadena_biljka = "PyPosuda je prazna"

    # ovdje se ispisuje ime posude i koja se biljka nalazi u posudi
    label(
        frame_za_tekst,
        f"Posuda: '{ime_posude}'\nBiljka u posudi: {posadena_biljka}",
        ("Quicksand", 10),
        "warning",
        "center",
        None,
        "center",
        0.5,
        0.8,
    )


def prikaz_posude_prema_id_u_bazi_za_azuriranje(
    frame, frame_za_tekst, repozitorij, id_slike, relx, rely
):
    """ova funkcija nakon klika na gumb posude
    dohvaca posudu prema njezinom ID-u iz baze
    te daje prikaz njezinih podataka iz baze;
    kod nje nemamo prikaz senzora vec samo podaci o posudi
    koji se mogu izmijeniti u prozoru u kojem se
    zove ova funkcija"""

    pyposuda = repozitorij.dohvati_posudu_prema_idu_sqlalchemy_query(id=id_slike)
    if pyposuda:
        img = dohvati_sliku(
            width=250,
            height=165,
            ime_slike=pyposuda.slika_posude,
            folder_name="SLIKE_POSUDA",
        )
        if img is not None:
            label_slika = ImageTk.PhotoImage(img)
            label_kao_slika(
                frame=frame,
                image=label_slika,
                bootsytle="light_inverse",
                borderwidth=15,
                relief="groove",
                anchor="center",
                relx=relx,  # o3
                rely=rely,  # 025
            )
            ubaci_tekst_u_label(
                frame_za_tekst,
                ime_slike=pyposuda.ime_posude,
                font="quicksand, 15",
                bootsytle="dark",
                relx=0.28,
                rely=0.1,
            )

        ime_posude = pyposuda.ime_posude
        posadena_biljka = pyposuda.ime_posadjene_biljke()

        if posadena_biljka is None:
            posadena_biljka = "nema biljke"
            # print("PyPosuda je prazna.")

    # ovdje se ispisuje ime posude i koja se biljka nalazi u posudi
    label(
        frame_za_tekst,
        f"Posuda: '{ime_posude}'\nBiljka: '{posadena_biljka}'",
        ("Quicksand", 12),
        "dark",
        "center",
        None,
        "center",
        0.5,
        0.6,
    )


def prikaz_slike_posude_prema_id_u_bazi(frame, repozitorij, id_slike, relx, rely):
    """ova funkcija crta (samo) sliku posude
    prema njezinom idu iz baze"""

    pyposuda = repozitorij.dohvati_posudu_prema_idu_sqlalchemy_query(id=id_slike)
    if pyposuda:
        img = dohvati_sliku(
            width=250,
            height=165,
            ime_slike=pyposuda.slika_posude,
            folder_name="SLIKE_POSUDA",
        )
        if img is not None:
            label_slika = ImageTk.PhotoImage(img)
            label_kao_slika(
                frame=frame,
                image=label_slika,
                bootsytle="light_inverse",
                borderwidth=15,
                relief="groove",
                anchor="center",
                relx=relx,  # o3
                rely=rely,
            )  # 025


def gumb_kojim_dohvacamo_detalje_o_biljci_iz_baze(root, session, id_slike, gui_objekt):
    pyposuda = session.query(PyPosude).filter_by(id=id_slike).first()
    # print(f"Ovo je id dohvacene slike: '{id_slike}'")
    if pyposuda:
        biljka_u_posudi = pyposuda.ime_posadjene_biljke()
        if biljka_u_posudi is not None:
            # print(f"ovo je '{biljka_u_posudi}', a ja trebam ID")
            biljka = session.query(Biljke).filter_by(ime_biljke=biljka_u_posudi).first()
            if biljka:
                # print(biljka.ispisi_podatke())
                button(
                    frame=root,
                    style="warning",
                    bootstyle=None,
                    text=f"{biljka_u_posudi}",
                    command=lambda: gui_objekt.prozor_s_detaljima_o_biljci(
                        id_slike=biljka.id,
                        command_za_button_BACK=lambda: gui_objekt.prozor_s_detaljima_o_posudi(
                            id_slike=id_slike
                        ),
                    ),
                    padding=10,
                    width=20,
                    anchor="center",
                    relx=0.3,
                    rely=0.58,
                )
        else:
            biljka_u_posudi = "nema biljke"
            showinfo(
                title="info",
                message="U ovoj PyPosudi nema biljke\nMožete je dodati pomoću opcije 'ažuriraj posudu'",
            )


def prikaz_posude_za_azuriranje_prema_id_u_bazi(
    frame, frame_za_tekst, repozitorij, id_slike
):
    """ova funkcija nakon klika na gumb posude
    dohvaca posudu prema njezinom ID-u iz baze
    te daje prikaz njezinih podataka iz baze"""

    # ovime SQLalchemy querijem je odabrana posuda prema navedenom id-u iz baze
    # ovaj query zamjenjuje raw sql koji sam ranije koristila
    pyposuda = repozitorij.dohvati_posudu_prema_idu_sqlalchemy_query(id=id_slike)
    # posuda_prema_idu_sqlalchemy_query(session,id_slike)
    # session.query(PyPosude).filter_by(id=id_slike).first()
    if pyposuda:
        img = dohvati_sliku(
            width=250,
            height=165,
            ime_slike=pyposuda.slika_posude,
            folder_name="SLIKE_POSUDA",
        )
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
                rely=0.5,
            )
            ubaci_tekst_u_label(
                frame=frame_za_tekst,
                ime_slike=pyposuda.ime_posude,
                font="quicksand, 15",
                bootsytle="dark",
                relx=0.5,
                rely=0.1,
            )

            ime_posude = pyposuda.ime_posude

            if posadena_biljka is not None:
                # ime posadene biljke dohvacam sada preko posude iz baze i metode klase PyPosuda .ime_posadene_biljke()
                posadena_biljka = pyposuda.ime_posadjene_biljke()
            else:
                posadena_biljka = "PyPosuda je prazna"

    # ovdje se ispisuju karakteristike biljaka vezane za NJEGU
    label(
        frame_za_tekst,
        f"Posuda: '{ime_posude}'\n\n Biljka u posudi: {posadena_biljka}",
        ("Quicksand", 10),
        "dark",
        None,
        None,
        "nw",
        0.1,
        0.7,
    )


def otvori_sliku_posude_od_korisnika(ime_nove_posude):
    """ova metoda otvara posudu iz foldera korisnika
    i sprema je u isti folder
    s imenom koje je korisnik odabrao"""
    # otvaranje slike iz foldera
    photo_filename = filedialog.askopenfilename(title="Open image")
    img = Image.open(str(photo_filename))
    img = img.resize((150, 110))
    label_slika = ImageTk.PhotoImage(img)

    # spremanje slike i putanje u folder
    putanja_slike = f"{ime_nove_posude.get()}.jpg"

    if img:
        nova_slika = f"{ime_nove_posude.get()}.jpg"
        putanja_do_slike = spoji_sliku_s_folderom(
            nova_slika, folder_name="SLIKE_POSUDA"
        )
        # na disk spremamo sa punom putanjom da se ne spremi
        # u folderu iz kjeg je pozvana aplikacija
        img.save(putanja_do_slike)
        img.close()
    else:
        nova_slika = ""

        # repozitorij.spremi_posudu_preko_imena(
    #     ime_posude=ime_nove_posude.get(),
    #     slika_posude=nova_slika,
    #     ime_biljke=posadena_biljka.get(),
    # )
    # showinfo(title="YES!", message=f"Posuda '{putanja_slike}' uspješno spremljena!")
    # gui_objekt.prozor_prikaz_posuda_PyPosuda()


def izbrisi_biljku_iz_posude(repozitorij, id_slike, gui_objekt):
    """ova funkcija brise biljku iz posude u koju je posadena
    te je uklanja isto tako iz baze;
    to radi na taj nacin da najprije dohvaca odgovarajucu posudu iz baze
    prema njezinom id-u te na taj nacin pristupa biljci.
    Nakon toga poziva repozitorij te metodu za brisanje biljke iz baze;
    na kraju otvara prozor s prikazom svih posuda u bazi"""

    pyposuda = repozitorij.dohvati_posudu_prema_idu_sqlalchemy_query(id=id_slike)
    ime_biljke = pyposuda.ime_posadjene_biljke()

    repozitorij.izbrisi_posadenu_biljku_iz_posude(id_slike=id_slike)
    showinfo(
        title="OK",
        message=f"Biljka '{ime_biljke}' je uklonjena.\n'{pyposuda.ime_posude}' je prazna",
    )
    gui_objekt.prozor_prikaz_posuda_PyPosuda()


def izbrisi_posudu_iz_baze(repozitorij, id_posude, gui_objekt):
    """ova se funkcija koristi za brisanje posude na gui;
    izvrsava se pritiskom na gumb 'izbrisi posudu';
    javlja da je brisanje uspjesno nakon brisanja posude
    te nakon akcije brisanja prikazuje prozor sa svim posudama"""

    repozitorij.izbrisi_pyposudu(id=id_posude)
    showinfo(title="OK", message="Posuda je uspješno izbrisana!")
    gui_objekt.prozor_prikaz_posuda_PyPosuda()


# PROBA PANDASA
def proba_prikaza_podataka_o_biljci_iz_baze(ime_baze):
    session = spoji_se_na_bazu(ime_baze)
    ime_tablice_iz_baze = "biljke"  # ovo je ime tablice u SQL_PyFlora_Baza.sqlite
    # mora biti ime tablice jer koristim funkciju "read_sql_table" iz pandasa
    # ako mijenjam ime tablice dobijem podatke iz svih tih drugih
    connection = session.connection()
    biljka = pd.read_sql_table(table_name=ime_tablice_iz_baze, con=connection)
    print(biljka)
