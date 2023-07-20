
import cv2
import numpy as np



class Engine:
    def __init__(self):
        pass

    def load_object_detection_model(self, model_path, cfg_path):
        model = cv2.net