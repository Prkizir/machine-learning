import numpy as np
import matplotlib.pyplot as plt

from keras import models
from keras.preprocessing import image

# Trained Model
model = models.load_model("rotten_vs_fresh_oranges_2.h5")

print(model.summary())

# Image Source
#img_path = 'test1.png'

# Image Preprocessing to fit Model Criteria
#img = image.load_img(img_path,  target_size=(150,150,3))
#img_tensor = image.img_to_array(img)
#img_tensor = np.expand_dims(img_tensor, axis = 0)
#img_tensor /= 255.

# Model Response
#answer  = model.predict_classes(img_tensor)
#class_value = model.predict_classes(img_tensor)
#confindence = model.predict(img_tensor)
#print("class: %s confidence (prob of being 1) %s" % (class_value[0][0], confindence[0][0]))
#plt.imshow(img_tensor[0])
#plt.show()
