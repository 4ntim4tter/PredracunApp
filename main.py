import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import tkinter.font as tkFont
from ttkwidgets import autocomplete

#check if /jobs/ data directory exists, create new if not
JOBS_STORAGE_PATH = os.path.join(os.path.dirname(__file__) + '\jobs\\')
if not os.path.isdir(JOBS_STORAGE_PATH):
    os.mkdir(JOBS_STORAGE_PATH)

BACKGROUND_COLOR = 'gray'
FOREGROUND_COLOR = 'white'

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
    def __init__(self, label_name, frame, font_style, packing_style:tuple, label_packing:str, width:int):
        self.label_name = label_name
        self.frame = frame
        self.font_style = font_style
        self.packing_style = packing_style
        self.label_packing = label_packing
        self.width = width
        
        self.label = ttk.Label(self.frame, font=self.font_style, text=self.label_name,  background=BACKGROUND_COLOR)
        self.label.pack(side=self.label_packing)
        self.add_text = tk.Entry(self.frame, width=self.width, font=self.font_style, justify='center')
        self.add_text.config(highlightbackground='black', highlightcolor='black', highlightthickness=2)
        self.add_text.pack(side=self.packing_style[0], pady=self.packing_style[1])
        
    def set_focus(self):
        self.add_text.focus_set()
        
    def get_text(self):
        return self.add_text.get()
    
    def set_text(self, text):
        self.add_text.delete(0, 'end')
        return self.add_text.insert('end', text)
    
    def set_state(self, text:bool):
        if text:
            self.add_text.config(state='normal')
        else:
            self.add_text.config(state='readonly')

#base class for autocomplete entry widget
class AutocompleteTemplate(object):
    def __init__(self, label_name, frame, font_style, database) -> None:
        self.label_name = label_name
        self.frame = frame
        self.font_style = font_style
        self.database = database
        
        ttk.Label(self.frame, font=self.font_style, text=self.label_name, background=BACKGROUND_COLOR).pack(side='top')
        self.autocomplete = autocomplete.AutocompleteCombobox(self.frame, width=30, completevalues=self.database, font=self.font_style, justify='center')
        self.autocomplete.option_add('*Tcombobox*Listbox.Justify', 'center')
        self.autocomplete.pack(side='top', pady=(5,0))
        
    def take_focus(self):
        self.autocomplete.focus_set()
        
    def is_focused(self):
        return self.autocomplete.focus_get()
        
    def get_text(self):
        return self.autocomplete.get()
    
    def set_text(self, text:str):
        return self.autocomplete.set(text)
    

#base class for treeview widget
class TreeviewTemplate(object):
    def __init__(self, treeview_frame, columns, style):
        self.treeview_frame = treeview_frame
        self.columns = columns
        self.style = style
        
        self.treeview = ttk.Treeview(treeview_frame, columns=columns, show='headings', style='mystyle.Treeview', height=20)
        
        for column in columns:
            self.treeview.heading(column, text=column)
            self.treeview.column(column, anchor='center')
            
        scrollbar = tk.Scrollbar(treeview_frame, orient='vertical', command=self.treeview.yview)
        scrollbar.pack(side='right', fill='y')
        self.treeview.config(yscrollcommand=scrollbar.set)
        
        self.treeview.pack(side='left', fill='both', expand=True)
    
    def insert(self, location, values, tag):
        self.treeview.insert(location, 'end', values=values, tags=tag)
    
    def clear(self):
        self.treeview.delete(*self.treeview.get_children())

#base class for adding new workorder frame widgets
class WorkorderRowTemplate(object):
    def __init__(self, main_frame, font_style, row):
        self.main_frame = main_frame
        self.font_style = font_style
        self.row = row
        
        self.part_frame = tk.Frame(self.main_frame)
        self.part_frame.config(background=BACKGROUND_COLOR)
        self.part_frame.grid(row=self.row, column=1)
        
        self.brand_frame = tk.Frame(self.main_frame)
        self.brand_frame.config(background=BACKGROUND_COLOR)
        self.brand_frame.grid(row=self.row, column=2)
        
        self.price_frame = tk.Frame(self.main_frame)
        self.price_frame.config(background=BACKGROUND_COLOR)
        self.price_frame.grid(row=self.row, column=3)
        
        self.amount_frame = tk.Frame(self.main_frame)
        self.amount_frame.config(background=BACKGROUND_COLOR)
        self.amount_frame.grid(row=self.row, column=4)
        
        self.total_frame = tk.Frame(self.main_frame)
        self.total_frame.config(background=BACKGROUND_COLOR)
        self.total_frame.grid(row=self.row, column=5)
        
        self.part_entry = EntryTemplate('Dio', self.part_frame, font_style, ('top', (5,0)), 'left', width=20)
        self.brand_entry = EntryTemplate('Marka', self.brand_frame, font_style, ('top', (5,0)), 'left', width=20)
        self.price_entry = EntryTemplate('Cijena', self.price_frame, font_style, ('top', (5,0)), 'left', width=20)
        self.amount_entry = EntryTemplate('Količina', self.amount_frame, font_style, ('top', (5,0)), 'left', width=20)
        self.total_entry = EntryTemplate('Ukupno', self.total_frame, font_style, ('top', (5,0)), 'left', width=20)
        self.total_entry.set_state(False)
    
    def calculate_total(self):
        if self.price_entry.get_text() != '' and self.amount_entry.get_text() != '':
            total = self.price_entry.get_text() + '*' + self.amount_entry.get_text()
            total = round(eval(total), 2)
            self.total_entry.set_state(True)
            self.total_entry.set_text(str(total))
            self.total_entry.set_state(False)
    
    def get_all_values(self):
        self.calculate_total()
        return [self.part_entry.get_text().strip().title(), 
                self.brand_entry.get_text().strip().title(), 
                self.price_entry.get_text(), 
                self.amount_entry.get_text(), 
                self.total_entry.get_text()]
                  
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

#needed global for adding new workorders
ENTRY_COUNTER = 0
#add work order, create csv for workorder       
def new_workorder(master_window, parent_window, database, font_style, csv_folder):
    
    main_frame = tk.Toplevel(parent_window)
    main_frame.config(background=BACKGROUND_COLOR, highlightbackground='black', highlightcolor='black', highlightthickness=2)
    
    child_frame = tk.Frame(main_frame)
    child_frame.config(background=BACKGROUND_COLOR, highlightbackground='black', highlightcolor='black', highlightthickness=2)
    child_frame.grid()
    
    file_path = JOBS_STORAGE_PATH + csv_folder + '\\' + str(datetime.date.today().strftime('%d_%b_%Y')) + '_' + str(len(os.listdir(JOBS_STORAGE_PATH + csv_folder))) + '.csv'

    if not os.path.isfile(file_path) and csv_folder != '_':
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['dio', 'marka', 'cijena', 'količina', 'ukupno'])
    
    
    entry_list = []
    global ENTRY_COUNTER
    first_entry = WorkorderRowTemplate(child_frame, font_style, ENTRY_COUNTER)
    entry_list.append(first_entry)


    def increment_counter():
        global ENTRY_COUNTER
        ENTRY_COUNTER += 1
    add_new_entry_button = ttk.Button(child_frame, width=3, text='+', style='bttn_style.TButton', 
                                    command=lambda:[increment_counter(), 
                                                    entry_list.append(WorkorderRowTemplate(child_frame, font_style, ENTRY_COUNTER)), 
                                                    main_frame.update(),
                                                    insert_button_frame.grid(row=ENTRY_COUNTER+1, column=5, sticky='se'),
                                                    cancel_button_frame.grid(row=ENTRY_COUNTER+1, column=4, sticky='se')])
    add_new_entry_button.grid(row=0, column=0)
    
    
    def calculate_totals(list_of_workorders):
        for entry in list_of_workorders:
            entry.calculate_total()
    
    
    def set_counter_to_zero():
        global ENTRY_COUNTER
        ENTRY_COUNTER = 0
        main_frame.destroy()
        
        for slave in parent_window.pack_slaves():
            slave.update()
      
        
    def populate_csv(list_of_workorders):
        with open(file_path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for row in list_of_workorders:
                writer.writerow(row.get_all_values())
    
    insert_button_frame = tk.Frame(child_frame)
    insert_button_frame.config(background=BACKGROUND_COLOR, highlightbackground='black', highlightcolor='black', highlightthickness=2)
    insert_button_frame.grid(row=ENTRY_COUNTER+1, column=5, sticky='se', pady=(3, 0))
    
    insert_contents = ttk.Button(insert_button_frame, text="Otvori novi predračun", width=19, style='bttn_style.TButton', 
                                 command=lambda:[populate_csv(entry_list), main_frame.destroy()])
    insert_contents.grid()
    
    
    cancel_button_frame = tk.Frame(child_frame)
    cancel_button_frame.config(background=BACKGROUND_COLOR, highlightbackground='black', highlightcolor='black', highlightthickness=2)
    cancel_button_frame.grid(row=ENTRY_COUNTER+1, column=4, sticky='se', pady=(3, 0))
    
    cancel_contents = ttk.Button(cancel_button_frame, text="Odustani", width=19, style='bttn_style.TButton', 
                                 command=lambda:set_counter_to_zero())
    cancel_contents.grid()
    
    
    main_frame.focus_set()
    main_frame.bind('<Return>', lambda event:calculate_totals(entry_list))
    main_frame.bind('<Escape>', lambda event:main_frame.destroy())
    
    
    main_frame.protocol('WM_DELETE_WINDOW', set_counter_to_zero)


#FIND CUSTOMER ADD NEW WORK TO EXISTING WORK FILE
def find_customer_window(master_window, parent_window, database, font_style):

    def tree_double_click(event):
        pass
      
    def autofill_fields(event):
        tree_jobs.clear()
        if name_autocomplete.is_focused() and name_autocomplete.get_text() != '':
            customer = next(item for item in database.customer_data if item['ime'] == name_autocomplete.get_text().title())
            car_autocomplete.set_text(customer['vozilo'])
            reg_autocomplete.set_text(customer['reg_broj'])
                    
        if reg_autocomplete.is_focused() and reg_autocomplete.get_text() != '':
            customer = next(item for item in database.customer_data if item['reg_broj'] == reg_autocomplete.get_text().upper())
            name_autocomplete.set_text(customer['ime'])
            car_autocomplete.set_text(customer['vozilo'])
            
        if name_autocomplete.get_text() != '' and reg_autocomplete.get_text() != '':
            csv_file_path = name_autocomplete.get_text().lower().replace(' ', '') + '_' + reg_autocomplete.get_text().upper()
            
            directory_contents = os.listdir(f'{JOBS_STORAGE_PATH}{csv_file_path}') 
            
            parts = []
            total_price = 0
            for csv_file in directory_contents:
                with open(f'{JOBS_STORAGE_PATH}{csv_file_path}\\{csv_file}', 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        parts.append(row['dio']+',')
                        total_price += int(row['ukupno'])           
                tree_jobs.insert('', [csv_file.replace('.csv', ''), parts, str(total_price)], tag='folder')
                parts = []
                total_price = 0
                    # for count, row in enumerate(reader):
                #         print(row.values())
                #         even_odd=''
                #         if count % 2 == 0:
                #             even_odd = 'even'
                #         else:
                #             even_odd = 'odd'
                    
                #         tree_jobs.insert(csv_file.replace('.csv', ''), list(row.values()), tag=even_odd)
    
    
    find_customer_frame = tk.Frame(parent_window)
    find_customer_frame.pack(side='top')
    
    fields_frame = tk.Frame(parent_window)
    fields_frame.config(background=BACKGROUND_COLOR, highlightbackground='black', highlightcolor='black', highlightthickness=2)
    fields_frame.pack(side='left', expand=True, fill='both', anchor='nw')
    
    name_autocomplete = AutocompleteTemplate('Ime i Prezime', fields_frame, font_style, database.name_auto_complete)
    name_autocomplete.take_focus()
    car_autocomplete = AutocompleteTemplate('Vozilo', fields_frame, font_style, None)
    reg_autocomplete= AutocompleteTemplate('Registracija', fields_frame, font_style, database.reg_auto_complete)
    master_window.bind('<Return>', lambda event:autofill_fields(event))
    
    
    #Repair list, treeview, scrollbar
    treeview_frame = tk.Frame(fields_frame)
    treeview_frame.config(background=BACKGROUND_COLOR, highlightbackground='black', highlightcolor='black', highlightthickness=2)
    treeview_frame.pack(side='top', fill='both', expand=True, pady=(10,0))
    
    tree_columns = ('Datum', 'Dijelovi', 'Ukupna Cijena[KM]')
    
    tree_style = ttk.Style()
    tree_style.configure('Treeview.Heading', font=font_style)
    tree_style.configure('mystyle.Treeview', font=font_style)
    
    tree_jobs = TreeviewTemplate(treeview_frame, tree_columns, tree_style)
    
    buttons_frame = tk.Frame(fields_frame)
    buttons_frame.config(background=BACKGROUND_COLOR, highlightbackground='black', highlightcolor='black', highlightthickness=2)
    buttons_frame.pack(side='top', anchor='ne')
    
    def is_data_entered(name, car, reg):
        if name == '' or car == '' or reg == '':
            messagebox.showerror('Upozorenje!', 'Ne možete unijeti novi predračun bez pronađene mušterije.')
            return None
        new_workorder(master_window, 
                      fields_frame, 
                      database, 
                      font_style, 
                      name_autocomplete.get_text().lower().replace(' ', '') + '_' + reg_autocomplete.get_text().upper())
        
    add_new_workorder = ttk.Button(buttons_frame, width=20,text='Novi Predračun', style='bttn_style.TButton', 
                                   command=lambda:is_data_entered(name_autocomplete.get_text(), car_autocomplete.get_text(), reg_autocomplete.get_text()))
    add_new_workorder.pack(side='top')


#ADD CUSTOMER AND CREATE WORK DATA FILE
def add_customer_window(master_window, parent_window, database, font_style):
    
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
        if not os.path.isdir(f'{JOBS_STORAGE_PATH}{name_reg_nospace}'):
            os.mkdir(f'{JOBS_STORAGE_PATH}{name_reg_nospace}\\')
            # with open(f'{JOBS_STORAGE_PATH}\{name_reg_nospace}\\', 'a', newline='', encoding='utf-8') as file:
            #     writer = csv.writer(file)
            #     writer.writerow(['dio', 'marka', 'količina', 'cijena', 'ukupno'])
        for slave in parent_window.pack_slaves():
            slave.destroy()
        find_customer_window(master_window, parent_window, database, font_style)
        add_customer_frame.destroy()
        
    add_customer_frame = tk.Frame(parent_window)
    if len(parent_window.pack_slaves()) > 2:
        slave_list = parent_window.pack_slaves()
        slave_list[2].destroy()
    add_customer_frame.config(background=BACKGROUND_COLOR, highlightbackground='black', highlightcolor='black', highlightthickness=2)
    add_customer_frame.pack(side='top', anchor='nw')

    master_window.bind('<Return>', lambda event:add_to_csv())
    
    #Add new user to database
    name_entry = EntryTemplate('Ime i Prezime', add_customer_frame, font_style, ('top', (5,0)), 'top', width=30)
    name_entry.set_focus()
    car_entry = EntryTemplate('Vozilo', add_customer_frame, font_style, ('top', (5,0)), 'top', width=30)
    reg_entry = EntryTemplate('Registracija', add_customer_frame, font_style, ('top', (5,0)), 'top', width=30)
    
    confirm_button = ttk.Button(add_customer_frame, text='Unos u Bazu', width=20, style='bttn_style.TButton', command=add_to_csv)
    confirm_button.pack(side='top', pady=(5, 5))


def main():
    #store data from csv in cache for use
    database = DataVariables()
    database.parse_data()
    
    def clear_children():
        list_of_slaves = windows_frame.pack_slaves()
        for frame in list_of_slaves:
            if '!frame' in str(frame):
                frame.destroy()
        
    #main window
    master_window = tk.Tk()
    master_window.title('Predračun')
    master_window.attributes('-fullscreen', False)
    master_window.config(background=BACKGROUND_COLOR)
    
    #create tiled background image from selected photo
    # background_image = Image.open('background.jpg')
    # bg_w, bg_h = background_image.size
    # new_image = Image.new('RGB', (2000, 2000))
    # w, h = new_image.size

    # for i in range(0, w, bg_w):
    #     for j in range(0, h, bg_h):
    #         new_image.paste(background_image,(i,j))

    # new_image.save('new_background_image.jpg')
    # new_background_image = ImageTk.PhotoImage(Image.open('new_background_image.jpg'))
    # bg_label = tk.Label(master_window, image=new_background_image, pady=-50, padx=-50)
    # bg_label.place(anchor='nw')
        
    #usable font style passed to functions
    font_style = tkFont.Font(family='Times New Roman', size=13, weight='bold')
    
    #button style for the application
    bttn_style = ttk.Style()
    bttn_style.configure('bttn_style.TButton', font=font_style, background=BACKGROUND_COLOR)
    
    #search for customers button
    buttons_frame = tk.Frame(master_window)
    buttons_frame.config(background=BACKGROUND_COLOR)
    buttons_frame.pack(side='top', anchor='nw')
    
    windows_frame = tk.Frame(master_window)
    windows_frame.config(background=BACKGROUND_COLOR)
    windows_frame.pack(side='left', fill='both', expand=True)
    
    
    #find customer button
    query_customer_button = ttk.Button(buttons_frame, width=20,text='Pretraga Mušterije', style='bttn_style.TButton', 
                                       command=lambda:[clear_children(), 
                                                       find_customer_window(master_window, windows_frame, database, font_style)])
    query_customer_button.pack(side='left')
    find_customer_window(master_window, windows_frame, database, font_style)
    #add new customer button
    add_customer_button = ttk.Button(buttons_frame, width=20, text='Dodaj Mušteriju', style='bttn_style.TButton', 
                                    command=lambda:[add_customer_window(master_window, windows_frame, database, font_style)])
    add_customer_button.pack(side='left')

    master_window.bind('<Escape>', lambda event:master_window.destroy())
    master_window.mainloop()

if __name__ == '__main__':
    main()