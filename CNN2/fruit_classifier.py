from keras import layers
from keras import models
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator

train_dir = 'subsets/train'
validation_dir = 'subsets/validation'

train_datagen = ImageDataGenerator(rescale= 1./255)
test_datagen = ImageDataGenerator(rescale = 1./255)

train_generator = train_datagen.flow_from_directory(
  train_dir,
  target_size = (150, 150),
  batch_size = 20,
  class_mode = 'binary'
)

validation_generator = test_datagen.flow_from_directory(
  validation_dir,
  target_size = (150, 150),
  batch_size = 20,
  class_mode = 'binary'
)


model = models.Sequential()

model.add(layers.Conv2D(32, (3, 3), activation='relu',
                        input_shape = (150, 150, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(loss = 'binary_crossentropy',
              optimizer = optimizers.RMSprop(lr=1e-4),
              metrics = ['acc'])

history = model.fit_generator(
    train_generator,
    steps_per_epoch = 100,
    epochs = 30,
    validation_data = validation_generator,
    validation_steps = 50
)

model.save('rotten_vs_fresh_oranges.h5')
