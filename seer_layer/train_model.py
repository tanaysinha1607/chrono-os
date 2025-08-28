import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

# --- Load Processed Data ---
data = np.load('processed_data.npz')
X = data['X']
y = data['y']
vocab_size = data['vocab_size'][0]

SEQUENCE_LENGTH = X.shape[1]
EMBEDDING_DIM = 64  
LSTM_UNITS = 128    

print("Building the LSTM model...")
model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=EMBEDDING_DIM, input_length=SEQUENCE_LENGTH),
    LSTM(LSTM_UNITS, return_sequences=False),     
    Dense(vocab_size, activation='softmax')
])

model.summary()

# Compiling
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

checkpoint = ModelCheckpoint('best_app_predictor.h5', monitor='val_accuracy', save_best_only=True, mode='max')
#early stop
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# Training 
print("\nStarting model training...")
history = model.fit(
    X, y,
    epochs=50,
    batch_size=128,
    validation_split=0.2, 
    callbacks=[checkpoint, early_stopping]
)

print("\nTraining complete. Best model saved as best_app_predictor.h5")