# -*- coding: utf-8 -*-
"""
@author: António Brito / Carlos Bragança
(2021)
#objective: order project classes and forms
#%%
"""""
from PIL import Image, ImageTk
import tkinter.filedialog
from tkinter import ttk
from forms.grafico_form import Grafico_Form
from classes.cliente_login import Cliente_login
from classes.quarto import Quarto
from classes.reserva import Reserva
from classes.reservaservico import ReservaServico
from classes.servico import Servico
from forms.admin_servicos_forms import AbrirAdminServicos
from forms.admin_quartos_forms import AbrirAdminQuartos
from forms.admin_reservas_forms import AbrirAdminReservas
import pandas as pd

from tkinter import *


class Admin_forms(Tk):
    def __init__(self, login):
        super().__init__()
        self.cliente = login
        # Set the window title
        self.protocol("WM_DELETE_WINDOW", self.call_exit)
        self.title('Modo Funcionário         user login: ' + Cliente_login.login)
        self.path = 'data/'
        self.mode1 = 1   # edit off (editmode = 0)
        # if login is off (user='') or user group equal to admin -> edit on
        self.login = Cliente_login.login
        self.geometry('720x700+600+80')  #largura x altura+ x + y
        self.resizable(False, False) 
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2,weight=1)
        self.columnconfigure(3,weight=1)
        self.columnconfigure(4,weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.canvas=Canvas(self,height=700,width=970,bg= '#F5CBA7')
        self.canvas.grid(columnspan=5,rowspan=4)
        self.create_buttons()
        self.welcome=Label(self,text='Modo Funcionário', fg='white',bg= '#F5CBA7',font=('Times New Roman',30))   
        self.welcome.grid(row=1,column=1,columnspan=3)
        Cliente_login.read(self.path)
        Quarto.read(self.path)
        Reserva.read(self.path)
        ReservaServico.read(self.path)
        Servico.read(self.path)
        # Set the filters
        if self.login == '':
            self.mode2 = 1
        else:
            self.group = Cliente_login.login_list[self.login].group
            if self.group != 'admin':
                self.mode2 = 0
                objl = Customer_login.find(self.login, 'login')
                if objl != []:
                    login = objl[0].login
                    f_dic = {'cliente_login': [login]}
                    Quarto.set_filter(f_dic)
                    Quarto.current(self.login)
                    self.mode2 = 1
            else:
                self.mode2 = 1
        self.receitas()
        
    def call_reservas(self):
        labels = ['Código:', 'Data Inicial:', 'Data Final:', 'Login Cliente:', 'Quarto:', 'Custo:']
        labels_child= ["Reserva", "Código Serviço", "Quantidade","Preço"]
        s2 = AbrirAdminReservas(self, Reserva, labels, classObjLink=ReservaServico,
                      attnamesLink=labels_child, filePath=self.path, editmode = 1)
    def call_quartos(self):
        labels = ['Código:', 'Login:', 'Estado:', "Tipo:"]
        s3 = AbrirAdminQuartos(self, Quarto, labels, 
                      filePath=self.path, editmode = self.mode1)

    def call_servicos(self):
        labels = ['Código:', 'Nome:', 'Preço:']
        s4 = AbrirAdminServicos(self, Servico, labels, filePath=self.path, editmode=self.mode1)
    
    def call_exit(self):
        self.destroy()
        
        
        
    def create_buttons(self):
        # Creates the buttons
        btn_p = Button(self, text='Meu Perfil', command=self.ver_meu_perfil, fg='black', font=('Times New Roman',20))
        btn_p.grid(row=2, column=0, padx = 10, pady = 10)
        btn_o = Button(self, text='Quartos', command=self.call_quartos, fg='black', font=('Times New Roman',20))
        btn_o.grid(row=2, column=1, padx = 10, pady = 10)
        btn_op = Button(self, text='Serviços', command=self.call_servicos, fg='black', font=('Times New Roman',20))
        btn_op.grid(row=2, column=2, padx = 10, pady = 10)
        btn_p = Button(self, text='Reservas', command=self.call_reservas, fg='black', font=('Times New Roman',20))
        btn_p.grid(row=2, column=3, padx = 10, pady = 10)
        btn_graf = Button(self, text = 'Estatística', command= self.call_grafico, fg = 'black', font=('Times New Roman',20))
        btn_graf.grid(row=3, column=2,padx=10,pady=10)
        btn_q = Button(self, text='Exit', command=self.call_exit, fg='black', font=('Times New Roman',20))
        btn_q.grid(row=2, column=4, padx = 10, pady = 10)

    def ver_meu_perfil(self):
        meu_perfil=Toplevel(self)
        meu_perfil.title('O Meu Perfil')
        meu_perfil.geometry('800x330+600+80')
        meu_perfil.resizable(False, False)
        meu_perfil.columnconfigure(0, weight=1)
        meu_perfil.columnconfigure(1, weight=1)
        meu_perfil.columnconfigure(2,weight=1)
        meu_perfil.columnconfigure(3,weight=1)
        meu_perfil.rowconfigure(0, weight=1)
        meu_perfil.rowconfigure(1, weight=1)
        meu_perfil.rowconfigure(2, weight=1)
        canvas=Canvas(meu_perfil,height=330,width=800,bg= '#F5CBA7')
        canvas.grid(columnspan=4,rowspan=3)
        
        cod_var = Cliente_login.login_list[self.cliente].codigo
        temp_cod = f'Código = {cod_var}'
        codigo=Label(meu_perfil, text=temp_cod, fg='black',bg= '#F5CBA7',font=('Times New Roman',15))   
        codigo.grid(row=0,column=0)
        #print(a)

        nome_var = Cliente_login.login_list[self.cliente].nome
        temp_nome = f'Nome: {nome_var}'
        nome = Label(meu_perfil, text =temp_nome, fg='black', bg='#F5CBA7', font=('Times New Roman',15))
        nome.grid(row = 0, column = 1)
        
        email_var = Cliente_login.login_list[self.cliente].email
        temp_email = f'E-mail: {email_var}'
        nome = Label(meu_perfil, text =temp_email, fg='black', bg='#F5CBA7', font=('Times New Roman',15))
        nome.grid(row = 0, column = 2)
        
        telemovel_var = Cliente_login.login_list[self.cliente].telemovel
        temp_telemovel = f'Telemóvel: {telemovel_var}'
        nome = Label(meu_perfil, text =temp_telemovel, fg='black', bg='#F5CBA7', font=('Times New Roman',15))
        nome.grid(row = 1, column = 0)
        
        login_var = self.cliente
        temp_login = f'Login: {login_var}'
        nome = Label(meu_perfil, text =temp_login, fg='black', bg='#F5CBA7', font=('Times New Roman',15))
        nome.grid(row = 1, column = 1)
        
        group_var = Cliente_login.login_list[self.cliente].group
        temp_group = f'Grupo: {group_var}'
        nome = Label(meu_perfil, text =temp_group, fg='black', bg='#F5CBA7', font=('Times New Roman',15))
        nome.grid(row=1, column =2)
    
    def call_grafico(self):
        grafico = Grafico_Form()


    def receitas(self):
        soma = 0
        for k in list(Reserva.obj.keys()):
            soma += float(Reserva.obj[k].custo)
        df = pd.read_csv('data/reservaservico.csv', sep =';')
        temp = df.loc[df['preco'] != 0]['preco'].sum()
        soma += temp
        labelreceita = Label(self, text =f'Receita Total: {soma:.2f}€', fg='black', bg='#F5CBA7', font=('Times New Roman',18))
        labelreceita.grid(row=0,column=3)
            
     
