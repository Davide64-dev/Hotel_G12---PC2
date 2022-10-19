# -*- coding: utf-8 -*-
"""
@author: António Brito / Carlos Bragança
(2021)
#objective: class Customer_login

"""""
#Class Customer_login
import bcrypt
import sys
from tkinter import messagebox
class Cliente_login:
    
    
    att = ['_codigo', '_nome', '_email', '_telemovel', '_login', '_password', '_group']
    # Dictionary of objects
    obj = dict()
    lst = list()
    login_list = dict()
    pos = 0
    sortkey = ''
    user = None
    # Constructor: Called when an object is instantiated
    def __init__(self, codigo, nome, email, telemovel, login, password, group):
        # Object attributes
        self._codigo = codigo
        self._nome = nome
        self._email = email
        self._telemovel = telemovel
        self._login = login
        self._password = password
        self._group = group
        # Add the new object to the Customer_login list
        Cliente_login.obj[codigo] = self
        Cliente_login.lst.append(codigo)
        Cliente_login.login_list[login] = self
        
    # Object properties
    # getter methodes
    # code property getter method
    @property
    def codigo(self):
        return self._codigo
    # name property getter method
    @property
    def nome(self):
        return self._nome
    # address property getter method
    @property
    def email(self):
        return self._email
    # phone property getter method
    @property
    def telemovel(self):
        return self._telemovel
    # login property getter method
    @property
    def login(self):
        return self._login
    # password property getter method
    @property
    def password(self):
        return self._password
    
    @property
    def group(self):
        return self._group
    # setter methodes
    # code property setter method
    
    @codigo.setter
    def codigo(self, code):
         self._codigo = code
         
    # name property setter method
    @nome.setter
    def nome(self, nome):
        self._nome = nome
    # address property setter method
    @email.setter
    def email(self, email):
        self._email = email
    # phone property setter method
    @telemovel.setter
    def telemovel(self, telemovel):
        self._telemovel = telemovel
    # login property setter method
    @login.setter
    def login(self, login):
        self._login = login
    # password property setter method
    @password.setter
    def password(self, password):
        self._password = password
    
    
    # for login
    
    @classmethod
    def get_att(self):
        return Cliente_login.att
    
    @classmethod
    def chk_password(self, login, password):
        if login in Cliente_login.login_list:
            obj = Cliente_login.login_list[login]
            k = 'not valid'
            if obj.password == password:
                k = 'valid'
            if k != 'valid':
                messagebox.showerror('Error', 'Wrong password')
                k = 'not valid'
            return k
        else:
            messagebox.showinfo('Error', 'Not existent user')
            return False
    
    @classmethod
    def set_password(self, password):
        passencrypted = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return passencrypted.decode()
                
                
                
#################################################        
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
        except BaseException as err:
            print(f"Error in read method:\n{err}\n{type(err)}")
            sys.exit()
    # Instance method to obtain object info
    def __str__(self):
        strprint = "f'"
        for att in list(self.__dict__.keys()):
            strprint += '{self.' + att + '};'
        strprint = strprint[:-1] + "'"
        return eval(strprint)
