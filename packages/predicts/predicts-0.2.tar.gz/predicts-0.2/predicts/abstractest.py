from abc import ABC, abstractmethod

class AbstracPrediction(ABC):

    def __init__(self):
        super(Prediction, self).__init__()

    @abstractmethod
    def predict(self):
        pass