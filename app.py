import openai
import streamlit as st

# Configuración de OpenAI
openai.api_key = "your_api_key"

# Función para generar preguntas utilizando GPT-3
def generar_preguntas(tema, n):
    preguntas = []
    for i in range(n):
        prompt = f"Genera una pregunta de respuesta corta sobre {tema}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        pregunta = response.choices[0].text.strip()
        preguntas.append(pregunta)
    return preguntas

# Generar el examen
def generar_examen(tema, n):
    examen = []
    preguntas = generar_preguntas(tema, n)
    for pregunta in preguntas:
        examen.append({
            "pregunta": pregunta,
            "respuesta_correcta": ""
        })
    return examen

# Mostrar el examen al usuario
def mostrar_examen(examen):
    st.title(f"Examen de respuesta corta sobre {tema}")
    puntaje_total = 0
    for i, pregunta in enumerate(examen):
        st.subheader(f"Pregunta {i+1}")
        st.write(pregunta["pregunta"])
        respuesta_seleccionada = st.text_input("Ingrese su respuesta")
        pregunta["respuesta_seleccionada"] = respuesta_seleccionada
        if respuesta_seleccionada.strip().lower() == pregunta["respuesta_correcta"].strip().lower():
            puntaje_total += 1
    st.write(f"Tu puntaje total es {puntaje_total}/{len(examen)}")

# Interfaz de usuario con botón "Generar examen"
st.title("Generador de exámenes de respuesta corta")
tema = st.text_input("Ingrese el tema del examen")
n = st.slider("Número de preguntas", 1, 20, 10)
if st.button("Generar examen"):
    examen = generar_examen(tema, n)
    mostrar_examen(examen)
