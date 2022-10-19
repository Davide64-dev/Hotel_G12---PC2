#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 10 14:55:20 2022

@author: davideteixeira
"""

from classes.reserva import Reserva
from classes.servico import Servico

class ReservaServico:
    
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att=['_codigo_reserva','_codigo_servico','_quantidade','_preco']
    def __init__(self, codigo_reserva, codigo_servico, quantidade, preco):
        if codigo_reserva in Reserva.lst:
            if codigo_servico in Servico.lst:
                self._codigo_reserva = codigo_reserva
                self._codigo_servico = codigo_servico
                self._quantidade = quantidade
                self._preco = preco
                ReservaServico.obj[codigo_reserva + codigo_servico] = self
                ReservaServico.lst.append(codigo_reserva + codigo_servico)
            else:
                print(f'Servico {codigo_servico} não encontrado')
        else:
            print(f'Reserva {codigo_reserva} não encontrada')
        
        @property
        def codigo_reserva(self):
            return self._codigo_reserva
        
        @property
        def codigo_servico(self):
            return self._codigo_servico
        
        @property
        def quantidade(self):
            return self._quantidade
        
        @property
        def preco(self):
            return self._reserva
        
        @quantidade.setter
        def quantidade(self, quantidade):
            self._quantidade = quantidade
        
        @preco.setter
        def preco(self, preco):
            self._preco = preco

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
        if len(firstkey)< 4:
            return list(filter(lambda x: x.endswith(firstkey),cls.lst))
        else:
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
        for att in cls.att:
            if att[0] == '_':
                strprint += att[1:] + ';'
            else:
                strprint += att + ';'
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

