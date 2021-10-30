#import numpy as np
import pandas as pd
import plotly as px

#read_csv('C:\Users\nicol\OneDrive\Escritorio\Automatizacion de tareas con PY')

#archivo = open('datos.xlsx',encoding = 'utf-8')

#========== DATOS DE ENTRADA =============

ri = 2
re = 3

di = ri*2
de = re*2

e = re-ri

#==========================================


df = pd.read_excel('datos.xlsx')


df['Maxima_Prof'] = df.max(axis=1)
df['Minima_Prof'] = df.min(axis=1)
 
df




