import tkinter as tk
from tkinter import messagebox
import random

# Kaartide väärtused (2 kuni 11)
kaardid = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]  # 10 on kuningas, emand, poiss ja 11 on äss

# Mängija ja arvuti algsed väärtused
mängija_kaardid = []
arvuti_kaardid = []
mängija_summa = 0
arvuti_summa = 0

# Funktsioon juhusliku kaardi valimiseks
def loe_kaart():
    return random.choice(kaardid)

# Funktsioon mängija mängu algatamiseks
def alusta_mängu():
    global mängija_kaardid, arvuti_kaardid, mängija_summa, arvuti_summa

    mängija_kaardid = [loe_kaart(), loe_kaart()]
    arvuti_kaardid = [loe_kaart(), loe_kaart()]
    mängija_summa = sum(mängija_kaardid)
    arvuti_summa = sum(arvuti_kaardid)

    mängija_kaardid_tekst.set(f"Mängija kaardid: {mängija_kaardid} | Summa: {mängija_summa}")
    arvuti_kaardid_tekst.set(f"Arvuti kaardid: [{arvuti_kaardid[0]}, ?]")  # Näita ainult esimest kaarti
    mängu_seis.set("Mäng algas! Võta kaart või peatu.")

    # Nuppude olekud
    võta_kaart_btn.config(state="normal")
    peatu_btn.config(state="normal")
    vaata_ajalugu_btn.config(state="normal")

# Funktsioon mängija järgmise kaardi võtmiseks
def võta_kaart():
    global mängija_summa, mängija_kaardid

    kaart = loe_kaart()
    mängija_kaardid.append(kaart)
    mängija_summa = sum(mängija_kaardid)

    mängija_kaardid_tekst.set(f"Mängija kaardid: {mängija_kaardid} | Summa: {mängija_summa}")

    if mängija_summa > 21:
        mängu_seis.set("Kaotasite! Summa ületas 21.")
        lõpp_mäng()
    elif mängija_summa == 21:
        mängu_seis.set("Palju õnne! Sa jõudsid 21-ni.")
        lõpp_mäng()

# Funktsioon mängija peatamiseks ja arvuti mängu alustamiseks
def peatu():
    global arvuti_summa, arvuti_kaardid

    arvuti_kaardid_tekst.set(f"Arvuti kaardid: {arvuti_kaardid} | Summa: {arvuti_summa}")

    # Arvuti mängimine
    while arvuti_summa < 17:
        kaart = loe_kaart()
        arvuti_kaardid.append(kaart)
        arvuti_summa = sum(arvuti_kaardid)
        arvuti_kaardid_tekst.set(f"Arvuti kaardid: {arvuti_kaardid} | Summa: {arvuti_summa}")
        
    arvuta_tulemus()

# Funktsioon mängu tulemuse arvutamiseks
def arvuta_tulemus():
    global mängija_summa, arvuti_summa
    if arvuti_summa > 21:
        mängu_seis.set("Arvuti kaotas! Võitsite!")
        salvesta_tulemus("Võit")
    elif mängija_summa > arvuti_summa:
        mängu_seis.set("Võitsite!")
        salvesta_tulemus("Võit")
    elif mängija_summa < arvuti_summa:
        mängu_seis.set("Kaotasite! Arvuti võitis.")
        salvesta_tulemus("Kaotus")
    else:
        mängu_seis.set("Viik!")
        salvesta_tulemus("Viik")
    
    lõpp_mäng()

# Funktsioon mängu lõppemiseks
def lõpp_mäng():
    # Nuppude olekud
    võta_kaart_btn.config(state="disabled")
    peatu_btn.config(state="disabled")

# Funktsioon mängu tulemuse salvestamiseks faili
def salvesta_tulemus(tulemus):
    mängija_nimi = nimi_sisend.get()
    if not mängija_nimi:
        mängija_nimi = "Tundmatu"

    try:
        with open("tulemused.txt", "a") as f:
            f.write(f"{mängija_nimi}: {tulemus} | Mängija summa: {mängija_summa} | Arvuti summa: {arvuti_summa}\n")
    except Exception as e:
        messagebox.showerror("Viga", f"Tulemuste salvestamisel tekkis viga: {e}")

# Funktsioon mänguajaloost tulemuste kuvamiseks
def näita_ajalugu():
    try:
        with open("tulemused.txt", "r") as f:
            ajalugu = f.readlines()
            ajalugu_tekst.set("Mänguajalugu:\n" + "".join(ajalugu))
    except FileNotFoundError:
        ajalugu_tekst.set("Mänguajalugu puudub.")

# GUI loomine
root = tk.Tk()
root.title("Mäng 21")
root.geometry("600x500")
root.config(bg="#2d3b4e")

# Erilised muutujad GUI jaoks
mängija_kaardid_tekst = tk.StringVar()
arvuti_kaardid_tekst = tk.StringVar()
mängu_seis = tk.StringVar()
ajalugu_tekst = tk.StringVar()

# Mängija nimi sisend
nimi_label = tk.Label(root, text="Sisesta oma nimi:", font=("Arial", 12), bg="#2d3b4e", fg="#ffffff")
nimi_label.pack(pady=5)

nimi_sisend = tk.Entry(root, font=("Arial", 14), bg="#ffffff", fg="#000000")
nimi_sisend.pack(pady=5)

# Mängu alguse nupud ja tulemused
mängu_seis_label = tk.Label(root, textvariable=mängu_seis, font=("Arial", 14), bg="#2d3b4e", fg="#ffffff")
mängu_seis_label.pack(pady=5)

mängija_kaardid_label = tk.Label(root, textvariable=mängija_kaardid_tekst, font=("Arial", 12), bg="#2d3b4e", fg="#ffffff")
mängija_kaardid_label.pack(pady=5)

arvuti_kaardid_label = tk.Label(root, textvariable=arvuti_kaardid_tekst, font=("Arial", 12), bg="#2d3b4e", fg="#ffffff")
arvuti_kaardid_label.pack(pady=5)

# Nupud
alusta_btn = tk.Button(root, text="Alusta mängu", font=("Arial", 12), bg="#4caf50", fg="#ffffff", command=alusta_mängu)
alusta_btn.pack(pady=10)

võta_kaart_btn = tk.Button(root, text="Võta kaart", font=("Arial", 12), bg="#4caf50", fg="#ffffff", command=võta_kaart, state="disabled")
võta_kaart_btn.pack(pady=10)

peatu_btn = tk.Button(root, text="Peatu", font=("Arial", 12), bg="#f44336", fg="#ffffff", command=peatu, state="disabled")
peatu_btn.pack(pady=10)

vaata_ajalugu_btn = tk.Button(root, text="Vaata ajalugu", font=("Arial", 12), bg="#2196f3", fg="#ffffff", command=näita_ajalugu)
vaata_ajalugu_btn.pack(pady=10)

# Mängu ajalugu kuvamine
ajalugu_label = tk.Label(root, textvariable=ajalugu_tekst, font=("Arial", 12), bg="#2d3b4e", fg="#ffffff")
ajalugu_label.pack(pady=10)

root.mainloop()

