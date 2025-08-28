import json
import numpy as np
import tensorflow as tf

class SeerEngine:
    def __init__(self, model_path='chrono_os_seer.tflite', vocab_path='app_vocab.json'):
        """
        Initializes the Seer by loading the TFLite model and vocabulary.
        """
        with open(vocab_path, 'r') as f:
            self.app_to_int = json.load(f)
        
        self.int_to_app = {i: app for app, i in self.app_to_int.items()}
        
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
        print("Seer Engine initialized successfully.")

    def predict_next_apps(self, recent_apps, num_predictions=4):
        """
        Predicts the most likely next apps based on recent usage.
        
        :param recent_apps: A list of the most recent app names.
        :param num_predictions: The number of top predictions to return.
        :return: A list of predicted app names.
        """
        input_sequence = [self.app_to_int.get(app, -1) for app in recent_apps]
        input_sequence = [id for id in input_sequence if id != -1]

        input_data = np.array([input_sequence], dtype=np.float32)

        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        
        top_indices = np.argsort(output_data)[-num_predictions:][::-1]
        
        predicted_apps = [self.int_to_app.get(i, "unknown") for i in top_indices]
        
        return predicted_apps

