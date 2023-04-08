from PYFlora_baza_repozitorij import SQLAlchemyRepozitorij, spoji_se_na_bazu
from gui_app import PyFlora

session = spoji_se_na_bazu("SQLalchemy_PyFlora_Baza.sqlite")
repozitorij = SQLAlchemyRepozitorij(session)

if __name__ == "__main__":
    gui_program = PyFlora(repozitorij=repozitorij)
    gui_program.pokreni()

    gui_program.prozor_prikaz_biljaka_PyPosuda()
    #gui_program.dodajte_novu_biljku_iz_foldera()
    #gui_program.naslovnica()
    #gui_program.nacrtaj_prvi_prozor_login()
    #gui_program.prozor_ulaska_login_ili_registracija()
    #gui_program.nacrtaj_treci_prozor_moj_profil()
    #gui_program.prozor_moji_podaci()
    #gui_program.prozor_prikaz_korisnika()
    #gui_program.prozor_prikaz_posuda_PyPosuda()
    gui_program.root.mainloop()