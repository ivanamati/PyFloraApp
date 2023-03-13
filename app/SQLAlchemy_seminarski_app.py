from SQLAlchemy_seminarski_repo import Korisnik, Biljke, SQLAlchemyRepozitorij, spoji_se_na_bazu

def kreiraj_korisnika(repozitorij):
    korisnicko_ime = input("Unesite ime korisnika: ")
    lozinka = input ("Unesite lozinku: ")
    user = Korisnik(username = korisnicko_ime, password = lozinka)
    repozitorij.create_user(user)

def spremi_biljku_u_bazu(repozitorij):
    zeljena_biljka = input("Unesite ime biljke: ")
    putanja_do_biljke = input("Unesite naziv fotografije: ")

    moja_biljka = Biljke(ime_biljke = zeljena_biljka, slika_biljke= putanja_do_biljke)

    repozitorij.spremi_biljku(moja_biljka)

def kreiraj_korisnika_koji_ne_postoji(repozitorij):
    korisnicno_ime = input("Unesi korisnicko ime: ")
    user = repozitorij.get_user_by_username(korisnicno_ime)
    if not user:
        lozinka = input ("Unesite lozinku: ")
        user = Korisnik(
            username=korisnicno_ime,
            password=lozinka
        )
        #user.ispisi_podatke()
        # tek nakon poziva ove metode imamo objekt u BAZI
        print("Upisujemo korisnika...")
        repozitorij.create_user(user)
    else:
        print(f"Djelatnik sa korisnickim imenom '{korisnicno_ime.upper()}' postoji u bazi")
        #promijenimo_mail_zaposlenika(djelatnik, repozitorij)
    print("Podaci upisanog korisnika su: ", end='')
    user.ispisi_podatke()
    return user

def promijenimo_korisnicko_ime(user, repozitorij):
    ime = input(f"U koje ime želimo promijeniti ime korisnika {user.username}: ")
    # promijenimo mu ime
    user.username = ime
    repozitorij.update_user(user)

def promijenimo_lozinku_korisnika(user, repozitorij):
    lozinka = input(f"Unesite lozinku koju želite promijeniti {user.password}")
    user.password = lozinka
    repozitorij.update_user(user) 


def pokreni_aplikaciju(ime_baze):
    # s ova dva reda ispod se spajamo na bazu i povezujemo s repozitorijem
    session = spoji_se_na_bazu(ime_baze)
    repozitorij = SQLAlchemyRepozitorij(session)

    #repozitorij.delete_user(11)
    # while True:
    #     print('*'*50)
    #     print('Ovo su trenutni korisnici u bazi: ')
    #     repozitorij.get_all_users()
    #     kreiraj_korisnika(repozitorij)

    #     novi_korisnik = input("Zelite li unijeti novoga, odaberite da za nastavak ")
    #     if novi_korisnik == "ne":
    #         break


    #repozitorij.delete_biljka(4)
    #print('*'*50)
    #print('Ovo su trenutni korisnici u bazi: ')
    #repozitorij.get_all_users()
    #kreiraj_korisnika(repozitorij)


    #spremi_biljku_u_bazu(repozitorij)
    # print('*'*50)
    # print('Ovo su trenutne slike u bazi: ')
    # repozitorij.get_all_biljke()

    #print("Sad ćemo provjeriti korisnika:")
    #kreiraj_korisnika_koji_ne_postoji (repozitorij)

    #repozitorij.delete_all_users()
    #repozitorij.delete_user(4) # ovime sam izbrisala usera pod id-em 10



# ovime se postiže da se kod importa ovog modula ne izvodi ništa
if __name__ == "__main__":
    pokreni_aplikaciju("SQL_PyFlora_Baza.sqlite")
