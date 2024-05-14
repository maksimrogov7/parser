import parseWB
import parseItemWb
import pandas as pd
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import csv
import os
import shutil

def change(*args):
    if combobox.get() == marketplaces[0]:
        combobox1.config(values=actionsWb)
    elif combobox.get() == marketplaces[1]:
        combobox1.config(values=actionsOZ)

def ParseCommand():
    messagebox.showinfo(title='Parse', message='Выполняется')
    if combobox1.get() == actionsWb[0]:
        parseItemWb.Parser(UrlEntry.get()).parse()
        read_file = pd.read_csv('data.csv')
        read_file.to_excel('data.xlsx', index=None, header=True)
        combobox2.config(values=download2)
    elif combobox1.get() == actionsWb[1]:
        parseWB.ParserSearch(UrlEntry.get()).parse()
        read_file = pd.read_csv('data.csv')
        read_file.to_excel('data.xlsx', index=None, header=True)
        read_file = pd.read_csv('statistics.csv')
        read_file.to_excel('statistics.xlsx', index=None, header=True)
        combobox2.config(values=download1)
    elif combobox1.get() == actionsWb[2]:
        parseWB.ParserBrand(UrlEntry.get()).parse()
        read_file = pd.read_csv('data.csv')
        read_file.to_excel('data.xlsx', index=None, header=True)
        read_file = pd.read_csv('statistics.csv')
        read_file.to_excel('statistics.xlsx', index=None, header=True)
        combobox2.config(values=download1)
    elif combobox1.get() == actionsWb[3]:
        parseWB.ParserSeller(UrlEntry.get()).parse()
        read_file = pd.read_csv('data.csv')
        read_file.to_excel('data.xlsx', index=None, header=True)
        read_file = pd.read_csv('statistics.csv')
        read_file.to_excel('statistics.xlsx', index=None, header=True)
        combobox2.config(values=download1)




def save_file():
    #data = [('All tyes(*.*)', '*.*'), ("csv file(*.csv)", "*.csv")]
    #file = filedialog.asksaveasfilename(filetypes=data, defaultextension=data)

    saveHere = filedialog.askdirectory(initialdir='/', title='Select File')
    shutil.copy(combobox2.get(), saveHere)





root = Tk()
root.title('ParserApp')
root.geometry('800x400')
root.resizable(False, False)



actionsWb = ['Информация о товаре', 'Список товаров поискового запроса', 'Список товаров бренда', 'Список товаров продавца']
actionsOZ = []
download1=['data.csv', 'data.xlsx', 'statistics.csv', 'statistics.xlsx']
download2 = ['data.csv', 'data.xlsx', 'dataPrice.csv']

marketplaces = ['Wildberies', 'Ozon']
combobox = ttk.Combobox(values=marketplaces)
combobox1 = ttk.Combobox(values=None, width=35)
UrlEntry = Entry(bg='lightgrey', width=65)
combobox.bind("<<ComboboxSelected>>", change)
combobox.grid(column=0, row=0, padx=5, pady=10)
combobox1.grid(column=1, row=0, padx=5, pady=10)
UrlEntry.grid(column=2, row=0, padx=5, pady=10)

ButtonParse = Button(bg= 'lightgrey', text='Выполнить', command = ParseCommand)
ButtonParse.place(relx=.5, rely=.2, anchor=CENTER)

label1 = Label(text= 'Выберите файл для сохранения  ',bg='lightgrey')
label1.place(relx=.22, rely=.4, anchor=CENTER)
combobox2 = ttk.Combobox(values=None, width=35)
combobox2.place(relx=.48, rely=.4, anchor=CENTER)
ButtonDownload = Button(bg= 'lightgrey', text='Сохранить', command= save_file)
ButtonDownload.place(relx=.67, rely=.4, anchor=CENTER)


root.mainloop()