import csv
import os
import sys
import shutil
import re
import decimal
import webbrowser
import pandas as pd 
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import tkinter.font as tkFont

#check if /jobs/ data directory exists, create new if not

JOBS_STORAGE_PATH = ''
if getattr(sys, 'frozen', False):
    JOBS_STORAGE_PATH = sys._MEIPASS
else:
    JOBS_STORAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__) + '\jobs'))
    JOBS_STORAGE_PATH = JOBS_STORAGE_PATH + '\\'
if not os.path.isdir(JOBS_STORAGE_PATH):
    os.mkdir(JOBS_STORAGE_PATH)
print(JOBS_STORAGE_PATH)

ARCHIVE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__) + '\\archive\\'))
ARCHIVE_PATH = ARCHIVE_PATH + '\\'
if not os.path.isdir(ARCHIVE_PATH):
    os.mkdir(ARCHIVE_PATH)
print(ARCHIVE_PATH)

BACKGROUND_COLOR = 'gray'
FOREGROUND_COLOR = 'white'
#needed global for adding new workorders
ENTRY_COUNTER = 0
CUSTOMER_VALUES = []

#CLASSES
#################################################################################################
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

    def delete(self):
        self.add_text.delete(0, 'end')

#base class for autocomplete entry widget // UNUSED
# class AutocompleteTemplate(object):
#     def __init__(self, label_name, frame, font_style, database) -> None:
#         self.label_name = label_name
#         self.frame = frame
#         self.font_style = font_style
#         self.database = database
        
#         ttk.Label(self.frame, font=self.font_style, text=self.label_name, background=BACKGROUND_COLOR).pack(side='top')
#         self.autocomplete = autocomplete.AutocompleteCombobox(self.frame, width=30, completevalues=self.database, font=self.font_style, justify='center')
#         self.autocomplete.option_add('*Tcombobox*Listbox.Justify', 'center')
#         self.autocomplete.pack(side='top', pady=(5,0))
        
#     def get_text(self):
#         return self.autocomplete.get()
    
#     def set_text(self, text:str):
#         return self.autocomplete.set(text)
    
#     def clear(self):
#         self.autocomplete.set('')
    
#base class for treeview widget
class TreeviewTemplate(object):
    def __init__(self, treeview_frame, columns, style):
        self.treeview_frame = treeview_frame
        self.columns = columns
        self.style = style
        self.previous_bind = None
        
        self.treeview = ttk.Treeview(treeview_frame, columns=columns, show='headings', style='mystyle.Treeview')
        self.treeview.config()
        
        if self.columns is not None:
            for column in self.columns:
                self.treeview.heading(column, text=column)
                self.treeview.column(column, anchor='center')
            
        self.scrollbar = tk.Scrollbar(treeview_frame, orient='vertical', command=self.treeview.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.treeview.config(yscrollcommand=self.scrollbar.set)
        
        self.treeview.pack(side='left', fill='both', expand=True)
    
    def insert(self, location, values, tag):
        self.treeview.insert(location, 0, values=values, tags=tag)
        
    def clear(self):
        self.treeview.delete(*self.treeview.get_children())
        
    def delete(self, customer_folder):
        if not os.path.isdir(f"{ARCHIVE_PATH}{customer_folder}"):
            os.mkdir(f"{ARCHIVE_PATH}{customer_folder}")

        if self.treeview.selection() != ():
            #shutil.move()
            file_to_move = f"{customer_folder}\{self.treeview.item(self.treeview.selection()[0])['values'][0].replace('.','_')}.csv"
            file_for_rename = f"{customer_folder}\{self.treeview.item(self.treeview.selection()[0])['values'][0].replace('.','_')}_0.csv"
            while os.path.isfile(ARCHIVE_PATH + file_for_rename):
                #print(file_for_rename)
                sub = re.findall(r'\)_(.*)\.', file_for_rename)
                number_of_copy = str(int(sub[0])+1)
                file_for_rename = re.sub(r'\)_(.*)\.', f')_{number_of_copy}.', file_for_rename)
            else:
                os.rename(JOBS_STORAGE_PATH + file_to_move, JOBS_STORAGE_PATH + file_for_rename)
                shutil.move(JOBS_STORAGE_PATH + file_for_rename, ARCHIVE_PATH + file_for_rename)
            self.treeview.delete(self.treeview.selection()[0])
        
    def bind_key(self, sequence, function):
        self.previous_bind = self.treeview.bind(sequence=sequence, func=function)

    def previous_bind_get(self):
        return self.previous_bind
    
    def remove_current_bind(self, string):
        self.treeview.unbind(string)
        
    def return_selection(self):
        if not self.treeview.selection():
            messagebox.showerror('Upozorenje!', 'Niste označili polje!')
            return None
        else:
            return self.treeview.item(self.treeview.selection()[0])

    def get_selected_row_number(self):
        if not self.treeview.selection():
            messagebox.showerror('Upozorenje!', 'Niste označili polje!')
            return None
        return self.treeview.index(self.treeview.selection()[0])
    
    def return_total(self):
        total = 0
        for child in self.treeview.get_children():
            total += decimal.Decimal(self.treeview.set(child, 'Ukupno[KM]'))
        return total

#base class for adding new workorder frame widgets
class WorkorderRowTemplate(object):
    def __init__(self, main_frame, font_style, row, width):
        self.main_frame = main_frame
        self.font_style = font_style
        self.row = row
        self.width = width
        
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
        
        self.part_entry = EntryTemplate('Materijal', self.part_frame, font_style, ('top', (5,0)), 'left', width=self.width)
        self.brand_entry = EntryTemplate('Marka', self.brand_frame, font_style, ('top', (5,0)), 'left', width=self.width)
        self.price_entry = EntryTemplate('Cijena[KM]', self.price_frame, font_style, ('top', (5,0)), 'left', width=self.width)
        self.amount_entry = EntryTemplate('Količina', self.amount_frame, font_style, ('top', (5,0)), 'left', width=self.width)
        self.total_entry = EntryTemplate('Ukupno[KM]', self.total_frame, font_style, ('top', (5,0)), 'left', width=self.width)
        self.total_entry.set_state(False)
    
    def calculate_total(self):
        if self.price_entry.get_text() != '' and self.amount_entry.get_text() != '':
            if self.price_entry.get_text().replace('.','').isdigit() and self.amount_entry.get_text().replace('.','').isdigit():
                total = self.price_entry.get_text() + '*' + self.amount_entry.get_text()
                total = round(eval(total), 2)
                self.total_entry.set_state(True)
                self.total_entry.set_text(str(total))
                self.total_entry.set_state(False)
                return True
            else:
                return False

    def get_all_values(self):
        if self.part_entry.get_text() != '' or self.brand_entry.get_text() != '' or self.price_entry.get_text() != '' or self.amount_entry.get_text() != '':
            checker = self.calculate_total()          
            if checker:    
                return [self.part_entry.get_text().strip().title(), 
                        self.brand_entry.get_text().strip().title(), 
                        self.price_entry.get_text(), 
                        self.amount_entry.get_text(), 
                        self.total_entry.get_text()]
            else:
                messagebox.showerror("Upozorenje!", f"U polja \"Cijena\" i \"Količina\" možete unijeti samo brojeve!", parent=self.main_frame)
                return None
        else:
            return None
    
    def insert_values(self, selection):
        self.part_entry.set_text(selection['values'][0])
        self.brand_entry.set_text(selection['values'][1])
        self.price_entry.set_text(selection['values'][2])
        self.amount_entry.set_text(selection['values'][3])
        self.calculate_total()
#################################################################################################

       
#HELPER FUNCTIONS
#################################################################################################
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
        
#clear children help function
def clear_children(frame_one, frame_two):
        list_of_slaves = frame_one.pack_slaves()
        for frame in list_of_slaves:
            if '!frame' in str(frame):
                frame.destroy()
        
        list_of_slaves = frame_two.pack_slaves()
        for frame in list_of_slaves:
            if '!frame' in str(frame):
                frame.destroy()

#helper function to fill the workorder tree    
def fill_workorder_tree(name, reg, tree):
    if name != '' and reg != '':
        csv_file_path = name.lower().replace(' ', '') + '_' + reg.upper().replace(' ','')
        
        directory_contents = os.listdir(f'{JOBS_STORAGE_PATH}{csv_file_path}') 
        
        parts = []
        total_price = 0
        for csv_file in directory_contents:
            with open(f'{JOBS_STORAGE_PATH}{csv_file_path}\\{csv_file}', 'r', encoding='utf-8') as file:
                reader = csv.reader(file)           
                for row in list(reader)[1:]:
                    if row != '':
                        parts.append(row[0]+',')
                        total_price += (decimal.Decimal(row[4]))  
                parts[-1] = parts[-1][:-1]  
            tree.insert('', [csv_file.replace('.csv', '').replace('_', '.'), ' '.join(parts), str(total_price)], tag='folder')
            parts = []
            total_price = 0
            
def csv_to_html(parent_window, file_location, work_price, total_value, CUSTOMER_VALUES):
    if work_price is None or work_price == "":
        messagebox.showerror("Upozorenje!", "Potrebno je unijeti cijenu rada!", parent=parent_window)
        return None
    
    if work_price.isnumeric() is False:    
        messagebox.showerror("Upozorenje!", "U polje \"Rad\" možete unijeti samo brojeve.", parent=parent_window)
        return None
    
    dataframe = pd.read_csv(file_location)
    pd.set_option('colheader_justify', 'center')
    
    html_string_table_header = ''' 
    <html>
        <head><title>Predračun</title></head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <link rel="stylesheet" type="text/css" href="table_style.css"/>
        <body>
            <div>
                <div class="inline-block">
                    <img src="logo.png">
                    <img src="kontakt.png">
                </div>
            </div>
            <center class="dataframe fontstyle"><strong>PREDRAČUN</strong></center>
            {customer_data}
            {to_browser}
            {second_html_table}
            {third_html_table}
        </body>
    </html>
    '''
    
    customer_data = '''
            <table border="1" class="dataframe customerstyle">
    <thead>
        <tr style="text-alight: left;">
        <th>IME I PREZIME</th>
        <th>{customer_name}</th>
    </thead>
    <tbody>
        <tr>
        <td>MARKA I MODEL VOZILA</td>
        <td>{customer_car}</td>
        </tr>
        <tr>
        <td>REGISTARSKI BROJ</td>
        <td>{customer_reg}</td>
        </tr>
    </tbody>
    '''
    
    second_html_table = '''
            <table border="1" class="dataframe mystyle">
    <thead>
        <tr style="text-align: center;">
        <th>RAD[KM]</th>
        <th>DIJELOVI TOTAL[KM]</th>
        </tr>
    </thead>
    <tbody>
        <tr>
        <td>{work_price}</td>
        <td>{total_price}</td>
        </tr>
    </tbody>
    '''
    third_html_table = '''
            <table border="1" class="dataframe mystyle">
    <thead>
        <tr style="text-align: center;">
        <th>TOTAL CIJENA[KM]</th>
        </tr>
    </thead>
    <tbody>
        <tr>
        <td>{final_price}</td>
        </tr>
    </tbody>
    '''
    
    with open('data.html', 'w', encoding='utf-8') as f:
        f.write(html_string_table_header.format(customer_data=customer_data.format(customer_name=CUSTOMER_VALUES[0], customer_car=CUSTOMER_VALUES[1], customer_reg=CUSTOMER_VALUES[2]), to_browser=dataframe.to_html(classes=['mystyle'], index=False), 
                                                second_html_table=second_html_table.format(work_price=work_price, total_price=total_value),
                                                third_html_table=third_html_table.format(final_price=decimal.Decimal(work_price)+decimal.Decimal(total_value))))
        
    webbrowser.open('data.html', new=1)
    
#################################################################################################

#FRAME CREATIONG FUNCTIONS
#################################################################################################
#new window tree fill from selected csv with hands price entry, button to convert to PDF
def workorder_for_printing(parent_window, font_style, tree_style, selected_file, customer_name, CUSTOMER_VALUES):
    if not selected_file:
        return None
    
    #help loop for window refresh
    for child in parent_window.winfo_children():
        if child.winfo_class() == 'Toplevel':
            child.destroy()
    
    #modification of csv for printing   
    def modify_csv_entry(selection, edited_values):
        if edited_values is None:
            return None
        turned_string = []
        for item in selection['values']:
            turned_string.append(str(item))
        index = estimate_tree.get_selected_row_number()
        with open(file_location, 'r', encoding='utf-8') as mod_file:
            mod_reader = csv.reader(mod_file)
            file_holder = list(mod_reader)[1:]
            file_holder.remove(turned_string)
            file_holder.insert(index, edited_values)

        with open(file_location, 'w', newline='', encoding='utf-8') as edited_file:
            edit_writer = csv.writer(edited_file)
            edit_writer.writerow(['materijal', 'marka', 'cijena[KM]', 'količina', 'ukupno[KM]'])
            for row in reversed(file_holder):
                edit_writer.writerow(row)
    
    #frame for modification of csv file which takes and returns values
    def edit_selection(selection):
        if selection is None:
            return None

        if len(button_frame.winfo_children()) == 4:
            button_frame.winfo_children()[-1].destroy()
            button_frame.winfo_children()[-1].destroy()
            
        if len(button_frame.winfo_children()) < 3:
            selection_frame = tk.Frame(button_frame)
            selection_frame.pack(side='left')
            
            mod_button_frame = tk.Frame(button_frame)
            mod_button_frame.pack(side='bottom')
            
            selection_for_edit = WorkorderRowTemplate(selection_frame, font_style, 0, 10)
            selection_for_edit.total_frame.grid_forget()
            selection_for_edit.insert_values(selection)
            
            modify_button = ttk.Button(mod_button_frame, width=20, text='Modifikuj', style='bttn_style.TButton', 
                                    command=lambda:[modify_csv_entry(estimate_tree.return_selection(),selection_for_edit.get_all_values()), printing_frame.destroy(),
                                                    workorder_for_printing(parent_window, font_style, tree_style, selected_file, customer_name, CUSTOMER_VALUES)])
            modify_button.pack(side='bottom', anchor='se')
            
            estimate_tree.bind_key('<Double-Button-1>', lambda event:edit_selection(estimate_tree.return_selection()))
            
    
    file_for_printing = selected_file['values'][0].replace('.','_') + '.csv'
    file_location = f'{JOBS_STORAGE_PATH}{customer_name}\{file_for_printing}'
    
    
    printing_frame = tk.Toplevel(parent_window)
    printing_frame.geometry('+5+5')
    printing_frame.config(background=BACKGROUND_COLOR, highlightbackground='black', highlightcolor='black', highlightthickness=2)
    
    treeview_frame = tk.Frame(parent_window)
    treeview_frame.pack(side='top')
    
    button_frame = tk.Frame(printing_frame)
    button_frame.config(background=BACKGROUND_COLOR, highlightbackground='black', highlightcolor='black', highlightthickness=2)
    button_frame.pack(side='bottom', fill='x')
    
    work_entry_frame = tk.Frame(printing_frame)
    work_entry_frame.config(background=BACKGROUND_COLOR)
    work_entry_frame.pack(side='bottom', anchor='w')
    
    edit_button_frame = tk.Frame(button_frame)
    edit_button_frame.config(background=BACKGROUND_COLOR)
    edit_button_frame.pack(side='left', fill='x')
    
    print_button_frame = tk.Frame(button_frame)
    print_button_frame.config(background=BACKGROUND_COLOR)
    print_button_frame.pack(side='left', fill='x')
    
    estimate_columns = ('Materijal', 'Marka', 'Cijena[KM]', 'Količina', 'Ukupno[KM]')
    
    estimate_tree = TreeviewTemplate(printing_frame, estimate_columns, tree_style)
    estimate_tree.remove_current_bind('<Double-Button-1>')
    estimate_tree.bind_key('<Double-Button-1>', lambda event:edit_selection(estimate_tree.return_selection()))
    
    edit_button = ttk.Button(edit_button_frame, width=20, text='Modifikovanje', style='bttn_style.TButton', 
                             command=lambda:[edit_selection(estimate_tree.return_selection())])
    edit_button.pack(side='left', anchor='sw')
    
    print_button = ttk.Button(print_button_frame, width=20, text='Printanje', style='bttn_style.TButton',
                              command=lambda:[csv_to_html(printing_frame, file_location, work_amount_entry.get_text(), 
                                                          estimate_tree.return_total(), CUSTOMER_VALUES)])
    print_button.pack(side='left', anchor='sw')
    
    work_amount_entry = EntryTemplate('Rad', work_entry_frame, font_style, ('left', (5, 0)), 'left', 20)
    km_label = ttk.Label(work_entry_frame, font=font_style, text='BAM', background=BACKGROUND_COLOR)
    km_label.pack(side='left')

    with open(file_location, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in list(reader)[1:]:
            estimate_tree.insert('',row,tag='estimate')
            
#add work order, create csv for workorder       
def new_workorder(master_window, parent_window, database, font_style, csv_folder):
    
    main_frame = tk.Toplevel(parent_window)
    main_frame.config(background=BACKGROUND_COLOR, highlightbackground='black', highlightcolor='black', highlightthickness=2)
    
    child_frame = tk.Frame(main_frame)
    child_frame.config(background=BACKGROUND_COLOR, highlightbackground='black', highlightcolor='black', highlightthickness=2)
    child_frame.grid()
    
    #necessary file paths and variables
    todays_date = datetime.date.today().strftime('%d_%m_%Y')
    length_of_customer_directory = 0
    date_file_name = f'{todays_date}({length_of_customer_directory}).csv'
    
    def filename_number(filename, length):
        storage = ''
        if filename not in os.listdir(JOBS_STORAGE_PATH + csv_folder):
            return filename
        else:
            storage = filename_number(f'{todays_date}({length+1}).csv', length+1)
            return storage

    file_path = f'{JOBS_STORAGE_PATH}{csv_folder}\\{filename_number(date_file_name, length_of_customer_directory)}'
    
    length_of_customer_directory = 0
    
    #first entry form when window is called
    entry_list = []
    global ENTRY_COUNTER
    first_entry = WorkorderRowTemplate(child_frame, font_style, ENTRY_COUNTER, 20)
    entry_list.append(first_entry)

    #increment global counter for adding new forms
    def increment_counter():
        global ENTRY_COUNTER
        ENTRY_COUNTER += 1

    #create new part form
    add_new_entry_button = ttk.Button(child_frame, width=3, text='+', style='bttn_style.TButton', 
                                    command=lambda:[increment_counter(), 
                                                    entry_list.append(WorkorderRowTemplate(child_frame, font_style, ENTRY_COUNTER, 20)), 
                                                    main_frame.update(),
                                                    insert_button_frame.grid(row=ENTRY_COUNTER+1, column=5, sticky='se'),
                                                    cancel_button_frame.grid(row=ENTRY_COUNTER+1, column=4, sticky='se')])
    add_new_entry_button.grid(row=0, column=0)
    
    #calculate totals of price and amount fileds
    def calculate_totals(list_of_workorders):
        for entry in list_of_workorders:
            entry.calculate_total()
    
    #modify global counter variable
    def set_counter_to_zero():
        global ENTRY_COUNTER
        ENTRY_COUNTER = 0
        main_frame.destroy()
    
    #create and populate a new CSV file    
    def populate_csv(list_of_workorders):
        if not os.path.isfile(file_path) and csv_folder != '_':
            with open(file_path, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['materijal', 'marka', 'cijena[KM]', 'količina', 'ukupno[KM]'])
                for row in list_of_workorders:
                    if row.get_all_values() is not None:
                        writer.writerow(row.get_all_values())
        else:
            messagebox.showwarning("Upozorenje.", "Predračun već postoji.", parent=main_frame)
            return None

    def make_new_workorder():
        for item in entry_list:
            if item.get_all_values() is None:
                messagebox.showerror("Upozorenje.", "Potrebna polja nisu popunjena.", parent=main_frame)
                return None
        populate_csv(entry_list)
        parent_window.focus_set()
        parent_window.event_generate('<Return>') 
        set_counter_to_zero()
        main_frame.destroy()
    
    #button to create and populate a new CSV file
    insert_button_frame = tk.Frame(child_frame)
    insert_button_frame.config(background=BACKGROUND_COLOR, highlightbackground='black', highlightcolor='black', highlightthickness=2)
    insert_button_frame.grid(row=ENTRY_COUNTER+1, column=5, sticky='se', pady=(3, 0))
    
    insert_contents_button = ttk.Button(insert_button_frame, text="Otvori novi predračun", width=19, style='bttn_style.TButton', 
                                 command=lambda:[make_new_workorder()])
    insert_contents_button.grid()
    
    
    #cancel workorder button
    cancel_button_frame = tk.Frame(child_frame)
    cancel_button_frame.config(background=BACKGROUND_COLOR, highlightbackground='black', highlightcolor='black', highlightthickness=2)
    cancel_button_frame.grid(row=ENTRY_COUNTER+1, column=4, sticky='se', pady=(3, 0))
    
    cancel_contents_button = ttk.Button(cancel_button_frame, text="Odustani", width=19, style='bttn_style.TButton', 
                                 command=lambda:set_counter_to_zero())
    cancel_contents_button.grid()
    
    
    #destroy main frame and calculate prices for workorder on bind press
    main_frame.focus_set()
    main_frame.bind('<Return>', lambda event:calculate_totals(entry_list))
    main_frame.bind('<Escape>', lambda event:main_frame.destroy())
    main_frame.protocol('WM_DELETE_WINDOW', set_counter_to_zero)

#FIND CUSTOMER ADD NEW WORK TO EXISTING WORK FILE
def find_customer_window(master_window, parent_window, parent_window2, database, font_style, tree_style):
    global CUSTOMER_VALUES
    #delete workorder
    def delete_workorder():
        tree_jobs.delete(f"{name_autocomplete.get_text().lower().replace(' ', '')}_{reg_autocomplete.get_text().upper().replace(' ','')}")
    
    #fill customer tree
    def fill_from_database():
        tree_jobs.clear()
        global CUSTOMER_VALUES
        CUSTOMER_VALUES = []
        selected = tree_customer_database.treeview.selection()
        if selected != ():
            selected_list = tree_customer_database.treeview.item(selected[0])['values'][0].split(':')
        
            with open('data.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['ime'] == selected_list[0].replace('_', ' ') and row['reg_broj'] == selected_list[1].replace('_', ' '):
                        name_autocomplete.set_text(row['ime'])
                        car_autocomplete.set_text(row['vozilo'])
                        reg_autocomplete.set_text(row['reg_broj'])
                        
                        CUSTOMER_VALUES.append(name_autocomplete.get_text())
                        CUSTOMER_VALUES.append(car_autocomplete.get_text())
                        CUSTOMER_VALUES.append(reg_autocomplete.get_text())
                        
                        fill_workorder_tree(name_autocomplete.get_text(), reg_autocomplete.get_text(), tree_jobs)
    
    #customer treeview
    customer_database_columns = ['Mušterija']
    
    tree_customer_database = TreeviewTemplate(parent_window2, customer_database_columns, tree_style)
    tree_customer_database.bind_key('<Double-Button-1>', lambda event:fill_from_database())
    
    for column in customer_database_columns:
        tree_customer_database.treeview.column(column, width=250)
    
    with open('data.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tree_customer_database.insert('', f"{row['ime'].replace(' ', '_')}:{row['reg_broj'].replace(' ','_')}", 'None')
    
    #name, car, registration number
    fields_frame = tk.Frame(parent_window)
    fields_frame.config(background=BACKGROUND_COLOR, highlightbackground='black', highlightcolor='black', highlightthickness=2)
    fields_frame.pack(side='left', expand=True, fill='both')
    
    name_autocomplete = EntryTemplate('Ime i Prezime', fields_frame, font_style, ('top', (5,0)), 'top', width=30)
    car_autocomplete = EntryTemplate('Vozilo', fields_frame, font_style, ('top', (5,0)), 'top', width=30)
    reg_autocomplete = EntryTemplate('Registracija', fields_frame, font_style, ('top', (5,0)), 'top', width=30)
    
    #Repair list, treeview, scrollbar
    treeview_frame = tk.Frame(fields_frame)
    treeview_frame.config(background=BACKGROUND_COLOR, highlightbackground='black', highlightcolor='black', highlightthickness=2)
    treeview_frame.pack(side='top', fill='both', expand=True, pady=(10,0))
    
    tree_columns = ('Datum', 'Dijelovi', 'Ukupna Cijena[KM]')
    
    tree_jobs = TreeviewTemplate(treeview_frame, tree_columns, tree_style)
    tree_jobs.bind_key('<Double-Button-1>', 
                       lambda event:workorder_for_printing(parent_window, 
                                                           font_style, 
                                                           tree_style,
                                                           tree_jobs.return_selection(), 
                                                           f'{name_autocomplete.get_text().lower().replace(" ","")}_{reg_autocomplete.get_text().upper().replace(" ","")}',
                                                           CUSTOMER_VALUES))
    
    #check if data is entered in customer query
    def is_data_entered(name, car, reg):
        if name == '' or car == '' or reg == '':
            messagebox.showerror('Upozorenje!', 'Ne možete unijeti novi predračun bez pronađene mušterije.')
            return None
        new_workorder(master_window, 
                      fields_frame, 
                      database, 
                      font_style, 
                      name_autocomplete.get_text().lower().replace(' ', '') + '_' + reg_autocomplete.get_text().upper().replace(' ',''))
    
    #binds and buttons
    #add new workorder button
    buttons_frame_add = tk.Frame(fields_frame)
    buttons_frame_add.config(background=BACKGROUND_COLOR, highlightbackground='black', highlightcolor='black', highlightthickness=2)
    buttons_frame_add.pack(side='right', anchor='nw') 
    
    open_workorder_button = ttk.Button(buttons_frame_add, width=20,text='Otvori Predračun', style='bttn_style.TButton',
                                       command=lambda:workorder_for_printing(parent_window, font_style, tree_style, 
                                        tree_jobs.return_selection(), f'{name_autocomplete.get_text().lower().replace(" ","")}_{reg_autocomplete.get_text().upper().replace(" ","")}',
                                        CUSTOMER_VALUES))
    open_workorder_button.pack(side='right')
    
    add_new_workorder_button = ttk.Button(buttons_frame_add, width=20,text='Novi Predračun', style='bttn_style.TButton', 
                                   command=lambda:is_data_entered(name_autocomplete.get_text(), car_autocomplete.get_text(), reg_autocomplete.get_text()))
    add_new_workorder_button.pack(side='right')
    
    #delete selection button
    buttons_frame_delete = tk.Frame(fields_frame)
    buttons_frame_delete.config(background=BACKGROUND_COLOR, highlightbackground='black', highlightcolor='black', highlightthickness=2)
    buttons_frame_delete.pack(side='left', anchor='ne')
    
    delete_workorder_button = ttk.Button(buttons_frame_delete, width=20,text='Obriši Predračun', style='bttn_style.TButton', 
                                   command=lambda:delete_workorder())
    delete_workorder_button.pack(side='top', anchor='nw')
    
#ADD CUSTOMER AND CREATE WORK DATA FILE
def add_customer_window(master_window, parent_window, parent_window2, database, font_style, tree_style):
    
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

        for slave in parent_window.pack_slaves():
            slave.destroy()

        for slave in parent_window2.pack_slaves():
            slave.destroy()
            
        find_customer_window(master_window, parent_window, parent_window2, database, font_style, tree_style)
        add_customer_frame.destroy()
    
    #frame for adding new customers to the database    
    add_customer_frame = tk.Frame(parent_window)
    if len(parent_window.pack_slaves()) > 1:
        slave_list = parent_window.pack_slaves()
        slave_list[1].destroy()
    add_customer_frame.config(background=BACKGROUND_COLOR, highlightbackground='black', highlightcolor='black', highlightthickness=2)
    add_customer_frame.pack(side='right', anchor='ne')

    master_window.bind('<Return>', lambda event:add_to_csv())
    
    #Add new user to database
    name_entry = EntryTemplate('Ime i Prezime', add_customer_frame, font_style, ('top', (5,0)), 'top', width=30)
    car_entry = EntryTemplate('Vozilo', add_customer_frame, font_style, ('top', (5,0)), 'top', width=30)
    reg_entry = EntryTemplate('Registracija', add_customer_frame, font_style, ('top', (5,0)), 'top', width=30)
    
    confirm_button = ttk.Button(add_customer_frame, text='Unos u Bazu', width=20, style='bttn_style.TButton', command=add_to_csv)
    confirm_button.pack(side='top', pady=(5, 5))
#################################################################################################

#MAINLOOP
#################################################################################################
def main():
    #store data from csv in cache for use
    database = DataVariables()
    database.parse_data()
    
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
    bttn_style.theme_use('default')
    bttn_style.configure('bttn_style.TButton', font=font_style, background='Light Gray')
    
    #style for treeview
    tree_style = ttk.Style()
    tree_style.theme_use('default')
    tree_style.configure('Treeview.Heading', font=font_style, background='Light Gray')
    tree_style.configure('mystyle.Treeview', font=font_style)
    
    #search for customers button
    buttons_frame = tk.Frame(master_window)
    buttons_frame.config(background=BACKGROUND_COLOR, highlightbackground='black', highlightcolor='black', highlightthickness=2)
    buttons_frame.pack(side='top', anchor='ne')

    windows_frame2 = tk.Frame(master_window)
    windows_frame2.config(background='blue')
    windows_frame2.pack(side='left', fill='y')

    windows_frame = tk.Frame(master_window)
    windows_frame.config(background=BACKGROUND_COLOR)
    windows_frame.pack(side='left', fill='both', expand=True)
    
    
    #find customer button
    query_customer_button = ttk.Button(buttons_frame, width=20,text='Pretraga Mušterije', style='bttn_style.TButton', 
                                       command=lambda:[clear_children(windows_frame, windows_frame2), 
                                                       find_customer_window(master_window, windows_frame, windows_frame2, database, font_style, tree_style)])
    query_customer_button.pack(side='right')
    find_customer_window(master_window, windows_frame, windows_frame2, database, font_style, tree_style)
    
    #add new customer button
    add_customer_button = ttk.Button(buttons_frame, width=20, text='Dodaj Mušteriju', style='bttn_style.TButton', 
                                    command=lambda:[add_customer_window(master_window, windows_frame, windows_frame2, database, font_style, tree_style)])
    add_customer_button.pack(side='right')

    master_window.bind('<Escape>', lambda event:master_window.destroy())
    master_window.mainloop()
#################################################################################################

if __name__ == '__main__':
    main()