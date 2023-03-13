from enum import unique
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
    #slika_biljke = db.Column(db.BLOB)

    def ispisi_podatke(self):
        print(f"ID={self.id}, naziv_biljke = {self.ime_biljke}, putanja do slike = {self.slika_biljke}") 

def spoji_se_na_bazu(ime_baze):
    """
    Glavna funkcija ovog modula
    Spaja se na bazu i kreria tablicu ako ne postoji
    """
    # Povezimo se s bazom koristeci SQLAlchemy
    db_engine = db.create_engine(f"sqlite:///{ime_baze}")

    # Kreiraj bazu sa tablicom koju smo deklarirali u klasi Korisnik
    # odnosno izvršit će SQL upit:
    """
        CREATE TABLE IF NOT EXISTS Korisnici (
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

    def create_user(self, user: Korisnik):
        """
        spremi objekt tipa Employee u bazu i vrati isti objekt natrag
        :param djelatnik: objekt tipa Employee
        :type djelatnik: Employee
        :return: Employee
        :rtype: Employee
        """

        # INSERT INTO Employees(id, name, email) VALUES(?, ?, ?)
        self.session.add(user)
        self.session.commit()
        return user

    def update_user(self, user):
        """
        promijeni objekt tipa Employee u bazi i vrati isti objekt natrag

        NE sprema se novi!

        :param djelatnik: objekt tipa Employee
        :type djelatnik: Employee
        :return: Employee
        :rtype: Employee
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

    def spremi_biljku(self, biljka: Biljke):
        """
        spremi objekt tipa Employee u bazu i vrati isti objekt natrag
        :param djelatnik: objekt tipa Employee
        :type djelatnik: Employee
        :return: Employee
        :rtype: Employee
        """

        # INSERT INTO Employees(id, name, email) VALUES(?, ?, ?)
        self.session.add(biljka)
        self.session.commit()
        return biljka

    def azuriraj_biljku(self, biljka):
        """
        promijeni objekt tipa Employee u bazi i vrati isti objekt natrag

        NE sprema se novi!

        :param djelatnik: objekt tipa Employee
        :type djelatnik: Employee
        :return: Employee
        :rtype: Employee
        """
        return self.spremi_biljku(biljka)

    def select_biljka_by_id(self, id):
        """
        SELECT * FROM Korisnik 
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

    def spoji_repozitorij_s_bazom(ime_baze):
        session = spoji_se_na_bazu(ime_baze)
        repozitorij2 = SQLAlchemyRepozitorijBiljke(session)
        return repozitorij2

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



    

# class Biljke(Base):
#     __tablename__ = "biljke"
#     id = db.Column(db.Integer, primary_key=True)
#     ime_biljke = db.Column(db.String(250), unique=True, nullable = False)
#     slika_biljke = db.Column(db.String)

#     # treba li jos nesto?

#     def ispisi_podatke(self):
#         print(f"ID={self.id}, naziv_biljke = {self.ime_biljke}, putanja do slike = {self.slika_biljke}") 

# def spoji_se_na_bazu(ime_baze):
#     """
#     Glavna funkcija ovog modula
#     Spaja se na bazu i kreria tablicu ako ne postoji
#     """
#     # Povezimo se s bazom koristeci SQLAlchemy
#     db_engine = db.create_engine(f"sqlite:///{ime_baze}")

#     # Kreiraj bazu sa tablicom koju smo deklarirali u klasi Korisnik
#     # odnosno izvršit će SQL upit:
#     """
#         CREATE TABLE IF NOT EXISTS Korisnici (
#             id INTEGER PRIMARY KEY,
#             username TEXT NOT NULL UNIQUE,
#             password TEXT NOT NULL, 
#         );
#     """
#     Base.metadata.create_all(db_engine)

#     # otvori konekciju koju ćemo koristiti za upite prema bazi
#     Session = sessionmaker()
#     Session.configure(bind=db_engine)
#     session = Session()
#     return session

class SQLAlchemyRepozitorijBiljke:

    def __init__(self, session):
        # ovo je session koji dobijemo nakon poziva funkcije spoji_se_na_bazu
        self.session = session

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

