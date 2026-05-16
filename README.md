# Eco-Formula Delivery Time Predictor API

A production-ready Flask microservice that estimates package delivery times (in hours) for bike couriers based on customer distance and package weight. The core logic relies on a specialized machine learning "Eco-Formula" designed to balance operational efficiency and courier well-being.

---

## 📋 Project Architecture

This repository forms a complete Machine Learning Deployment Pipeline in miniature, split into three functional stages:
1. **Training Stage (`train.py`):** Encapsulates the tracking variables and mathematical logic inside an objective object structure and serializes it into a persistent storage file (`delivery_model.pkl`).
2. **Serving Stage (`app.py`):** Instantiates a lightweight Flask web application that serves a public REST API endpoint to accept inputs, process calculations, and safely reconstruct pickled model architectures inside production environments.
3. **Deployment Configuration (`requirements.txt`):** Enumerates specific application dependencies required to instantiate a high-concurrency production gateway via Gunicorn.

```text
├── train.py               # Serializes the formula and model parameters
├── app.py                 # Core API code featuring the Custom Unpickler fix
├── requirements.txt       # Production library definitions
└── delivery_model.pkl     # Frozen machine learning brain / serialized class
```

---

## 🧮 Core Formula & Business Logic

The startup utilizes an operational **Eco-Formula** to ensure bike couriers are never overloaded with unrealistic schedules. The delivery time estimation behaves linearly:

$$Time = 0.5 + (Distance \times 0.2) + (Weight \times 0.1)$$

### Variables Explained:
- **Base Overhead (0.5 hours):** Accounting for sorting, order acceptance, courier dispatching, and safety checks.
- **Distance Coefficient (0.2 hours per unit distance):** Accounts for variable travel fatigue and route safety.
- **Weight Coefficient (0.1 hours per unit mass):** Accounts for physical expenditure adjustments for bike couriers moving heavy cargo.

---

## 🛠️ Implementation Details

### 1. Training Script (`train.py`)
This script instantiates the initial model parameters and writes out a binary serialization map. 

```python
import pickle

class DeliveryModel:
    def __init__(self):
        self.base_time = 0.5
        self.dist_coeff = 0.2
        self.weight_coeff = 0.1

    def predict(self, distance, weight):
        return self.base_time + (distance * self.dist_coeff) + (weight * self.weight_coeff)

if __name__ == '__main__':
    model = DeliveryModel()
    with open('delivery_model.pkl', 'wb') as file:
        pickle.dump(model, file)
    print("Model has been trained and saved as delivery_model.pkl")
```

### 2. Serving Script (`app.py` with Production Pickle Fix)
When deploying a serialized Python object to a WSGI server managed by **Gunicorn**, the execution runtime reassigns the local environment's namespace module framework (`__main__`). Standard unpicklers will fail to match namespace tracking records, resulting in an `AttributeError: module '__main__' has no attribute 'DeliveryModel'`.

To resolve this, a robust custom deserialization handler overrides module mappings, routing Gunicorn dynamically to the structural object architecture defined inside the server module.

```python
from flask import Flask, request, jsonify
import pickle
import sys

app = Flask(__name__)

# --- MODEL DEFINITION ---
class DeliveryModel:
    def __init__(self):
        self.base_time = 0.5
        self.dist_coeff = 0.2
        self.weight_coeff = 0.1

    def predict(self, distance, weight):
        return self.base_time + (distance * self.dist_coeff) + (weight * self.weight_coeff)

# --- ROBUST PICKLE LOADING FIX ---
class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == '__main__':
            return DeliveryModel
        return super().find_class(module, name)

# Load the saved model through our isolated namespace mapping proxy
with open('delivery_model.pkl', 'rb') as file:
    model = CustomUnpickler(file).load()

@app.route('/')
def home():
    return "Delivery Prediction API is Running!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request payload. Content-Type must be application/json"}), 415
        
    dist = data.get('distance')
    weight = data.get('weight')
    
    if dist is None or weight is None:
        return jsonify({"error": "Missing 'distance' or 'weight' fields in JSON"}), 400
        
    prediction = model.predict(float(dist), float(weight))
    return jsonify({
        "estimated_delivery_time_hours": round(prediction, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)
```

### 3. Dependencies (`requirements.txt`)
```text
flask
gunicorn
```

---

## 🚀 Deployment Manual (Render Ecosystem)

Because the continuous integration environment may operate with restricted Git scopes, use a **Public Repository Framework** to interface seamlessly with Render without requiring third-party OAuth access profiles.

1. Create an independent, clean public GitHub repository.
2. Direct-upload your local workspace files (`train.py`, `app.py`, `requirements.txt`, and your generated `delivery_model.pkl`).
3. Access your account space on the [Render Dashboard](https://render.com).
4. Click **New +** $\rightarrow$ **Web Service**.
5. Select the **Public Git Repository** option tab and input the public GitHub project link:
   `https://github.com/your-username/your-repository-name`
6. Set the system parameters inside the configuration screen exactly as follows:
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** `Free`
7. Click **Create Web Service** and track the active terminal output streaming to your dashboard view until the build deployment signals confirmation (`Your service is live 🎉`).

---

## 🧪 Verification & API Endpoint Contract

### Request Definition:
- **HTTP Method:** `POST`
- **Path Location:** `/predict`
- **Request Headers:** `Content-Type: application/json`

#### Body Payload Example (JSON Format):
```json
{
  "distance": 10,
  "weight": 5
}
```

### Response Profile (JSON Format):
```json
{
  "estimated_delivery_time_hours": 3.0
}
```

### 📐 Calculator Mathematical Verification (PEMDAS Proof)

To validate the deployment execution state alongside runtime calculations, evaluate the linear criteria profile externally against a scientific layout context:

$$\text{Target Inputs: } \text{Distance} = 10, \quad \text{Weight} = 5$$

$$\text{Execution Pipeline: } \text{Time} = 0.5 + (10 \times 0.2) + (5 \times 0.1)$$
$$\text{Step 1 (Fatigue Adjustment): } 10 \times 0.2 = 2.0$$
$$\text{Step 2 (Mass Adjustment): } 5 \times 0.1 = 0.5$$
$$\text{Step 3 (Overhead Aggregation): } 0.5 + 2.0 + 0.5 = 3.0 \text{ hours}$$

The absolute correlation between Postman UI telemetry output records and standard functional criteria proves the validity of the underlying system model architecture.
