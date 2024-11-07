from store import patient_image_store as pis
from dto.patient_image import Patient_image
import cv2
import numpy as np

# Load the input image
img = cv2.imread(r"C:\Users\devor\Downloads\images.png")

# Convert the image to bytes
image_bytes = cv2.imencode('.png', img)[1].tobytes()

# Create a Patient_image object
new_image = Patient_image(patientId="256987458", image=image_bytes)

# Insert the image into the database
pis.insert_image(new_image)
