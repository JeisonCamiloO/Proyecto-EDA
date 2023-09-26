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

df = pd.read_csv('C:/Users/jeison.orjuela/Documents/Repo Git/Proyecto-EDA/data.csv', sep=';')
course_list = df['Course'].unique().tolist()
course_dict = {
    33: "Biofuel Production Technologies",
    171: "Animation and Multimedia Design",
    8014: "Social Service (evening attendance)",
    9003: "Agronomy",
    9070: "Communication Design",
    9085: "Veterinary Nursing",
    9119: "Informatics Engineering",
    9130: "Equinculture",
    9147: "Management",
    9238: "Social Service",
    9254: "Tourism",
    9500: "Nursing",
    9556: "Oral Hygiene",
    9670: "Advertising and Marketing Management",
    9773: "Journalism and Communication",
    9853: "Basic Education",
    9991: "Management (evening attendance)"
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
            html.P("Seleccione el Curso"),
            dcc.Dropdown(
                options=[{"label": valor, "value": clave} for clave, valor in course_dict.items()],
                value=course_list[:], 
                id='dropdown-course',
                multi=True
            ),
            html.Br(),
            html.P("Seleccione Jornada"),
            dcc.Checklist(
                options=[{"label": valor, "value": clave} for clave, valor in daytime_dict.items()],
                inline = True,
                value=[1, 0],
                id='checklist-daytime'
            ),
            html.Br(),
            html.P("Seleccione Estado del Estudiante"),
            dcc.Checklist(
                options=[{"label": j, "value": j} for j in df["Target"].unique()],
                inline = True,
                value=['Dropout', 'Enrolled', 'Graduate'],
                id='checklist-target'
            ),
            html.Br(),
            html.Br(),
            html.Div(
                id="reset-btn-outer",
                children=html.Button(id="reset-btn", children="Reset", n_clicks=0),
            ),
        ],
    )

def description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Clinical Analytics"),
            html.H3("Welcome to the Clinical Analytics Dashboard"),
            html.Div(
                id="intro",
                children="Explore clinic patient volume by time of day, waiting time, and care score. Click on the heatmap to visualize patient experience at different time points.",
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
            children=[description_card(), generate_control_card()]
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
                dcc.Graph(id='bar-graph'),
                html.Br(),
                dcc.Graph(id='bar-graph-daytime'),
                html.Div(id='pandas-output')
            ],
        ),
])


@app.callback(
    Output('bar-graph', 'figure'),
    Input('dropdown-course', 'value'),
    Input('checklist-daytime', 'value'),
    Input('checklist-target', 'value')
)
def update_output(course_value, daytime_value, target_value):
    filtered_df = df[df['Course'].isin(course_value) & df['Daytime/evening attendance\t'].isin(daytime_value) & df['Target'].isin(target_value)]
    fig2 = px.histogram(filtered_df, x="Target", color = "Course", text_auto=True)
    fig2.update_layout(
        xaxis_title='Estado del Estudiante',
        yaxis_title='Conteo',
        title='Histograma de los Estados de los Estudiante'
    )
    return fig2 

@app.callback(
    Output('bar-graph-daytime', 'figure'),
    Input('dropdown-course', 'value'),
    Input('checklist-daytime', 'value'),
    Input('checklist-target', 'value')
)
def update_output(course_value, daytime_value, target_value):
    filtered_df = df[df['Course'].isin(course_value) & df['Daytime/evening attendance\t'].isin(daytime_value) & df['Target'].isin(target_value)]
    fig2 = px.histogram(filtered_df, x="Target", color = "Daytime/evening attendance\t", text_auto=True)
    fig2.update_layout(
        xaxis_title='Jornada',
        yaxis_title='Conteo',
        title='Cantidad de estudiantes por jornada'
    )
    return fig2 

@app.callback(
    Output('pandas-output', 'children'),
    Input('dropdown-course', 'value')
)
def update_output(value):
    return f'You have selected {value}'

if __name__ == '__main__':
    app.run_server(debug=True)

#Hacer más gráficas