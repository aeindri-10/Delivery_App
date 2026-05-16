from flask import Flask, request, jsonify
import pickle
import sys

app = Flask(__name__)

class DeliveryModel:
    def __init__(self):
        self.base_time = 0.5
        self.dist_coeff = 0.2
        self.weight_coeff = 0.1

    def predict(self, distance, weight):
        return self.base_time + (distance * self.dist_coeff) + (weight * self.weight_coeff)

class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == '__main__':
            return DeliveryModel
        return super().find_class(module, name)

with open('delivery_model.pkl', 'rb') as file:
    model = CustomUnpickler(file).load()

@app.route('/')
def home():
    return "Delivery Prediction API is Running!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    dist = data.get('distance')
    weight = data.get('weight')
    
    prediction = model.predict(dist, weight)
    
    return jsonify({
        "estimated_delivery_time_hours": round(prediction, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)
