from enum import unique
from tkinter.messagebox import NO
from turtle import pos
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import TextClause
from tkinter.messagebox import showinfo, showwarning

### OVAJ MODUL SADRZI KLASE: Korisnik, Biljke i PyPosude te SQLAlchemyRepozitorij s metodama za rad s bazom

Base = declarative_base()


# Klasa Korisnik
class Korisnik(Base):
    __tablename__ = "korisnici"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def ispisi_podatke(self):
        print(f"ID={self.id}, Name={self.username}, email={self.password}")

# Klasa Biljke
class Biljke(Base):
    __tablename__ = "biljke"
    id = db.Column(db.Integer, primary_key=True)
    ime_biljke = db.Column(db.String(250), unique=True, nullable=False)
    slika_biljke = db.Column(db.String)
    zalijevanje = db.Column(db.String)  # jednom dnevno/tjedno/mjesecno
    mjesto = db.Column(db.String)  # tamno/svijetlo, toplo/hladno
    supstrat = db.Column(db.String)  # da/ne

    # ovime povezujem PyPosude s biljkom preko ForeignKeya
    biljka = relationship("PyPosude", backref=backref("biljka"))

    def ispisi_podatke(self):
        print(
            f"ID={self.id}, naziv_biljke = {self.ime_biljke}, putanja do slike = {self.slika_biljke}"
        )
        print(
            f"zalijeva se jednom {self.zalijevanje}, odgovara joj {self.mjesto} mjesto, supstrat: {self.supstrat}"
        )

# Klasa PyPosude
class PyPosude(Base):
    __tablename__ = "pyposude"
    id = db.Column(db.Integer, primary_key=True)
    ime_posude = db.Column(db.String(250), unique=True, nullable=False)
    slika_posude = db.Column(db.String)
    posadena_biljka = db.Column(db.Integer, db.ForeignKey("biljke.id")) #string (ime_biljke)
    # biljka_id = db.Column(db.Integer, db.ForeignKey("biljke.id"))

    # definiramo ForeignKey vezu na stupac "id" u klasi "Biljke"

    def ispisi_podatke(self):
        print(
            f"ID={self.id}, ime posude = {self.ime_posude}, posadena biljka = {self.posadena_biljka}"
        )

    def ime_posadjene_biljke(self):
        if self.biljka:
            return self.biljka.ime_biljke
        return None

# funkcija za spajanje na bazu
def spoji_se_na_bazu(ime_baze):
    """glavna funkcija ovog modula
    Spaja se na bazu i kreria tablicu ako ne postoji"""
    # Povezimo se s bazom koristeci SQLAlchemy
    db_engine = db.create_engine(f"sqlite:///{ime_baze}")

    # Kreiraj bazu sa tablicom koju smo deklarirali u klasi Korisnik(Biljke,PyPosude)
    # odnosno izvršit će SQL upit:
    Base.metadata.create_all(db_engine)

    # otvori konekciju koju ćemo koristiti za upite prema bazi
    Session = sessionmaker()
    Session.configure(bind=db_engine)
    session = Session()
    return session

# Klasa SQLAlchemyRepozitorij
class SQLAlchemyRepozitorij:
    """klasa koja sadrzi metode za rad s klasama
    Biljke, Korisnik te PyPosude"""
    def __init__(self, session):
        # ovo je session koji dobijemo nakon poziva funkcije spoji_se_na_bazu
        self.session = session

    # KORISNICI
    # metode za korisnike

    def create_user(self, user: Korisnik):
        """ova metoda kreira korisnika;
        koristim ovu metodu"""
        # INSERT INTO Korisnik(id, name, password) VALUES(?, ?, ?)
        self.session.add(user)
        self.session.commit()
        return user

    def dohvati_sve_korisnike(self):
        """ove metoda dohvaca sve korisnike u bazi;
        koristim ovu metodu"""
        return self.session.query(Korisnik).all()

    def update_user(self, user):
        """ne koristim ovu metodu"""
        return self.create_user(user)

    def dohvati_korisnika_prema_id(self, id):
        """ova metoda dohvaca korisnika prema njegovom idu
        u bazi; koristim je"""
        # ako nemamo u bazi zapisa koji ima ID = id, ovo vraća None!
        return self.session.query(Korisnik).filter_by(id=id).first()

    def get_user_by_username(self, username):
        """ne koristim ovu metodu"""
        # ako nemamo u bazi zapisa koji ima username = username, ovo vraća None!
        return (
            self.session.query(Korisnik).filter(Korisnik.username == username).first()
        )

    def izbrisi_korisnika(self, id, gui_objekt):
        """ova metoda dohvaca korisnika prema idu
        i onda brise dohvacenog korisnika iz baze"""
        korisnik = self.dohvati_korisnika_prema_id(id)
        if korisnik:
            self.session.delete(korisnik)
        self.session.commit()

        showinfo(
            title="ok",
            message=f"Izbrisali smo korisnika '{(korisnik.username).capitalize()}'",
        )
        gui_objekt.prozor_prikaz_korisnika()

    def azuriraj_korisnika(self, id, korisnicko_ime, lozinka, gui_objekt):
        korisnik = self.dohvati_korisnika_prema_id(id)
        if korisnik:
            korisnik.username = korisnicko_ime
            korisnik.password = lozinka
        self.session.commit()

        showinfo(
            title="super",
            message=f"Ažurirali smo korisnika '{(korisnik.username).capitalize()}'",
        )
        gui_objekt.prozor_prikaz_korisnika()

    def delete_all_users(self):
        """ne koristim ovu metodu"""
        self.session.query(Korisnik).delete()
        self.session.commit()

    # BILJKE
    # metode za biljke

    def spremi_biljku(self, biljka: Biljke, gui_objekt):
        """ova metoda sprema biljku u bazu
        kad joj se predaju svi trazeni atributi klase "Biljke"
        za spremanje u bazu; nakon toga se pokazuje obavijest 
        da je biljka uspjesno spremljena i prikazuje se
        prozor koji sadrzi sve biljke iz baze
        """
        self.session.add(biljka)
        self.session.commit()
        showinfo(title="YES!", message=f"Biljka '{biljka.ime_biljke}' je uspješno spremljena!")
        gui_objekt.prozor_prikaz_biljaka_PyPosuda()
        return biljka

    def dohvati_sve_biljke_iz_baze(self):
        """ovom metodom dohvacam sve biljke iz baze"""
        return self.session.query(Biljke).all()

    def azuriraj_biljku(
        self, ime_biljke, zalijevanje, mjesto, supstrat, id_biljke, gui_objekt
    ):
        """ova metoda azurira biljku u bazi prema podacima
        koje korisnik izmijeni u prozoru;
        metoda dohvaca biljku prema njezinom idu te mijenja
        postojece podatke novima unesenima u prozor
        """
        biljka = self.dohvati_biljku_prema_idu_u_bazi(id=id_biljke)
        if biljka:
                biljka.ime_biljke=ime_biljke
                biljka.zalijevanje=zalijevanje
                biljka.mjesto=mjesto
                biljka.supstrat=supstrat
                print(f"vrijednosti nakon azuriranja: {biljka.ime_biljke},{biljka.zalijevanje},{biljka.mjesto},{biljka.supstrat}")
        self.session.commit()
        
        # nakon azuriranja biljke iz baze prikazuje se obavijest da su podaci spremljeni
        # i otvara se prozor na kojem su prikazane sve biljke iz baze
        showinfo(title="OK!", message="Podaci uspješno spremljeni!")
        gui_objekt.prozor_prikaz_biljaka_PyPosuda()

    def izbrisi_posadenu_biljku_iz_posude(self, id_slike):
        """ova metoda brise posadenu biljku
        koja je POSADENA u posudi tako da posadena_biljku
        stavi na None"""
        posuda = self.session.query(PyPosude).filter_by(id=id_slike).first()
        if posuda:
            posuda.posadena_biljka = None
            self.session.commit()

    def dohvati_biljku_prema_idu_u_bazi(self, id):
        """ova metoda dohvaca biljku
        prema njezinom idu iz bazu"""
        # ako nemamo u bazi zapisa koji ima ID = id, ovo vraća None!
        return self.session.query(Biljke).filter_by(id=id).first()

    def popis_imena_svih_biljaka_iz_baze(self):
        """ova metoda vraca listu imena biljaka iz baze;
        koristim je kod comboboxa za odabir biljke koju sadim u posudu"""
        baza_biljaka = self.session.query(Biljke).all()
        biljka = [biljka.ime_biljke for biljka in baza_biljaka]
        return biljka

    def get_biljka_by_ime(self, ime_biljke):
        # ako nemamo u bazi zapisa koji ima username = username, ovo vraća None!
        return (
            self.session.query(Biljke).filter(Biljke.ime_biljke == ime_biljke).first()
        )

    def get_biljke_for_pyposuda(self, biljka_id):
        return (
            self.session.query(PyPosude).filter(PyPosude.biljka.id == biljka_id).first()
        )

    def delete_biljka(self, id, gui_objekt):
        """ova metoda brise odabranu biljku ako biljka postoji,
        a ne koristi se u pyposudi;
        ako je biljka posadena u posudi,
        tada se vraca obavijest da je biljka posadena"""

        biljka = self.dohvati_biljku_prema_idu_u_bazi(id)

        if biljka:
            koristi_li_se = (
                self.session.query(PyPosude)
                .filter(PyPosude.posadena_biljka == biljka.id)
                .count()
                > 0
            )
            
            if not koristi_li_se:
                self.session.delete(biljka)
                showinfo(title="OK", message=f"Biljka je uspješno izbrisana!")
                gui_objekt.prozor_prikaz_biljaka_PyPosuda()
            else:
                showwarning(
                    title="oprez!", message=f"Brisanje nije moguće. \nBiljka '{biljka.ime_biljke}'je posadena u PyPosudi."
                )
                #print(f"{biljka.ime_biljke} se koristi u PyPosudi")
        self.session.commit()

    # PY POSUDE
    # metode za Pyposude

    def spremi_posudu(self, posuda: PyPosude):
        self.session.add(posuda)
        self.session.commit()
        return posuda

    def spremi_posudu_preko_imena(self, ime_posude, slika_posude, ime_biljke,gui_objekt):
        """ """
        biljka = self.session.query(Biljke).filter_by(ime_biljke=ime_biljke).first()
        posuda = PyPosude(ime_posude=ime_posude, slika_posude=slika_posude)
        if biljka:
            posuda.posadena_biljka = biljka.id

        self.session.add(posuda)
        self.session.commit()
        showinfo(title="YES!", message=f"Posuda '{ime_posude}' uspješno spremljena!")
        gui_objekt.prozor_prikaz_posuda_PyPosuda()
        return posuda

    def azuriraj_pyposudu_u_bazi(self, id_posude, ime_posude, posadena_biljka,gui_objekt):
        posuda = self.dohvati_posudu_prema_idu_sqlalchemy_query(id=id_posude)
        # posuda = self.session.query(PyPosude).filter_by(id=id_posude).first()
        if posuda:
            biljka = (
                self.session.query(Biljke).filter_by(ime_biljke=posadena_biljka).first()
            )
            if biljka:
                posuda.posadena_biljka = biljka.id
            posuda.ime_posude = ime_posude
        self.session.commit()
        showinfo(title="OK!", message="Podaci uspješno spremljeni!")
        gui_objekt.prozor_prikaz_posuda_PyPosuda()


    def dohvati_sve_posude_iz_baze(self):
        """ova metoda dohvaca i vraca sve posude u bazi"""
        return self.session.query(PyPosude).all()

    def dohvati_posudu_prema_idu_sqlalchemy_query(self, id):
        """ova metoda dohvaca tocno odredenu posudu
        prema njezinom id-u iz baze koristeci sqlalchemy query,
        dok je prije posuda dohvacana pomocu raw sql zahtjeva"""
        # ako nemamo u bazi zapisa koji ima ID = id, ovo vraća None!
        return self.session.query(PyPosude).filter_by(id=id).first()

    def dohvati_ime_posude(self, id):
        """ova metoda dohvaca samo ime posude iz baze
        koristeci sqlalchemy query"""
        pyposuda = self.dohvati_posudu_prema_idu_sqlalchemy_query(id)
        return pyposuda.ime_posude

    def izbrisi_pyposudu(self, id):
        """ova metoda dohvaca posudu prema njezinom idu
        te je brise ako posuda postoji"""
        posuda = self.dohvati_posudu_prema_idu_sqlalchemy_query(id)
        if posuda:
            self.session.delete(posuda)
        self.session.commit()
