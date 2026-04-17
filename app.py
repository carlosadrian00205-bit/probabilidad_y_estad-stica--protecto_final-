import streamlit as st
import pandas as pd

st.title("📊 Asistente de Estadística - UPChiapas")

st.header("1. Carga de datos")
archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])

if archivo is not None:
    df = pd.read_csv(archivo)
    st.success("¡Archivo cargado!")
    
    st.subheader("Vista previa")
    st.dataframe(df.head())
    
    st.header("2. Visualización de Distribuciones")
    
    columna = st.selectbox("Selecciona una columna para analizar", df.columns)
    
    st.subheader("Análisis de la distribución")
    pregunta_1 = st.radio("¿La distribución parece normal?", ["Sí", "No", "No estoy seguro"])
    detalles = st.text_area("¿Hay sesgo u outliers? (Explica lo que ves)")
    
else:
    st.info("Esperando archivo CSV...")