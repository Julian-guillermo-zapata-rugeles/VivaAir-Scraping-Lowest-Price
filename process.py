import pandas as pd
import numpy as np
import time

process =open("AnaliticasVivaAir.csv").read()
process =process.replace(" ","").replace(".","")
salida = open("AnaliticasVivaAir_process.csv","w")
salida.write(process)
salida.close()

cabezeras = ["año_prueba", "mes_prueba", "dia_prueba","hora_prueba", "nombre_dia","dia", "nombre_mes", "precio","salida", "destino"]
my_dataframe = pd.read_csv("AnaliticasVivaAir_process.csv" , sep=";" , names=cabezeras)
my_dataframe.columns = cabezeras

#print(my_dataframe)
precios = my_dataframe[(my_dataframe.nombre_mes=="FEBRERO")&(my_dataframe.salida=="SMR")]
#precios['precio'] = precios['precio'].str.replace(".","",regex=True).astype(int)
#print(precios)

menor_precio_mes = precios.min().precio
dataframe_salida = precios[(precios.dia_prueba == time.localtime()[2])&(precios.hora_prueba==time.localtime()[3])]
dataframe_salida.sort_values("precio", inplace = True)
dataframe_salida.sort_values("dia", inplace = True)
print(dataframe_salida)