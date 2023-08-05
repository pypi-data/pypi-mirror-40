from abc import ABCMeta, abstractmethod

class PyfuncWrapper(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, artifacts, objects):
        pass

    @abstractmethod
    def predict(self, input_df):
        pass


class PyfuncBuilder(object):

    def __init__(self):
        self.artifacts = {}
        self.objects = {}
        self.wrapper = None

    def set_wrapper(self, wrapper):
        self.wrapper = wrapper

    def add_artifact(self, name, path, run_id=None):
        self.artifacts[name] = path # Do something with run_id too

    def add_object(self, name, py_obj):
        self.objects[name] = py_obj

    def save(self, path, conda_env=None, code=None):
        pass

    def log(self, path, conda_env=None, code=None):
        pass


if __name__ == "__main__":
    import mlflow.pyfunc

    class FilterALSWrapper(PyfuncWrapper):

        def __init__(self, artifacts, objects):
            self.als_model = mlflow.pyfunc.load_model(artifacts["als_model"])
            with open(artifacts["whitelist"], "r") as f:
                self.whitelist = f.readlines()

        def predict(self, input_df):
            unfiltered_preds = self.als_model.predict(input_df)
            return filter(lambda item : item in self.whitelist, unfiltered_preds)


    builder = PyfuncBuilder()
    builder.set_wrapper(FilterALSWrapper)
    builder.add_artifact("als_model", "<model_path>", "<run_id>")
    builder.add_artifact("whitelist", "<whitelist_path", run_id=None)
    builder.save("my_custom_model", conda_env=None, code=None)
