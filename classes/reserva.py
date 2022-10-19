#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 12:17:29 2022

@author: davideteixeira
"""
import datetime as dt
from classes.quarto import Quarto
from classes.cliente_login import Cliente_login
import sys
class Reserva:
    
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_codigo', '_dataini', '_datafin', '_codigo_cliente', '_codigo_quarto']
    att1 = ['_codigo', '_dataini', '_datafin', '_codigo_cliente', '_codigo_quarto']
    
    def __init__(self, codigo, dataini, datafin, codigo_cliente, codigo_quarto): 
        self._codigo = codigo
        self._dataini = dt.date(int(dataini[0:4]), int(dataini[5:7]), int(dataini[8:10]))
        self._datafin = dt.date(int(datafin[0:4]), int(datafin[5:7]), int(datafin[8:10]))
        
        self._codigo_cliente = codigo_cliente
        self._codigo_quarto = codigo_quarto
        #self._custo = custo
        self._custo = float(Quarto.precos[Quarto.obj[codigo_quarto].tipo] * ((self._datafin - self._dataini).days))
        Reserva.obj[codigo] = self
        Reserva.lst.append(codigo)
    
    @property
    def codigo(self):
        return self._codigo
    
    @property
    def dataini(self):
        return self._dataini
    
    @property
    def datafin(self):
        return self._datafin
    
    @property
    def codigo_quarto(self):
        return self._codigo_quarto
    
    @property
    def codigo_cliente(self):
        return self._codigo_cliente
    
    @property
    def custo(self):
        return self._custo

    @codigo.setter
    def codigo(self, codigo):
        self._codigo = codigo
    
    @dataini.setter
    def dataini(self, dataini):
        self._dataini = dt.date.fromisoformat(dataini)
    
    @datafin.setter
    def datafin(self, datafin):
        self._datafin = dt.date.fromisoformat(datafin)
    
    @codigo_quarto.setter
    def quarto(self, codigo_quarto):
        self._codigo_quarto = codigo_quarto
    
    @codigo_cliente.setter
    def codigo_cliente(self, codigo_cliente):
        self._codigo_cliente = codigo_cliente
    
    
    
    
    
    @staticmethod
    def quantos_disponiveis(dataini, datafin, tipo):
        disponiveis = list()
        for k in list(Reserva.obj.keys()):
            temp1 = Reserva.obj[k].dataini
            temp2 = Reserva.obj[k].datafin
            
            codigo_quarto = Reserva.obj[k].codigo_quarto
            
            tipo_quarto = Quarto.obj.get(codigo_quarto).tipo
            
            if (((temp1.year, temp1.month, temp1.day) <= (dataini.year, dataini.month, dataini.day) <= (temp2.year, temp2.month, temp2.day)) or ((temp1.year, temp1.month, temp1.day) <= (datafin.year, datafin.month, datafin.day) <= (temp2.year, temp2.month, temp2.day)) or (((dataini.year, dataini.month, dataini.day) <= (temp1.year, temp1.month, temp1.day)) and ((datafin.year,datafin.month,datafin.day) >= (temp2.year, temp2.month, temp2.day)))) and (tipo_quarto == tipo):
                disponiveis.append(codigo_quarto)
        return disponiveis
    
    @staticmethod
    def ocupar_quartos():
        today = dt.date.today()
        for k in list(Quarto.obj.keys()):
            quarto = Quarto.obj[k]
            quarto.libertar()
        
        for k in list(Reserva.obj.keys()):
            temp1 = Reserva.obj[k].dataini
            temp2 = Reserva.obj[k].datafin
            if ((temp1.year, temp1.month, temp1.day) <= (today.year, today.month, today.day) <= (temp2.year, temp2.month, temp2.day)):
                pessoa = Reserva.obj[k].codigo_cliente
                quarto = Quarto.obj[Reserva.obj[k].codigo_quarto]
                quarto.ocupar()
                quarto.login = Cliente_login.obj[pessoa].login
    
    
    
# generic code: no need to change for a new class    
    # Class method to implement constructor overloading
    @classmethod
    def from_string(cls, str_data):
        str_list = str_data.split(";")
        strarg = 'cls(str_list[0]'
        for i in range(1, len(str_list)):
            strarg += ',str_list[' + str(i) + ']'
        strarg += ')'
        return eval(strarg)
    # Reset the class
    @classmethod
    def reset(cls):
        cls.obk = dict()
        cls.lst = list()
        cls.pos = 0
    # Class method to return the primary key related lines
    @classmethod
    def getlines(cls, firstkey):
        return list(filter(lambda x: x.startswith(firstkey),cls.lst))
    # Class methods to iterate (forward and backward) through the class objects
    @classmethod
    def nextrec(cls):
        cls.pos += 1
        return cls.current()
    @classmethod
    def previous(cls):
        cls.pos -= 1
        return cls.current()
    @classmethod
    def current(cls, code = None):
        if code in cls.lst:
            cls.pos = cls.lst.index(code)
        if cls.pos < 0:
            cls.pos = 0
            return None
        elif cls.pos >= len(cls.lst):
            cls.pos = len(cls.lst) - 1
            return None
        else:
            code = cls.lst[cls.pos]
            return cls.obj[code]
    @classmethod
    def first(cls):
        cls.pos = 0
        return cls.current()
    @classmethod
    def last(cls):
        cls.pos = len(cls.lst) - 1
        return cls.current()
    # Object delete method
    @classmethod
    def remove(cls, p):
        cls.lst.remove(p)
        del cls.obj[p]
    # Sort objects by attribute class methods
    @classmethod
    def orderfunc(cls, e):
        return getattr(cls.obj[e], cls.sortkey)
    @classmethod
    def sort(cls, att, reverse = False):
        cls.sortkey = att
        cls.lst.sort(key=cls.orderfunc, reverse= reverse)
    # Find objects having an attribute equal to value
    @classmethod
    def find(cls, value, att):
        lobj = cls.obj.values()
        fobj = [obj for obj in lobj if getattr(obj, att) == value]
        return fobj
    # Apply a filter by attribute class methods
    @classmethod
    def set_filter(cls, f_dic = {}):
        if f_dic:
            code = cls.att[0]
            lobj = cls.obj.values()
            s = set()
            for att,listf in f_dic.items():
                s1 = set([getattr(obj, code) for obj in lobj if getattr(obj, att) in listf])
                s = s.union(s1)
            if len(s) > 0:
                cls.lst = list(s)
                cls.pos = 0
        else:
            obj = cls.current()
            cls.lst = list(cls.obj.keys())
            code = cls.att[0]
            cls.current(getattr(obj, code))
    # Get a list of objects attribute values
    @classmethod
    def getatlist(cls, att):
        return [getattr(obj, att) for obj in list(cls.obj.values())]
    # Write object to csv file
    @classmethod
    def write(cls, path = ''):
        fh = open(path + cls.__name__ + '.csv', 'w')
        strprint = ""
        for att1 in cls.att:
            if att1[0] == '_':
                strprint += att1[1:] + ';'
            else:
                strprint += att1 + ';'
        fh.write(strprint[:-1] + '\n')
        for p in cls.obj.values():
            fh.write(p.__str__() + '\n')
        fh.close()
    # Read objects from csv file
    @classmethod
    def read(cls, path = ''):
        cls.obj = dict()
        cls.lst = list()
        try:
            file = path + cls.__name__ + '.csv'
            fh = open(file, 'r')
            fh.readline()
            for p in fh:
                cls.from_string(p.strip())
            fh.close()
        except FileNotFoundError:
            print(f"{file} data file not found, a new one will be created")
        except BaseException as err:
            print(f"Error in read method:\n{err}\n{type(err)}")
            sys.exit()
    # Instance method to obtain object info
    def __str__(self):
        strprint = "f'"
        for att in type(self).att:
            strprint += '{self.' + att + '};'
        strprint = strprint[:-1] + "'"
        return eval(strprint)

