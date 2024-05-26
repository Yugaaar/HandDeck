import cv2
import mediapipe as mp
import mouse
import pyautogui
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def calcular_distancia(p1, p2):
    return ((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2) ** 0.5

def mover_raton(dedo):
    screen_width, screen_height = pyautogui.size()
    mouse.move(screen_width - int(dedo.x * screen_width), int(dedo.y * screen_height))
    
def click(distancia):
    if (distancia <= 0.05):
        mouse.click('left')
        time.sleep(0.5)
        
def dibujar_linea(dedo1, dedo2):
    cv2.line(image, (int(dedo1.x * image.shape[1]), int(dedo1.y * image.shape[0])),
                         (int(dedo2.x * image.shape[1]), int(dedo2.y * image.shape[0])), (0, 0, 255), 2)

camara = cv2.VideoCapture(0)
with mp_hands.Hands(model_complexity=1,min_detection_confidence=0.6,min_tracking_confidence=0.5) as hands:
    while camara.isOpened:
        exito, image = camara.read()
        if not exito:
            print("no hay camara")
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
                
                pulgar = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                indice = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                menique = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
                corazon = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                
                falangemediomedio = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
                
                
                mover_raton(indice)
                dibujar_linea(pulgar,falangemediomedio)
                click(calcular_distancia(pulgar, falangemediomedio))
                print(calcular_distancia(pulgar,falangemediomedio ))
                
        cv2.imshow('Handeck', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:  #27 el asci del escape 
            break
  
camara.release