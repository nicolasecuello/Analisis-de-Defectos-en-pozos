#import numpy as np
import pandas as pd

#------------- DATOS DE ENTRADA -------------

ri = 2
re = 3
n = 4           # CANTIDAD DE DEDOS

#--------------------------------------------

radios_cuad = re**2-ri**2
di = ri*2
de = re*2
e = re-ri

#------------------- LECTURA DE DATOS ----------------------

df = pd.read_excel('datos.xlsx')
df2 = df.drop(columns=['Profundidad'])
print('Carga de datos OK')

#---------------RECORRE DATAFRAME Y CORRIGE VALORES FUERA DEL RADIO INTERNO Y EXTERNO----

for i in range(0,len(df2)):
   for j in range(0,n):
       if df2.loc[i,:][j]<ri: df2.loc[i,:][j] = ri
       if df2.loc[i,:][j]>re: df2.loc[i,:][j] = re
       else: df2.loc[i,:][j] = df2.loc[i,:][j]
         
#---------------CALCULOS DE MAXIMAS Y MINIMAS PENETRACIONES POR FILA------------------

df2['Maxima_Prof'] = [re     if df2.max(axis=1)[i]>re    else df2.max(axis=1)[i]     for i in range(len(df['Profundidad'])) ]
df2['Minima_Prof'] = [ri     if df2.min(axis=1)[i]<ri    else df2.min(axis=1)[i]     for i in range(len(df['Profundidad'])) ]

print('Calulo de máximas y mínimas penetraciones de defectos OK')

#---------------CALCULO DE PERDIDA DE AREA EN FUNCION DE LOS DEDOS----------------------

lista = []
for i in range(0,len(df2)):
   a1 = 0
   for j in range(0,n):
       a = re**2 - df2.loc[i,:][j]**2
       a1 = a + a1
   PM = 100 - 100/(n*radios_cuad) * a1    
   lista.append(PM.round(2))
   
df2['Perdida_de_metal'] = lista
   