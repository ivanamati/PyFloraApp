from SQLAlchemy_seminarski_repo import SQLAlchemyRepozitorij, spoji_se_na_bazu
from PyFlora_ttk_app import PyFlora

session = spoji_se_na_bazu("SQL_PyFlora_Baza.sqlite")
repozitorij = SQLAlchemyRepozitorij(session)

if __name__ == "__main__":
    gui_program = PyFlora(repozitorij=repozitorij)
    #gui_program.pokreni()
    gui_program.nacrtaj_treci_prozor_moj_profil()
    gui_program.root.mainloop()