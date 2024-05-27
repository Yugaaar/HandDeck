import cv2
import mediapipe as mp
import mouse
import keyboard
import pyautogui
import time

class HandDeck:
    def __init__(self):
        self.eje_x = None
        self.eje_y = None
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        
    def calcular_distancia(self, p1, p2):
        return ((p2.x - p1.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5

    def mover_raton(self, dedo):
        screen_width, screen_height = pyautogui.size()
        coordenada_x = screen_width - int(dedo.x * screen_width)
        coordenada_y = int(dedo.y * screen_height)

        if self.eje_x == None or self.eje_y == None:
            suavizar_x, suavizar_y = coordenada_x, coordenada_y
        else:
            suavizar_x = int(self.eje_x + 0.2 * (coordenada_x - self.eje_x))
            suavizar_y = int(self.eje_y + 0.2 * (coordenada_y - self.eje_y))

        mouse.move(suavizar_x, suavizar_y)
        self.eje_x, self.eje_y = suavizar_x, suavizar_y


    def click(self, distancia):
        if distancia <= 0.05:
            mouse.click('left')
            time.sleep(0.5)

    def dibujar_linea(self, image, dedo1, dedo2, color):
        if color == "rojo":
            color = (255,0,0)
        if color == "verde":
            color = (0,255,0)
        if color == "azul":
            color = (0,0,255)
        
        cv2.line(image, (int(dedo1.x * image.shape[1]), int(dedo1.y * image.shape[0])),
                 (int(dedo2.x * image.shape[1]), int(dedo2          .y * image.shape[0])), color, 2)

    def run(self):
        try:
            camara = cv2.VideoCapture(0)
            with self.mp_hands.Hands(model_complexity=1, min_detection_confidence=0.6, min_tracking_confidence=0.5) as hands:
                while camara.isOpened():    
                    ret, image = camara.read()
                    if not ret:
                        print("error la camara")
                        break

                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    resultados = hands.process(image_rgb)

                    if resultados.multi_hand_landmarks:
                        for hand_landmarks in resultados.multi_hand_landmarks:
                            self.mp_drawing.draw_landmarks(
                                image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                                self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
                                self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2))

                            pulgar = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                            indice = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                            falange_medio_pip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP]

                            self.mover_raton(indice)
                            self.dibujar_linea(image, pulgar, falange_medio_pip, "rojo")
                            self.click(self.calcular_distancia(pulgar, falange_medio_pip))
                            
                  
                    cv2.imshow('Handeck manos', cv2.flip(image, 1))
                    if cv2.waitKey(5) & 0xFF == 27: #27 porque tiene que ser escape en asci
                        break

            camara.release()
            cv2.destroyAllWindows()
        except Exception:
            print(f"Error en el bucle principal {Exception}")
        finally:
            camara.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        main = HandDeck()
        main.run()
    except Exception:
        print(f"error en el programa: {Exception}")
    finally:
        cv2.destroyAllWindows()
        