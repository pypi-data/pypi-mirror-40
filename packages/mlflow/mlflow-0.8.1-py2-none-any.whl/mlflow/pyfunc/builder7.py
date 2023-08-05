import os
from abc import ABCMeta, abstractmethod

import cloudpickle

import mlflow.pyfunc
from mlflow.models import Model
from mlflow.utils.file_utils import TempDir 
from mlflow.utils.file_utils import _copy_file_or_tree 
from mlflow.utils.model_utils import _get_flavor_configuration
from mlflow.tracking.utils import _get_model_log_dir


class PyfuncWrapper(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def predict(self, input_df):
        pass

    @classmethod
    def create_dependencies(cls, *args, **kwargs):
        import inspect
        print(inspect.getargspec(cls.__init__))


def save_model(path, wrapper, conda_env=None, code=None, *args, **kwargs):
    path = os.path.abspath(path)
    if os.path.exists(path):
        raise Exception
    os.makedirs(path)

    saved_artifacts = {}
    artifacts_dir_subpath = "artifacts"
    os.makedirs(os.path.join(path, artifacts_dir_subpath))
    for artifact_name, artifact_path in kwargs.items():
        dst_artifact_subpath = os.path.join(artifacts_dir_subpath, artifact_name)
        dst_artifact_subpath = _copy_file_or_tree(
                    src=artifact_path, dst=path, dst_dir=dst_artifact_subpath)
        saved_artifacts[artifact_name] = dst_artifact_subpath

    wrapper_subpath = "wrapper.pkl"
    with open(os.path.join(path, "wrapper.pkl"), "wb") as out:
        cloudpickle.dump(wrapper, out)

    model_conf = Model()
    pyfunc_conf_kwargs = {
        "model": model_conf,
        "loader_module": "mlflow.pyfunc.builder7",
        "artifacts": saved_artifacts,
        "wrapper": wrapper_subpath,
        "data": None,
    }

    mlflow.pyfunc.add_to_model(**pyfunc_conf_kwargs)
    model_conf.save(os.path.join(path, "MLmodel"))


def _load_pyfunc(path):
    from mlflow.utils.model_utils import _get_flavor_configuration
    flavor_conf = _get_flavor_configuration(path, mlflow.pyfunc.FLAVOR_NAME)

    with open(os.path.join(path, flavor_conf["wrapper"]), "rb") as f:
        Wrapper = cloudpickle.load(f)

    artifacts = {}
    for artifact_name, artifact_path in flavor_conf["artifacts"].items():
        artifact_path = os.path.join(path, artifact_path)
        artifacts[artifact_name] = artifact_path

    wrapper = Wrapper(**artifacts)

    return wrapper


class FilterALSWrapper(PyfuncWrapper):

    def __init__(self, als_model, whitelist):
        self.als_model = als_model
        with open(whitelist, "r") as f:
            self.whitelist = f.read() 

    def predict(self, input_df):
        print(self.als_model)
        print(self.whitelist)

if __name__ == "__main__":
    als_model_path = "/tmp/als_model.test"
    with open(als_model_path, "w") as f:
        f.write("TESTMODEL")

    whitelist_path = "/tmp/whitelist.test"
    with open(whitelist_path, "w") as f:
        f.write("WHITELIST")

    FilterALSWrapper.create_dependencies("cat")
    # save_model(path="testmodel1", wrapper=FilterALSWrapper, als_model=als_model_path, whitelist=whitelist_path)
