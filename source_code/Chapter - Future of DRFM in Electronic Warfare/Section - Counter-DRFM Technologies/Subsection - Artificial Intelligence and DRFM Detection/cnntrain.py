import tensorflow as tf
from tensorflow.keras import layers, models

# Simple CNN for spectrogram inputs (batch, time, freq, 1)
def build_model(input_shape):
    x = layers.Input(shape=input_shape)
    y = layers.Conv2D(32, (3,3), activation='relu')(x)   # conv layer
    y = layers.MaxPool2D((2,2))(y)
    y = layers.Conv2D(64, (3,3), activation='relu')(y)
    y = layers.GlobalAveragePooling2D()(y)
    y = layers.Dense(64, activation='relu')(y)
    out = layers.Dense(1, activation='sigmoid')(y)      # binary output
    return models.Model(x, out)

# Assume train_ds yields (spectrogram, label) pairs
input_shape = (128, 256, 1)                             # time x freq x channel
model = build_model(input_shape)
model.compile(optimizer='adam', loss='binary_crossentropy',
              metrics=['AUC'])                          # monitor AUC

# Train with callbacks for early stopping and best-model checkpointing
callbacks = [tf.keras.callbacks.EarlyStopping(patience=5),
             tf.keras.callbacks.ModelCheckpoint('best.h5', save_best_only=True)]
model.fit(train_ds, validation_data=val_ds, epochs=50, callbacks=callbacks)
# Save a TfLite quantized model for edge deployment (post-training quantization recommended)