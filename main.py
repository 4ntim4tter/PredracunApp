import csv
import os
import tkinter as tk
from ttkwidgets import autocomplete
from tkinter import ttk
from tkinter import messagebox

#stored data from files
DUPLICATE_CHECK_DATA = []
NAME_AUTO_COMPLETE = []
REG_BROJ_COMPLETE = []
CUSTOMER_DATA = []

#check if data file exists, create new file if not
if os.path.isfile("data.csv"):
    pass
else:
    with open("data.csv", "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ime", "vozilo", "reg_broj"])
        
def create_new_customer(name:str, car:str, reg_broj:str):
    with open("data.csv", "a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([name.strip().capitalize(), car.strip().capitalize(), reg_broj.strip().upper()])

#FIND CUSTOMER ADD NEW WORK TO EXISTING WORK FILE
def find_customer_window(master_window, CUSTOMER_DATA, NAME_AUTO_COMPLETE, REG_BROJ_COMPLETE):
      
    def get_name(event):
        if name_combo.focus_get():
            customer = next(item for item in CUSTOMER_DATA if item["ime"] == name_combo.get().capitalize())
            car_combo.set(customer["vozilo"])
            reg_combo.set(customer["reg_broj"])
            
    def get_reg_broj(event):
        if reg_combo.focus_get():
            customer = next(item for item in CUSTOMER_DATA if item["reg_broj"] == reg_combo.get().upper())
            name_combo.set(customer["ime"])
            car_combo.set(customer["vozilo"])
    
    frame = tk.Toplevel(master_window)
    frame.title("Pretraga Mušterije")
    frame.pack_propagate()
     
    #Ime i prezime label and combobox
    ttk.Label(frame, font=("Arial", 14, "bold"), text="Ime i Prezime").pack(side='top')
    name_combo = autocomplete.AutocompleteCombobox(frame, width=20, completevalues=NAME_AUTO_COMPLETE, font=("Arial", 14))
    name_combo.pack(side='top')
    name_combo.bind("<Return>", get_name)
    
    #Vozilo label and combobox
    ttk.Label(frame, font=("Arial", 14, "bold"), text="Vozilo").pack(side='top')
    car_combo = autocomplete.AutocompleteCombobox(frame, width=20, font=("Arial", 14))
    car_combo.pack(side='top')
    
    #Registracija label and combobox
    ttk.Label(frame, font=("Arial", 14, "bold"), text="Reg. Broj").pack(side='top')
    reg_combo = autocomplete.AutocompleteCombobox(frame, width=20, completevalues=REG_BROJ_COMPLETE, font=("Arial", 14))
    reg_combo.pack(side='top')
    reg_combo.bind("<Return>", get_reg_broj)
    
    #Repair list, listbox, scrollbar
    listbox_frame = tk.Frame(frame)
    listbox_frame.pack(side='top', expand=True, fill='both')
    
    repair_listbox = tk.Listbox(listbox_frame, width=29, height=10, font=("Arial", 12))
    repair_listbox.pack(side='left', fill='both', expand=True)
    
    scrollbar = tk.Scrollbar(listbox_frame, orient='vertical', command=repair_listbox.yview)
    scrollbar.pack(side='right', fill='y')
    
    repair_listbox.config(yscrollcommand=scrollbar.set)
    
    for char in range(25):
        repair_listbox.insert(char, "test" + str(char))

#ADD CUSTOMER AND CREATE WORK DATA FILE
def add_customer_window(master_window):
    def add_to_csv():
        if name_add_text.get() == '' or car_add_text.get() == '' or reg_add_text.get() == '':
            messagebox.showwarning("Upozorenje!", "Jedno ili više polja je prazno!")
            return None
        
        if f"{name_add_text.get().capitalize()},{car_add_text.get().capitalize()},{reg_add_text.get().upper()}" in DUPLICATE_CHECK_DATA:
            messagebox.showwarning("Upozorenje!", "Korisnik i Registracija već postoje u bazi podataka.")
            return None

        #update cache variables and data for new user real time
        create_new_customer(name_add_text.get(),car_add_text.get(), reg_add_text.get())
        messagebox.showinfo("Uspjeh", "Nova mušterija dodana.")
        DUPLICATE_CHECK_DATA.append(f"{name_add_text.get()},{car_add_text.get()},{reg_add_text.get()}")
        CUSTOMER_DATA.append({'ime':name_add_text.get().capitalize(), 
                              'vozilo':car_add_text.get().capitalize(), 
                              'reg_broj':reg_add_text.get().upper()})
        NAME_AUTO_COMPLETE.append(name_add_text.get().capitalize())
        REG_BROJ_COMPLETE.append(reg_add_text.get().upper())
    
    frame = tk.Toplevel(master_window)
    frame.title("Nova Mušterija")
    frame.pack_propagate()
    
    #Add new customer name
    ttk.Label(frame, font=("Arial", 14, "bold"), text="Ime i Prezime").pack(side='top')
    name_add_text = tk.Entry(frame, width=20, font=("Arial", 14))
    name_add_text.pack(side='top')
    
    #Add new car name
    ttk.Label(frame, font=("Arial", 14, "bold"), text="Vozilo").pack(side='top')
    car_add_text = tk.Entry(frame, width=20, font=("Arial", 14))
    car_add_text.pack(side='top')
    
    #Add new reg number name
    ttk.Label(frame, font=("Arial", 14, "bold"), text="Registracija").pack(side='top')
    reg_add_text = tk.Entry(frame, width=20, font=("Arial", 14))
    reg_add_text.pack(side='top')
    
    confirm_button = ttk.Button(frame, text="Dodaj Mušteriju", style="bttn_style.TButton", command=add_to_csv)
    confirm_button.pack(side='top')


def main():
    #store data from csv in cache for use
    with open("data.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            CUSTOMER_DATA.append(row)
             
    with open("data.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for data in reader:
            NAME_AUTO_COMPLETE.append(data["ime"])
                
    with open("data.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for data in reader:
            if data["reg_broj"] in REG_BROJ_COMPLETE:
                pass
            else:
                REG_BROJ_COMPLETE.append(data["reg_broj"])
    
    #data for checking duplicates
    for data in CUSTOMER_DATA:
        DUPLICATE_CHECK_DATA.append("{},{},{}".format(data['ime'],data['vozilo'],data['reg_broj']))
    
    #main window
    master_window = tk.Tk()
    master_window.title("Predračun")
    master_window.config(background="Gray")
    
    bttn_style = ttk.Style()
    bttn_style.configure("bttn_style.TButton", font=("Arial", 14, "bold"), background="Gray")
    
    #search for customers button
    query_customer_button = ttk.Button(master_window, width=20,text="Pretraga Mušterije", style="bttn_style.TButton", 
                                       command=lambda:find_customer_window(master_window, CUSTOMER_DATA, NAME_AUTO_COMPLETE, REG_BROJ_COMPLETE))
    query_customer_button.grid(row=0, column=0)
    
    #add new customer button
    add_customer_button = ttk.Button(master_window, width=20, text="Dodaj Mušteriju", style="bttn_style.TButton", 
                                     command=lambda:add_customer_window(master_window))
    add_customer_button.grid(row=1, column=0)
    
    master_window.mainloop()

if __name__ == '__main__':
    main()