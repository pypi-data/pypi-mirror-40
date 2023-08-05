
import os
from subprocess import check_output, Popen, PIPE, STDOUT

from azureml.core.model import Model

def get_conda_bin_path():
    conda_symlink_cmd = "which conda"
    symlink_path = check_output(conda_symlink_cmd.split(" ")).decode("utf-8").rstrip()
    conda_full_path_cmd = "realpath {symlink_path}".format(symlink_path=symlink_path)
    full_path = check_output(conda_full_path_cmd.split(" ")).decode("utf-8").rstrip()
    return os.path.dirname(full_path)

def init():
    # model_path = Model.get_model_path(model_name="{model_name}", version={model_version})
    model_path = os.path.abspath(Model.get_model_path(model_name="mlflow-1vcm3o1usdqw56g28fmctg"))
    conda_bin_path = get_conda_bin_path()
    conda_activate_path = os.path.join(conda_bin_path, "activate")

    import multiprocessing
    cmd = ("source {conda_activate_path} {conda_env_name} &&"
            " gunicorn --timeout 60 -k gevent -b 127.0.0.1:8080 -w {nworkers}"
           " 'mlflow.sagemaker.container.scoring_server.wsgi:app(model_path=\"{model_path}\")'").format(
                       conda_activate_path=conda_activate_path,
                       model_path=model_path,
                       nworkers=multiprocessing.cpu_count(),
                       conda_env_name="custom_env")


    # cmd = ("source {{conda_activate_path}} {conda_env_name} && python py27server.py" 
    #        "{{model_path}}".format(
    #             activate_path=conda_activate_path, model_path=model_path))
    cmd = ["/bin/bash", "-c", cmd]

    # proc = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    print(cmd)
    proc = Popen(cmd)
    proc.wait()

def run(s):
    import requests
    print(s)
    response = requests.post(
            url="http://localhost:8080/invocations",
            headers={"Content-type": "application/json"},
            data=s)
    return response.text
    #
    # input_df = pd.read_json(s, orient="records")
    # return get_jsonable_obj(model.predict(input_df))

if __name__ == "__main__":
    init()
