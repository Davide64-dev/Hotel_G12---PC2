# -*- coding: utf-8 -*-
"""
Created on Fri May 13 16:56:30 2022

@author: leono
"""

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import *
import tkinter.filedialog
from datetime import date
from time import strftime
from datetime import timedelta, datetime, date
from datetime import datetime
from classes.cliente_login import Cliente_login
from forms.reservarquarto import ReservarQuarto
from classes.reserva import Reserva
from classes.servico import Servico
import datetime as dt
from classes.reservaservico import ReservaServico
import pandas as pd
from forms.cliente_servicos_forms import AbrirClienteServicos

#def fazer_reserva():  esta função abre a janela fazer_reserva_cliente

class Cliente_forms(Toplevel):
    
    def __init__(self, login):
        self.cliente = login
        self.root = Tk()
        self.root.title('Hotel Damago')
        self.root.geometry('800x800+600+80')  #largura x altura+ x + y
        self.root.resizable(False, False)  
#ABERTURA DA JANELA
        self.root.title('Hotel Damago')                                 
        self.root.geometry('720x700+600+80')  #largura x altura+ x + y
        self.root.resizable(False, False)     #janela não expande
#root.attributes('-alpha', 0.9)  #tranparência da janela
        
        for i in range(15):
            self.root.rowconfigure(i, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2,weight=1)
        self.root.columnconfigure(3,weight=1)
        
   

#window.lift(another_window)    traz janela para a frente no ecrã
#window.lower(another_window)    traz janela para trás no ecrã

        self.canvas=Canvas(self.root,height=700,width=720,bg= '#F5CBA7')
        self.canvas.grid(columnspan=4,rowspan=3)

        self.preco()
        self.perfil_cliente=Button(self.root, text='O Meu Perfil', fg='black', font=('Times New Roman',18),command=self.ver_meu_perfil)
        self.perfil_cliente.grid(row=2,column=0)
    
        self.reservar_quarto = Button(self.root, text='Nova Reserva', fg='black', font=('Times New Roman',18), command= self.abrir_janela_reservar)
        self.reservar_quarto.grid(row=2, column=1)
    
        self.ver_reservas= Button(self.root, text='Serviços', fg='black', font=('Times New Roman',18), command= self.ver_servicos) 
        self.ver_reservas.grid(row=2,column=2)
    
        self.terminar_sessão=Button(self.root,text='Terminar Sessão', font=('Times New Roman',18), command=self.logout)
        self.terminar_sessão.grid(row=2,column=3) 
    
        self.welcome=Label(self.root,text='Welcome to Damago', fg='white',bg= '#F5CBA7',font=('Times New Roman',28))   
        self.welcome.grid(row=1,column=1,columnspan=2)
        self.root.mainloop()
    
    
    def button_cancel_click(self,event=None):
       self.destroy()
       self.root.destroy()
       
    def logout(self, event = None):
        self.root.destroy()
        
    def abrir_janela_reservar(self):
        a = ReservarQuarto(self.cliente)
    
    

    def ver_meu_perfil(self):
        meu_perfil=Toplevel(self.root)
        meu_perfil.title('O Meu Perfil')
        meu_perfil.geometry('800x720+600+80')
        meu_perfil.resizable(False, False)
        # for i in range(15):
        #     self.root.rowconfigure(i, weight=1)
        meu_perfil.columnconfigure(0, weight=1)
        meu_perfil.columnconfigure(1, weight=1)
        meu_perfil.columnconfigure(2,weight=1)
        meu_perfil.columnconfigure(3,weight=1)
        
      
        canvas=Canvas(meu_perfil,height=720,width=1000,bg= '#F5CBA7')
        canvas.grid(columnspan=4,rowspan=15)
        
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
        nome.grid(row = 1, column = 2)
        c=0
        for i in range(len(Reserva.lst)):
            cliente_var= Reserva.obj[Reserva.lst[i]].codigo_cliente
            login_var= Cliente_login.login_list[self.cliente].codigo
            dataini = Reserva.obj[Reserva.lst[i]].dataini
            datafin = Reserva.obj[Reserva.lst[i]].datafin
            today = dt.date.today()
            if login_var == cliente_var and ((dataini.year,dataini.month,dataini.day)<=(today.year, today.month, today.day)<=(datafin.year,datafin.month,datafin.day)):
                c= c+1
                reserva_var= Reserva.obj[Reserva.lst[i]].codigo
                temp_reserva = f'Reserva{c}: {reserva_var}'
                nome = Label(meu_perfil, text =temp_reserva, fg='black', bg='#F5CBA7', font=('Times New Roman',15))
                nome.grid(row = 2+i, column = 1)
                
    def preco(self):
        today = dt.date.today()
        total = 0
        for k in list(Reserva.obj.keys()):
            dataini = Reserva.obj[k].dataini
            datafin = Reserva.obj[k].datafin
            if (Reserva.obj[k].codigo_cliente == Cliente_login.login_list[self.cliente].codigo) and ((dataini.year,dataini.month,dataini.day)<=(today.year, today.month, today.day)<=(datafin.year,datafin.month,datafin.day)):
                total += Reserva.obj[k].custo
                df = pd.read_csv('data/reservaservico.csv', sep = ';')
                temp = df.loc[df['codigo_reserva'] == int(Reserva.obj[k].codigo)]['preco'].sum()
                total += temp
        labeltotal = Label(self.root, text =f'Custo Total: {total:.2f}€', fg='black', bg='#F5CBA7', font=('Times New Roman',20))
        labeltotal.grid(row=0,column=3)
    
    
    
    def ver_servicos(self):
        labels = ['Código:', 'Nome:', 'Preço:']
        labels_child= ["Serviço", "Código Reserva", "Quantidade","Preço"]
        s4 = AbrirClienteServicos(self.root, Servico, labels,classObjLink=ReservaServico, attnamesLink=labels_child, filePath='data/', editmode=1)
