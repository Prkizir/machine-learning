import matplotlib.pyplot as plt

from keras import layers
from keras import models
from keras import optimizers

from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator

# Train and Validation Directories
train_dir = 'subsets/train'
validation_dir = 'subsets/validation'

# Train Data Augmentation
train_datagen = ImageDataGenerator(
    rescale= 1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(rescale = 1./255)

# Train Classes from Dataset (Binary)
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size = (150, 150),
    batch_size = 32,
    class_mode = 'binary'
)

# Validation Classes from Dataset (Binary)
validation_generator = test_datagen.flow_from_directory(
    validation_dir,
    target_size = (150, 150),
    batch_size = 32,
    class_mode = 'binary'
)


# Model Architecture

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
model.add(layers.Dropout(0.5))
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

# Compile the Model
model.compile(loss = 'binary_crossentropy',
              optimizer = optimizers.RMSprop(lr=1e-4),
              metrics = ['acc'])

# Train the Model for 100 epochs
history = model.fit_generator(
    train_generator,
    steps_per_epoch = 100,
    epochs = 100,
    validation_data = validation_generator,
    validation_steps = 50
)

# Accuracy Data
acc = history.history['acc']
val_acc = history.history['val_acc']

# Loss Data
loss = history.history['loss']
val_loss = history.history['val_loss']

# Epochs
epochs = range(1, len(acc) + 1)

# Plot Training vs Validation Accuracy
plt.plot(epochs, acc, 'bo', label = 'Training acc')
plt.plot(epochs, val_acc, 'b', label = 'Validation acc')
plt.title('Training and validation Accuracy')
plt.legend()

plt.figure()

# Plot Training vs Validation Loss
plt.plot(epochs, loss, 'bo', label = 'Training loss')
plt.plot(epochs, val_loss, 'b', label = 'Validation loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()

# Save the Trained Model as a HDF5 File Type
model.save('rotten_vs_fresh_oranges_2.h5')
