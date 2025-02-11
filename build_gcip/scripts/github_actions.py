import os
from os import *
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

def read_gav_coordinates(params: PipelineParameters):
    if params.is_template_test:
        logger.info("We are generating jobs in template test mode.")
        templates_dir = f"{project_dir}/templates/env_templates"
        # getting build artifact
        build_artifact = get_gav_coordinates_from_build()
        group_id = build_artifact["group_id"]
        artifact_id = build_artifact["artifact_id"]
        params.env_template_version = build_artifact["version"]
        version = build_artifact["version"]
        # get env_names for all templates types
        templateFiles = [
            os.path.splitext(f)[0]
            for f in listdir(templates_dir)
            if os.path.isfile(os.path.join(templates_dir, f))
            and (f.endswith(".yaml") or f.endswith(".yml"))
        ]
        params.env_names = "\n".join(templateFiles)
    else:
        group_id = ""
        artifact_id = ""
        version = ""

    gav_data = f"{group_id},{artifact_id},{version}"
    with open("/repo/gav_output.txt", "w") as f:
        f.write(gav_data)

    logger.info(f"GAV data saved: {gav_data}")


@cli.command("validate_pipeline")
def validate_pipeline_command():
    params = prepare_input_params()
    validate_pipeline(params)
    read_gav_coordinates(params)


if __name__ == "__main__":
 cli()