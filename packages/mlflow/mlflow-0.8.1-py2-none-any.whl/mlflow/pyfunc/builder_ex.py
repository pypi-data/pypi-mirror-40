import pandas

import mlflow.pyfunc

def predict(ctx, input_data):
    print(ctx.objects["items"])
    print(ctx.df)
    return ctx.models["sklearn_1"].predict(input_data)

def init(ctx):
    with open(ctx.files["saved_df"], "r") as f:
        ctx.df = pandas.read_json(f, orient="records")


def get_data():
    data_json = '{"fixed acidity":{"0":7.0},"volatile acidity":{"0":0.27},"citric acid":{"0":0.36},"residual sugar":{"0":20.7},"chlorides":{"0":0.045},"free sulfur dioxide":{"0":45.0},"total sulfur dioxide":{"0":170.0},"density":{"0":1.001},"pH":{"0":3.0},"sulphates":{"0":0.45},"alcohol":{"0":8.8}}'
    return pandas.read_json(data_json, orient="records") 


def save():
    items_dict = {
        "cat": 1,
        "a test": "string",
    }

    with open("/tmp/file1.json", "w") as f:
        f.write(get_data().to_json(orient="records"))

    with mlflow.pyfunc.build_model() as builder:
        builder.add_model("sklearn_1", 
                          model_path="/Users/czumar/AML/mlruns/0/69ee3341d2ae4b538ab31850721c3457/artifacts/model")
        builder.add_object("items", items_dict)
        builder.add_file("saved_df", "/tmp/file1.json")
        builder.set_predict(predict)
        builder.set_init(init)
        builder.save("/tmp/test1")


def load():
    loaded_pyfunc = mlflow.pyfunc.load_pyfunc("/tmp/test1")
    print(loaded_pyfunc.predict(get_data()))


def save2():
    with mlflow.pyfunc.build_model() as builder:
        builder.add_model("sklearn_1",
                          model_path="/Users/czumar/AML/mlruns/0/69ee3341d2ae4b538ab31850721c3457/artifacts/model",
                          load_pyfunc=False)

        def init(ctx):
            import mlflow.sklearn
            ctx.models["sklearn_1"] = mlflow.sklearn.load_model(ctx.models["sklearn_1"])

        def predict(ctx, input_data):
            return ctx.models["sklearn_1"].predict(input_data)

        builder.set_init(init)
        builder.set_predict(predict)
        builder.save("/tmp/test1")


if __name__ == "__main__":
    # save()
    save2()
    load()
