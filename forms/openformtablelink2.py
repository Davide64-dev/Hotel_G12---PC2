# -*- coding: utf-8 -*-
"""
Created on 2022

@author:António Brito / Carlos Bragança

#objective: Class OpenFormTableLink to manage child class objects from main linked class
"""

# import all components
# from the tkinter library
from tkinter import *
from tkinter import ttk
from classes.servico import Servico
from classes.reserva import Reserva


class OpenFormTableLink2(Toplevel):
    def __init__(self, root, classObj, attnames, maincode, filePath = './', editmode = 1):
        super().__init__(root)
        self.root = root
        self.classObj = classObj
        self.maincode = maincode
        self.editmode = editmode
        # Set attribute names and labels
        obj = classObj.first()
        self.att = self.classObj.att
        self.filePath = filePath
        self.attnames =attnames

        # Set root title
        self.title(self.classObj.__name__)
        #self.root.iconbitmap('./images/3549293.ico')
        self.create_frames()
        self.create_buttons()
        self.create_treeview()  
        self.create_entries()
        
        self.config_mode("Show")
        
        self.fillTree()
        if len(self.my_tree.get_children()) > 0:
            self.my_tree.focus(self.my_tree.get_children()[0])
            self.my_tree.selection_set(self.my_tree.get_children()[0])
        
        # Let the root wait for any events
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
        self.frame_edit_button.grid(row=0,column=0)
        # Treeview Frame
        self.frame_Treeview = LabelFrame(self,text = self.classObj.__name__)
        self.frame_Treeview.grid(row=4,column=0,padx=10,pady=10)
        # Frame to edit entries
        self.frame_class = LabelFrame(self,text ='Edit Product')
        self.frame_class.grid(row=2,column=0,padx=5,pady=2)

    def create_buttons(self):
        # Move Buttons  
        self.button_first = Button(self.frame_move_button,text="<<",  command= lambda: self.SelectTreeLine('F'))
        self.button_back = Button(self.frame_move_button,text="<",  command= lambda: self.SelectTreeLine('P'))
        self.button_next = Button(self.frame_move_button,text=">",command= lambda: self.SelectTreeLine('N'))
        self.button_last = Button(self.frame_move_button,text=">>",command= lambda: self.SelectTreeLine('L'))
        # Move Buttons to Grid
        self.button_first.grid(row=0,column=0)
        self.button_back.grid(row=0,column=1)
        self.button_next.grid(row=0,column=3)
        self.button_last.grid(row=0,column=4)
        
         # Exit Button
        self.button_exit = Button(self.frame_buttons,text="Exit",command=self.app_end)
        self.button_exit.grid(row=0,column=5,padx=10)
            
        # Edit Buttons  
        #self.button_edit = Button(self.frame_edit_button,text="Edit",  command= lambda: self.button_edit_click())
        #self.button_delete = Button(self.frame_edit_button,text="Delete",  command= lambda: self.button_delete_click())
        #self.button_insert = Button(self.frame_edit_button,text="Insert",command= lambda: self.button_insert_click())
        #self.button_save = Button(self.frame_edit_button,text="Save",command= lambda: self.button_save_click())
        #self.button_cancel = Button(self.frame_edit_button,text="Cancel",command= lambda: self.button_cancel__click())
        # Edit Buttons to Grid
        # self.button_edit.grid(row=0,column=0)
        # self.button_delete.grid(row=0,column=1)
        # self.button_insert.grid(row=0,column=3)
        # self.button_save.grid(row=0,column=4)
        # self.button_cancel.grid(row=0,column=5)

    def create_treeview(self):        
        # create a vertical scrollbar
        self.scrollbar_V = Scrollbar(self.frame_Treeview)
        self.scrollbar_V.pack(side = RIGHT , fill = Y)
        
        # create a horizontal scrollbar
        self.scrollbar_H = Scrollbar(self.frame_Treeview,orient = 'horizontal')
        self.scrollbar_H.pack(side = BOTTOM , fill = X)    
        # selectmode = "extended" -> default, multi line select
        # selectmode = "browse" -> one line select
        # selectmode = "none" - desabled
        self.my_tree = ttk.Treeview(self.frame_Treeview ,yscrollcommand = self.scrollbar_V.set,xscrollcommand = self.scrollbar_H.set, selectmode = "browse")
        self.my_tree.pack()
        
        # Configure  scrollbars
        self.scrollbar_V.config(command= self.my_tree.yview)
        self.scrollbar_H.config(command= self.my_tree.xview)
         
        # Fields to Treeview
        self.my_tree['columns'] = self.attnames[1:]
        self.my_tree.column('#0',width = 0 , stretch = NO)
        
        self.my_tree.heading('#0')
        for attname in self.attnames[1:]:
            self.my_tree.column(attname)
            self.my_tree.heading(attname,text = attname)
    
        # Binding Treview
        self.my_tree.bind("<Double-1>", self.select_line)

    def create_entries(self):
        # Creates the labels and field entries
        self.ent = list()
        r = 0
        c = 0
        for desc in self.attnames[1:]:
            lbl = Label(self.frame_class, text=desc)
            lbl.grid(row=r, column=c, padx=10, pady=1)
            ent = Entry(self.frame_class)
            ent.grid(row=r+1, column=c, padx=10, pady=1)
            self.ent.append(ent)
            c = c + 1
            
    def app_end(self, event = None):
		# ends the application
        self.destroy()

    def select_line(self, event):
        if self.editmode == 1:
            self.button_edit_click()
  
    # Fill the treeview from class
    def fillTree(self):
        for record in self.my_tree.get_children():
            self.my_tree.delete(record)
            
        lines = self.classObj.getlines(self.maincode)
        for code in lines:
            obj = self.classObj.obj[code]
            objvalues = list()
            objvalues.append(getattr(obj, self.att[0]))
            for idx in range(len(self.att[2:])):
                objvalues.append(getattr(obj, self.att[idx+2]))
            # self.my_tree.insert(parent='', index ='end',iid=line ,text='', values = (obj.code,obj.name,obj.price,obj.stock) )
            self.my_tree.insert(parent='', index ='end',iid=code ,text='', values = objvalues )
            # line +=1
            
    # Create New Object
    def Creat_newobj_from_Entry(self):
        objvalues = list()
        for ent in self.ent:
            objvalues.append(ent.get())
        objvalues.pop()
        preco= Servico.obj[self.maincode].preco
        precoTotal= preco * int(self.ent[1].get())
        objvalues.append(str(precoTotal))
        
        str_obj = self.maincode
        for x in objvalues:
            str_obj = str_obj + ';' + x
        final= objvalues[0] + ';' + objvalues[1] + ';' + objvalues[2] 
        
        # for ent in self.ent:
        #     str_obj = str_obj + ';' + ent.get()
        return self.classObj.from_string(str_obj)
    
    # update  Object from form
    def update_my_object(self, objet):
        for idx, ent in enumerate(self.ent):
            setattr(objet, type(self.att[idx+1])(self.att[idx+1]), ent.get())
    
    def cleanForm(self):
        # clean all entrys
        for ent in self.ent:
            ent.config(state='normal')
            ent.delete(0, 'end')

    def button_edit_click(self):
        if self.my_tree.focus() != '':
            self.config_mode("Edit")
            self.selected_to_entrys()
            self.ent[2]['state'] = 'readonly'
            self.ent[0]['state'] = 'readonly'
    def button_delete_click(self):
        selected_code = self.my_tree.focus()
        if selected_code:
            resp = messagebox.askyesno(title='delete record', message='Are you sure?')
            if resp:
                self.classObj.remove(selected_code)
                self.classObj.write(self.filePath)
                index = self.my_tree.index(selected_code)
                self.my_tree.delete(selected_code)
                reclist = self.my_tree.get_children()
                if len(reclist) > 0:
                    if index > len(reclist) - 1:
                        index -= 1
                    selected_code = reclist[index]
                    self.my_tree.focus(selected_code)
                    self.my_tree.selection_set(selected_code)
               
            self.config_mode("Show")
    
    def button_insert_click(self):
        self.visible_object = None
        self.config_mode("Edit")
        self.ent[2]['state'] = 'readonly'
        
    def button_save_click(self):
        objvalues = list()
        for ent in self.ent:
            objvalues.append(ent.get())
        objvalues.pop()
        preco= Servico.obj[self.maincode].preco
        precoTotal= preco * int(self.ent[1].get())
        objvalues.append(precoTotal)
        if self.visible_object == None:
            # Insert new
            self.visible_object = self.Creat_newobj_from_Entry()
            lines = self.classObj.getlines(self.maincode)
            code = lines[-1]
            self.visible_object = self.classObj.obj[code]
            self.my_tree.insert(parent='', index ='end',iid=code ,text='', values = objvalues )
        else:
            #Update 
            selected_row_number = self.my_tree.focus()
            self.update_my_object(self.visible_object)
            self.my_tree.item(selected_row_number, values = objvalues )
           
        self.classObj.write(self.filePath)
        # self.fillTree()
        self.config_mode("Show")
        self.cleanForm()
        
    def button_cancel__click(self):
        self.visible_object=self.classObj.current() 
        self.config_mode("Show")
        self.cleanForm()
    
    def hideEntryFields(self):
        self.frame_class.grid_remove()
        
    def showEntryFields(self):
        self.frame_class.grid()

    def config_mode(self, mode):
        if mode == "Show":
            
            # self.button_first['state'] = "normal"
            # self.button_back['state'] = "normal"
            # self.button_next['state'] = "normal"
            # self.button_last['state'] = "normal"
            if self.editmode == 1:
                pass
                # self.button_edit['state'] = "normal"
                # self.button_delete['state'] = "normal"
                # self.button_insert['state'] = "normal"
            else:
                pass
                # self.button_edit['state'] = "disabled"
                # self.button_delete['state'] = "disabled"
                # self.button_insert['state'] = "disabled"

            # self.button_save['state'] = "disabled"
            # self.button_cancel['state'] = "disabled"
            # self.button_exit['state'] = "normal"
            self.hideEntryFields()
            
        elif mode == "Edit":
            # self.button_first['state'] = "disabled"
            # self.button_back['state'] = "disabled"
            # self.button_next['state'] = "disabled"
            # self.button_last['state'] = "disabled"
            
            # self.button_edit['state'] = "disabled"
            # self.button_delete['state'] = "disabled"
            # self.button_insert['state'] = "disabled"
            # self.button_save['state'] = "normal"
            # self.button_cancel['state'] = "normal"
            
            # self.button_exit['state'] = "disabled"     
            
            self.showEntryFields()
            self.ent[0].focus_set()
           
    # update entry fields
    def objectToEntrys(self):
        for idx, ent in enumerate(self.ent):
            ent.delete(0, 'end')
            ent.insert(0, getattr(self.visible_object, self.att[idx+1]))
        
    def selected_to_entrys(self):
        selected_code = self.my_tree.focus()
        self.visible_object = self.classObj.obj[selected_code]
        self.objectToEntrys()
    
    # update fields
    def SelectTreeLine(self, option):
        # F - first; P - previous; N - next; L - last
        option = option.upper()
        reclist = self.my_tree.get_children()
        index = self.my_tree.index(self.my_tree.focus())
        if  option == 'F':
            nextP = 0
        elif  option == 'P':
            nextP = index - 1
            if nextP < 0:
                nextP = 0
        elif  option == 'N':
            nextP = index + 1
            rows_count = len(reclist) -1
            if nextP > rows_count :
                nextP = rows_count 
        elif  option == 'L':
            nextP = len(reclist) - 1
        
        self.my_tree.focus(reclist[nextP])
        self.my_tree.selection_set(reclist[nextP])
