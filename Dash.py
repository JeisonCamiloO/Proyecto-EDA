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

rutao = "C:/Users/jeison.orjuela/Documents/Repo Git/Proyecto-EDA/data.csv"
rutaj = "C:/Users/jgvm/OneDrive/Escritorio/Maestria/Primer Semestre (2023-2)/Analitica Computacional para la Toma de Decisiones/Proyecto/Proyecto-EDA/data.csv"

rutao_disc = "C:/Users/jeison.orjuela/Documents/Repo Git/Proyecto-EDA/data_discreta.csv"

df = pd.read_csv(rutao, sep=';')
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
        id="prediction-card",
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
                children="The Dashboard was created in a project that aims to contribute to the reduction of academic dropout and failure in higher education, , by using a bayesian network technique to identify students at risk at an early stage of their academic path, so that strategies to support them can be put into place.",
            )
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

app.layout =  html.Div(
    id="app-container",
    children= [
        # Left column
        html.Div( 
            id="left-column",
            className="four columns",
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
            children=[
                html.Div(id='pandas-output'),
                dcc.Graph(id='bar-graph'),
                html.Br(),
                dcc.Graph(id='bar-graph-daytime'),
                dcc.Graph(id='bar-graph-quality')
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
        xaxis_title='Estado del Estudiante',
        yaxis_title='Conteo',
        title='Histograma de los Estados de los Estudiantes'
    )
    fig3 = px.histogram(filtered_df, x="Target", color = "Daytime/evening attendance\t", text_auto=True)
    fig3.update_layout(
        xaxis_title='Jornada',
        yaxis_title='Conteo',
        title='Cantidad de estudiantes por jornada'
    )
    fig4 = px.histogram(filtered_df, x="Previous qualification (grade)", color = "Application mode", text_auto=True, nbins=10)
    fig4.update_layout(
        xaxis_title='Jornada',
        yaxis_title='Conteo',
        title='Cantidad de estudiantes por jornada'
    )
    return fig2, fig3, fig4

@app.callback(
    Output('pandas-output', 'children'),
    Input('predict-course', 'value'),
    Input('predict-attendance', 'value'),
    Input('predict-qualification-grade', 'value'),
    Input('predict-displaced', 'value'),
    Input('predict-tuition-fees', 'value'),
    Input('predict-scholarship', 'value'),
    Input('predict-evaluations', 'value'),
    Input('predict-grade-1st', 'value'),
    Input('predict-unemployment', 'value'),
    Input('predict-inflation', 'value'),
    Input('predict-gdp', 'value')
)
def update_output(v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11):
    df_pred = pd.DataFrame({
        'course': [v1],
        'daytime/evening attendance': [v2],
        'previous qualification (grade)': [v3],
        'displaced':[v4],
        'tuition fees up to date':[v5],
        'scholarship holder':[v6],
        'curricular units 1st sem (evaluations)':[v7],
        'curricular units 1st sem (grade)':[v8],
        'unemployment rate':[v9],
        'inflation rate':[v10],
        'gdp':[v11]
    })
    prediccion = 'Graduate'
    return f'Student will be: {prediccion}'

if __name__ == '__main__':
    app.run_server(debug=True)

#Hacer más gráficas