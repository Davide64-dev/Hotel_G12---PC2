#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 15:41:53 2022

@author: davideteixeira
"""

from classes.cliente_login import Cliente_login
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import ttk


class Formnovo(Toplevel):
    
    def __init__(self):
        self.root = Tk()
#ABERTURA DA JANELA
        self.root.title('Novo Usuário')                                 
        self.root.geometry('300x250+600+80')  #largura x altura+ x + y
        self.root.resizable(False, False)     #janela não expande
#root.attributes('-alpha', 0.9)  #tranparência da janela

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2,weight=1)
        self.root.columnconfigure(3,weight=1)
        
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=1)
        self.root.rowconfigure(4, weight=1)
        self.root.rowconfigure(5, weight=1)
        self.root.rowconfigure(6, weight=1)
        self.root.rowconfigure(7, weight=1)
        
        self.labelcodigo = Label(self.root, text = 'Código:')
        self.labelcodigo.grid(row = 0, column = 0)
    
        self.codigo = StringVar()
        self.entrycodigo = Entry(self.root, textvariable = self.codigo)
        self.entrycodigo.grid(row = 0, column = 1)
        
        self.labelnome = Label(self.root, text = 'Nome:')
        self.labelnome.grid(row=1, column=0)
        
        self.nome = StringVar()
        self.entrynome = Entry(self.root, textvariable = self.nome)
        self.entrynome.grid(row=1,column=1)

        
        self.label_email = Label(self.root, text = 'E-mail:')
        self.label_email.grid(row = 2, column = 0)
        
        self.email = StringVar()
        self.entryemail = Entry(self.root, textvariable = self.email)
        self.entryemail.grid(row=2, column=1)
        
        self.labeltelemovel = Label(self.root, text = 'Telemóvel:')
        self.labeltelemovel.grid(row=3, column = 0)
        
        self.telemovel = StringVar()
        self.entrytelemovel = Entry(self.root, textvariable=self.telemovel)
        self.entrytelemovel.grid(row=3, column=1)
        
        self.labellogin = Label(self.root, text = 'Login:')
        self.labellogin.grid(row = 4, column = 0)
        
        self.login = StringVar()
        self.entrylogin = Entry(self.root, textvariable = self.login)
        self.entrylogin.grid(row = 4, column = 1)
        
        self.labelpassword = Label(self.root, text = 'Password:')
        self.labelpassword.grid(row = 5, column = 0)
        
        self.password = StringVar()
        self.entrypassword = Entry(self.root, textvariable = self.password, show = '*')
        self.entrypassword.grid(row =5, column = 1)
        
        self.labelgroup = Label(self.root, text = 'Grupo:')
        self.labelgroup.grid(row=6, column = 0)
        
        self.group = StringVar()
        self.cbox_group = ttk.Combobox(self.root, textvariable=self.group)
        self.cbox_group['values'] = ['cliente', 'admin']
        self.cbox_group.grid(row=6, column = 1)
        
        self.botao = Button(self.root, text='Criar', command =self.criar)
        self.botao.grid(row = 7, column = 1)
        self.root.mainloop()
        self.entrycodigo.focus_set()
    
    def criar(self):
        codigo = self.entrycodigo.get()
        nome = self.entrynome.get()
        email = self.entryemail.get()
        telemovel = self.entrytelemovel.get()
        login = self.entrylogin.get()
        password = self.entrypassword.get()
        group = self.cbox_group.get()
        novo = Cliente_login(codigo, nome, email, telemovel, login, password, group)
        self.codigo.set('')
        self.nome.set('')
        self.email.set('')
        self.telemovel.set('')
        self.login.set('')
        self.password.set('')
        self.group.set('')
        Cliente_login.write('data/')
        self.root.destroy()
        #return novo