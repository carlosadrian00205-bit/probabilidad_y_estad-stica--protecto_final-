import streamlit as st
import pandas as pd
import plotly.express as px 

st.title("📊 Asistente de Estadística - UPChiapas")

st.header("1. Carga de datos")
archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])

if archivo is not None:
    df = pd.read_csv(archivo)
    st.success("¡Archivo cargado!")
    
    st.subheader("Vista previa")
    st.dataframe(df.head())
    
    st.header("2. Visualización de Distribuciones")
    
    columna = st.selectbox("Seleccione una columna para analizar", df.columns)
    
    st.subheader("Análisis de la distribución")
    pregunta_1 = st.radio("¿La distribución parece normal?", ["Sí", "No", "No estoy seguro"])
    detalles = st.text_area("¿Hay sesgo u outliers? (Explica lo que ves)")
    
else:
    st.info("Esperando archivo CSV...")

if columna:
    st.subheader(f"Análisis de: {columna}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Histograma")
        fig_hist = px.histogram(df, x=columna, marginal="rug", title=f"Histograma de {columna}")
        st.plotly_chart(fig_hist)
        
    with col2:
        st.write("### Boxplot (Caja y Bigotes)")
        fig_box = px.box(df, y=columna, title=f"Boxplot de {columna}")
        st.plotly_chart(fig_box)