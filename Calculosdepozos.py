import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#------------- DATOS DE ENTRADA -------------

ri = 49.78
re = 57.15
d = 40                     # CANTIDAD DE DEDOS
n = 0.8                   # COEFICIENTE PARA CALCULO DE VELOCIDAD DE CORROSION
t = 5.58630136986301                     # TIEMPO EN AÑOS DESDE BIF HASTA FECHA DE INSPECCION POR MIT
t_2 = 0.313                              # TIEMPO EN AÑOS PARA PROYECCION DE DAÑO POR CORROSION INTERNA
prof_punzados = 2000                 #m 
peso_lineal_lbft = 13.5            #lb/ft
prof_max = 3227                   #m
tension_de_fluencia = 552             #MPa

#COEFICIENTES DE POLINOMIO INTERPOLANTE DE GRANDIENTE DE PRESIONES
a_pol = 0
b_pol = 0.0061977068
c_pol = 30

#--------------------------------------------

radios_cuad = re**2-ri**2
di = ri*2
de = re*2
e = re-ri
peso_lineal_kgm = (0.453592/0.3048)*peso_lineal_lbft    

#------------------- LECTURA DE DATOS ----------------------

df = pd.read_excel('datos.xlsx')
df2 = df.drop(columns=['Profundidad'])
print('Carga de datos OK')

#---------------RECORRE DATAFRAME Y CORRIGE VALORES FUERA DEL RADIO INTERNO Y EXTERNO----

for i in range(0,len(df2)):
   print(i)
   for j in range(0,d):
       if df2.loc[i,:][j]<ri: df2.loc[i,:][j] = ri
       if df2.loc[i,:][j]>re: df2.loc[i,:][j] = re
       else: df2.loc[i,:][j] = df2.loc[i,:][j]
         
#---------------CALCULOS DE MAXIMAS Y MINIMAS PENETRACIONES POR FILA------------------

df2['Maxima_Prof'] = [re     if df2.max(axis=1)[i]>re    else df2.max(axis=1)[i]     for i in range(len(df['Profundidad'])) ]
df2['Minima_Prof'] = [ri     if df2.min(axis=1)[i]<ri    else df2.min(axis=1)[i]     for i in range(len(df['Profundidad'])) ]

print('Calculo de máximas y mínimas penetraciones de defectos OK')

df2['Penetraciones_mm'] = [ df2['Maxima_Prof'][i]-ri   for i in range(len(df['Profundidad']))]
df2['Penetraciones_%'] = [ (df2['Maxima_Prof'][i]-ri)*100/e   for i in range(len(df['Profundidad']))]

print('Calculo de penetraciones de defectos en mm y % OK')

#---------------CALCULO DE PERDIDA DE AREA EN FUNCION DE LOS DEDOS----------------------

lista = []
for i in range(0,len(df2)):
   a1 = 0
   for j in range(0,d):
       a = re**2 - df2.loc[i,:][j]**2
       a1 = a + a1
   PM = 100 - 100/(d*radios_cuad) * a1    
   lista.append(PM.round(3))
   
df2['Perdida_de_metal_%'] = lista

#---------------CALCULO DE VELOCIDAD DE CORROSION LOCALIZADA ----------------------

df2['Vel_loc'] = [ round( (df2['Maxima_Prof'][i]-ri)/t**n,5)     for i in range(len(df))]
print('Calculo de Velocidades de corrosión localizadas OK')

#---------------CALCULO DE VELOCIDAD DE CORROSION GENERALIZADA ----------------------

df2['r_int_corr'] = [ round(np.sqrt(re**2-(1-df2['Perdida_de_metal_%'][i]*0.01)*radios_cuad),3)      for i in range(len(df))]
df2['Vel_gen'] = [ round( (df2['r_int_corr'][i]-ri) /t**n,5)     for i in range(len(df))]
print('Calculo de Velocidades de corrosión generalizadas OK')

#---------------------- PROYECCION DE DAÑO -------------------------

df2['Penetraciones_PROYECTADA_mm'] = df2['Penetraciones_mm'] + df2['Vel_loc'] * t_2**n
df2['Penetraciones_PROYECTADA_%'] = df2['Penetraciones_PROYECTADA_mm'] * 100 / e
#df2['Perdida_de_metal_PROYECTADA_%']

#---------------CALCULO DE TENSION POR VON MISSES ----------------------

df2['Presion_interna_kg/cm2'] = [ a_pol*df['Profundidad'][i]**2 + b_pol*df['Profundidad'][i] + c_pol     for i in range(len(df['Profundidad'])) ]
df2['Tension_circunferencial_MPa'] = [  (df2['Presion_interna_kg/cm2'][i]*df2['r_int_corr'][i]/(e-df2['Penetraciones_mm'][i]))*0.0980665     for i in range(len(df['Profundidad']))]
df2['Area_remanente_m2'] = [ np.pi*((re/1000)**2-(df2['r_int_corr'][i]/1000)**2)  for i in range(len(df['Profundidad'])) ]
df2['Peso_colgado_N'] = [peso_lineal_kgm*9.81*(prof_max-df['Profundidad'][i])  for i in range(len(df['Profundidad'])) ]
df2['Tension_tangencial_MPa'] = df2['Peso_colgado_N']/df2['Area_remanente_m2']/1000000
df2['Tension_VM'] = np.sqrt(0.5*(   df2['Tension_circunferencial_MPa']**2   +   df2['Tension_tangencial_MPa']**2    +   (df2['Tension_circunferencial_MPa']-df2['Tension_tangencial_MPa'])**2     ))

print('Calculo de tension de VM OK')

#---------------SALIDA DE DATOS PROCESADOS ----------------------
df_final = pd.concat([df['Profundidad'],df2],axis=1)
df_final
df_final.to_excel('datos_procesados.xlsx', sheet_name='resultados')
