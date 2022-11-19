import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing import image
import os
from keras.utils import load_img,img_to_array

class Video(object): 
	def __init__(self):
		self.video = cv2.VideoCapture(0)
		self.roi_start = (50, 150)
		self.roi_end = (250, 350)
		self.model = load_model('C:/Users/rohit/OneDrive/Desktop/VII/IBM-Project-19465-1659698319/Project Development Phase/Sprint 2/asl.h5') # Execute Local Trained Model
		self.index=['A','B','C','D','E','F','G','H','I']
		self.y = None

	def __del__(self):
		k = cv2.waitKey(1)
		self.video.release()
	
	def get_frame(self):
		ret,frame = self.video.read()
		frame = cv2.resize(frame,(640,480))
		ret,jpg = cv2.imencode('.jpg', frame)
		return jpg.tobytes()