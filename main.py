import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import tkinter.font as tkFont
from ttkwidgets import autocomplete

#data class for parsing files to cache
class DataVariables(object):
    def __init__(self):
        self.duplicate_data_check = []
        self.name_auto_complete = []
        self.reg_auto_complete = []
        self.customer_data = []
        
    def parse_data(self):
        with open('data.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.customer_data.append(row)
                
        with open('data.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for data in reader:
                self.name_auto_complete.append(data['ime'].title())
                    
        with open('data.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for data in reader:
                if data['reg_broj'] in self.reg_auto_complete:
                    pass
                else:
                    self.reg_auto_complete.append(data['reg_broj'].upper())
    
        #data for checking duplicates
        for data in self.customer_data:
            self.duplicate_data_check.append('{},{},{}'.format(data['ime'].lower(),data['vozilo'].lower(),data['reg_broj'].lower()))

#base class for customer entry widgets
class EntryTemplate(object):
    def __init__(self, label_name, frame, font_style):
        self.label_name = label_name
        self.frame = frame
        self.font_style = font_style
        
        ttk.Label(self.frame, font=self.font_style, text=self.label_name).pack(side='top')
        self.add_text = tk.Entry(self.frame, width=30, font=self.font_style)
        self.add_text.config(highlightbackground='black', highlightcolor='black', highlightthickness=2)
        self.add_text.pack(side='top', pady=(5,0))
        
    def set_focus(self):
        self.add_text.focus_set()
        
    def get_text(self):
        return self.add_text.get()       

#check if /jobs/ data directory exists, create new if not
JOBS_STORAGE_PATH = os.path.join(os.path.dirname(__file__) + '/jobs/')
if not os.path.isdir(JOBS_STORAGE_PATH):
    os.mkdir(JOBS_STORAGE_PATH)

#create data.csv if one does not exist in root
if not os.path.isfile('data.csv'):
    with open('data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ime', 'vozilo', 'reg_broj'])
        
#add new customer to CSV file           
def create_new_customer(name:str, car:str, reg_broj:str):
    with open('data.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([name.strip().title(), car.strip().title(), reg_broj.strip().upper()])


#FIND CUSTOMER ADD NEW WORK TO EXISTING WORK FILE
def find_customer_window(master_window, database, font_style):
      
    def get_name(event):
        if name_combo.focus_get() and name_combo.get() != '':
            customer = next(item for item in database.customer_data if item['ime'] == name_combo.get().title())
            car_combo.set(customer['vozilo'])
            reg_combo.set(customer['reg_broj'])
            
            csv_path = name_combo.get().lower().replace(' ', '') + '_' + reg_combo.get()
            
            with open(f'{JOBS_STORAGE_PATH}/{csv_path}.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    tree_completed_jobs.insert('', tk.END, values=tuple(row.values()))
                
            
    def get_reg_broj(event):
        if reg_combo.focus_get() and reg_combo.get() != '':
            customer = next(item for item in database.customer_data if item['reg_broj'] == reg_combo.get().upper())
            name_combo.set(customer['ime'])
            car_combo.set(customer['vozilo'])
            
            csv_path = name_combo.get().lower().replace(' ', '') + '_' + reg_combo.get()
            
            with open(f'{JOBS_STORAGE_PATH}/{csv_path}.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    tree_completed_jobs.insert('', tk.END, values=tuple(row.values()))
                    
    
    frame = tk.Frame(master_window, border=5)
    frame.pack(side='top', fill='both', expand=True)
    master_window.bind('<Return>', get_name)
     
    #Ime i prezime label and combobox
    ttk.Label(frame, font=font_style, text='Ime i Prezime').pack(side='top')
    name_combo = autocomplete.AutocompleteCombobox(frame, width=20, completevalues=database.name_auto_complete, font=font_style)
    name_combo.focus_set()
    name_combo.pack(side='top')
    
    #Vozilo label and combobox
    ttk.Label(frame, font=font_style, text='Vozilo').pack(side='top')
    car_combo = autocomplete.AutocompleteCombobox(frame, width=20, font=font_style)
    car_combo.pack(side='top')
    
    #Registracija label and combobox
    ttk.Label(frame, font=font_style, text='Reg. Broj').pack(side='top')
    reg_combo = autocomplete.AutocompleteCombobox(frame, width=20, completevalues=database.reg_auto_complete, font=font_style)
    reg_combo.pack(side='top')
    reg_combo.bind('<Return>', get_reg_broj)
    
    #Repair list, treeview, scrollbar
    treeview_frame = tk.Frame(frame)
    treeview_frame.pack(side='top', fill='both', expand=True)
    
    tree_completed_jobs_columns = ('dio', 'marka', 'količina', 'ukupno')
    
    tree_style = ttk.Style()
    tree_style.configure('Treeview.Heading', font=font_style)
    tree_style.configure('mystyle.Treeview', font=font_style)
    
    tree_completed_jobs = ttk.Treeview(treeview_frame, columns=tree_completed_jobs_columns, show='headings', style='mystyle.Treeview')
    
    tree_completed_jobs.heading('dio', text='Dio')
    tree_completed_jobs.heading('marka', text='Marka')
    
    tree_completed_jobs.heading('količina', text='Količina')
    tree_completed_jobs.column('količina', anchor='e', width=75)
    
    tree_completed_jobs.heading('ukupno', text='Ukupno')
    tree_completed_jobs.column('ukupno', anchor='e', width=75)
    tree_completed_jobs.pack(side='left', fill='both', expand=True)

    
    scrollbar = tk.Scrollbar(treeview_frame, orient='vertical', command=tree_completed_jobs.yview)
    scrollbar.pack(side='right', fill='y')
    
    tree_completed_jobs.config(yscrollcommand=scrollbar.set)

    
    #Add new job button


#ADD CUSTOMER AND CREATE WORK DATA FILE
def add_customer_window(master_window, database, font_style):
    
    def add_to_csv():
        if name_entry.get_text() == '' or car_entry.get_text() == '' or reg_entry.get_text() == '':
            messagebox.showwarning('Upozorenje!', 'Jedno ili više polja je prazno!')
            return None
        
        if f'{name_entry.get_text().lower()},{car_entry.get_text().lower()},{reg_entry.get_text().lower()}' in database.duplicate_data_check:
            messagebox.showwarning('Upozorenje!', 'Korisnik i Registracija već postoje u bazi podataka.')
            return None

        #update cache variables and data for new user real time
        create_new_customer(name_entry.get_text(),car_entry.get_text(), reg_entry.get_text())
        database.duplicate_data_check.append(f'{name_entry.get_text().lower()},{car_entry.get_text().lower()},{reg_entry.get_text().lower()}')
        database.customer_data.append({'ime':name_entry.get_text().title(), 
                              'vozilo':car_entry.get_text().title(), 
                              'reg_broj':reg_entry.get_text().upper()})
        database.name_auto_complete.append(name_entry.get_text().title())
        database.reg_auto_complete.append(reg_entry.get_text().upper())
        messagebox.showinfo('Uspjeh', 'Nova mušterija dodana u bazu podataka.')
        
        #create work.csv file if one does not exist
        name_reg_nospace = name_entry.get_text().lower().replace(' ', '') + '_' + reg_entry.get_text().upper().replace(' ', '')
        if not os.path.isfile(f'{JOBS_STORAGE_PATH}/{name_reg_nospace}.csv'):
            with open(f'{JOBS_STORAGE_PATH}/{name_reg_nospace}.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['dio', 'marka', 'količina', 'cijena'])
         
    
    frame = tk.Frame(master_window)
    frame.config(width=640, height=480)
    frame.pack(side='top', fill='both', expand=True, padx=1, pady=1)
    master_window.bind('<Return>', lambda event:add_to_csv())
    
    #Add new user to database
    name_entry = EntryTemplate('Ime i Prezime', frame, font_style)
    name_entry.set_focus()
    car_entry = EntryTemplate('Vozilo', frame, font_style)
    reg_entry = EntryTemplate('Registracija', frame, font_style)
    
    confirm_button = ttk.Button(frame, text='Unos u Bazu', style='bttn_style.TButton', command=add_to_csv)
    confirm_button.pack(side='top', pady=(5, 0))


def main():
    #store data from csv in cache for use
    database = DataVariables()
    database.parse_data()
    
    def clear_children():
        list_of_slaves = master_window.pack_slaves()
        for frame in list_of_slaves:
            if '!frame' in str(frame):
                frame.destroy()
    
    
    #main window
    master_window = tk.Tk()
    master_window.title('Predračun')
    master_window.geometry('640x480')
    master_window.config(background='Gray')
    
    
    #create tiled background image from selected photo
    background_image = Image.open('background.jpg')
    bg_w, bg_h = background_image.size
    new_image = Image.new('RGB', (2000, 2000))
    w, h = new_image.size

    for i in range(0, w, bg_w):
        for j in range(0, h, bg_h):
            new_image.paste(background_image,(i,j))

    new_image.save('new_background_image.jpg')
    new_background_image = ImageTk.PhotoImage(Image.open('new_background_image.jpg'))
    bg_label = tk.Label(master_window, image=new_background_image)
    bg_label.place(anchor='nw')
        
    #usable font style passed to functions
    font_style = tkFont.Font(family='Times New Roman', size=14, weight='bold')
    
    #button style for the application
    bttn_style = ttk.Style()
    bttn_style.configure('bttn_style.TButton', font=font_style, background='Gray')
    
    #search for customers button
    query_customer_button = ttk.Button(master_window, width=20,text='Pretraga Mušterije', style='bttn_style.TButton', 
                                       command=lambda:[clear_children(), find_customer_window(master_window, database, font_style)])
    query_customer_button.pack(side='top', anchor="center", padx=2, pady=(2, 5))

    
    #add new customer button
    add_customer_button = ttk.Button(master_window, width=20, text='Dodaj Mušteriju', style='bttn_style.TButton', 
                                     command=lambda:[clear_children(), add_customer_window(master_window, database, font_style)])
    add_customer_button.pack(side='top', anchor="center", padx=2, pady=(0, 0))

    
    
    master_window.mainloop()

if __name__ == '__main__':
    main()