import pandas as pd
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD

#Lectura de datos
df = pd.read_csv("C:/Users/jgvm/OneDrive/Escritorio/Maestria/Primer Semestre (2023-2)/Analitica Computacional para la Toma de Decisiones/taller4/data_asia.csv", header = 0, index_col=0)

#Modelo con estructura inicial sin parámetros
mod_fit_mv= BayesianNetwork([("target","displaced"),("target","course"),("target","daytime/evening"), ("target","tutio fees up to date"), ("target","scholarship holder"), ("scholarship holder","curricular unots 1st sem (grade)"), ("curricular unots 1st sem (grade)","curricular units 1st sem (evaluations)"), ("curricular unots 1st sem (grade)","previous qualification (grade)")])
