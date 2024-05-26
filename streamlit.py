import streamlit as st
from pymongo import MongoClient
import json

def cargar_datos_desde_json():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['encuesta']
    collection = db['preguntas']
    if collection.count_documents({}) == 0:
        with open('preguntas.json') as f:
            preguntas = json.load(f)
            collection.insert_many(preguntas)

def main():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['encuesta']
    collection = db['preguntas']
    pregunta = collection.aggregate([{"$sample": {"size": 1}}]).next()
    st.subheader('Cuestionario')
    st.title(pregunta['texto'])
    opciones = pregunta['opciones']
    cols = st.columns(2)
    for i, opcion in enumerate(opciones):
        with cols[i % 2]:
            st.button(opcion, key=i, use_container_width=True)

cargar_datos_desde_json()

if __name__ == "__main__":
    main()
