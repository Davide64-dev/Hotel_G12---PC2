#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 16:18:44 2022

@author: davideteixeira
"""

class Servico:
    
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_codigo','_nome','_preco']
    def __init__(self, codigo, nome, preco):
        self._codigo = codigo
        self._nome = nome
        self._preco = int(preco)
        Servico.obj[codigo] = self
        Servico.lst.append(codigo)

    @property
    def codigo(self):
        return self._codigo
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def preco(self):
        return self._preco

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
    # Get a list of objects attribute values
    @classmethod
    def getatlist(cls, att):
        return [getattr(obj, att) for obj in list(cls.obj.values())]
    # Write object to csv file
    @classmethod
    def write(cls, path = ''):
        if len(cls.lst) > 0:
            fh = open(path + cls.__name__ + '.csv', 'w')
            p = cls.obj[cls.lst[0]]
            strprint = ""
            for att in list(p.__dict__.keys()):
                strprint += att[1:] + ';'
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
            fh = open(path + cls.__name__ + '.csv', 'r')
            fh.readline()
            for p in fh:
                cls.from_string(p.strip())
            fh.close()
        except:
            pass
        
        
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
            
    # Instance method to obtain object info
    def __str__(self):
        strprint = "f'"
        for att in list(self.__dict__.keys()):
            strprint += '{self.' + att + '};'
        strprint = strprint[:-1] + "'"
        return eval(strprint)
