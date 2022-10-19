# -*- coding: utf-8 -*-
"""
@author: Davide
(2022)
#objective: Main
#%%
"""""

from forms.formlogin import FormLogin
from classes.cliente_login import Cliente_login
from classes.quarto import Quarto
from classes.reserva import Reserva
from classes.reservaservico import ReservaServico
from classes.servico import Servico
from forms.cliente_forms import Cliente_forms
from PIL import Image, ImageTk
from forms.admin_servicos_forms import AbrirAdminServicos
# import the App class
from tkinter import *
from tkinter import ttk
import tkinter.filedialog



Cliente_login.read('data/')
Quarto.read('data/')
Reserva.read('data/')
Servico.read('data/')
ReservaServico.read('data/')
Reserva.ocupar_quartos()
Quarto.write('data/')

root = Tk()
root.title('Login')
root.withdraw()




loginf = FormLogin(root,filePath='data/')

root.mainloop()

Cliente_login.write('data/')
Reserva.write('data/')
Quarto.write('data/')
ReservaServico.write('data/')
Servico.write('data/')