import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import psycopg2
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la base de datos en Azure usando variables de entorno
server = os.getenv("AZURE_DB_SERVER")
database = os.getenv("AZURE_DB_NAME")
username = os.getenv("AZURE_DB_USER")
password = os.getenv("AZURE_DB_PASSWORD")

# Conectar a la base de datos
def conectar_bd():
    try:
        conn = psycopg2.connect(
            host=server,
            dbname=database,
            user=username,
            password=password,
            port=5432
        )
        print("Conectado a la base de datos en Azure.")
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Consultar datos de la base de datos
def obtener_datos():
    conn = conectar_bd()
    query = "SELECT temperature, humidity, fecha FROM datos_sensor ORDER BY fecha DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Encabezado con logo de la universidad
st.set_page_config(page_title="Monitoreo de Sensores IoT", layout="wide")
col1, col2 = st.columns([1, 3])

with col1:
    logo_image = Image.open("D:/Usuario/Desktop/IoT_Proyecto/Img_2368.png")  # Cambia el nombre al logo que tengas
    st.image(logo_image, use_column_width=True)

with col2:
    st.title("Visualización de Datos de Sensores")
    st.subheader("Monitoreo de temperatura y humedad en tiempo real")

# Obtener datos
df = obtener_datos()

# Sección de imagen de humedad y tabla de datos
st.write("### Datos recientes de sensores:")

col1, col2 = st.columns([1, 2])

with col1:
    image = Image.open("D:/Usuario/Desktop/IoT_Proyecto/humedad.png")
    st.image(image, caption="Sensor de Humedad", width=300)

with col2:
    st.dataframe(df, height=300)  # Altura ajustable para mejor visualización

# Gráficos de temperatura y humedad en tiempo real
st.write("### Gráficos de Temperatura y Humedad")
col1, col2 = st.columns(2)

with col1:
    st.write("#### Gráfico de Temperatura:")
    plt.figure(figsize=(10, 5))
    plt.plot(df['fecha'], df['temperature'], label='Temperatura', color='orange')
    plt.xlabel("Tiempo")
    plt.ylabel("Temperatura")
    plt.title("Temperatura en el tiempo")
    plt.xticks(rotation=45)
    st.pyplot(plt)

with col2:
    st.write("#### Gráfico de Humedad:")
    plt.figure(figsize=(10, 5))
    plt.plot(df['fecha'], df['humidity'], label='Humedad', color='blue')
    plt.xlabel("Tiempo")
    plt.ylabel("Humedad")
    plt.title("Humedad en el tiempo")
    plt.xticks(rotation=45)
    st.pyplot(plt)
    
# Texto explicativo sobre la regresión lineal
st.write("### Aplicación de Regresión Lineal")
st.markdown(
    """
    La regresión lineal es una excelente herramienta para analizar la relación entre dos variables continuas, en este caso, la **humedad** y la **temperatura**.
    
    ### Beneficios de la regresión lineal en este contexto:
    1. **Simplicidad y eficiencia**: Fácil de interpretar y rápida de ejecutar, ideal cuando trabajamos con grandes cantidades de datos en tiempo real provenientes de sensores.
    2. **Identificación de patrones**: Permite observar tendencias generales en los datos, crucial para entender cómo cambia la temperatura conforme a las variaciones de humedad.
    3. **Predicción de valores futuros**: Podemos predecir la temperatura en función de la humedad medida en tiempo real, útil para aplicaciones que necesiten mantener condiciones controladas.
    
    ### Posibilidades de predicción:
    Con un modelo de regresión lineal ajustado a estos datos, podemos:
    - **Predecir la temperatura futura** en función de los valores actuales de humedad.
    - **Detectar anomalías** en los datos de temperatura que no correspondan a los valores esperados de humedad.
    """
)

# Modelo de regresión lineal
st.write("### Análisis de Regresión Lineal para Predicción de Temperatura")
X = df[['humidity']]  # Variable independiente
y = df['temperature']  # Variable dependiente

# Dividir los datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear el modelo de regresión lineal
model = LinearRegression()
model.fit(X_train, y_train)

# Predecir en el conjunto de prueba
y_pred = model.predict(X_test)

# Mostrar resultados
st.write(f"**Coeficiente de regresión:** {model.coef_[0]}")
st.write(f"**Intercepto:** {model.intercept_}")
st.write(f"**Error cuadrático medio:** {mean_squared_error(y_test, y_pred)}")
st.write(f"**R²:** {r2_score(y_test, y_pred)}")

# Gráfico de la regresión
st.write("#### Gráfico de Regresión Lineal: Temperatura vs Humedad")
plt.figure(figsize=(10, 5))
plt.scatter(X_test, y_test, color='black', label='Datos reales')
plt.plot(X_test, y_pred, color='blue', linewidth=3, label='Regresión Lineal')
plt.xlabel("Humedad")
plt.ylabel("Temperatura")
plt.title("Regresión Lineal: Temperatura vs Humedad")
plt.legend()
st.pyplot(plt)

# Pie de página o información extra
st.markdown(
    """
    ---
    © 2024 Diego A. Lozano. Estudiante UNAB, Ingeniería de Sistemas. Proyecto IoT
    """,
    unsafe_allow_html=True
)
