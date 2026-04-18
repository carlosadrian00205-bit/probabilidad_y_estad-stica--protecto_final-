import streamlit as st
import pandas as pd
import plotly.express as px 

st.set_page_config(page_title="Asistente Estadístico", layout="wide")

st.title("📊 Asistente de Estadística - UPChiapas")

st.header("1. Carga de datos")
archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])

if archivo is not None:
    df = pd.read_csv(archivo)
    st.success("¡Archivo cargado!")
    
    st.subheader("Vista previa")
    st.dataframe(df)
    
    st.header("2. Visualización de Distribuciones")
    
    columnas_numericas = df.select_dtypes(include=['number']).columns
    
    if len(columnas_numericas) > 0:
        columna = st.selectbox("Selecciona una columna para analizar", columnas_numericas)
        
        st.subheader(f"Análisis visual de: {columna}")
        
        col1, col2 = st.columns(2)
        
        with col1:              
            st.write("### Histograma")
            fig_hist = px.histogram(df, x=columna, marginal="rug", 
                                   title=f"Histograma de {columna}",
                                   color_discrete_sequence=['#636EFA'])
            st.plotly_chart(fig_hist, use_container_width=True)
            
        with col2:
            st.write("### Boxplot (Caja y Bigotes)")
            fig_box = px.box(df, y=columna, title=f"Boxplot de {columna}",
                             color_discrete_sequence=['#EF553B'])
            st.plotly_chart(fig_box, use_container_width=True)
        
        st.divider()
        st.subheader("Análisis de la distribución")
        pregunta_1 = st.radio("¿La distribución parece normal?", ["Sí", "No", "No estoy seguro"])
        detalles = st.text_area("¿Hay sesgo u outliers? (Explica lo que ves)")
    else:
        st.warning("El archivo no contiene columnas numéricas.")
    
else:
    st.info("Esperando archivo CSV...")

