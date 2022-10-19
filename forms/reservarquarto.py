#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 17:23:34 2022

@author: davideteixeira
"""

from PIL import Image, ImageTk
import tkinter.filedialog
from tkinter import ttk
from classes.cliente_login import Cliente_login
from classes.quarto import Quarto
from classes.reserva import Reserva
from classes.reservaservico import ReservaServico
from classes.servico import Servico
from tkcalendar import *
from forms.admin_quartos_forms import AbrirAdminQuartos
from random import randint
import datetime as dt
import pandas as pd
import csv

from tkinter import *

class ReservarQuarto(Toplevel):
    
    def __init__(self, login):
        self.login = login
        self.root = Tk()
        self.root.title('Reservar')
        self.root.geometry('720x500+600+80')
        self.root.resizable(False, False)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2,weight=1)
        self.root.columnconfigure(3,weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3,weight=1)
        self.root.rowconfigure(4, weight=1)
        self.canvas=Canvas(self.root,height=800,width=900,bg= '#F5CBA7')
        self.canvas.grid(columnspan=7,rowspan=7)
    
        self.sel_tipo_quartos = Label(self.root,text="Tipo de Quartos",bg= '#F5CBA7',font=('Times New Roman',14))
        self.sel_tipo_quartos.grid(row=0,column=3)
        self.tipo_quartos=StringVar()
        self.tipo_quartos.set('Singular')
        self.tipo_quartos_cbox=ttk.Combobox(self.root,textvariable=self.tipo_quartos)
        self.tipo_quartos_cbox['values']=['Singular','Duplo','Triplo','Suite Executiva','Suite Presidencial']
        self.tipo_quartos_cbox['state']='readonly'
        self.tipo_quartos_cbox.grid(row=1,column=3)
        
        self.botaopesquisar = Button(self.root, text = 'Pesquisar Quartos Disponíveis', command = self.pesquisar)
        self.botaopesquisar.grid(row=4, column = 3)
        self.botaoadicionar = Button(self.root, text = 'Adicionar Data', command = self.adiciona_datas)
        self.botaoadicionar.grid(row=2, column=3)
        
        
        self.check = []
        self.sel_checkin_out = Label(self.root,text="Check-in - Check-out",bg= '#F5CBA7',font=('Times New Roman',14))
        self.sel_checkin_out.grid(row=0,column=1)
        hoje = dt.date.today()
        ano = hoje.year
        mes = hoje.month
        dia = hoje.day
        self.cal=Calendar(self.root,selectmode="day",year=ano,month=mes,day=dia)
        self.cal.grid(row=1,column=1)
        

        self.botaoreservar = Button(self.root, text = 'Reservar', command= self.reservar)
        self.botaoreservar.grid(row=3, column=1)
        
        self.root.mainloop()
        
        
    def adiciona_datas(self):
        temp = self.cal.get_date()
        a = temp.split('/')
        dateformat = dt.date(int(a[2])+2000, int(a[0]), int(a[1]))
        hoje = dt.date.today()
        if (hoje.year,hoje.month,hoje.day) <= (dateformat.year,dateformat.month, dateformat.day):
            self.check.append(temp)
        else:
            resp = messagebox.showerror(title='Erro', message='Data Inválida')
        self.check.sort()
        if len(self.check) == 1:
            temp2 = f'Check-in: {self.check[0]}'
        else:
            temp2 = f'Check-in: {self.check[0]} - Check-out: {self.check[1]}'
        self.checkincheckout = Label(self.root, text = temp2, bg= '#F5CBA7',font=('Calibri',14))
        self.checkincheckout.grid(row=2, column=1)
    
    def pesquisar(self):
        dataini = self.check[0]
        datafin = self.check[1]
        temp1 = dataini.split('/')
        temp2 = datafin.split('/')
        dateformat1 = dt.date(int(temp1[2])+2000, int(temp1[0]), int(temp1[1]))
        dateformat2 = dt.date(int(temp2[2])+2000, int(temp2[0]), int(temp2[1]))
        quantidade_indisponiveis = len(Reserva.quantos_disponiveis(dateformat1, dateformat2, self.tipo_quartos_cbox.get()))
        df = pd.read_csv('data/quarto.csv', sep = ';')
        todos = df.loc[df['tipo'] == self.tipo_quartos_cbox.get()]['tipo'].count()
        a = todos - quantidade_indisponiveis
        self.disponiveis = Label(self.root, text = a, bg= '#F5CBA7',font=('Calibri',14))
        self.disponiveis.grid(row=3, column=3)
    
    def reservar(self):
        codigo = randint(0,1000000)
        dataini = self.check[0]
        datafin = self.check[1]    
        
        temp1 = dataini.split('/')
        temp2 = datafin.split('/')
        
        
        dateformat1 = dt.date(int(temp1[2])+2000, int(temp1[0]), int(temp1[1]))
        dateformat2 = dt.date(int(temp2[2])+2000, int(temp2[0]), int(temp2[1]))
        mes1 = str(dateformat1.month)
        mes2 = str(dateformat2.month)
        dia1 = str(dateformat1.day)
        dia2 = str(dateformat2.day)
        
        if len(mes1) == 1:
            mes1 = f'0{mes1}'
        if len(mes2) == 1:
            mes2 = f'0{mes2}'
        
        if len(dia1) == 1:
            dia1 = f'0{dia1}'
        
        if len(dia2) == 1:
            dia2 = f'0{dia2}'
        
        
        
        dataini = str(f'{dateformat1.year}-{mes1}-{dia1}')
        datafin = str(f'{dateformat2.year}-{mes2}-{dia2}')
        
        codigo_cliente = Cliente_login.login_list[self.login].codigo
        
        
        quartos = Quarto.pesquisa_tipo(self.tipo_quartos_cbox.get())
        
        indisponiveis = Reserva.quantos_disponiveis(dateformat1, dateformat2, self.tipo_quartos_cbox.get())
        for k in indisponiveis:
            if k in quartos:
                quartos.remove(k)
        if len(quartos) == 0:
            resp = messagebox.showerror(title='Erro', message='Quartos Indisponíveis')
        else:
            codigo_quarto = quartos[0]
        
        novareserva = Reserva(str(codigo), str(dataini), str(datafin), str(codigo_cliente), str(codigo_quarto))
        Reserva.write('data/')