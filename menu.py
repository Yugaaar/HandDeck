import PIL.Image
import customtkinter as ctk
import cv2
import mediapipe as mp
import threading
import time
import PIL
from PIL import Image
from pymongo import MongoClient

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands




                      
                      
def obtener_pregunta_y_opciones(n_pregunta):
    cliente = MongoClient('localhost', 27017)
    base_de_datos = cliente["Manos"]
    coleccion = base_de_datos["Opciones"]
    documento = coleccion.find_one()
    preguntas = documento['preguntas']
    opciones = preguntas[n_pregunta]['opciones']
    
    return preguntas, opciones

def detectar_gestos(hand_landmarks):
    index_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
    middle_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
    ring_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
    pinky_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y
    
    index_pip_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
    middle_pip_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
    ring_pip_y = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y
    pinky_pip_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y
    
    if (index_tip_y < index_pip_y and
        middle_tip_y > middle_pip_y and
        ring_tip_y > ring_pip_y and
        pinky_tip_y > pinky_pip_y):
        button_callback(0)
    
    
    if (index_tip_y < index_pip_y and
        middle_tip_y < middle_pip_y and
        ring_tip_y > ring_pip_y and
        pinky_tip_y > pinky_pip_y):
        button_callback(1)
        
    if (index_tip_y < index_pip_y and
        middle_tip_y < middle_pip_y and
        ring_tip_y < ring_pip_y and
        pinky_tip_y > pinky_pip_y):
        button_callback(2)
    
    
    if (index_tip_y < index_pip_y and
        middle_tip_y < middle_pip_y and
        ring_tip_y < ring_pip_y and
        pinky_tip_y < pinky_pip_y):
        button_callback(3)

        
        
def button_callback(button_number):
    global n_pregunta, preguntas, opciones
    print(f"Seleccion: ", opciones[button_number])
    n_pregunta += 1
    if n_pregunta < len(preguntas):
        preguntas, opciones = obtener_pregunta_y_opciones(n_pregunta)
        update_gui()
    time.sleep(2)



def clear_gui():
    for widget in app.winfo_children():
        widget.grid_forget()

def update_gui():
    clear_gui()
    title_label = ctk.CTkLabel(app, text=preguntas[n_pregunta]['pregunta'] , font=("Helvetica", 29))
    title_label.grid(row=0, columnspan=2, pady=10)
    button_texts = [opciones[0], opciones[1], opciones[2], opciones[3]]
    for i, text in enumerate(button_texts):
        button = ctk.CTkButton(app, text=text, command=lambda i=i: button_callback(i), height=80, width=55, font=('helvetica', 15))
        button.grid(row=i//2 + 1, column=i%2, padx=150, pady=20)
    

def hilo_camara():
    camara = cv2.VideoCapture(0)
    with mp_hands.Hands(model_complexity=1, min_detection_confidence=0.6, min_tracking_confidence=0.5) as hands:
        while camara.isOpened():
            exito, image = camara.read()
            if not exito:
                print("No hay cámara")
                continue
            
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
                    gesto = detectar_gestos(hand_landmarks)
                    

            cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):  
                break
    
    camara.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    n_pregunta = 0
    preguntas, opciones = obtener_pregunta_y_opciones(n_pregunta)
    


    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("tema.json")

    app = ctk.CTk()
    app.title("My App")
    app.geometry("1000x600")
    app.update
    
    update_gui()

    title_label = ctk.CTkLabel(app, text=preguntas[n_pregunta]['pregunta'] , font=("Helvetica", 29))
    title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

    
    button_font = ("Helvetica", 50)
    button_texts = [opciones[0],opciones[1],opciones[2],opciones[3]]
    for i, text in enumerate(button_texts):
        button = ctk.CTkButton(app, text=text, command=lambda i=i: button_callback(i), height=80, width=55, font=('helvetica', 15))
        button.grid(row=i//2 + 1, column=i%2, padx=150, pady=20)


    image = PIL.Image.open('descarga.PNG')
    background_image = ctk.CTkImage(image, size=(150, 100))

    bg_lbl = ctk.CTkLabel(app, text="", image=background_image)
    bg_lbl.place(x=400, y=400)




    webcam_thread = threading.Thread(target=hilo_camara)
    webcam_thread.start()

    app.mainloop()