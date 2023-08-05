import os
import shutil
from importlib import import_module

import dill
import cloudpickle

import mlflow.pyfunc
from mlflow.models import Model
from mlflow.utils.file_utils import TempDir 
from mlflow.utils.file_utils import _copy_file_or_tree 
from mlflow.utils.model_utils import _get_flavor_configuration
from mlflow.tracking.utils import _get_model_log_dir


class ModelContext:

    def __init__(self):
        self.artifacts = {}
        self.objects = {}

class PyfuncModelBuilder:

    def __init__(self):
        pass

    def add_object(self, name, py_obj):
        pass

    def add_artifact(self, name, path, run_id):
        pass

    def set_init(self, init_fn):
        pass

    def set_predict(self, predict_fn):
        pass
