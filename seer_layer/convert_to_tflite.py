import tensorflow as tf
import numpy as np

keras_model_path = 'best_app_predictor.h5'
model = tf.keras.models.load_model(keras_model_path)
print("Keras model loaded successfully.")

converter = tf.lite.TFLiteConverter.from_keras_model(model)

converter.optimizations = [tf.lite.Optimize.DEFAULT]

converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS, 
    tf.lite.OpsSet.SELECT_TF_OPS 
]
converter._experimental_lower_tensor_list_ops = False

tflite_model = converter.convert()

tflite_model_path = 'chrono_os_seer.tflite'
with open(tflite_model_path, 'wb') as f:
    f.write(tflite_model)

print(f"\nModel converted and saved as {tflite_model_path}")
print(f"Original Keras model size: {tf.io.gfile.stat(keras_model_path).length / 1024:.2f} KB")
print(f"Quantized TFLite model size: {len(tflite_model) / 1024:.2f} KB")


print("\nVerifying the TFLite model...")
interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

dummy_input = np.random.randint(0, 50, size=input_details[0]['shape']).astype(np.float32)

interpreter.set_tensor(input_details[0]['index'], dummy_input)
interpreter.invoke()

# Prediction
output_data = interpreter.get_tensor(output_details[0]['index'])
predicted_app_index = np.argmax(output_data[0])

print("TFLite model verification successful.")
print(f"Input shape: {input_details[0]['shape']}")
print(f"Output shape: {output_details[0]['shape']}")
print(f"Dummy input prediction (top app index): {predicted_app_index}")