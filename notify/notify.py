import pandas as pd
import numpy as np
import time
import os 


cabezeras = ["año_prueba", "mes_prueba", "dia_prueba","hora_prueba", "nombre_dia","dia", "nombre_mes", "precio","salida", "destino"]
my_dataframe = pd.read_csv("AnaliticasVivaAir_latest.csv" , sep=";" , names=cabezeras)
my_dataframe.columns = cabezeras
my_dataframe.precio = my_dataframe.precio.str.replace(" ","")
my_dataframe.salida = my_dataframe.salida.str.replace(" ","")




min_mde_smr = my_dataframe[my_dataframe.salida=="MDE"].min()
min_smr_mde = my_dataframe[my_dataframe.salida=="SMR"].min()
salida1 = f"      MDE ---->   SMR {min_mde_smr.precio} {min_mde_smr.nombre_mes}"
salida2 = f"      SMR ---->   MDE {min_smr_mde.precio} {min_smr_mde.nombre_mes}"


final1 = "notify-send  '"+salida1+"'"
final2 = "notify-send  '"+salida2+"'"

os.system(final1)
os.system(final2)
