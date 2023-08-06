import abc


# This is the pricing engine interface
# It defines all the compulsory methods.
class PricingEngineInterface(abc.ABC):
    @abc.abstractmethod
    def get_predicted_price(self):
        pass

    @abc.abstractmethod
    def get_vehicle_info(self, vin):
        pass

    @abc.abstractmethod
    def get_prediction_range(self):
        pass

    @abc.abstractmethod
    def get_accuracy_and_prediction(self):
        pass

    @abc.abstractmethod
    def get_prediction_graph(self):
        pass
