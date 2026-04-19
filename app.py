import streamlit as st
import pandas as pd
import plotly.express as px 
import scipy.stats as stats 

st.set_page_config(page_title="Asistente Estadístico UPChiapas", layout="wide")

st.title("📊 Asistente de Estadística - UPChiapas")

st.header("1. Carga de datos")
archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])

if archivo is not None:
    df = pd.read_csv(archivo)
    
    df.columns = df.columns.str.strip() 
    
    st.success("¡Archivo cargado y sanitizado!")
    
    st.subheader("Vista previa completa")
    st.dataframe(df)
    
    st.header("2. Visualización de Distribuciones")
    columnas_numericas = df.select_dtypes(include=['number']).columns
    
    if len(columnas_numericas) > 0:
        columna = st.selectbox("Selecciona una variable para analizar", columnas_numericas)
        
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
        st.header("3. Prueba de Hipótesis (Prueba Z)")
        st.markdown(f"Vamos a evaluar si el promedio real de **{columna}** es diferente a un valor que tú propongas.")
        
        col_hip1, col_hip2 = st.columns(2)
        with col_hip1:
            media_hipotetica = st.number_input("Ingresa tu hipótesis (Media esperada \u03bc):", value=0.0)
        with col_hip2:
            alfa = st.selectbox("Nivel de significancia (\u03b1):", [0.01, 0.05, 0.10], index=1)
            
        if st.button("Calcular Prueba Z"):
            datos_limpios = df[columna].dropna()
            n = len(datos_limpios)
            
            if n < 2:
                st.error("Se necesitan al menos 2 datos para hacer la prueba.")
            else:
                media_real = datos_limpios.mean() 
                desviacion = datos_limpios.std(ddof=1) 
                error_estandar = desviacion / (n ** 0.5) 
                
                if error_estandar == 0:
                    st.warning("Todos los datos son idénticos, no hay variación para calcular Z.")
                else:
                    zstat = (media_real - media_hipotetica) / error_estandar
                    p_valor = 2 * (1 - stats.norm.cdf(abs(zstat)))
                    
                    st.subheader("Resultados Matemáticos")
                    metrica1, metrica2, metrica3 = st.columns(3)
                    metrica1.metric("Promedio Real (\u03bc)", f"{media_real:.2f}")
                    metrica2.metric("Puntuación Z", f"{zstat:.2f}")
                    metrica3.metric("Valor p", f"{p_valor:.4f}")
                    
                    if p_valor < alfa:
                        st.error(f"🚨 **Rechazamos la Hipótesis Nula.** La diferencia es matemáticamente significativa.")
                    else:
                        st.success(f"✅ **No hay evidencia para rechazar la Hipótesis Nula.** El promedio real es estadísticamente similar a {media_hipotetica}.")

    else:
        st.warning("El archivo no contiene columnas numéricas.")
    
else:
    st.info("Esperando archivo CSV...")