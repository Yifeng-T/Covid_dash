import pandas as pd
import dash
import plotly.express as px  
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import numpy as np
import flask
import glob
import os
import PIL
from PIL import Image



finaldata = pd.read_csv("final_data.csv")
xgb_predic_data = pd.read_csv("RF_Validation.csv")

States = list(set(xgb_predic_data["State"]))

mod = {"Model": ["XGB", "RF"]}
model = pd.DataFrame(mod)

num = {"num":[1,2,3,4,5,6,7]}
num = pd.DataFrame(num)

status = {"status": ["Death", "Case"]}
Status = pd.DataFrame(status)

typppe = {"t": ["Daily_Death", "Daily_Case"]}
typppe = pd.DataFrame(typppe)
#==readin local pic
listofima = [f for f in glob.glob("*.png")]
static_image_route = '/static/'
#=====================
#readin rmse

rmse = pd.read_csv("RMSE_f.csv")


#=====
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
            dbc.Col(html.H6(children='Could access resources at our git link https://github.com/Caihanwang/BIOS823_Final'), className="mb-4")
        ]),
        html.Hr(),

        dbc.Row([
            dbc.Col(html.H3(children='Background Introduction:'), className="mb-5")
        ]),
        html.H2(children='  COVID-19 (coronavirus disease 2019) is a disease caused by a virus named SARS-CoV-2, which has put health systems under tremendous strain.',
            style = {'font-family':'Helvetica',
                     'font-size': '15px',
                     'width':'100%',
                     'display': 'inline-block'}
                     ),
        html.H2(children='In this project, our goal was to predict the daily number of Covid-19 confirmed cases and deaths over a week. Compared to XGBoost, Random Forest model was our final choice considering it had lower RMSE. In this way, our final outputs were 14 Random Forest models, 7 for daily deaths forecast of future 7 days respectively and 7 for daily confirmed cases forecast of future 7 days. In addition, we validated our models by forecasting the daily death and daily cases from Nov 15 2021 to Nov 21 2021 and got acceptable results.',
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

        dbc.Row([ #subtitle
        dbc.Col(html.H5(children='past seven months dayly data', className="text-center"),
                className="mt-4")]),
        
        html.Div(children=[html.Div(children="Select States", className="menu-title"),
                                    dcc.Dropdown(id='eda_state',  value = 'Alabama',multi=False, 
                                    options=[{'label': x, 'value': x} for x in finaldata["State"].unique()])]),
        html.Div(children=[html.Div(children="Select Daily Data Type", className="menu-title"),
                                    dcc.Dropdown(id='eda_data', value='Daily_Case', multi=False, 
                                    options=[{'label': x, 'value': x} for x in typppe["t"].unique()])]),
        
        dcc.Graph(id='daily',
                            figure={}, clickData=None, hoverData=None,
                            config={'staticPlot': False,     
                                    'scrollZoom': True,      
                                    'doubleClick': 'reset',  
                                    'showTips': False,       
                                    'displayModeBar': True,  
                                    'watermark': True,}, 
                            className='six columns'),

        html.Hr(),
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='XGBoost and randomforest comparison',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mb-4")
        ]),
        html.Hr(),

        dbc.Row([ #subtitle
        dbc.Col(html.H5(children='Feature Importance', className="text-center"),
                className="mt-4")]),
        #two drop downs here: one is school, another one is majors
        
        html.Div(children=[html.Div(children="Select Death/Case", className="menu-title"),
                                    dcc.Dropdown(id='select_status', value='Case', multi=False, 
                                    options=[{'label': x, 'value': x} for x in Status["status"].unique()])]),
        html.Div(children=[html.Div(children="Select Model Number", className="menu-title"),
                                    dcc.Dropdown(id='select_num', value='2', multi=False, 
                                    options=[{'label': x, 'value': x} for x in num["num"].unique()])]),
        html.Div(children=[html.Div(children="Select Model", className="menu-title"),
                                    dcc.Dropdown(id='select_model', value='XGB', multi=False, 
                                    options=[{'label': x, 'value': x} for x in model["Model"].unique()])]),
        
        html.Img(id='f1'),
        html.Hr(),
        dbc.Row([ #subtitle
        dbc.Col(html.H5(children='XGBOOST and RandomForest Root Mean Square Error Comparision', className="text-center"),
                className="mt-4")]),
        html.Div(children=[html.Div(children="Select Daily/Death Data", className="menu-title"),
                                    dcc.Dropdown(id='rmse', value='Case', multi=False, 
                                    options=[{'label': x, 'value': x} for x in rmse["Status"].unique()])]),
        dcc.Graph(id='rmse_graph',
                            figure={}, clickData=None, hoverData=None,
                            config={'staticPlot': False,     
                                    'scrollZoom': True,      
                                    'doubleClick': 'reset',  
                                    'showTips': False,       
                                    'displayModeBar': True,  
                                    'watermark': True,}, 
                            className='six columns'),
        html.Hr(),
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='7 days Random forest prediction result',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mb-4")
        ]),

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

@app.callback(
    dash.dependencies.Output('f1', 'src'),
    [dash.dependencies.Input('select_status', 'value'),
     dash.dependencies.Input('select_num', 'value'),
     dash.dependencies.Input('select_model', 'value')
     ])
def update_image_src(status, num, model):
    name1 = str(model)+str(status)+str(num)+".png"
    #name2 = "RF"+str(status)+str(num)+".png"
    #print(name1)
    size = 750, 750
    fig1 = PIL.Image.open(name1)
    fig1.thumbnail(size, Image.ANTIALIAS)
    return  fig1

@app.callback(Output(component_id='rmse_graph', component_property='figure'),
              [Input(component_id='rmse', component_property='value')])

def draw(state):
    new = rmse[rmse["Status"] == state]
    fig = px.bar(new, x="Model", y="RMSE", 
                 color="Method", barmode="group")
    fig.update_layout(title_text=f'XGBoost RMSE V.S. RandomForest RMSE over 7 Models for Daily{state} data')
    return fig

@app.callback(Output(component_id='daily', component_property='figure'),
              [Input(component_id='eda_state', component_property='value'),
               Input(component_id='eda_data', component_property='value')])

def draw(state, data):
    df = finaldata[finaldata["State"] == state]
    fig = px.line(df, x="Date", y=data, title=f'{data} in {state} in the Past 7 Months')
    return fig


    



# to run the app
if __name__=='__main__':
    app.run_server(debug=True)