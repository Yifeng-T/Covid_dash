import pandas as pd
import dash
import plotly.express as px  
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import numpy as np

xgb_predic_data = pd.read_csv("XGB_Validation.csv")

States = list(set(xgb_predic_data["State"]))



#=====================
external_stylesheets = [dbc.themes.LUX]

#define the dash board app:
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

#define the layout here:
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Seven Days COVID-19🦠 New Cases and New Death Prediction in U.S.🇺🇸"), className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(html.H6(children='Project made by Yifeng Tang, Caihan Wang, and Yuxuan Chen'), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H6(children='Could access resources at: our git link https://github.com/Yifeng-T/Biostat823_HomeWork/tree/main/HW4'), className="mb-4")
        ]),
        html.Hr(),

        dbc.Row([
            dbc.Col(html.H3(children='Background Introduction:'), className="mb-5")
        ]),
        html.H2(children='  COVID-19 (coronavirus disease 2019) is a disease caused by a virus named SARS-CoV-2, which has put health systems under tremendous strain. The function of this program is to predict the following 7-days covid daily new cases and new death based on the previous 7 days data.',
            style = {'font-family':'Helvetica',
                     'font-size': '15px',
                     'width':'100%',
                     'display': 'inline-block'}
                     ),
        html.H2(children='  We intended to use the Random Forest and XGBoost methods to predict the outcome variables(daily cases and daily death). The independent variables we used are listed in the following table: for the strategy and explanations of the variables, please refer to our report file ()',
            style = {'font-family':'Helvetica',
                     'font-size': '15px',
                     'width':'100%',
                     'display': 'inline-block'}
                     ),
        html.Hr(),
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Overvie of exploratory data analysis',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mb-4")
        ]),
        html.Hr(),
        dbc.Row([ #subtitle
        dbc.Col(html.H5(children='XGBoost Daily Cases and Daily Death Prediction By states', className="text-center"),
                className="mt-4")]),
        #two drop downs here: one is school, another one is majors
        html.Div(children=[html.Div(children="Select States", className="menu-title"),
                                    dcc.Dropdown(id='state_select', value='United States', multi=False, 
                                    options=[{'label': x, 'value': x} for x in xgb_predic_data["State"].unique()])]),
        
        dcc.Graph(id='case-graph',
                            figure={}, clickData=None, hoverData=None,
                            config={'staticPlot': False,     
                                    'scrollZoom': True,      
                                    'doubleClick': 'reset',  
                                    'showTips': False,       
                                    'displayModeBar': True,  
                                    'watermark': True,}, 
                            className='six columns'),
        dcc.Graph(id='death-graph',
                            figure={}, clickData=None, hoverData=None,
                            config={'staticPlot': False,     
                                    'scrollZoom': True,      
                                    'doubleClick': 'reset',  
                                    'showTips': False,       
                                    'displayModeBar': True,  
                                    'watermark': True,}, 
                            className='six columns'),
        html.Hr()


    ])
])
    

@app.callback([Output(component_id='case-graph', component_property='figure'),
               Output(component_id='death-graph', component_property='figure')],
              [Input(component_id='state_select', component_property='value')])

def draw(state_chosen):
    #if status_select == "Death":
    State_data = xgb_predic_data[(xgb_predic_data["State"] == state_chosen)]
    State_data_case = State_data[["State", "Date", "True Cases", "Predict Cases"]]
    State_data_death = State_data[["State", "Date", "True Deaths", "Predict Deaths"]]

    fig1 = px.line(State_data_case, x = "Date", y = ["True Cases","Predict Cases"],title = f"Number of COVID-19 Cases from 11/15 to 11/21 in {state_chosen}")
    fig2 = px.line(State_data_death, x = "Date", y = ["True Deaths","Predict Deaths"],title = f"Number of COVID-19 Deaths from 11/15 to 11/21 in {state_chosen}")

    
    return fig1, fig2



# to run the app
if __name__=='__main__':
    app.run_server(debug=True)

