import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, sessionmaker

Base = declarative_base()


class Author(Base):
    __tablename__ = "autor"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)

    # tu SQLAlchemy radi: nađi mi sve podatke u tablici "blog" i tu mi stavi objekte
    # tipa Blog
    # što onda znači da je blogs LISTA objekata tipa Blog
    # SQLAlchemy će još k tome u objekt tipa Blog dodati atribut author koji je OBJEKT ovog tipa

    blogs = relationship("Blog", backref=backref("author"))
    # ovo je lista jer smo povezali blog i autora, na taj nacin da jedan autor (zbog foreignkey u klasi blog) ima vise blogova, koji su automatski u listi

    def ispisi_podatke(self):
        print(f"ID={self.id}, Name={self.name}, email={self.email}")


class Blog(Base):
    __tablename__ = "blog"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey("autor.id"))

    def ispisi_podatke(self):
        print(f"ID={self.id}, title={self.title}, body={self.body}")

    def ispisi_podatke_autora(self):
        # OVAJ .author je onaj author iz backref=backref("author")
        self.author.ispisi_podatke()


def spoji_se_na_bazu(ime_baze):
    """
    Glavna funkcija ovog modula

    Spaja se na bazu i kreria tablicu ako ne postoji

    """
    # Povezimo se s bazom koristeci SQLAlchemy
    db_engine = db.create_engine(f"sqlite:///{ime_baze}")

    # Kreiraj bazu sa tablicom koju smo deklarirali u klasi Employee
    Base.metadata.create_all(db_engine)

    # otovri konekciju koju ćemo koristiti za upite prema bazi
    Session = sessionmaker()
    Session.configure(bind=db_engine)
    session = Session()
    return session


class SQLAlchemyRepo:

    def __init__(self, session):
        # ovo je session koji dobijemo nakon poziva funkcije spoji_se_na_bazu
        self.session = session

    def get_author_by_id(self, author_id):
        return self.session.query(Author).filter_by(id=author_id).one_or_none()

    def get_author_by_email(self, author_email):
        return self.session.query(Author).filter_by(email=author_email).one_or_none()

    def create_author(self, author):
        self.session.add(author)
        self.session.commit()
        return author

    def get_blogs_for_author(self, author_id):
        return self.session.query(Blog).filter(Blog.author_id==author_id).all()

    def select_all_authors(self):
        return self.session.query(Author).all()

    def add_blog(self, blog):
        self.session.add(blog)
        self.session.commit()
        return blog

    def get_blog_by_id(self, blog_id):
        return self.session.query(Blog).filter_by(id=blog_id).one_or_none()