import openai
import streamlit as st
import random
import os

# Configurar la conexión a OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

openai.api_key = "your_api_key"

# Función para generar preguntas utilizando GPT-3
def generar_preguntas(tema, n):
    preguntas = []
    for i in range(n):
        prompt = f"Genera una pregunta de opción múltiple sobre {tema}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=2024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        pregunta = response.choices[0].text.strip()
        preguntas.append(pregunta)
    return preguntas

# Función para generar opciones de respuesta aleatorias
def generar_opciones(respuesta_correcta, opciones):
    opciones.remove(respuesta_correcta)
    opciones = random.sample(opciones, 3)
    opciones.append(respuesta_correcta)
    random.shuffle(opciones)
    return opciones

# Generar el examen
def generar_examen(tema, n):
    examen = []
    preguntas = generar_preguntas(tema, n)
    for pregunta in preguntas:
        prompt = f"Genera opciones de respuesta para la siguiente pregunta de opción múltiple: {pregunta}"
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        respuesta_correcta = response.choices[0].text.strip()
        opciones = generar_opciones(respuesta_correcta, response.choices[0].options)
        examen.append({
            "pregunta": pregunta,
            "opciones": opciones,
            "respuesta_correcta": respuesta_correcta
        })
    return examen

# Mostrar el examen al usuario
def mostrar_examen(examen):
    st.title(f"Examen de opción múltiple sobre {tema}")
    puntaje_total = 0
    for i, pregunta in enumerate(examen):
        st.subheader(f"Pregunta {i+1}")
        st.write(pregunta["pregunta"])
        respuesta_seleccionada = st.radio("Seleccione una respuesta", pregunta["opciones"])
        pregunta["respuesta_seleccionada"] = respuesta_seleccionada
        if respuesta_seleccionada == pregunta["respuesta_correcta"]:
            puntaje_total += 1
    st.write(f"Tu puntaje total es {puntaje_total}/{len(examen)}")

# Interfaz de usuario con botón "Generar examen"
st.title("Generador de exámenes de opción múltiple")
tema = st.text_input("Ingrese el tema del examen")
n = st.slider("Número de preguntas", 1, 20, 10)
if st.button("Generar examen"):
    examen = generar_examen(tema, n)
    mostrar_examen(examen)
