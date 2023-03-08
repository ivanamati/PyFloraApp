import os
import tkinter as tk
from tkinter.messagebox import showerror, showinfo
from tkinter import filedialog
from turtle import width
from PIL import ImageTk, Image

from SQLAlchemy_repo import Korisnik, spoji_repozitorij_s_bazom


def spoji_sliku_s_folderom(photo_filename):
    if os.path.exists(photo_filename):
        return photo_filename
    #  puna putanja do foldera sa slikama koji se nalazi odmah uz ovaj file
    folder_sa_slikama = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),   # folder u kojem se nalazi ovaj file
            "SLIKE"                      # folder u koji ćemo spremati slike
        )
    )
    profilna_slika_puna_putanja = os.path.join(
        folder_sa_slikama, 
        photo_filename
    )
    return profilna_slika_puna_putanja

def dohvati_sliku(photo_filename="algebra_ucionica.jpg", width=150, height=150):
    if not photo_filename:
        return None
        
    putanja = spoji_sliku_s_folderom(photo_filename)
    if not os.path.exists(putanja):
        return None


    try:
        img = Image.open(putanja) 
        img = img.resize((width, height))
        return img
    except FileNotFoundError:
        return None

class PyFlora:

    def __init__(self, ime_baze):
        # DIO ZA root ELEMENT
        self.root = tk.Tk()
        self.width = 700
        self.height = 300
        self.root.title('PyFlora Posuda')
        self.root.geometry(f'{self.width}x{self.height}')

        # ovo je samo ime baze, ne i veza na bazu
        self.ime_baze = ime_baze
        self.korisnik = ''
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def nacrtaj_prvi_prozor(self):
        self.clear_frame()
        frm_display_username = tk.Frame(self.root).grid()
        
        oznaka_username = tk.Label(frm_display_username, text='User name')
        oznaka_username.grid(column=2, row=0, padx=5, pady=5)

        self.username = tk.Entry(frm_display_username)
        self.username.grid(column=3, row=0, padx=25, pady=15)

        frm_display_lozinka = tk.Frame(self.root).grid()

        oznaka_lozinka = tk.Label(frm_display_lozinka, text='Password')
        oznaka_lozinka.grid(column=2, row=2, padx=55, pady=15)

        self.password = tk.Entry(frm_display_lozinka, show="*")
        self.password.grid(column=3, row=2, padx=55, pady=15)

        frm_action_buttons = tk.Frame(self.root).grid()

        button_ulogiraj = tk.Button(frm_action_buttons, text='PRIJAVI ME', command=self.dohvati_podatke, bg="grey")
        button_ulogiraj.grid(column=3, columnspan=3, row=4, ipadx=15, ipady=10, padx=15, pady=10)

    def nacrtaj_drugi_prozor(self):
        self.clear_frame()
        oznaka = tk.Label(
            self.root, 
            text=f'Dobro da ste tu, {self.korisnik}'
        )
        oznaka.grid(column=2, row=0, padx=5, pady=5, columnspan=2)
        button_povratak = tk.Button(
            self.root, 
            text='PRIKAŽI SLIKU', 
            command=self.nacrtaj_treci_prozor
            )
        button_povratak.grid(column=0, columnspan=3, row=2, ipadx=15, ipady=10, padx=15, pady=10)
        # ZADATAK: tu ispisati sve korisnike iz baze u nekom frameu,  koristiti neku listu

    def nacrtaj_treci_prozor(self):
        self.clear_frame()
        self.dodaj_sliku_u_frame(self.root, "algebra_ucionica.jpg")

        button_nema_nazad = tk.Button(
            self.root, 
            text='Ajmo dalje', 
            command=self.nacrtaj_cetvrti_prozor
        )
        button_nema_nazad.grid(column=2, columnspan=3, row=4, ipadx=15, ipady=10, padx=15, pady=10)

    def dodaj_sliku_u_frame(self, frame, putanja_do_slike):
        # napuni sliku
        img = dohvati_sliku(photo_filename=putanja_do_slike, width=100, height=75)
        if img is not None:
            label_slika = ImageTk.PhotoImage(img)
            lbl_slika = tk.Label(frame, image=label_slika)
            lbl_slika.image = label_slika
            lbl_slika.place(anchor="center", relx=0.5, rely=0.5)
        else:
            self.dodaj_tekst_u_frame(frame, f"Slika\n {putanja_do_slike}\n nije pronađena")

    def dodaj_tekst_u_frame(self, frame, tekst):
        # napuni tekst
        oznaka = tk.Label(
            frame, 
            text=tekst
        )
        oznaka.place(anchor="center", relx=0.5, rely=0.5)
    
    def dodaj_redak(self, redni_broj, kolona, broj_kolona):
        frame_pape = tk.Frame(self.root, width=250, height=150, bd=1, relief="solid")
        frame_pape.grid(
            row=redni_broj, 
            column=kolona, 
            columnspan=broj_kolona, 
            padx=20, pady=25
        )
        return frame_pape

    def dodaj_frame(self, parent_frame,  red, kolona, background_color):
        frame_child = tk.Frame(
            parent_frame, 
            width=125, height=150, 
            bd=0, relief="solid", bg=background_color
        )
        frame_child.grid(row=red, column=kolona)
        return frame_child
    
    def nacrtaj_podatke(self):
        max_kolona =  self.width//300

        korisnici = self.repozitorij.get_all_users()
        # za sve korisnike iz baze prikaži username uz sliku
        # ovako nekako treba ispisati posude sa cvijećem iz baze :D
        red = 0
        kolona = 0
        for korisnik in korisnici:
            # dio za skaliranje
            # self.root.columnconfigure(kolona, weight = 1, minsize = 100)
            # self.root.rowconfigure(red, weight = 1, minsize = 150)

            frame_pape = self.dodaj_redak(red, kolona*2, 2)
            frame_dite_livo = self.dodaj_frame(frame_pape, red, 0, "red")
            frame_dite_desno = self.dodaj_frame(frame_pape, red, 1, "blue")
            self.dodaj_sliku_u_frame(frame=frame_dite_livo, putanja_do_slike=korisnik.path_to_profile_picture)
            self.dodaj_tekst_u_frame(frame_dite_desno, f" {korisnik.id} \n {korisnik.username} ")
            kolona += 1
            if kolona >= max_kolona:
                kolona = 0
                red += 1


    def nacrtaj_cetvrti_prozor(self):
        self.clear_frame()
        self.nacrtaj_podatke()

        # da se možemo vratiti na početak
        button_nema_nazad = tk.Button(
            self.root, 
            text='Ponovimo', 
            command=self.nacrtaj_prozor_za_dodavanje,
            bg="green"
        )
        button_nema_nazad.grid(
            column=(self.width//300)//2, 
            columnspan=(self.width//300), 
            row=(self.height//250)+2, 
            ipadx=15, ipady=10, 
            padx=15, pady=10,
        )

    def nacrtaj_prozor_za_dodavanje(self):
        self.clear_frame()
        frm_display_username = tk.Frame(self.root).grid()
        
        oznaka_username = tk.Label(frm_display_username, text='User name')
        oznaka_username.grid(column=1, row=0, padx=5, pady=5)

        self.username = tk.Entry(frm_display_username)
        self.username.grid(column=2, row=0, padx=25, pady=15)

        frm_display_lozinka = tk.Frame(self.root).grid()

        oznaka_lozinka = tk.Label(frm_display_lozinka, text='Password')
        oznaka_lozinka.grid(column=1, row=2, padx=55, pady=15)

        self.password = tk.Entry(frm_display_lozinka, show="*")
        self.password.grid(column=2, row=2, padx=55, pady=15)

        # DIO ZA DODAVANJE SLIKE
        frm_picture_button = tk.Frame(self.root).grid()
        button_spremi_sliku = tk.Button(
            frm_picture_button, 
            text='Odaber sliku', 
            command=self.ucitaj_sliku,
            bg="purple"
        )
        
        oznaka_slika = tk.Label(frm_picture_button, text='Putanja do slike')
        oznaka_slika.grid(column=1, row=3, padx=55, pady=15)

        self.putanja_do_slike = tk.Entry(frm_picture_button)
        self.putanja_do_slike.grid(column=2, row=3, padx=55, pady=15)

        button_spremi_sliku.grid(column=3, row=3, ipadx=15, ipady=10, padx=15, pady=10)


        frm_action_buttons = tk.Frame(self.root).grid()

        # SPREMI NOVOG KORISNIKA
        button_spremi = tk.Button(
            frm_action_buttons, 
            text='SPREMI NOVOG KORISNIKA',
            command=self.spremi_korisnika, 
            bg="grey"
        )
        button_spremi.grid(column=3, row=4, ipadx=15, ipady=10, padx=15, pady=10)

        button_nazad = tk.Button(
            frm_action_buttons, 
            text='Odustani', 
            command=self.nacrtaj_cetvrti_prozor,
            bg="red"
        )
        button_nazad.grid(column=1, row=4, ipadx=15, ipady=10, padx=15, pady=10)

    def ucitaj_sliku(self):
        photo_filename = filedialog.askopenfilename(title ='Open image')
        if os.path.exists(photo_filename):
            self.putanja_do_slike.insert(0, os.path.abspath(photo_filename))
            self.dodaj_sliku_u_frame(self.putanja_do_slike.master, photo_filename)
            self.putanja_do_slike.configure(state="disabled")

    def spremi_korisnika(self):
        print(f"Username: {self.username.get()}")
        print(f"Lozinka: {self.password.get()}")
        username  = self.username.get()
        password = self.password.get()
        putanja_do_slike = self.putanja_do_slike.get()
        print(putanja_do_slike)
        if not username:
            showerror(title="Oj!", message="Alo, unesi ime!")
            return
        korisnik = self.repozitorij.get_user_by_username(username)
        if korisnik:
            showerror(title="Oj!", message=f"Korisnik {username} već postoji")
        else:
            # ZADATAK: tu dodati provjeru duljine lozinke i/ili kompleksnosti
            new_img = dohvati_sliku(photo_filename=putanja_do_slike, width=200, height=200)
            # ZADATAK: spremiti sliku u folder slike koji se nalazi uz ovaj file
            if new_img:
                profilna_slika_ime= f"profilna_slika_{username}.jpg"
                putanja_do_slike = spoji_sliku_s_folderom(profilna_slika_ime)
                # na disk spremamo sa punom putanjom da se ne spremi 
                # u folderu iz kjeg je pozvana aplikacija
                new_img.save(putanja_do_slike)
                new_img.close()
            else:
                profilna_slika_ime = ""
            # u bazu putanuu do slike spremamo samo ime slike
            self.repozitorij.create_employee(
                Korisnik(
                    username=username,
                    password=password,
                    path_to_profile_picture=profilna_slika_ime
                )
            )
            showinfo(title="Wohooo!", message=f"Korisnik {username} uspješno spremljen!")
            self.nacrtaj_cetvrti_prozor()


    def provjeri_lozinku(self, username, password):
        
        # dohvatimo objekt Korisnik iz baze ako postoji
        korisnik = self.repozitorij.get_user_by_username(username)
        if korisnik:
            # tu možemo provjeriti jesu li dva stringa ista
            # ne moramo opet zvati bazu za dohvat passworda jer smo dobili cijeli objekt iz baze
            if korisnik.password == password:
                print(f"Korisnik {username} postoji u bazi i puštamo ga dalje")
                return True
            else:
                print(f"Korisnik {username} postoji u bazi ali mu je kriva lozinka")
        else:
            print(f"Korisnik {username} ne postoji u bazi")
        return False

    def dohvati_podatke(self):
        print(f"Username: {self.username.get()}")
        print(f"Lozinka: {self.password.get()}")
        if self.provjeri_lozinku(self.username.get(), self.password.get()):
            self.korisnik = self.username.get()
            self.nacrtaj_drugi_prozor()
            # ZADATAK: na sljedećem ekranu u nekom objektu po želji
            # labela i tome nešto slično
            # prikaži korisničko ime
        else:
            showerror(title="Oj!", message="Alo! Kud si krenuo?")

    def pokreni(self):
        self.repozitorij = spoji_repozitorij_s_bazom(self.ime_baze)
        self.nacrtaj_cetvrti_prozor()
        self.root.mainloop()



if __name__ == "__main__":
    
    gui_program = PyFlora("SQLite_Baza_korisnici.sqlite")
    gui_program.pokreni()

# ZADATAK:

# 1. korištenjem primjer SQLAlchemy_repo.py napraviti repozitorij za
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
#    ako korisnik postoji provjeriti lozinku
#    vraća True ako je sve uspjelo
#    ako korisnik nije pronađen ili lozinka ne odgovara vraća False