import numpy as np
from PIL import Image
import dlib
import cv2
from imutils import face_utils


def get_faces(file_path):
    img_input = np.array(Image.open(file_path))
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')
    try:
        img_gray = cv2.cvtColor(img_input, cv2.COLOR_BGR2GRAY)
    except cv2.error as e:
        img_gray = img_input
    rectangles = detector(img_gray, 0)

    faces = []
    for r in rectangles:
        shape = predictor(img_gray, r)
        faces.append(face_utils.shape_to_np(shape))

    return faces
