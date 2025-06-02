import filecmp
import pytest
import difflib
import os
from ruamel.yaml import YAML
import json
from env_inventory_generation import handle_sd, Environment
from envgenehelper import *

yaml = YAML()

test_data = [
    ("test-solution-structure", "test-solution-structure-case-01", "test_001")
]

g_test_sd_dir = getAbsPath("../../test_data/test_sd")
g_sd_dir = getAbsPath("../../test_data/test_environments")
g_output_dir = getAbsPath("../../tmp/test_sd")

@pytest.fixture(autouse=True)
def change_test_dir(request, monkeypatch):
    monkeypatch.chdir(request.fspath.dirname+"/../..")

def load_yaml_file(file_path):
    with open(file_path, 'r') as f:
        return yaml.load(f)

def find_yaml_file(directory, base_name):
    """Find yaml file with either .yaml or .yml extension"""
    for ext in ['yaml', 'yml']:
        file_path = os.path.join(directory, f"{base_name}.{ext}")
        if os.path.exists(file_path):
            return file_path, f"{base_name}.{ext}"
    raise FileNotFoundError(f"YAML file {base_name} not found in {directory}")

@pytest.mark.parametrize("cluster_name, env_name, test_sd_name", test_data)
def test_sd(cluster_name, env_name, test_sd_name):
    # Load test data
    test_file, _ = find_yaml_file(g_test_sd_dir, test_sd_name)
    test_data = load_yaml_file(test_file)
    
    # Extract all required parameters
    sd_data = test_data.get("SD_DATA", "{}")  # Keep as string for json.loads in handle_sd
    sd_source_type = test_data.get("SD_SOURCE_TYPE", "")
    sd_version = test_data.get("SD_VERSION", "")
    sd_delta = test_data.get("SD_DELTA", "")
    
    # Create Environment object with test_sd_name in the path
    base_dir = g_output_dir  # base_dir = tmp/test_sd
    env = Environment(base_dir, test_sd_name, "")  # cluster = test_001, name = ""
    
    # Call the function with test data
    handle_sd(env, sd_source_type, sd_version, sd_data, sd_delta)
    
    # Compare files
    #ETALON SD FROM ENV
    expected_dir = os.path.join(g_sd_dir, cluster_name, env_name, "Inventory", "solution-descriptor")
    expected_file, sd_filename = find_yaml_file(expected_dir, "sd")
    files_to_compare = [sd_filename]
    
    # Get the actual output directory from env.env_path
    sd_output_dir = os.path.join(env.env_path, "Inventory", "solution-descriptor")
    
    # Check if directories and files exist
    logger.info(f"Expected directory: {expected_dir}")
    logger.info(f"Output directory: {sd_output_dir}")
    logger.info(f"Expected file: {expected_file}")
    logger.info(f"Output file: {os.path.join(sd_output_dir, sd_filename)}")
    
    # Ensure output directory exists
    os.makedirs(sd_output_dir, exist_ok=True)
    
    # List contents of both directories
    logger.info(f"Contents of expected directory: {os.listdir(expected_dir)}")
    logger.info(f"Contents of output directory: {os.listdir(sd_output_dir)}")
    
    match, mismatch, errors = filecmp.cmpfiles(expected_dir, sd_output_dir, files_to_compare, shallow=False)
    
    logger.info(f"Match: {dump_as_yaml_format(match)}")
    if len(mismatch) > 0:
        logger.error(f"Mismatch: {dump_as_yaml_format(mismatch)}")
        for file in mismatch:
            file1 = os.path.join(expected_dir, file)
            file2 = os.path.join(sd_output_dir, file)
            try:
                with open(file1, 'r') as f1, open(file2, 'r') as f2:
                    diff = difflib.unified_diff(
                        f1.readlines(),
                        f2.readlines(),
                        fromfile=file1,
                        tofile=file2,
                        lineterm=''
                    )
                    diff_text = '\n'.join(diff)
                    logger.error(f"Diff for {file}:\n{diff_text}")
            except Exception as e:
                logger.error(f"Could not read files for diff: {file1}, {file2}. Error: {e}")
    else:
        logger.info(f"Mismatch: {dump_as_yaml_format(mismatch)}")
    
    if len(errors) > 0:
        logger.fatal(f"Errors: {dump_as_yaml_format(errors)}")
        # Print file contents if they exist
        for file in errors:
            file1 = os.path.join(expected_dir, file)
            file2 = os.path.join(sd_output_dir, file)
            logger.info(f"Expected file exists: {os.path.exists(file1)}")
            logger.info(f"Output file exists: {os.path.exists(file2)}")
            if os.path.exists(file1):
                with open(file1, 'r') as f:
                    logger.info(f"Expected file contents:\n{f.read()}")
            if os.path.exists(file2):
                with open(file2, 'r') as f:
                    logger.info(f"Output file contents:\n{f.read()}")
    else:
        logger.info(f"Errors: {dump_as_yaml_format(errors)}")
    
    assert len(mismatch) == 0, f"Files from expected and actual result mismatch: {dump_as_yaml_format(mismatch)}"
    assert len(errors) == 0, f"Error during comparing expected and actual result: {dump_as_yaml_format(errors)}" 