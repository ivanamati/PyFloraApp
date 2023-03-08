from SQLAlchemy_seminarski_repo import Biljke, SQLAlchemyRepozitorij, spoji_se_na_bazu
from PIL import ImageTk, Image, ImageFilter

def spremi_biljku_u_bazu(repozitorij):
    zeljena_biljka = input("Unesite ime biljke: ")
    putanja_do_biljke = input("Unesite naziv fotografije: ")

    moja_biljka = Biljke(ime_biljke = zeljena_biljka, slika_biljke= putanja_do_biljke)

    repozitorij.spremi_biljku(moja_biljka)

# def spremi_novu_biljku_u_bazu(repozitorij, ime_nove_biljke, odabrana_slika):
#     """odabrana slika bi trebala biti ona odabrana slika iz  filea, a ime nove biljke self.ime_nove_biljke.get()"""
#     moja_nova_biljka = Biljke(ime_biljke = ime_nove_biljke, slika_biljke= odabrana_slika)

#     repozitorij.spremi_biljku(moja_nova_biljka)


def pokreni_aplikaciju(ime_baze):
    # s ova dva reda ispod se spajamo na bazu i povezujemo s repozitorijem
    session = spoji_se_na_bazu(ime_baze)
    repozitorij = SQLAlchemyRepozitorij(session)
    #repozitorij.delete_all_biljke()
    #repozitorij.delete_biljka(8)
    #repozitorij.delete_biljka(4)
    repozitorij.delete_biljka(5)


    #spremi_biljku_u_bazu(repozitorij)
    print('*'*50)
    print('Ovo su trenutne slike u bazi: ')
    repozitorij.get_all_biljke()
    #repozitorij.delete_all_biljke()


# ovime se postiže da se kod importa ovog modula ne izvodi ništa
if __name__ == "__main__":
    pokreni_aplikaciju("SQLite_Baza_PyFlora.sqlite")
