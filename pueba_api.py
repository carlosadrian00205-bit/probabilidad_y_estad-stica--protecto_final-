import google.generativeai as genai

# Tu llave directa
API_KEY = "AIzaSyDFNGRcFD52oNN-kk2lbyVok-9dX3zrUx8"
genai.configure(api_key=API_KEY)

print("Intentando conectar con el cerebro de Gemini...")

try:
    modelo = genai.GenerativeModel('gemini-pro')
    respuesta = modelo.generate_content("Hola, responde solo con la palabra: Conectado")
    print("¡ÉXITO! La IA dice:", respuesta.text)
except Exception as e:
    print("ERROR EXACTO:", e)