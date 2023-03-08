import requests

from seminarski_repo_veza import (
    Author,
    Blog,
    SQLAlchemyRepo,
    spoji_se_na_bazu,
)

BLOGS_URL = "https://jsonplaceholder.typicode.com/posts"
USERS_URL = "https://jsonplaceholder.typicode.com/users"


def dohvati_podatke_s_urla(url):
    """ ova metoda dohvaca podatke s weba """
    try: 
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            # dobili smo listu dictova
            json_s_weba = response.json()
        else:
            json_s_weba = []
    except Exception:
        print("Ooooops!!!")
    return json_s_weba


def kreiraj_autora_koji_ne_postoji(repozitorij, korisnik):
    author = repozitorij.get_author_by_id(korisnik.id)
    if not author:
        author = repozitorij.create_author(korisnik)
    #else:
        #print(f"Author postoji u bazi:")
    #author.ispisi_podatke()


def kreiraj_blog_koji_ne_postoji(repozitorij, blog_post):
    blog = repozitorij.get_blog_by_id(blog_post.id)
    if not blog:
        author = repozitorij.get_author_by_id(blog_post.author_id)
        if not author:
            print(f"No author found in database with id {blog_post.author_id}")
            return
        else:
            blog = repozitorij.add_blog(blog_post)
    #blog.ispisi_podatke()


def pokupi_autore(repozitorij):
    for korisnik in dohvati_podatke_s_urla(USERS_URL):
        kreiraj_autora_koji_ne_postoji(
            repozitorij,
            Author(id=korisnik["id"], name=korisnik["name"], email=korisnik["email"])
        )


def pokupi_blogove(repozitorij):
    for blog in dohvati_podatke_s_urla(BLOGS_URL):
        kreiraj_blog_koji_ne_postoji(
            repozitorij,
            Blog(id=blog["id"], title=blog["title"], body=blog["body"], author_id=blog["userId"])
        )


def ispisi_podatke_iz_baze(repozitorij):
    print("Svi autori u bazi:")
    for author in repozitorij.select_all_authors():
        print("Autor: ")
        author.ispisi_podatke()
        print("Njegovi blogovi: ")
        for blog in repozitorij.get_blogs_for_author(author.id):
            blog.ispisi_podatke()


def main(ime_baze):
    session = spoji_se_na_bazu(ime_baze)
    repozitorij = SQLAlchemyRepo(session)
    pokupi_autore(repozitorij)
    pokupi_blogove(repozitorij)
    print('proba... spojili smo se na bazu, dohvatili podatke i upisali ih u "SQLite_Baza_PyFlora.sqlite"')
    
    #ispisi_podatke_iz_baze(repozitorij)
 # tu zakomentirati printom da vidimo da prvi put samo dohvaca, napisat ce da ih nema u bazi,  a drugi put cemo ih vidjeti!

    # blog = repozitorij.get_blog_by_id(8)
    # blog.ispisi_podatke()
    # blog.author.ispisi_podatke()

    # OVAJ .author je onaj author iz backref=backref(author)
    #blog.author.ispisi_podatke()

    # autor = repozitorij.get_author_by_id(8)
    # print("Autor")
    # autor.ispisi_podatke()
    # print(f"Autor ima {len(autor.blogs)} blogova")
    # print("Ovo su njegovi blogovi: ")
    # for blog in autor.blogs[-2:]:  # -2: daje zadnja dva jer su blogs liste
    #     blog.ispisi_podatke()
    #     # a sada magija!
    #     print("I OPET AUTOR!!!")
    #     blog.ispisi_podatke_autora()


if __name__ == "__main__":
    main("SQLite_Baza_PyFlora.sqlite")
    


# ZADATAK:
# napravi button na trecem screenu GUI kad se klikne sync(!) da se dohvati podaci s weba i spreme u bazu

# BONUS zadatak
# nakon toga prikazati podatke na GUI !!!!

# ZADATAK za napredne
# robots.txt
# dohvati ovaj file i isparsiraj ga
# if line starts with sitemap (pa nesto get...)