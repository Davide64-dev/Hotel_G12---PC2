# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 10:02:10 2022

@author: dcout
"""

# import all components from the tkinter library
from tkinter import *
from tkinter import ttk
# imports the child window class
from forms.openformtablelink import OpenFormTableLink
from classes.cliente_login import Cliente_login
from classes.reserva import Reserva

class AbrirAdminReservas(Toplevel):
    def __init__(self, root, classObj, attnames, classObjLink = None,  
                 attnamesLink = [], ncols = 2, filePath = './', editmode = 1):
        super().__init__(root)
        self.root = root
        # Defines the main and child classes
        self.classObj = classObj
        self.classObjLink = classObjLink
        # Associate the <escape> key to exit window app_end()
        self.bind('<Escape>', self.app_end)
        self.att = self.classObj.att + ['_custo']
        self.filePath = filePath
        self.attnames =attnames
        self.attnamesLink =attnamesLink
        self.ncols = ncols
        self.editmode = editmode
        self.ocuparr=0
        # Set root title
        self.title(self.classObj.__name__)
        # Create the window widgets
        self.create_frames()
        self.create_buttons()
        self.create_entries()
        # display the firs record
        self.config_mode("Show")
        self.first()
        # start the application loop
        self.mainloop()

    def create_frames(self):
        # Frame to navegate  buttons   
        self.frame_buttons = Frame(self)
        self.frame_buttons.grid(row=0,column=0)
        # Frame to Move buttons
        self.frame_move_button = Frame(self.frame_buttons)
        self.frame_move_button.grid(row=0,column=1, padx=10)
        # Frame to Edit buttons
        self.frame_edit_button = Frame(self.frame_buttons)
        self.frame_edit_button.grid(row=0,column=0, padx=10)
        # Frame to class
        self.frame_class = LabelFrame(self,text = self.classObj.__name__)
        self.frame_class.grid(row=2,column=0,padx=10,pady=10)
        
    def create_buttons(self):
        # creates the buttons
        self.btn_first = Button(self.frame_move_button, text='<<', command = self.first)
        self.btn_back = Button(self.frame_move_button, text='<', command = self.back)
        self.btn_next = Button(self.frame_move_button, text='>', command = self.nextrec)
        self.btn_last = Button(self.frame_move_button, text='>>', command = self.last)
        self.btn_first.grid(row=0,column=0)
        self.btn_back.grid(row=0,column=1)
        self.btn_next.grid(row=0,column=2)
        self.btn_last.grid(row=0,column=3)

        
        self.btn_delete = Button(self.frame_edit_button, text='Eliminar', command = self.delete)
        self.btn_insert = Button(self.frame_edit_button, text='Inserir', command = self.insert)
        self.btn_save = Button(self.frame_edit_button, text='Guardar', command = self.save)
        self.btn_cancel = Button(self.frame_edit_button, text='Cancelar', command = self.cancel)
        self.btn_ok = Button(self.frame_edit_button, text='OK', command = self.ok)
      
        self.btn_delete.grid(row=0,column=2)
        self.btn_insert.grid(row=0,column=3)
        self.btn_save.grid(row=0,column=4)
        self.btn_cancel.grid(row=0,column=5)
        self.btn_ok.grid(row=0,column=6)

        
        self.btn_exit = Button(self.frame_buttons,text="Fechar",command=self.app_end)
        self.btn_exit.grid(row=0,column=3,padx=10)

        if self.classObjLink:
            # open lines Button if child window exists
            text = "Serviços Associados"
            self.btn_openlines = Button(self.frame_buttons,text=text,command= self.openlines)
            self.btn_openlines.grid(row=0,column=2,padx=10)

    def create_entries(self):
        # Creates the labels and field entries
        self.ent = list()
        i = 0
        r = 0
        c = 0
        for desc in self.attnames:
            lbl = Label(self.frame_class, text=desc)
            lbl.grid(row=r, column=c, padx=10, pady=10)
            lbl.bind('<Double-Button-1>', lambda event, x=i: self.sort(event,x))
            i += 1
            c = c + 1
            ent = Entry(self.frame_class)
            ent.grid(row=r, column=c, padx=10, pady=10)
            self.ent.append(ent)
            if c == 2 * self.ncols - 1:
                r = r + 1
                c = 0
            else:
                c = c + 1
    
    def ocupar(self):
        if self.classObj.lst != []:
            self.mode = 'Ocupar'
            self.config_mode('Ocupar')
            self.state_entries('normal')
            self.ent[0]['state'] = 'readonly'
            self.ent[2]['state'] = 'readonly'
            self.ent[3]['state'] = 'readonly'
        
        
    def app_end(self, event = None):
		# ends the application
        self.destroy()

    def sort(self, event, x):
		# Sort by labels
        self.classObj.sort(self.att[x])
        
    def disp_obj(self):
		# displays the current object attributes
        if self.classObj.lst != []:
            obj = self.classObj.current()
            self.state_entries('normal')
            self.clean_form()
            for idx, ent in enumerate(self.ent):
                ent.config(state='normal')
                ent.delete(0, 'end')
                ent.insert(0, getattr(obj, self.att[idx]))
                ent.config(state='readonly')
            self.state_entries('readonly')
        else:
            self.clean_form()
            self.state_entries('readonly')

    def create_obj(self):
        #creates a new object
          
        codigo = self.ent[0].get()
        nome= self.ent[1].get()
        preco= self.ent[2].get()
        return self.classObj(codigo, nome, preco)
    
    def update_obj(self):
        # update Object from form
        
        obj = self.classObj.current()
        if self.mode=="Ocupar":
            if self.ent[1].get() in list(Cliente_login.login_list.keys()):
                for idx, ent in enumerate(self.ent):
                    setattr(obj, self.att[idx], ent.get())
                login= self.classObj.login
                obj.ocupar(login)
                self.ocuparr=0
        else:
            for idx, ent in enumerate(self.ent):
                setattr(obj, self.att[idx], ent.get())
        self.state_entries('readonly')
    
    def clean_form(self):
        # clean all entrys
        for ent in self.ent:
            ent.config(state='normal')
            ent.delete(0, 'end')
        self.ent[0].focus_set()
        
    def first(self):
		# go to the first object and displays its attributes
        self.classObj.first()
        self.disp_obj()
    
    def back(self):
		# go to the previous object and displays its attributes
        self.classObj.previous()
        self.disp_obj()
    
    def nextrec(self):
		# go to the next object and displays its attributes
        self.classObj.nextrec()
        self.disp_obj()
    
    def last(self):
		# go to the last object and displays its attributes
        self.classObj.last()
        self.disp_obj()

    def find(self):
        # change to find mode
        if self.classObj.lst != []:
            self.mode = 'find'
            self.state_entries('normal')
            self.clean_form()
            self.config_mode('Find')

    def edit(self):
        # change to edit mode
        if self.classObj.lst != []:
            self.mode = 'Edit'
            self.config_mode('Edit')
            self.state_entries('normal')
            self.ent[0]['state'] = 'readonly'
            self.ent[2]['state'] = 'readonly'
            self.ent[3]['state'] = 'readonly'
        
    
    def delete(self):
        # deletes the current record
        if self.classObj.lst != []:
            resp = messagebox.askyesno(title='delete record', message='Are you sure?')
            if resp:
                obj = self.classObj.current()
                code = getattr(obj, self.att[0])
                if self.classObjLink:
                    # deletes the lines from the child class if exists
                    lines = self.classObjLink.getlines(code)
                    for child in lines:
                        self.classObjLink.remove(child)
                    self.classObjLink.write(self.filePath)
                self.classObj.remove(code)

                self.classObj.write(self.filePath)
                self.classObj.previous()
                self.disp_obj()
    
    def insert(self):
        # change to insert mode
        self.mode = 'Insert'
        self.state_entries('normal')
        self.clean_form()
        self.config_mode('Edit')
        

    def save(self):
		# save a new or updated object
        if self.mode == 'Insert':
            self.create_obj()
            self.classObj.last()
        elif self.mode == 'Edit':
            self.update_obj()
        elif self.mode =="Ocupar":
            self.update_obj()

        self.config_mode('Show')
        self.state_entries('readonly')
        self.disp_obj()
        self.classObj.write(self.filePath)
     
    def cancel(self):
		# cancel edit or insert mode
        if self.mode == 'find':
            self.classObj.set_filter()
        self.disp_obj()
        self.config_mode('Show')
        self.state_entries('readonly')

    def ok(self):
        # change to insert mode
        f_dic = dict()
        for idx, ent in enumerate(self.ent):
            if ent.get() != "":
                f_dic[self.att[idx]] = ent.get()
        self.classObj.set_filter(f_dic)
        self.config_mode('Find')
        self.state_entries('readonly')
        self.disp_obj()
        self.btn_ok['state'] = "disabled"
        self.btn_cancel['state'] = "normal"
        self.btn_arrow("normal")
        
    def openlines(self):
        # call the child form window
        obj = self.classObj.current()
        if obj != None:
            objcode = getattr(obj, self.att[0])
            OpenFormTableLink(self, self.classObjLink, self.attnamesLink,
                        objcode,filePath=self.filePath,editmode=self.editmode)

    def config_mode(self, mode):
        #configure form according to the state
        if mode == "Show":
            self.btn_arrow("normal")
            if self.editmode == 1:
                self.btn_mode("normal")
            else:
                self.btn_mode("disabled")
                self.btn_exit['state'] = "normal"
            self.btn_save['state'] = "disabled"
            self.btn_cancel['state'] = "disabled"
            self.btn_ok['state'] = "disabled"
            if self.classObjLink:
                self.btn_openlines['state'] = "normal"
        else:
            self.btn_arrow("disabled")
            self.btn_mode("disabled")
            self.btn_cancel['state'] = "normal"
            self.btn_ok['state'] = "disabled"
            if self.classObjLink:
                self.btn_openlines['state'] = "disabled"
            if mode == "Edit":
                self.btn_save['state'] = "normal"
            elif mode == "Find":
                self.btn_save['state'] = "disabled"
                self.btn_ok['state'] = "normal"
            elif mode =="Ocupar":
                self.btn_save['state']= "normal"
               
                
    def btn_arrow(self, state):
        self.btn_back['state'] = state
        self.btn_next['state'] = state
        self.btn_last['state'] = state
        
    def btn_mode(self, state):
        self.btn_delete['state'] = state
        self.btn_insert['state'] = state
        self.btn_exit['state'] = state
        
    def state_entries(self, state):
        # set the entries state
        for ent in self.ent:
            ent['state'] = state
# root = Tk()
# a = AbrirAdminServicos(root, Servico, ['Código:', 'Nome:', 'Preço:'])