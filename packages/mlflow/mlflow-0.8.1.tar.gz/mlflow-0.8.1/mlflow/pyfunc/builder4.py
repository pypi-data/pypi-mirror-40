from abc import ABCMeta, abstractmethod

class PyfuncWrapper(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, artifacts, objects):
        pass

    @abstractmethod
    def predict(self, input_df):
        pass


def save_model(path, artifacts, objects, wrapper, conda_env, code=None):
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


    artifacts = {
        "als_model": {
            "path": "<model_path>",
            "run_id": "<run_id>"
        },
        "whitelist": {
            "path": "<whitelist_path>"
        }
    }

    # Eventually, `artifacts` could be something like
    # artifacts = {
    #     "als_model": "artifact://run_id:path",
    #     "whitelist": "/absolute/path/to/whitelist",
    # }

    save_model("my_custom_model", artifacts=artifacts, objects=None, wrapper=FilterALSWrapper, 
               conda_env=None, code=None) 
