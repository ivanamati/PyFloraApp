from enum import unique
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import TextClause

Base = declarative_base()


class Korisnik(Base):
    __tablename__ = "korisnici"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable = False)
    password = db.Column(db.String, nullable=False)

    def ispisi_podatke(self):
        print(f"ID={self.id}, Name={self.username}, email={self.password}")

class Biljke(Base):
    __tablename__ = "biljke"
    id = db.Column(db.Integer, primary_key=True)
    ime_biljke = db.Column(db.String(250), unique=True, nullable = False)
    slika_biljke = db.Column(db.String)
    zalijevanje = db.Column(db.String) #jednom dnevno/tjedno/mjesecno
    mjesto = db.Column(db.String) #tamno/svijetlo, toplo/hladno
    supstrat = db.Column(db.String) #da/ne
 
    def ispisi_podatke(self):
        print(f"ID={self.id}, naziv_biljke = {self.ime_biljke}, putanja do slike = {self.slika_biljke}") 
        print(f"zalijeva se jednom {self.zalijevanje}, odgovara joj {self.mjesto} mjesto, supstrat: {self.supstrat}")

class PyPosude(Base):
    __tablename__ = "pyposude"
    id = db.Column(db.Integer, primary_key=True)
    ime_posude = db.Column(db.String(250), unique=True, nullable = False)
    slika_posude = db.Column(db.String)
    posadena_biljka = db.Column(db.String,db.ForeignKey("biljke.id")) # moze li se ovo povezati s ovako?

    def ispisi_podatke(self):
        print(f"ID={self.id}, ime posude = {self.ime_posude}, posadena biljka = {self.posadena_biljka}")

def spoji_se_na_bazu(ime_baze):
    """
    Glavna funkcija ovog modula
    Spaja se na bazu i kreria tablicu ako ne postoji
    """
    # Povezimo se s bazom koristeci SQLAlchemy
    db_engine = db.create_engine(f"sqlite:///{ime_baze}")

    # Kreiraj bazu sa tablicom koju smo deklarirali u klasi Korisnik(Biljke,PyPosude)
    # odnosno izvršit će SQL upit:
    """
        CREATE TABLE IF NOT EXISTS korisnici(biljke,pyposude) (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL, 
        );
    """
    Base.metadata.create_all(db_engine)

    # otvori konekciju koju ćemo koristiti za upite prema bazi
    Session = sessionmaker()
    Session.configure(bind=db_engine)
    session = Session()
    return session

class SQLAlchemyRepozitorij:

    def __init__(self, session):
        # ovo je session koji dobijemo nakon poziva funkcije spoji_se_na_bazu
        self.session = session

    # KORISNICI

    def create_user(self, user: Korisnik):
        """
        spremi objekt tipa Korisnik u bazu i vrati isti objekt natrag
        :param djelatnik: objekt tipa Korisnik
        :type djelatnik: Korisnik
        :return: Korisnik
        :rtype: Korisnik
        """

        # INSERT INTO Korisnik(id, name, password) VALUES(?, ?, ?)
        self.session.add(user)
        self.session.commit()
        return user

    def update_user(self, user):
        """
        promijeni objekt tipa Korisnik u bazi i vrati isti objekt natrag
        NE sprema se novi!
        """
        return self.create_user(user)

    def select_users_by_id(self, id):
        """
        SELECT * FROM Korisnik 
        WHERE ID = ? 
        LIMIT = 1
        """
        # ako nemamo u bazi zapisa koji ima ID = id, ovo vraća None!
        return self.session.query(Korisnik).filter_by(id=id).first()

    def get_user_by_username(self, username):
        # ako nemamo u bazi zapisa koji ima username = username, ovo vraća None!
        return self.session.query(Korisnik).filter(Korisnik.username==username).first()

    def get_all_users(self):
        for user in self.session.query(Korisnik).all():
            user.ispisi_podatke()

    def spoji_repozitorij_s_bazom(ime_baze):
        session = spoji_se_na_bazu(ime_baze)
        repozitorij = SQLAlchemyRepozitorij(session)
        return repozitorij

    def delete_user(self, id):
        user = self.select_users_by_id(id)
        if user:
            self.session.delete(user)
        self.session.commit()

    def delete_all_users(self):
         self.session.query(Korisnik).delete()
         self.session.commit()


    # BILJKE

    def spremi_biljku(self, biljka: Biljke):
        """
        spremi objekt tipa Biljke u bazu i vrati isti objekt natrag
        :param djelatnik: objekt tipa Biljke
        :type djelatnik: Biljke
        :return: Biljke
        :rtype: Biljke
        """
        self.session.add(biljka)
        self.session.commit()
        return biljka

    def azuriraj_biljkicu(self,biljka):
        """
        promijeni objekt tipa Biljke u bazi i vrati isti objekt natrag
        NE sprema se novi!
        Ovu metodu ne koristim
        """
        #return self.session.commit()
        return self.spremi_biljku(biljka)
    
    def azuriraj_biljku(self,ime_baze,ime_biljke,zalijevanje, mjesto,supstrat,id_biljke):
        """ ova metoda klase se najprije spaja na bazu i kada zavrsi svoju radnju,
        zatvara bazu pomocu opcije 'with';
        zatim ulazi u bazu i mijenja zadane parametre biljke na tom id-u
        pomocu podataka koje je unio korisnik na gui u prozoru 'prozor_azuriraj_biljku_iz_baze'
        """
        with spoji_se_na_bazu(ime_baze) as session:
            session.execute(TextClause(f"UPDATE biljke SET ime_biljke = '{ime_biljke}', zalijevanje='{zalijevanje}', mjesto='{mjesto}', supstrat='{supstrat}' WHERE id = {id_biljke}"))
            session.commit()

    # def konekcija_s_bazom(self,ime_baze):
    #     db_engine = db.create_engine(f"sqlite:///{ime_baze}")
    #     return db_engine

    def select_biljka_by_id(self, id):
        """
        SELECT * FROM Biljke 
        WHERE ID = ? 
        LIMIT = 1
        """
        # ako nemamo u bazi zapisa koji ima ID = id, ovo vraća None!
        return self.session.query(Biljke).filter_by(id=id).first()

    def get_biljka_by_ime(self, ime_biljke):
        # ako nemamo u bazi zapisa koji ima username = username, ovo vraća None!
        return self.session.query(Biljke).filter(Biljke.ime_biljke==ime_biljke).first()

    def get_all_biljke(self):
        for biljka in self.session.query(Biljke).all():
            biljka.ispisi_podatke()

    def delete_biljka(self, id):
        biljka = self.select_biljka_by_id(id)
        if biljka:
            self.session.delete(biljka)
        self.session.commit()

    def delete_all_biljke(self):
         self.session.query(Biljke).delete()
         self.session.commit()

    def koliko_biljaka_imamo_u_bazi(self):
        return self.session.query(Biljke).count()
    
    # PY POSUDE

    def spremi_posudu(self, posuda: PyPosude):
        """
        spremi objekt tipa PyPosude u bazu i vrati isti objekt natrag
        :param djelatnik: objekt tipa PyPosude
        :type djelatnik: PyPosude
        :return: PyPosude
        :rtype: PyPosude
        """

        self.session.add(posuda)
        self.session.commit()
        return posuda
    
    def select_posuda_by_id(self, id):
        """
        SELECT * FROM PyPosude 
        WHERE ID = ? 
        LIMIT = 1
        """
        # ako nemamo u bazi zapisa koji ima ID = id, ovo vraća None!
        return self.session.query(PyPosude).filter_by(id=id).first()
    
    def delete_posuda(self, id):
        posuda = self.select_posuda_by_id(id)
        if posuda:
            self.session.delete(posuda)
        self.session.commit()
    

def izbrisi_korisnika_iz_baze(repozitorij,session,id_korisnika):
    tablica_korisnika = session.execute(TextClause(f"SELECT * FROM Korisnici WHERE id = {id_korisnika}"))
    for korisnik in tablica_korisnika:
        if korisnik:
            repozitorij.delete_user(id=id_korisnika)
    

    # def spremi_biljku(self, biljka: Biljke):
    #     """
    #     spremi objekt tipa Employee u bazu i vrati isti objekt natrag
    #     :param djelatnik: objekt tipa Employee
    #     :type djelatnik: Employee
    #     :return: Employee
    #     :rtype: Employee
    #     """

    #     # INSERT INTO Employees(id, name, email) VALUES(?, ?, ?)
    #     self.session.add(biljka)
    #     self.session.commit()
    #     return biljka

    # def azuriraj_biljku(self, biljka):
    #     """
    #     promijeni objekt tipa Employee u bazi i vrati isti objekt natrag

    #     NE sprema se novi!

    #     :param djelatnik: objekt tipa Employee
    #     :type djelatnik: Employee
    #     :return: Employee
    #     :rtype: Employee
    #     """
    #     return self.spremi_biljku(biljka)

    # def select_biljka_by_id(self, id):
    #     """
    #     SELECT * FROM Korisnik 
    #     WHERE ID = ? 
    #     LIMIT = 1
    #     """
    #     # ako nemamo u bazi zapisa koji ima ID = id, ovo vraća None!
    #     return self.session.query(Biljke).filter_by(id=id).first()

    # def get_biljka_by_ime(self, ime_biljke):
    #     # ako nemamo u bazi zapisa koji ima username = username, ovo vraća None!
    #     return self.session.query(Biljke).filter(Biljke.ime_biljke==ime_biljke).first()

    # def get_all_biljke(self):
    #     for biljka in self.session.query(Biljke).all():
    #         biljka.ispisi_podatke()

    # def spoji_repozitorij_s_bazom(ime_baze):
    #     session = spoji_se_na_bazu(ime_baze)
    #     repozitorij2 = SQLAlchemyRepozitorijBiljke(session)
    #     return repozitorij2

    # def delete_biljka(self, id):
    #     biljka = self.select_biljka_by_id(id)
    #     if biljka:
    #         self.session.delete(biljka)
    #     self.session.commit()

    # def delete_all_biljke(self):
    #      self.session.query(Biljke).delete()
    #      self.session.commit()

    # def koliko_biljaka_imamo_u_bazi(self):
    #     return self.session.query(Biljke).count()

