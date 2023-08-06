from source.model.car import Car


# this class is use to store the objects
class AccuracyPredictionStore:
    def __init__(self):
        # self.car = Car()
        self.vin = {
            self.algorithm_name: Car(),
        }
