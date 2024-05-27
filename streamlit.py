import streamlit as st
from pymongo import MongoClient
import json

def cargar_datos_desde_json():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['encuesta']
        collection = db['preguntas']
        if collection.count_documents({}) == 0:
            with open('preguntas.json') as f:
                preguntas = json.load(f)
                collection.insert_many(preguntas)
    except Exception:
        print(f"error accediendo a la bbdd: {Exception}")

def main():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['encuesta']
        collection = db['preguntas']    
        pregunta = collection.aggregate([{"$sample": {"size": 1}}]).next()
        st.subheader('Cuestionario')
        st.title(pregunta['texto'])
        opciones = pregunta['opciones']
        columnas = st.columns(2)
        for i, opcion in enumerate(opciones):
            with columnas[i % 2]:
                st.button(opcion, key=i, use_container_width=True)
    except Exception:
        print(f"error en el bucle principal: {Exception }")

cargar_datos_desde_json()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(f"error en el programa: {Exception}")
