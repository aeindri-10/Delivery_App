from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

class DeliveryModel:
    def __init__(self):
        self.base_time = 0.5
        self.dist_coeff = 0.2
        self.weight_coeff = 0.1

    def predict(self, distance, weight):
        return self.base_time + (distance * self.dist_coeff) 
        + (weight * self.weight_coeff)

with open('delivery_model.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def home():
    return "Delivery Prediction API is Running!"

@app.route('/predict', methods=['POST'])
def predict():
    # Get JSON data from the request
    data = request.get_json()
    
    # Extract values
    dist = data.get('distance')
    weight = data.get('weight')
    
    # Calculate prediction
    prediction = model.predict(dist, weight)
    
    # Return the result as JSON
    return jsonify({
        "estimated_delivery_time_hours": round(prediction, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)