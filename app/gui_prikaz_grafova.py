import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PyFlora_simulator_senzora import dohvati_podatke_sa_senzora

### OVAJ SE MODUL KORISTI OBRADU PODATAKA SA SENZORA TE CRTANJE GRAFOVA U GUI-u


def obradi_i_pivotiraj_podatke():
    """ova funkcija dohvaca podatke sa senzora
    te ih pivotira prema dohvatu vremena za obradu i prikaz grafova;
    funkcija vraca te pivotirane podatke"""

    podaci = dohvati_podatke_sa_senzora()
    df = pd.DataFrame(podaci)
    df["vrijeme dohvata"] = pd.to_datetime(
        df["vrijeme dohvata"], format="%Y-%m-%d %H:%M"
    )
    pivoted_df = df.pivot(
        index="vrijeme dohvata", columns="ime senzora", values="vrijednost"
    )
    return pivoted_df


def obradi_dohvacene_podatke_i_nacrtaj_line_chart_graf(root, title):
    """ova se funkcija koristi u gui_app za obradu podataka dobivenih s rasberry_pi
    te crtanje grada bas u samom GUI prozoru"""
    pivoted_df = obradi_i_pivotiraj_podatke()

    # Stvaranje figur4
    fig = Figure(figsize=(6, 6), dpi=80)
    # Dodavanje subplot-a na figure
    plot1 = fig.add_subplot(132)
    # Prikazivanje podataka na subplot-u
    pivoted_df.plot(
        kind="area", ax=plot1, subplots=True, title=title, ylabel="vrijednost"
    )
    # Stvaranje canvas-a za tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    # Prikazivanje canvas-a
    canvas.get_tk_widget().place(anchor="center", relx=0.5, rely=0.4)


def obradi_dohvacene_podatke_i_nacrtaj_graf_histogram(root, title):
    """ova se funkcija koristi u gui_app za obradu podataka dobivenih s rasberry_pi
    te crtanje grada bas u samom GUI prozoru"""

    pivoted_df = obradi_i_pivotiraj_podatke()

    # Stvaranje figur4
    fig = Figure(figsize=(6, 5), dpi=90, layout="constrained")
    # Dodavanje subplot-a na figure
    plot1 = fig.add_subplot(132)
    # Prikazivanje podataka na subplot-u
    pivoted_df.plot(ax=plot1, subplots=True, title=title)

    plot2 = fig.add_subplot(131)
    pivoted_df.hist(ax=plot2)
    # Stvaranje canvas-a za tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()

    # Prikazivanje canvas-a
    canvas.get_tk_widget().place(anchor="center", relx=0.5, rely=0.4)


def obradi_dohvacene_podatke_i_nacrtaj_treci_graf(root, title):
    """ova se funkcija koristi u gui_app za obradu podataka dobivenih s rasberry_pi
    te crtanje grada bas u samom GUI prozoru"""
    pivoted_df = obradi_i_pivotiraj_podatke()

    # Stvaranje figur4
    fig = Figure(figsize=(6.5, 4), dpi=90, layout="constrained")
    # Dodavanje subplot-a na figure
    plot1 = fig.add_subplot(132)
    # Prikazivanje podataka na subplot-u
    pivoted_df.plot(kind="box", ax=plot1, subplots=True, title=title)
    # Stvaranje canvas-a za tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    # Prikazivanje canvas-a
    canvas.get_tk_widget().place(anchor="center", relx=0.5, rely=0.4)

""" prilikom prikaza grafova na GUI, dobiva se slijedeća obavijest u terminalu: 
    UserWarning: To output multiple subplots, the figure containing the passed axes is being cleared.
    pivoted_df.plot(kind="box", ax=plot1, subplots=True, title=title);
    ovo nije greška, nego informacija na to što se događa iza kulisa prilikom crtanja grafova s više potgrafova;
    budući da se svaki potgrafikon crta u zasebnom polju, postojeća slika se mora obrisati prije iscrtavanja novog grafa"""
