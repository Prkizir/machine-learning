import numpy as np

from keras import models
from keras.preprocessing import image

# Trained Model
model = models.load_model("rotten_vs_fresh_oranges_2.h5")

json_model = model.to_json()

with open('rvfo.json','w') as json_file:
    json_file.write(json_model)

model.save_weights('rvfo_weights.h5')
