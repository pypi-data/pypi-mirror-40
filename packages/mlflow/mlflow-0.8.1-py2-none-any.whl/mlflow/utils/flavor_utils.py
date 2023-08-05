import os

from mlflow.exceptions import MlflowException
from mlflow.models import Model
from mlflow.protos.databricks_pb2 import RESOURCE_DOES_NOT_EXIST

def _get_flavor_configuration(model_configuration_path, flavor_name):
    """
    Obtains the configuration for the specified flavor from the specified
    model configuration (`MLmodel`) path. If the model does not contain
    the specified flavor, an exception will be thrown.

    :return: The flavor configuration as a dictionary
    """
    m = Model.load(os.path.join(model_configuration_path, 'MLmodel'))
    if flavor_name not in m.flavors:
        raise MlflowException("Model does not have {} flavor".format(flavor_name),
                              RESOURCE_DOES_NOT_EXIST)
    conf = m.flavors[flavor_name]
    return conf
    
