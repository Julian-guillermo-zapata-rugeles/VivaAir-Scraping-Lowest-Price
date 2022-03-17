from .viva_air import VivaAir as viva
from settings.constants import Constants as CONST
import pandas as pd 

class Processor():
    
    @staticmethod
    def get_dataframe():
        viva_controller = viva()
        print("START GET DATAFRAME")
        viva_controller.obtener_precios_bajos_dia()
        print("END.. GET DATAFRAME")
        viva_controller.close()
        
    @staticmethod 
    def load_dataframe(name_df):
        dataframe = pd.read_csv(name_df,
                                delimiter=";",
                                names=["dia","n_day","mes","precio","desde","hacia"]
                                )
        #print(dataframe)
        dataframe['precio'] = dataframe['precio'].str.replace(".","")
        dataframe = dataframe[dataframe.precio.str.isnumeric()]
        print(dataframe)
        return dataframe
        