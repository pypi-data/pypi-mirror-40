import os
from abc import ABCMeta, abstractmethod

import cloudpickle

import mlflow.pyfunc
from mlflow.models import Model
from mlflow.utils.file_utils import TempDir 
from mlflow.utils.file_utils import _copy_file_or_tree 
from mlflow.utils.model_utils import _get_flavor_configuration
from mlflow.tracking.utils import _get_model_log_dir


class Artifact:

    def __init__(self, path, run_id=None):
        self.path = path
        self.run_id = run_id

class PyfuncModel(object):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        self.artifacts = {}
        self.objects = {}
        self._tmp_artifacts_dir = TempDir()
        self._tmp_artifacts_dir.__enter__()

        for name, item in kwargs.items():
            if isinstance(item, Artifact):
                self.artifacts[name] = self._fetch_artifact(name=name, artifact=item) 
            else:
                self.objects[name] = item

    @staticmethod
    @abstractmethod
    def set_up(self, **kwargs):
        pass

    @abstractmethod
    def predict(self, input_df):
        pass

    def _fetch_artifact(self, name, artifact):
        artifact_path = artifact.path
        if artifact.run_id is not None:
            artifact_path = _get_model_log_dir(artifact_path, artifact.run_id)

        tmp_artifact_base_path = self._tmp_artifacts_dir.path("artifact-{artifact_name}".format(
            artifact_name=name))
        tmp_artifact_subpath = _copy_file_or_tree(
                src=artifact_path, dst=tmp_artifact_base_path, dst_dir=None)
        tmp_artifact_path = os.path.join(tmp_artifact_base_path, tmp_artifact_subpath)

        return tmp_artifact_path

    def save(self, path, conda_env=None, code=None):
        path = os.path.abspath(path)
        if os.path.exists(path):
            raise Exception
        os.makedirs(path)

        saved_artifacts = {}
        artifacts_dir_subpath = "artifacts"
        os.makedirs(os.path.join(path, artifacts_dir_subpath))
        for artifact_name, artifact_path in self.artifacts.items():
            dst_artifact_subpath = os.path.join(artifacts_dir_subpath, artifact_name)
            dst_artifact_subpath = os.path.join(
                    dst_artifact_subpath, 
                    _copy_file_or_tree(
                        src=artifact_path, dst=path, dst_dir=dst_artifact_subpath))
            saved_artifacts[artifact_name] = dst_artifact_subpath

        init_fn_subpath = "init.pkl"
        with open(os.path.join(path, init_fn_subpath), "wb") as out:
            cloudpickle.dump(self.set_up, out)

        predict_fn_subpath = "predict.pkl"
        with open(os.path.join(path, predict_fn_subpath), "wb") as out:
            cloudpickle.dump(self.predict, out)

        model_conf = Model()
        pyfunc_conf_kwargs = {
            "model": model_conf,
            "loader_module": "mlflow.pyfunc.builder6",
            "artifacts": saved_artifacts,
            "predict_fn": predict_fn_subpath,
            "init_fn": init_fn_subpath,
            "data": None,
        }

        mlflow.pyfunc.add_to_model(**pyfunc_conf_kwargs)
        model_conf.save(os.path.join(path, "MLmodel"))

    def log(self, artifact_path, conda_env=None, code=None):
        pass


def _load_pyfunc(path):
    from mlflow.utils.model_utils import _get_flavor_configuration
    flavor_conf = _get_flavor_configuration(path, mlflow.pyfunc.FLAVOR_NAME)

    with open(os.path.join(path, flavor_conf["predict_fn"]), "rb") as f:
        predict_fn = cloudpickle.load(f)

    with open(os.path.join(path, flavor_conf["init_fn"]), "rb") as f:
        init_fn = cloudpickle.load(f)

    artifacts = {}
    for artifact_name, artifact_path in flavor_conf["artifacts"].items():
        artifact_path = os.path.join(path, artifact_path)
        artifacts[artifact_name] = artifact_path

    print(artifacts)
    wrapper = _PyfuncWrapper(predict_fn=predict_fn)
    init_fn(wrapper, **artifacts)

    return wrapper

class _PyfuncWrapper(object):

    def __init__(self, predict_fn):
        self.predict = predict_fn


class FilterALSModel(PyfuncModel):

    def __init__(self, als_model, whitelist):
        super(FilterALSModel, self).__init__(als_model=als_model, whitelist=whitelist)

    @staticmethod
    def set_up(self, als_model=None, whitelist=None):
        self.als_model = als_model
        self.whitelist = whitelist

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

    model = FilterALSModel(als_model=Artifact(path=als_model_path), 
                           whitelist=Artifact(path=whitelist_path))

    model.save("testmodel1")
