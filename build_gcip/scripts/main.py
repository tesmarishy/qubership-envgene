from os import getenv
from pprint import pformat
from dataclasses import fields

import click

from envgenehelper import logger
from gitlab_ci import build_pipeline
from validations import validate_pipeline
from pipeline_parameters import PipelineParameters

@click.group(chain=True)
def gcip():
    pass

def prepare_input_params() -> PipelineParameters:
    params = PipelineParameters()
    params_log = (f"Input parameters are: ")
    for param in fields(params):
        params_log += f"\n{param.name.upper()}: {pformat(getattr(params, param.name))}"
    logger.info(params_log)
    return params

@gcip.command("generate_pipeline")
def generate_pipeline():
    perform_generation()

def perform_generation():
    params = prepare_input_params()
    validate_pipeline(params)
    build_pipeline(params)  

if __name__ == "__main__":
    gcip()
