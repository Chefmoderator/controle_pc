import mss
import base64
import cv2
import numpy as np


class CameraManager:

    @staticmethod
    def get_screen():
        with mss.mss() as sct:
            img = np.array(sct.grab(sct.monitors[1]))
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            _, buffer = cv2.imencode(".jpg", img)
            encoded = base64.b64encode(buffer).decode("utf-8")
            return encoded

    @staticmethod
    def get_camera():
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            return None
        ret, frame = cam.read()
        cam.release()
        if not ret:
            return None
        _, buffer = cv2.imencode(".jpg", frame)
        encoded = base64.b64encode(buffer).decode("utf-8")
        return encoded
