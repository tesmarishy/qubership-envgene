import os
from pprint import pformat
from dataclasses import fields

import click

from envgenehelper import logger
from gitlab_ci import build_pipeline
from validations import validate_pipeline
from pipeline_parameters import PipelineParameters

@click.group()
def cli():
    pass

def prepare_input_params() -> PipelineParameters:
    params = PipelineParameters()
    params_log = "Input parameters are:"
    for param in fields(params):
        params_log += f"\n{param.name.upper()}: {pformat(getattr(params, param.name))}"
    logger.info(params_log)
    return params

@cli.command("validate_pipeline")
def validate_pipeline_command():
    params = prepare_input_params()
    validate_pipeline(params)
    read_gav_coordinates(params)


if __name__ == "__main__":
 cli()