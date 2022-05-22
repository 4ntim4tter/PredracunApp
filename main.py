import csv
import os
import tkinter as tk
from ttkwidgets import autocomplete
from tkinter import ttk

if os.path.isfile("data.csv"):
    pass
else:
    with open("data.csv", "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ime", "vozilo", "reg_broj"])

def create_new_customer(name, car, reg_broj):
    with open("data.csv", "a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([name, car, reg_broj])
        
    # with open("data.csv", "r", encoding="utf-8") as file:
    #     reader = csv.DictReader(file)
    #     for customer_data in reader:
    #         print(customer_data["ime"], customer_data["vozilo"], customer_data["reg_broj"])

def query_window(master_window, customer_data, name_auto_complete, reg_broj_complete):
    
    customer_data = customer_data     

    def get_name(event):
        if name_combo.focus_get():
            customer = next(item for item in customer_data if item["ime"] == name_combo.get())
            car_combo.set(customer["vozilo"])
            reg_combo.set(customer["reg_broj"])
            
    def get_vehicle(event):
        if car_combo.focus_get():
            print(car_combo.get())
            
    def get_reg_broj(event):
        if car_combo.focus_get():
            print(car_combo.get())
    
    frame = tk.Toplevel(master_window)
    frame.title("Pretraga Mušterije")
    frame.grid()
        
    #Ime i prezime label and combobox
    ttk.Label(frame, font=("Arial", 14, "bold"), text="Ime i Prezime").grid(column=0, row=0)
    name_combo = autocomplete.AutocompleteCombobox(frame, width=30, completevalues=name_auto_complete, font=("Arial", 16))
    name_combo.grid(row=0, column=1)
    name_combo.bind("<Return>", get_name)
    
    #Vozilo label and combobox
    ttk.Label(frame, font=("Arial", 14, "bold"), text="Vozilo").grid(column=0, row=1)
    car_combo = autocomplete.AutocompleteCombobox(frame, width=30, font=("Arial", 16))
    car_combo.grid(row=1, column=1)
    car_combo.bind("<Return>", get_vehicle)
    
    #Registracija label and combobox
    ttk.Label(frame, font=("Arial", 14, "bold"), text="Reg. Broj").grid(column=0, row=2)
    reg_combo = autocomplete.AutocompleteCombobox(frame, width=30, completevalues=reg_broj_complete, font=("Arial", 16))
    reg_combo.grid(row=2, column=1)
    reg_combo.bind("<Return>", get_reg_broj)

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
    
    button_style = ttk.Style()
    button_style.configure("button_style.TButton", font=("Arial", 14, "bold"), background="Gray")
    
    query_button = ttk.Button(master_window, text="Pretraga Mušterije", style="button_style.TButton", command=lambda : query_window(master_window, customer_data, name_auto_complete, reg_broj_complete))
    query_button.grid(row=1, column=1)
    
    master_window.mainloop()

if __name__ == '__main__':
    main()