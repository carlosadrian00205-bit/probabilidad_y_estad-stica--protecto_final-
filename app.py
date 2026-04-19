import streamlit as st
import pandas as pd
import plotly.express as px 
import scipy.stats as stats 
import google.generativeai as genai 

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
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("### Histograma")
            fig_hist = px.histogram(df, x=columna, marginal="rug", title=f"Histograma de {columna}", color_discrete_sequence=['#636EFA'])
            st.plotly_chart(fig_hist, use_container_width=True)
        with col2:
            st.write("### Boxplot")
            fig_box = px.box(df, y=columna, title=f"Boxplot de {columna}", color_discrete_sequence=['#EF553B'])
            st.plotly_chart(fig_box, use_container_width=True)
        
        st.divider()
        st.header("3. Prueba de Hipótesis (Prueba Z)")
        
        col_hip1, col_hip2 = st.columns(2)
        with col_hip1:
            media_hipotetica = st.number_input("Ingresa tu hipótesis (Media esperada \u03bc):", value=0.0)
        with col_hip2:
            alfa = st.selectbox("Nivel de significancia (\u03b1):", [0.01, 0.05, 0.10], index=1)
            
        if st.button("Calcular Prueba Z"):
            datos_limpios = df[columna].dropna()
            n = len(datos_limpios)
            
            if n >= 2:
                media_real = datos_limpios.mean() 
                desviacion = datos_limpios.std(ddof=1) 
                error_estandar = desviacion / (n ** 0.5) 
                
                if error_estandar != 0:
                    zstat = (media_real - media_hipotetica) / error_estandar
                    p_valor = 2 * (1 - stats.norm.cdf(abs(zstat)))
                    
                    metrica1, metrica2, metrica3 = st.columns(3)
                    metrica1.metric("Promedio Real", f"{media_real:.2f}")
                    metrica2.metric("Puntuación Z", f"{zstat:.2f}")
                    metrica3.metric("Valor p", f"{p_valor:.4f}")
                    
                    if p_valor < alfa:
                        st.error(f"🚨 Rechazamos la Hipótesis Nula. La diferencia es estadísticamente significativa.")
                    else:
                        st.success(f"✅ No hay evidencia para rechazar la Hipótesis Nula.")
                        
        st.divider()
        st.header("🤖 4. Asistente Virtual IA")
        st.markdown("Hazle preguntas a Gemini sobre tus datos o conceptos de estadística.")
        
        clave_api = st.text_input("Ingresa tu API Key de Gemini:", type="password")
        
        if clave_api:
            genai.configure(api_key=clave_api)
            modelo = genai.GenerativeModel('gemini-1.5-flash')
            
            pregunta = st.text_area("¿En qué te puedo ayudar?")
            
            if st.button("Preguntar a la IA"):
                if pregunta:
                    with st.spinner("Analizando tus datos..."):
                        try:
                            resumen = df.describe().to_string()
                            prompt = f"Eres un profesor de estadística de la UPChiapas. Te han subido unos datos cuyo resumen matemático es este:\n{resumen}\n\nResponde de forma clara a esta pregunta del alumno: {pregunta}"
                            
                            respuesta = modelo.generate_content(prompt)
                            st.info(respuesta.text)
                        except Exception as e:
                            st.error(f"Error de conexión con la API: {e}")
                else:
                    st.warning("Escribe una pregunta antes de enviar.")
        else:
            st.warning("🔑 Consigue tu API Key gratuita en Google AI Studio y pégala arriba para activar la inteligencia artificial.")

    else:
        st.warning("El archivo no contiene columnas numéricas.")
else:
    st.info("Esperando archivo CSV...")