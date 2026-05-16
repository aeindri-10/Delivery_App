import pickle

class DeliveryModel:
    def __init__(self):
        self.base_time = 0.5
        self.dist_coeff = 0.2
        self.weight_coeff = 0.1

    def predict(self, distance, weight):
        # Time = 0.5 + (Distance * 0.2) + (Weight * 0.1)
        return self.base_time + (distance * self.dist_coeff)
        + (weight * self.weight_coeff)

model = DeliveryModel()

with open('delivery_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("Model has been trained and saved as delivery_model.pkl")