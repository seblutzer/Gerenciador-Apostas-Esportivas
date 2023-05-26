from Pacotes_Lutzer.filtros import agregar_datas
import pandas as pd
import plotly.express as px
import tkinter as tk
from plotly import figure_factory as ff
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import tempfile
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math


# Defina o dataframe df_tabela (substitua com seu próprio dataframe)
df_tabela = pd.read_csv("Apostas.csv")

# Defina as colunas_agg, colun_data e metodos
colunas_agg = 'lucro_estimado'
colun_data = 'add'
metodos= 'sum'
range_val = 5
periodo_tempo = 'dia'

atividade_hora = agregar_datas(df_tabela, colun_data, periodo_tempo, colunas_agg, metodos=metodos, range_val=range_val, cont_hora=True)
print(atividade_hora)
