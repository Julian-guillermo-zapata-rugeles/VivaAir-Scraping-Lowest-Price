from dash import Dash, html , dcc
import pandas as pd
class Generator():
    
    @staticmethod
    def generate_div( id_name :str , contain : any ):
        div = html.Div(
            id = id_name,
            className= id_name,
            children = contain
        )
        return div
    
    @staticmethod
    def generate_button(id_name :str , contain : any ):
        button = html.Button(
            id = id_name,
            className= id_name,
            children = contain
        )
        return button
    
    @staticmethod
    def generate_simple_graphic(dataframe):
        desde = dataframe['desde'].iloc[0]
        hacia = dataframe['hacia'].iloc[0]
        to_show = []
        meses = dataframe['mes'].unique()
        for i in meses:
            tmp_df  = dataframe[dataframe.mes==i]
            print(tmp_df)
            item = {'x':tmp_df['n_day'],'y':tmp_df['precio'],'type': 'scatter', 'name': i}
            to_show.append(item)
        
        
        fig=dcc.Graph(
        figure={
            'data': to_show,
            'layout': {
                'title': 'Valor minimo del tiquete desde '+desde+"  hacia "+hacia
                }
            }
        )
        return fig
    
    
    @staticmethod
    def generate_timeline_graphic(dataframe , dataframe2):
        
        pb_historico = dataframe2['precio'].astype(int).min()
        sillas_historico = dataframe2['precio'].astype(int).value_counts()[pb_historico]
        try:
            
            sillas_recientes = dataframe['precio'].astype(int).value_counts()[pb_historico]
            
        except Exception as e:
            sillas_recientes = 0
        
        df = [ dataframe['n_day'].astype(str) +"_"+dataframe['mes'] , dataframe['precio']]
        df = pd.concat(df,axis=1,keys=["mes_dia","precio"])
        desde = dataframe['desde'].iloc[0]
        hacia = dataframe['hacia'].iloc[0]
        
        
        
        
        
        df2 = [ dataframe2['n_day'].astype(str) +"_"+dataframe2['mes'] , dataframe2['precio']]
        df2 = pd.concat(df2,axis=1,keys=["mes_dia","precio"])
        desde2 = dataframe2['desde'].iloc[0]
        hacia2 = dataframe2['hacia'].iloc[0]
        
        
        
        
        
        
        fig=dcc.Graph(
        figure={
            'data': [ {'x':df['mes_dia'],'y':df['precio'],'type': 'scatter', 'name':  f"N : {desde}-{hacia}"},
                      {'x':df2['mes_dia'],'y':df2['precio'],'type': 'scatter', 'name':f"V : {desde2}-{hacia2}"}],
            'layout': {
                'title': 'LINEAS DE TIEMPO DE DATAFRAMES\n'
                }
            }
        )
        
        
        fig2=dcc.Graph(
        figure={
            'data': [ {'x':['Sillas V ','Sillas N '],'y':[sillas_historico,sillas_recientes],'type': 'bar', 'name': "SILLAS DISPONIBLES CON VALOR DE "+str(pb_historico) },
                    ],
            'layout': {
                'title': "SILLAS DISPONIBLES CON VALOR DE "+str(pb_historico)
                }
            }
        )
        return fig , fig2