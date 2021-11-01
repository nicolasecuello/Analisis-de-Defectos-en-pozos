import numpy as np
import pandas as pd

#------------- DATOS DE ENTRADA -------------

ri = 2
re = 3
d = 4           # CANTIDAD DE DEDOS
n = 0.8         # COEFICIENTE PARA CALCULO DE VELOCIDAD DE CORROSION
t = 2           # TIEMPO EN AÑOS DESDE BIF HASTA FECHA DE INSPECCION POR MIT

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
   for j in range(0,d):
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
   for j in range(0,d):
       a = re**2 - df2.loc[i,:][j]**2
       a1 = a + a1
   PM = 100 - 100/(d*radios_cuad) * a1    
   lista.append(PM.round(2))
   
df2['Perdida_de_metal'] = lista

#---------------CALCULO DE VELOCIDAD DE CORROSION LOCALIZADA ----------------------

df2['Vel_loc'] = [ round(df2['Maxima_Prof'][i]/t**n,3)     for i in range(len(df))]
print('Calculo de Velocidades de corrosión localizadas OK')

#---------------CALCULO DE VELOCIDAD DE CORROSION GENERALIZADA ----------------------

df2['r_int_corr'] = [ round(np.sqrt(re**2-(1-df2['Perdida_de_metal'][i]*0.01)*radios_cuad),3)      for i in range(len(df))]
df2['Vel_gen'] = [ round(df2['r_int_corr'][i]/t**n,3)     for i in range(len(df))]
print('Calculo de Velocidades de corrosión generalizadas OK')

#---------------SALIDA DE DATOS PROCESADOS ----------------------

df2.to_excel('datos_procesados.xlsx', sheet_name='resultados')
