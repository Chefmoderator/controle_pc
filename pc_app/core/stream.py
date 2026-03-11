import mss
import base64
import numpy as np
import cv2

class Stream:
    @staticmethod
    def get_screen():
        with mss.mss() as sct:
            img = np.array(sct.grab(sct.monitors[1]))
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            _, buffer = cv2.imencode(".jpg", img)
            encoded = base64.b64encode(buffer).decode("utf-8")
            return encoded