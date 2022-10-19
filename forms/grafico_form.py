# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 15:30:23 2022

@author: leono
"""

import tkinter as tk
import matplotlib

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

import pandas as pd

class Grafico_Form(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Ocupação por Tipo de Quarto')
        df = pd.read_csv('data/quarto.csv', sep = ';')
        self.x_points = ['Singular', 'Duplo', 'Triplo', 'Suite Executiva', 'Suite Presidencial']
        self.y_points = [0]*5
            
            
        total_singular = df.loc[df['tipo'] == 'Singular']['tipo'].count()
        singular_ocupado = df.loc[(df['tipo'] == 'Singular') & (df['estado'] == 'Ocupado')]['tipo'].count()
        self.y_points[0] = int(singular_ocupado / total_singular * 100)
            
        total_duplo = df.loc[df['tipo'] == 'Duplo']['tipo'].count()
        duplo_ocupado = df.loc[(df['tipo'] == 'Duplo') & (df['estado'] == 'Ocupado')]['tipo'].count()
        self.y_points[1] = int(duplo_ocupado / total_duplo * 100)
            
        total_triplo = df.loc[df['tipo'] == 'Triplo']['tipo'].count()
        triplo_ocupado = df.loc[(df['tipo'] == 'Triplo') & (df['estado'] == 'Ocupado')]['tipo'].count()
        self.y_points[2] = int(triplo_ocupado / total_triplo * 100)
            
        total_se = df.loc[df['tipo'] == 'Suite Executiva']['tipo'].count()
        se_ocupado = df.loc[(df['tipo'] == 'Suite Executiva') & (df['estado'] == 'Ocupado')]['tipo'].count()
        self.y_points[3] = int(se_ocupado / total_se * 100)
            
        total_sp = df.loc[df['tipo'] == 'Suite Presidencial']['tipo'].count()
        sp_ocupado = df.loc[(df['tipo'] == 'Suite Presidencial') & (df['estado'] == 'Ocupado')]['tipo'].count()
        self.y_points[4] = int(sp_ocupado / total_sp * 100)
            
        self.x_index = len(self.x_points)
        
        # create a figure
        figure = Figure(figsize=(10, 6), dpi=100)

        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure, self)

        # create the toolbar
        NavigationToolbar2Tk(figure_canvas, self)

        # create axes
        axes = figure.add_subplot()

        # create the barchart
        axes.bar(self.x_points, self.y_points)
        axes.set_title('Tipo de Quarto')
        axes.set_ylabel('Ocupação(%)')

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.mainloop()

