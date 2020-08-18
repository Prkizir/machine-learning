from keras.preprocessing import image 
from keras import models
import numpy as np
import matplotlib.pyplot as plt
#to test an image, you must have a the  model already trained and stored in a file

model = models.load_model("my_model.h5")  #model to be loaded

#\cats_and_dogs_small\test\cats
img_path = 'dog2.jpg'   #image to be tested

#image preprocessing to be used
img = image.load_img(img_path,  target_size=(64,64,3))
img_tensor = image.img_to_array(img)
img_tensor = np.expand_dims(img_tensor, axis = 0)
img_tensor /= 255.

#model response
answer  = model.predict_classes(img_tensor)
class_value = model.predict_classes(img_tensor)
confindence = model.predict(img_tensor)
print("class: %s confidence (prob of being 1) %s" % (class_value[0][0], confindence[0][0]))
plt.imshow(img_tensor[0])
plt.show()
