from abc import abstractmethod

class PyfuncModelSpec(object):

    def __init__(self, artifacts, objects):
        pass

    @abstractmethod
    def set_up(self, artifacts, objects):
        pass
    
    @abstractmethod
    def predict(self, input_df):
        pass
