from tkinter import *
from tkinter import messagebox

from PolovniBackend import Automobil

def ucitajAutomobile():
    automobiliLista = []
    with open('automobili.txt', 'r') as f:
        for linija in f:
            splituj = linija.strip().split('|')
            if len(splituj) == 4:
                ispisiAutomobile = Automobil(splituj[0], splituj[1], splituj[2], splituj[3])
                automobiliLista.append(ispisiAutomobile)
    return automobiliLista

def prikazi_automobile():
    prikaz_auta = ucitajAutomobile()
    for i in prikaz_auta:
        lista_automobila.insert(END, str(i))

def filtriraj_automobile():
    try:
        marka = entrypregledAuta_marka.get().strip().capitalize()
        model = entrypregledAuta_model.get().strip().capitalize()
        godiste = entrypregledAuta_godiste.get().strip().capitalize()

        min_price = float(entry_filter_od.get()) if entry_filter_od.get().strip() != "" else None
        max_price = float(entry_filter_do.get()) if entry_filter_do.get().strip() != "" else None
    except ValueError:
        messagebox.showerror("Greška", "Unesite validne vrednosti za cene.")
        return

    lista_automobila.delete(0, END)

    prikaz_auta = ucitajAutomobile()
    for auto in prikaz_auta:
        if ((marka == "" or auto.marka.capitalize() == marka) and
                (model == "" or auto.model.capitalize() == model) and
                (godiste == "" or auto.godiste.capitalize() == godiste) and
                (min_price is None or min_price <= float(auto.cena)) and
                (max_price is None or float(auto.cena) <= max_price)):
            lista_automobila.insert(END, str(auto))

def otvori_novi_prozor_za_dodavanje():
    global entry_dodaj_marka, entry_dodaj_model, entry_dodaj_godiste, entry_dodaj_cena

    novi_prozor = Toplevel(root)
    novi_prozor.title("Dodaj Novi Automobil")
    novi_prozor.geometry("400x400")
    novi_prozor['bg'] = 'black'

    Label(novi_prozor, text="Dodaj Automobil", bg="darkgray", fg='blue', width=30, height=2).pack(pady=10)

    # Entry za dodavanje automobila po marki
    entry_dodaj_marka = Entry(novi_prozor)
    entry_dodaj_marka.pack(pady=10)
    entry_dodaj_marka.insert(0, "Marka")

    # Entry za dodavanje automobila po modelu
    entry_dodaj_model = Entry(novi_prozor)
    entry_dodaj_model.pack(pady=10)
    entry_dodaj_model.insert(0, "Model")

    # Entry za dodavanje automobila po godištu
    entry_dodaj_godiste = Entry(novi_prozor)
    entry_dodaj_godiste.pack(pady=10)
    entry_dodaj_godiste.insert(0, "Godište")

    # Entry za dodavanje automobila po ceni
    entry_dodaj_cena = Entry(novi_prozor)
    entry_dodaj_cena.pack(pady=10)
    entry_dodaj_cena.insert(0, "Cena")

    Button(novi_prozor, text="Dodaj", command=lambda: dodaj_auta(novi_prozor)).pack(pady=10)

def dodaj_auta(novi_prozor):
    try:
        marka = entry_dodaj_marka.get().strip()
        model = entry_dodaj_model.get().strip()
        godiste = entry_dodaj_godiste.get().strip()
        cena = entry_dodaj_cena.get().strip()

        if marka and model and godiste and cena:
            novi_auto = f"{marka}|{model}|{godiste}|{cena}"
            with open('automobili.txt', 'a') as f:
                f.write(novi_auto + "\n")

            lista_automobila.insert(END, novi_auto)
            lista_automobila.itemconfig(lista_automobila.size() - 1, {'fg': 'red'})

            entry_dodaj_marka.delete(0, END)
            entry_dodaj_model.delete(0, END)
            entry_dodaj_godiste.delete(0, END)
            entry_dodaj_cena.delete(0, END)

            novi_prozor.destroy()  # Zatvara prozor nakon dodavanja automobila
        else:
            messagebox.showerror("Greška", "Unesite validne podatke za automobil.")
    except Exception as e:
        messagebox.showerror("Greška", "Desila se neka čudna greška!")

def obrisi_auto():
    try:
        selektovan = lista_automobila.curselection()
        if not selektovan:
            messagebox.showerror("Greška", "Selektujte automobil za brisanje.")
            return

        auto_za_brisanje = lista_automobila.get(selektovan)

        automobili = ucitajAutomobile()
        automobili = [auto for auto in automobili if str(auto) != auto_za_brisanje]

        with open('automobili.txt', 'w') as f:
            for auto in automobili:
                f.write(f"{auto.marka}|{auto.model}|{auto.godiste}|{auto.cena}\n")

        lista_automobila.delete(selektovan)
    except Exception as e:
        messagebox.showerror("Greška", f"Desila se neka čudna greška: {e}")

root = Tk()
root['bg'] = 'black'
root.title("Polovni Automobili")
root.geometry('1000x1000')

# Frame za listu automobila (leva strana)
frame_leva_strana = Frame(root, bg='black')
frame_leva_strana.pack(side=LEFT, padx=30, pady=40)

#========= Postavljanje listbox-a========
lista_automobila = Listbox(frame_leva_strana, width=90, height=30, font=('Arial', 10))
lista_automobila.pack()

# Dugme za brisanje automobila
dugme_obrisi = Button(frame_leva_strana, text="Obriši Selektovani Automobil", command=obrisi_auto)
dugme_obrisi.pack(pady=10)

# ==================DESNO=======================

# Frame za unos polja (desna strana)
frame_desna_strana = Frame(root, bg='darkgray')
frame_desna_strana.pack(side=LEFT, padx=50, pady=20)

# Pregled auta Labela
pregledAuta_label = Label(frame_desna_strana, text="Pregled Ponude Automobila", bg='#ABABAB', fg='blue', width=30, height=2)
pregledAuta_label.pack()

# Entry za pregled automobila po marki
entrypregledAuta_marka = Entry(frame_desna_strana)
entrypregledAuta_marka.pack()
entrypregledAuta_marka.insert(0, "Marka")

# Entry za pregled automobila po modelu
entrypregledAuta_model = Entry(frame_desna_strana)
entrypregledAuta_model.pack()
entrypregledAuta_model.insert(0, "Model")

# Entry za pregled automobila po godištu
entrypregledAuta_godiste = Entry(frame_desna_strana)
entrypregledAuta_godiste.pack()
entrypregledAuta_godiste.insert(0, "Godište")

#----------- Dugme za filtriranje po marki/modelu/godištu i ceni-------------
dugme_prikazi = Button(frame_desna_strana, text="Filtriraj", command=filtriraj_automobile)
dugme_prikazi.pack(pady=10)

# ===========================CENA FILTER=============================

filterCene_label = Label(frame_desna_strana, text="Filtriraj cenu", bg="#ABAB99", fg='blue', width=30, height=2)
filterCene_label.pack()

# Entry za minimalnu cenu
entry_filter_od = Entry(frame_desna_strana)
entry_filter_od.pack(pady=10)
entry_filter_od.insert(0, "Od")

# Entry za maksimalnu cenu
entry_filter_do = Entry(frame_desna_strana)
entry_filter_do.pack(pady=10)
entry_filter_do.insert(0, "Do")

dodajLabel = Label(frame_desna_strana, text="Dodaj Automobil", bg="#ABAB99", fg='blue', width=30, height=2)
dodajLabel.pack()

# Dugme za otvaranje novog prozora za dodavanje automobila
dugme_otvori_prozor = Button(frame_desna_strana, text="Dodaj Novi Automobil", command=otvori_novi_prozor_za_dodavanje)
dugme_otvori_prozor.pack(pady=10)

# ----------Poziv funkcije za prikaz automobila--------------#
prikazi_automobile()

root.mainloop()
