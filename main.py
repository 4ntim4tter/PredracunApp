import csv
import os
import tkinter as tk
from ttkwidgets import autocomplete
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont

#stored data from files
DUPLICATE_CHECK_DATA = []
NAME_AUTO_COMPLETE = []
REG_BROJ_COMPLETE = []
CUSTOMER_DATA = []

#check if data file exists, create new file if not
JOBS_STORAGE_PATH = os.path.join(os.path.dirname(__file__) + '/jobs/')
if not os.path.isdir(JOBS_STORAGE_PATH):
    os.mkdir(JOBS_STORAGE_PATH)


if os.path.isfile('data.csv'):
    pass
else:
    with open('data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ime', 'vozilo', 'reg_broj'])
        
#add new customer to CSV file           
def create_new_customer(name:str, car:str, reg_broj:str):
    with open('data.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([name.strip().title(), car.strip().title(), reg_broj.strip().upper()])


#FIND CUSTOMER ADD NEW WORK TO EXISTING WORK FILE
def find_customer_window(master_window, CUSTOMER_DATA, NAME_AUTO_COMPLETE, REG_BROJ_COMPLETE, font_style):
      
    def get_name(event):
        if name_combo.focus_get():
            customer = next(item for item in CUSTOMER_DATA if item['ime'] == name_combo.get().title())
            car_combo.set(customer['vozilo'])
            reg_combo.set(customer['reg_broj'])
            
            csv_path = name_combo.get().lower().replace(' ', '') + '_' + reg_combo.get()
            
            with open(f'{JOBS_STORAGE_PATH}/{csv_path}.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    tree_completed_jobs.insert('', tk.END, values=tuple(row.values()))
                
            
    def get_reg_broj(event):
        if reg_combo.focus_get():
            customer = next(item for item in CUSTOMER_DATA if item['reg_broj'] == reg_combo.get().upper())
            name_combo.set(customer['ime'])
            car_combo.set(customer['vozilo'])
            
            csv_path = name_combo.get().lower().replace(' ', '') + '_' + reg_combo.get()
            
            with open(f'{JOBS_STORAGE_PATH}/{csv_path}.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    tree_completed_jobs.insert('', tk.END, values=tuple(row.values()))
                    
    
    frame = tk.Frame(master_window)
    #frame.title('Pretraga Mušterije')
    frame.grid()
     
    #Ime i prezime label and combobox
    ttk.Label(frame, font=font_style, text='Ime i Prezime').pack(side='top')
    name_combo = autocomplete.AutocompleteCombobox(frame, width=20, completevalues=NAME_AUTO_COMPLETE, font=font_style)
    name_combo.pack(side='top')
    name_combo.bind('<Return>', get_name)
    
    #Vozilo label and combobox
    ttk.Label(frame, font=font_style, text='Vozilo').pack(side='top')
    car_combo = autocomplete.AutocompleteCombobox(frame, width=20, font=font_style)
    car_combo.pack(side='top')
    
    #Registracija label and combobox
    ttk.Label(frame, font=font_style, text='Reg. Broj').pack(side='top')
    reg_combo = autocomplete.AutocompleteCombobox(frame, width=20, completevalues=REG_BROJ_COMPLETE, font=font_style)
    reg_combo.pack(side='top')
    reg_combo.bind('<Return>', get_reg_broj)
    
    #Repair list, treeview, scrollbar
    treeview_frame = tk.Frame(frame)
    treeview_frame.pack(side='top', expand=True, fill='both')
    
    tree_completed_jobs_columns = ('dio', 'marka', 'količina', 'ukupno')
    
    tree_style = ttk.Style()
    tree_style.configure('Treeview.Heading', font=font_style)
    tree_style.configure('mystyle.Treeview', font=font_style)
    
    tree_completed_jobs = ttk.Treeview(treeview_frame, columns=tree_completed_jobs_columns, show='headings', style='mystyle.Treeview')
    
    tree_completed_jobs.heading('dio', text='Dio')
    tree_completed_jobs.heading('marka', text='Marka')
    
    tree_completed_jobs.heading('količina', text='Količina')
    tree_completed_jobs.column('količina', anchor='e')
    
    tree_completed_jobs.heading('ukupno', text='Ukupno')
    tree_completed_jobs.column('ukupno', anchor='e')
    tree_completed_jobs.pack(side='left', fill='both', expand=True)
    
    scrollbar = tk.Scrollbar(treeview_frame, orient='vertical', command=tree_completed_jobs.yview)
    scrollbar.pack(side='right', fill='y')
    
    tree_completed_jobs.config(yscrollcommand=scrollbar.set)
    
    #Add new job button


#ADD CUSTOMER AND CREATE WORK DATA FILE
def add_customer_window(master_window, font_style):
    
    def add_to_csv():
        if name_add_text.get() == '' or car_add_text.get() == '' or reg_add_text.get() == '':
            messagebox.showwarning('Upozorenje!', 'Jedno ili više polja je prazno!')
            return None
        
        if f'{name_add_text.get().lower()},{car_add_text.get().lower()},{reg_add_text.get().lower()}' in DUPLICATE_CHECK_DATA:
            messagebox.showwarning('Upozorenje!', 'Korisnik i Registracija već postoje u bazi podataka.')
            return None

        #update cache variables and data for new user real time
        create_new_customer(name_add_text.get(),car_add_text.get(), reg_add_text.get())
        messagebox.showinfo('Uspjeh', 'Nova mušterija dodana u bazu podataka.')
        DUPLICATE_CHECK_DATA.append(f'{name_add_text.get().lower()},{car_add_text.get().lower()},{reg_add_text.get().lower()}')
        CUSTOMER_DATA.append({'ime':name_add_text.get().title(), 
                              'vozilo':car_add_text.get().title(), 
                              'reg_broj':reg_add_text.get().upper()})
        NAME_AUTO_COMPLETE.append(name_add_text.get().title())
        REG_BROJ_COMPLETE.append(reg_add_text.get().upper())
        
        name_reg_nospace = name_add_text.get().lower().replace(' ', '') + '_' + reg_add_text.get().upper().replace(' ', '')
        
        if not os.path.isfile(f'{JOBS_STORAGE_PATH}/{name_reg_nospace}.csv'):
            with open(f'{JOBS_STORAGE_PATH}/{name_reg_nospace}.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['dio', 'marka', 'količina', 'cijena'])
         
    
    frame = tk.Frame(master_window)
    frame.grid()
    
    #Add new customer name
    ttk.Label(frame, font=font_style, text='Ime i Prezime').pack(side='top')
    name_add_text = tk.Entry(frame, width=20, font=font_style)
    name_add_text.pack(side='top')
    
    #Add new car name
    ttk.Label(frame, font=font_style, text='Vozilo').pack(side='top')
    car_add_text = tk.Entry(frame, width=20, font=font_style)
    car_add_text.pack(side='top')
    
    #Add new reg number name
    ttk.Label(frame, font=font_style, text='Registracija').pack(side='top')
    reg_add_text = tk.Entry(frame, width=20, font=font_style)
    reg_add_text.pack(side='top')
    
    confirm_button = ttk.Button(frame, text='Dodaj Mušteriju', style='bttn_style.TButton', command=add_to_csv)
    confirm_button.pack(side='top')


def main():
    #store data from csv in cache for use
    with open('data.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            CUSTOMER_DATA.append(row)
             
    with open('data.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for data in reader:
            NAME_AUTO_COMPLETE.append(data['ime'].title())
                
    with open('data.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for data in reader:
            if data['reg_broj'] in REG_BROJ_COMPLETE:
                pass
            else:
                REG_BROJ_COMPLETE.append(data['reg_broj'].upper())
    
    #data for checking duplicates
    for data in CUSTOMER_DATA:
        DUPLICATE_CHECK_DATA.append('{},{},{}'.format(data['ime'].lower(),data['vozilo'].lower(),data['reg_broj'].lower()))
    
    
    def clear_children():
        list_of_slaves = master_window.grid_slaves()
        for frame in list_of_slaves:
            if '!frame' in str(frame):
                frame.destroy()
    
    
    #main window
    master_window = tk.Tk()
    master_window.title('Predračun')
    master_window.config(background='Gray')
    
    #usable font style passed to functions
    font_style = tkFont.Font(family='Times New Roman', size=14, weight='bold')
    
    #button style for the application
    bttn_style = ttk.Style()
    bttn_style.configure('bttn_style.TButton', font=font_style, background='Gray')
    
    #search for customers button
    query_customer_button = ttk.Button(master_window, width=20,text='Pretraga Mušterije', style='bttn_style.TButton', 
                                       command=lambda:[clear_children(), find_customer_window(master_window, CUSTOMER_DATA, NAME_AUTO_COMPLETE, REG_BROJ_COMPLETE, font_style)])
    query_customer_button.grid(row=0, column=0)
    
    #add new customer button
    add_customer_button = ttk.Button(master_window, width=20, text='Dodaj Mušteriju', style='bttn_style.TButton', 
                                     command=lambda:[clear_children(), add_customer_window(master_window, font_style)])
    add_customer_button.grid(row=1, column=0)
    
    master_window.mainloop()

if __name__ == '__main__':
    main()