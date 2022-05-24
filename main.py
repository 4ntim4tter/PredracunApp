import csv
import os
import tkinter as tk
from ttkwidgets import autocomplete
from tkinter import ttk
from tkinter import messagebox

if os.path.isfile("data.csv"):
    pass
else:
    with open("data.csv", "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ime", "vozilo", "reg_broj"])

def create_new_customer(name:str, car:str, reg_broj:str):
    with open("data.csv", "a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([name.strip(), car.strip(), reg_broj.strip()])

#FIND CUSTOMER ADD NEW WORK TO EXISTING WORK FILE
def find_customer_window(master_window, customer_data, name_auto_complete, reg_broj_complete):  

    def get_name(event):
        if name_combo.focus_get():
            customer = next(item for item in customer_data if item["ime"] == name_combo.get())
            car_combo.set(customer["vozilo"])
            reg_combo.set(customer["reg_broj"])
            
    def get_reg_broj(event):
        if reg_combo.focus_get():
            customer = next(item for item in customer_data if item["reg_broj"] == reg_combo.get())
            name_combo.set(customer["ime"])
            car_combo.set(customer["vozilo"])
    
    frame = tk.Toplevel(master_window)
    frame.title("Pretraga Mušterije")
    frame.pack_propagate()
        
    #Ime i prezime label and combobox
    ttk.Label(frame, font=("Arial", 14, "bold"), text="Ime i Prezime").pack(side='top')
    name_combo = autocomplete.AutocompleteCombobox(frame, width=20, completevalues=name_auto_complete, font=("Arial", 14))
    name_combo.pack(side='top')
    name_combo.bind("<Return>", get_name)
    
    #Vozilo label and combobox
    ttk.Label(frame, font=("Arial", 14, "bold"), text="Vozilo").pack(side='top')
    car_combo = autocomplete.AutocompleteCombobox(frame, width=20, font=("Arial", 14))
    car_combo.pack(side='top')
    
    #Registracija label and combobox
    ttk.Label(frame, font=("Arial", 14, "bold"), text="Reg. Broj").pack(side='top')
    reg_combo = autocomplete.AutocompleteCombobox(frame, width=20, completevalues=reg_broj_complete, font=("Arial", 14))
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
def add_customer_window(master_window, customer_data):
    
    def add_to_csv():
        if name_add_text.get() != '' and car_add_text.get() != '' and reg_add_text.get() != '':
            create_new_customer(name_add_text.get(),car_add_text.get(), reg_add_text.get())
            messagebox.showinfo("Uspjeh", "Nova mušterija dodana.")
        else:
            messagebox.showwarning("Upozorenje!", "Jedno ili više polja je prazno!")
    
    frame = tk.Toplevel(master_window)
    frame.attributes('-topmost', 'true')
    frame.title("Nova Mušterija")
    frame.pack_propagate()
    
    #Add new customer name
    ttk.Label(frame, font=("Arial", 14, "bold"), text="Ime i Prezime").pack(side='top')
    name_add_text = tk.Entry(frame, width=20, font=("Arial", 14))
    name_add_text.pack(side='top')
    
    #Add new customer name
    ttk.Label(frame, font=("Arial", 14, "bold"), text="Vozilo").pack(side='top')
    car_add_text = tk.Entry(frame, width=20, font=("Arial", 14))
    car_add_text.pack(side='top')
    
    #Add new customer name
    ttk.Label(frame, font=("Arial", 14, "bold"), text="Registracija").pack(side='top')
    reg_add_text = tk.Entry(frame, width=20, font=("Arial", 14))
    reg_add_text.pack(side='top')
    
    confirm_button = ttk.Button(frame, text="Dodaj Mušteriju", style="bttn_style.TButton", command=add_to_csv)
    confirm_button.pack(side='top')


def main():
    
    #store data from csv in memory for use
    customer_data = []
    with open("data.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            customer_data.append(row)
             
    with open("data.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        name_auto_complete = []
        for data in reader:
            name_auto_complete.append(data["ime"])
                
    with open("data.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        reg_broj_complete = []
        for data in reader:
            if data["reg_broj"] in reg_broj_complete:
                pass
            else:
                reg_broj_complete.append(data["reg_broj"])
    
    #main window
    master_window = tk.Tk()
    master_window.title("Predračun")
    master_window.config(background="Gray")
    
    bttn_style = ttk.Style()
    bttn_style.configure("bttn_style.TButton", font=("Arial", 14, "bold"), background="Gray")
    
    #search for customers button
    query_customer_button = ttk.Button(master_window, width=20,text="Pretraga Mušterije", style="bttn_style.TButton", command=lambda:find_customer_window(master_window, customer_data, name_auto_complete, reg_broj_complete))
    query_customer_button.grid(row=0, column=0)
    
    #add new customer button
    add_customer_button = ttk.Button(master_window, width=20, text="Dodaj Mušteriju", style="bttn_style.TButton", command=lambda:add_customer_window(master_window, customer_data))
    add_customer_button.grid(row=1, column=0)
    
    master_window.mainloop()

if __name__ == '__main__':
    main()