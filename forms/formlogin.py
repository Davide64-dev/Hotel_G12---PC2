# -*- coding: utf-8 -*-
"""
Created on 2022

@author:António Brito / Carlos Bragança

#objective: Class Formlogin to authenticate/manage users
"""
# import all components from the tkinter library
from tkinter import *
from PIL import Image, ImageTk
from classes.cliente_login import Cliente_login
from tkinter import messagebox
from forms.cliente_forms import Cliente_forms
from forms.admin_forms import Admin_forms
from forms.formnovo import Formnovo

class FormLogin(Toplevel):
    def __init__(self, root, ncols = 2, filePath = './'):
        super().__init__(root)
        self.protocol("WM_DELETE_WINDOW", self.button_cancel_click)
        root.eval(f'tk::PlaceWindow {str(self)} center')
        self.grab_set()
        self.focus()
        # Customer_login.read('data/')
        self.root = root
        self.filePath = filePath
        self.ncols = 1
        self.resizable(False,False)
        self.classObj = Cliente_login
        self.classObj.read(self.filePath)
        # Set attribute names and labels
        obj = self.classObj.first()
        self.att = self.classObj.att
        
        self.attnames =['Login:','Password:']
        # Set root title
        self.title('Login')

                
        # Frame to navegate  buttons   
        self.frame_buttons = Frame(self)
        self.frame_buttons.grid(row=2,column=0)
        
        # Frame to Edit buttons
        self.frame_edit_button = Frame(self.frame_buttons)
        self.frame_edit_button.grid(row=0,column=0, padx=10)
        # Edit Buttons  
        self.button_login = Button(self.frame_edit_button,text="Login",  command= self.button_login_click)
        self.button_cancel = Button(self.frame_edit_button,text="Cancelar",  command= self.button_cancel_click)
        self.button_create = Button(self.frame_edit_button,text="Novo",command= self.button_create_click)
        # put Edit Buttons in frame Grid
        self.button_login.grid(row=0,column=0)
        self.button_cancel.grid(row=0,column=1)
        self.button_create.grid(row=0,column=3)
        self.button_login.bind('<Return>',self.button_login_click)
        self.button_cancel.bind('<Return>',self.button_cancel_click)
        self.button_create.bind('<Return>',self.button_create_click)
        
        # Frame to class
        self.frame_class = LabelFrame(self,text = 'Login')
        self.frame_class.grid(row=1,column=0,padx=10,pady=10)
        
        
        # Creates the labels and field entries
        self.ent = list()
        r = 0
        c = 0
        for desc in self.attnames:
            lbl = Label(self.frame_class, text=desc)
            lbl.grid(row=r, column=c, padx=10, pady=10)
            c = c + 1
            if desc == 'Password:':
                ent = Entry(self.frame_class, show = '*')
            else:
                ent = Entry(self.frame_class)
            ent.grid(row=r, column=c, padx=10, pady=10)
            self.ent.append(ent)
            if c == 2 * self.ncols - 1:
                r = r + 1
                c = 0
            else:
                c = c + 1

        Cliente_login.username = ''
        self.ent[0].focus_set()
        # Let the root wait for any events
        self.mainloop()
    
    def cleanForm(self):
        # clean all entrys
        for ent in self.ent:
            ent.config(state='normal')
            ent.delete(0, 'end')
    
    def button_login_click(self,event=None):
        
        loginIn = self.ent[0].get()
        passwordIn = str(self.ent[1].get())
        
        if Cliente_login.chk_password(loginIn, passwordIn) == 'valid':
            if Cliente_login.login_list[loginIn].group == 'cliente':
                Cliente_login.login = loginIn
                formcliente = Cliente_forms(loginIn)
                self.destruir()
            else:
                Cliente_login.login = loginIn
                formadmin = Admin_forms(loginIn)
                self.destruir
            

    def button_cancel_click(self,event=None):
       Cliente_login.login = ''
       self.destroy()
       self.root.destroy()
    
    def button_create_click(self,event=None):
        cria = Formnovo()       
    
    def destruir(self):
        self.destroy()
        self.root.destroy()