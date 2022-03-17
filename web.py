from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from dash import Dash, html, dcc
import dash
from generator.generator import Generator as gen
from processor.processor import Processor as pcc
from settings.constants import Constants as CONST
import pandas as pd


app = Dash(__name__)

author_message  = gen.generate_div("author","Desarrollado por Julián Guillermo  Zapata Rugeles")
welcome_message = gen.generate_div("description","Viva Air Analitics")
refres_layout = gen.generate_div("refresh_div",[
                                    gen.generate_button("all_time_line", " Línea Tiempo"),
                                    gen.generate_button("change_history"," Históricos  "),
                                    gen.generate_button("offline_button"," Data Local  "),
                                    gen.generate_button("refresh_button"," Data Remota "),
                                    
                                    ])
graphic_layout= gen.generate_div("graphic","")


desde = dcc.Dropdown(
   id = "desde",
   className="desde",
   options=[
       {'label': '  Medellin     ', 'value': 'MDE'},
       {'label': '  Santa Marta  ', 'value': 'SMR'},
       {'label': '  Bogotá       ', 'value': 'BOG'},
       {'label': '  Pasto        ', 'value': 'PSO'},
       {'label': '  Cali         ', 'value': 'CLO'},
       {'label': '  San Andrés   ', 'value': 'ADZ'},
   ],
   value='MDE'
)


hacia= dcc.Dropdown(
   id = "hacia",
   className="hacia",
   options=[
       {'label': '  Medellin     ', 'value': 'MDE'},
       {'label': '  Santa Marta  ', 'value': 'SMR'},
       {'label': '  Bogotá       ', 'value': 'BOG'},
       {'label': '  Pasto        ', 'value': 'PSO'},
       {'label': '  Cali         ', 'value': 'CLO'},
       {'label': '  San Andrés   ', 'value': 'ADZ'},
   ],
   value='SMR'
)

travel_selector = gen.generate_div("travel_selector",[desde,hacia,refres_layout])

app.layout = html.Div([
   
    welcome_message,
    author_message,
    travel_selector,
    graphic_layout
])


@app.callback(
    Output(component_id='graphic', component_property='children'),
    Input(component_id='refresh_button', component_property='n_clicks'),
    Input(component_id='desde', component_property='value'),
    Input(component_id='hacia', component_property='value'),
    Input(component_id='offline_button', component_property='n_clicks'),
    Input(component_id='all_time_line', component_property='n_clicks'),
    prevent_initiall_call=True
)
def call_back_action(click,desde,hacia,offline,hist):
    ctx = dash.callback_context
    if not ctx.triggered:
        
        return "ESPERANDO POR ORDENES"
    else:
        action_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if action_id == "refresh_button":
            CONST.FROM = desde
            CONST.TOWARDS = hacia
            pcc.get_dataframe()
            load_dataframe = pcc.load_dataframe(CONST.PATH_DATA_SHORT)
            graphic = gen.generate_simple_graphic(load_dataframe)
            return graphic 
            
        elif action_id == "offline_button":
            load_dataframe = pcc.load_dataframe(CONST.PATH_DATA_SHORT)
            graphic = gen.generate_simple_graphic(load_dataframe)
            return graphic
        
        elif action_id == "all_time_line":
            load_dataframe1 = pcc.load_dataframe(CONST.PATH_DATA_SHORT)
            load_dataframe2 = pcc.load_dataframe(CONST.PATH_INIT_COMPARE)
            graphic = gen.generate_timeline_graphic(load_dataframe1,load_dataframe2)
            return graphic
        else:
            CONST.FROM = desde
            CONST.TOWARDS = hacia
            return f"CONFIGURADO DESDE {CONST.FROM} HACIA {CONST.TOWARDS}"








if __name__ == '__main__':
    app.run_server(debug=True)