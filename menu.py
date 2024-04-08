import customtkinter as ctk
import cv2
import mediapipe as mp
import threading

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

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
        button_callback(1)
    
    
    if (index_tip_y < index_pip_y and
        middle_tip_y < middle_pip_y and
        ring_tip_y > ring_pip_y and
        pinky_tip_y > pinky_pip_y):
        button_callback(2)
        
    if (index_tip_y < index_pip_y and
        middle_tip_y < middle_pip_y and
        ring_tip_y < ring_pip_y and
        pinky_tip_y > pinky_pip_y):
        button_callback(3)
    
    
    if (index_tip_y < index_pip_y and
        middle_tip_y < middle_pip_y and
        ring_tip_y < ring_pip_y and
        pinky_tip_y < pinky_pip_y):
        button_callback(4)

        
        
def button_callback(button_number):
    print(f"Button {button_number} pressed")
    

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


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("My App")
app.geometry("600x400")

button_texts = ["pregunta 1", "pregunta 2", "pregunta 3", "pregunta 4"]
for i, text in enumerate(button_texts):
    button = ctk.CTkButton(app, text=text, command=lambda i=i: button_callback(i+1))
    button.grid(row=i//2, column=i%2, padx=20, pady=20)


webcam_thread = threading.Thread(target=hilo_camara)
webcam_thread.start()


app.mainloop()
