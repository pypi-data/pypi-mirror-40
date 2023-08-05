from abc import ABCMeta, abstractmethod

class PredictionContext(object):

    def __init__(self, params, artifacts):
        self._params = params
        self._artifacts = artifacts

    @property
    def params(self):
        return self._params

    @property
    def artifacts(self):
        return self._artifacts


class PyfuncModelWrapper(object):

    __metaclass__ = ABCMeta

    def __init__(self, context):
        self.context = context

    @abstractmethod
    def predict(self, input_df):
        pass


def save_model(path, wrapper, params, artifacts, code=None, conda_env=None):
    pass
