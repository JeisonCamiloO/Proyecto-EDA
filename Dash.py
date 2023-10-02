# -*- coding: utf-8 -*-

# Ejecute esta aplicación con 
# python app1.py
# y luego visite el sitio
# http://127.0.0.1:8050/ 
# en su navegador.

import dash
from dash import dcc  # dash core components
from dash import html # dash html components
from dash.dependencies import Input, Output 
import plotly.express as px
import pandas as pd
import os 
rutao = "D:/OneDrive - Universidad de los Andes/Uniandes/Maestría/Tercer Semestre/Analitica Comp/Proyecto/eda"
os.chdir(rutao)

import prediccion

rutaj = "C:/Users/jgvm/OneDrive/Escritorio/Maestria/Primer Semestre (2023-2)/Analitica Computacional para la Toma de Decisiones/Proyecto/Proyecto-EDA/data.csv"

rutao_disc = "data_discreta.csv"
rutaj_disc = "C:/Users/jgvm/OneDrive/Escritorio/Maestria/Primer Semestre (2023-2)/Analitica Computacional para la Toma de Decisiones/Proyecto/Proyecto-EDA/data_discreta.csv"


df = pd.read_csv("data.csv", sep=';')
df_disc = pd.read_csv(rutao_disc, sep=';')

course_list = df['Course'].unique().tolist()
course_dict = {
    33: "Biofuel Production Technologies",  # Ciencias exactas
    171: "Animation and Multimedia Design", # Diseño
    8014: "Social Service (evening attendance)", # Ciencias sociales
    9003: "Agronomy", # Ciencias agrarias
    9070: "Communication Design", # Diseño
    9085: "Veterinary Nursing", # Ciencias de la salud
    9119: "Informatics Engineering", # Ciencias exactas
    9130: "Equinculture", # Ciencias agrarias
    9147: "Management", # Ciencias exactas
    9238: "Social Service", # Ciencias Sociales
    9254: "Tourism", # Ciencias Sociales
    9500: "Nursing", # Ciencias de la salud
    9556: "Oral Hygiene", # Ciencias de la salud
    9670: "Advertising and Marketing Management", # Diseño
    9773: "Journalism and Communication", # Ciencias sociales
    9853: "Basic Education", # Ciencias sociales
    9991: "Management (evening attendance)" # Ciencias exactas

    # Ciencias exactas, Diseño, Ciencias sociales, Ciencias agrarias, Ciencias de la salud
}
daytime_dict = {
    1: "Daytime",
    0: "Evening"
}
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

#Definición de barra lateral
def generate_control_card():
    """

    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.B("Select Courses"),
            dcc.Dropdown(
                options=[{"label": valor, "value": clave} for clave, valor in course_dict.items()],
                value=course_list[:], 
                id='dropdown-course',
                multi=True
            ),
            html.Br(),
            html.P("Select daytime attendance"),
            dcc.Checklist(
                options=[{"label": valor, "value": clave} for clave, valor in daytime_dict.items()],
                inline = True,
                value=[1, 0],
                id='checklist-daytime'
            ),
            html.Br(),
        ],
    )
def generate_prediction_card():
    """

    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="prediction-card2",
        children=[
            html.Br(),
            html.B("Select a discipline"),
            dcc.Dropdown(
                options=df_disc["course"].unique(), 
                id='predict-course',
                value = 'Diseno'
                # inline = False
            ),
            html.Br(),
            html.B("Select Daytime attendance"),
            dcc.RadioItems(
                options=df_disc["daytime/evening attendance"].unique(), 
                id='predict-attendance',
                inline = True,
                value = 1
            ),
            html.Br(),
            html.B("Select Previous qualification grade level"),
            dcc.Dropdown(
                options=df_disc["previous qualification (grade)"].unique(), 
                id='predict-qualification-grade',
                value = 'Desemp. Basico'
            ),
            html.Br(),
            html.B("Select displaced"),
            dcc.RadioItems(
                options=df_disc["displaced"].unique(), 
                id='predict-displaced',
                inline = True,
                value = 1
            ),
            html.Br(),
            html.B("Select tuition fees up to date"),
            dcc.RadioItems(
                options=df_disc["tuition fees up to date"].unique(), 
                id='predict-tuition-fees',
                inline = True,
                value = 1
            ),
            html.Br(),
            html.B("Select Scholarship holder"),
            dcc.RadioItems(
                options=df_disc["scholarship holder"].sort_values(ascending = False).unique(), 
                id='predict-scholarship',
                inline = True,
                value = 1
            ),
            html.Br(),
            html.B("Select evaluations in 1st semester"),
            dcc.Dropdown(
                options=df_disc["curricular units 1st sem (evaluations)"].unique(), 
                id='predict-evaluations',
                value = 'MB'
            ),
            html.Br(),
            html.B("Select grade in 1st semester"),
            dcc.Dropdown(
                options=df_disc["curricular units 1st sem (grade)"].unique(), 
                id='predict-grade-1st',
                value = 'Desemp. Muy Bajo'
            ),
            html.Br(),
            html.B("Select Unemployment rate level"),
            dcc.Dropdown(
                options=df_disc["unemployment rate"].unique(), 
                id='predict-unemployment',
                value = 'Unemployment R. Bajo'
            ),
            html.Br(),
            html.B("Select Inflation rate level"),
            dcc.Dropdown(
                options=df_disc["inflation rate"].unique(), 
                id='predict-inflation',
                value = 'M'
            ),
            html.Br(),
            html.B("Select GDP level"),
            dcc.Dropdown(
                options=df_disc["gdp"].unique(), 
                id='predict-gdp',
                value = 'GDP. Muy Bajo'
            ),
            html.Br(),
            html.Hr(),
        ],
    )

def description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Students Prediction"),
            html.H3("Welcome to the Students Prediction Dashboard"),
            html.Div(
                id="intro",
                children="The Dashboard was created as part of a project with the objective of contributing to the reduction of academic dropout and failure in higher education. It leverages Bayesian network techniques to identify students at risk at an early stage of their academic journey. To generate a prediction and assess students' risk, please follow these steps:",
            ),
            html.Ol([
                html.Li("Use the provided dropdown menus and checklist filters to select the relevant parameters and attributes related to the student's profile and academic situation."),
                html.Li("After selecting the desired filters, view the selected values in the right panel and observe the generated prediction.."),
                html.Li("Utilize the generated predictions to implement appropriate strategies and support measures to help students succeed in their academic endeavors.")
            ]),
        ],
    )
def description_prediction():
    """
    :return: A description about levels to be set in prediction dash
    """
    return html.Div(
        id="description-prediction",
        children=[
            html.H3("Other Visualizations"),
            html.Div(
                id="intro-prediction",
                children="Select filters to see information",
            ),
        ],
    )
def bayesian_network():
    return html.Div(
        id="bayesian_network",
        children=[
            
        ],
    )

app.layout =  html.Div(
    id="app-container",
    children= [
        # Banner
        html.Div(
            id="banner",
            className="banner",
            children=[html.Img(src=app.get_asset_url("logo_uniandes.png"))],
        ),
        # Left column
        html.Div( 
            id="left-column",
            className="three columns",
            children=[ description_card(), generate_prediction_card(), description_prediction(), generate_control_card()]
            + [
                html.Div(
                    ["initial child"], id="output-clientside", style={"display": "none"}
                )
            ],
        ),
         # Right column
        html.Div(
            id="right-column",
            className="eight columns",
            children= [
                html.Div(
                    id="prediction-card",
                    children = [
                        html.H2("Bayesian Network to Predict Target"),
                        html.Img(src=app.get_asset_url("RedBayesiana2.png"), className='center'),
                        html.Br(),
                        html.H3("Prediction with selected values"),
                        html.Div(id='selected-values'),
                        html.Br(),
                        html.H3("Real cases"),
                        dcc.Graph(id='real-cases'),
                    ],
                ),
                html.Div(
                    id="other-graphs",
                    children = [
                        dcc.Graph(id='bar-graph'),
                        html.Br(),
                        dcc.Graph(id='bar-graph-daytime'),
                        dcc.Graph(id='bar-graph-quality')
                    ],
                )
            ],
        ),
])


@app.callback(
    Output('bar-graph', 'figure'),
    Output('bar-graph-daytime', 'figure'),
    Output('bar-graph-quality', 'figure'),
    Input('dropdown-course', 'value'),
    Input('checklist-daytime', 'value')
)
def update_output(course_value, daytime_value):
    filtered_df = df[df['Course'].isin(course_value) & df['Daytime/evening attendance\t'].isin(daytime_value)]
    fig2 = px.histogram(filtered_df, x="Target", color = "Course", text_auto=True)
    fig2.update_layout(
        xaxis_title='Target',
        yaxis_title='Count',
        title='Target by course Histogram'
    )
    fig3 = px.histogram(filtered_df, x="Target", color = "Daytime/evening attendance\t", text_auto=True)
    fig3.update_layout(
        xaxis_title='Target',
        yaxis_title='Count',
        title='Daytime/evening attendance Histogram'
    )
    fig4 = px.histogram(filtered_df, x="Curricular units 1st sem (grade)", color = "Application mode", text_auto=True, nbins=10)
    fig4.update_layout(
        xaxis_title='curricular units 1st sem (grade)',
        yaxis_title='Count',
        title='1st sem grade Histogram by application mode'
    )
    return fig2, fig3, fig4

@app.callback(
    [ Output('selected-values', 'children'),
     Output('real-cases', 'figure')],
    [Input('predict-course', 'value'),
     Input('predict-attendance', 'value'),
     Input('predict-qualification-grade', 'value'),
     Input('predict-displaced', 'value'),
     Input('predict-tuition-fees', 'value'),
     Input('predict-scholarship', 'value'),
     Input('predict-evaluations', 'value'),
     Input('predict-grade-1st', 'value'),
     Input('predict-unemployment', 'value'),
     Input('predict-inflation', 'value'),
     Input('predict-gdp', 'value')]
)
def update_output(v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11):
    prediccion_resultado = prediccion.prediccion_dash([v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11])
    
    df_pred = pd.DataFrame({
        'course': [v1],
        'daytime attendance': [v2],
        'previous grade': [v3],
        'displaced': [v4],
        'tuition fees': [v5],
        'scholarship': [v6],
        '1st sem (evaluations)': [v7],
        '1st sem (grade)': [v8],
        'unemployment rate': [v9],
        'inflation rate': [v10],
        'gdp': [v11],
        'prediction': [prediccion_resultado["target"]]
    })
    
    tabla = html.Table([
        html.Tr([html.Th(col) for col in df_pred.columns]),
        html.Tr([html.Td(df_pred.iloc[0][col]) for col in df_pred.columns])
    ])
    
    # Filtrar el DataFrame df_disc
    filtered_df = df_disc[
        (df_disc['course'] == v1) &
        (df_disc['daytime/evening attendance'] == v2) &
        (df_disc['previous qualification (grade)'] == v3) &
        (df_disc['displaced'] == v4) &
        (df_disc['tuition fees up to date'] == v5) &
        (df_disc['scholarship holder'] == v6) &
        (df_disc['curricular units 1st sem (evaluations)'] == v7) &
        (df_disc['curricular units 1st sem (grade)'] == v8) &
        (df_disc['unemployment rate'] == v9) &
        (df_disc['inflation rate'] == v10) &
        (df_disc['gdp'] == v11)
    ]
    
    fig2 = px.histogram(filtered_df, x="target", text_auto=True)
    fig2.update_layout(
        xaxis_title='Target',
        yaxis_title='Count',
        title='Target Histogram - Real cases'
    )
    
    return tabla, fig2



if __name__ == '__main__':
    app.run_server(debug=True)

