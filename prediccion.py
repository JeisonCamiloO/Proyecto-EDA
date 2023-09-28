import pandas as pd
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
import os

rutao = "C:/Users/jeison.orjuela/Documents/Repo Git/Proyecto-EDA/"
rutaj = "C:/Users/jgvm/OneDrive/Escritorio/Maestria/Primer Semestre (2023-2)/Analitica Computacional para la Toma de Decisiones/Proyecto/Proyecto-EDA/"


os.chdir(rutaj)

#Lectura de datos
df = pd.read_csv("data_discreta.csv", header = 0, index_col=0, sep=";")

# Identificando columnas de tipo entero
int_columns = df.select_dtypes(include=['int64', 'float64']).columns

# Cambiando el tipo de esas columnas a string
df[int_columns] = df[int_columns].astype(str)

print(df.dtypes)

print(df.head())

missing_data = df.isnull().sum()
print(missing_data)

#Modelo con estructura inicial sin parámetros
mod_fit_mv= BayesianNetwork([("target","displaced"),("target","course"),("target","daytime/evening attendance"), ("target","tuition fees up to date"), ("target","scholarship holder"), 
                             ("scholarship holder","curricular units 1st sem (grade)"), 
                             ("curricular units 1st sem (grade)","curricular units 1st sem (evaluations)"), 
                             ("curricular units 1st sem (grade)","previous qualification (grade)"),
                             ("tuition fees up to date","unemployment rate"),("tuition fees up to date","inflation rate"),
                             ("inflation rate", "gdp"),
                             ("unemployment rate","gdp"),
                             ("daytime/evening attendance","unemployment rate")])

#División entre Train y Test
from sklearn.model_selection import train_test_split

train, test = train_test_split(df, test_size=0.20, random_state=42)


print(train.head())
print(test.head())

'''
index_to_remove = train[train['target'] == 'Graduate'].index[:616]  # Tomamos los primeros 2 índices

# Eliminamos esas filas del DataFrame
train = train.drop(index_to_remove)


print(train.groupby(by="target").agg({"target":"count"}))
print(abs(train.groupby(by="target").agg({"target":"count"}).loc["Dropout"] - train.groupby(by="target").agg({"target":"count"}).loc["Graduate"] ))
'''

#Modulo de ajuste para algunas CPDs del nuevo modelo
from pgmpy.estimators import MaximumLikelihoodEstimator
emv = MaximumLikelihoodEstimator(model=mod_fit_mv, data=train)

#Parámetros obtenidos con la estumación de Máxima verosimilitud
mod_fit_mv.fit(data=train, estimator = MaximumLikelihoodEstimator) 
for i in mod_fit_mv.nodes():
    print(mod_fit_mv.get_cpds(i)) 





#Modelo de inferencia
from pgmpy.inference import VariableElimination
infer = VariableElimination(mod_fit_mv)

pred_test= []

#Predicciones
pred = []

for i in range(len(test)):
    course_v = test.iloc[i][0]
    daytime_v = test.iloc[i][1]
    previous_qualification_grade_v = test.iloc[i][2]
    displaced_v = test.iloc[i][3]
    tuition_v = test.iloc[i][4]
    scholarship_v = test.iloc[i][5]
    curricular_units_1sem_evaluations_v = test.iloc[i][6]
    curricular_units_1sem_grade_v = test.iloc[i][7]
    unemployment_rate_v = test.iloc[i][8]
    inflation_rate_v = test.iloc[i][9]
    gdp_v = test.iloc[i][10]

    pred_test = infer.map_query(["target"], 
                                evidence={"course": course_v, "daytime/evening attendance": daytime_v, "previous qualification (grade)": previous_qualification_grade_v, 
                                          "displaced":displaced_v, "tuition fees up to date": tuition_v, "scholarship holder": scholarship_v, 
                                          "curricular units 1st sem (evaluations)": curricular_units_1sem_evaluations_v, "curricular units 1st sem (grade)":curricular_units_1sem_grade_v,
                                          "unemployment rate":unemployment_rate_v, "inflation rate":inflation_rate_v,
                                          "gdp":gdp_v}, show_progress=False)
    pred.append(pred_test["target"])

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix


print("Aciertos:", accuracy_score(test.loc[:,"target"], pred, normalize=False))
print("Tasa de aciertos: ", accuracy_score(test.loc[:,"target"], pred))

tn, fp, fn, tp = confusion_matrix(test.loc[:,"target"], pred, labels=["Dropout", "Graduate"]).ravel()

encabezado = ["tn", "fp", "fn", "tp"]
resultados = [tn, fp, fn, tp]

#Matriz de confusión
result = pd.DataFrame( [resultados], columns=encabezado )
print(result)
