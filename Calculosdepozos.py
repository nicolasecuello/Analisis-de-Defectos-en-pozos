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
df2 = df.drop(columns=['Profundidad'])


df['Maxima_Prof'] = [re     if df2.max(axis=1)[i]>re    else df2.max(axis=1)[i]     for i in range(len(df['Profundidad'])) ]
df['Minima_Prof'] = [ri     if df2.min(axis=1)[i]<ri    else df2.min(axis=1)[i]     for i in range(len(df['Profundidad'])) ]

df




