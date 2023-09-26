from app.batch import app

from .methods import build_model


@app.task(rate_limit="1/m")
def invoke_build():
    build_model()
