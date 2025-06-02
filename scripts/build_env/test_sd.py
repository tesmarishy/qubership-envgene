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
    
    # Ensure output directory exists
    os.makedirs(g_output_dir, exist_ok=True)
    
    # Create Environment object with the correct base path
    base_dir = os.path.dirname(os.path.dirname(g_output_dir))  # Go up two levels from tmp/test_sd
    env = Environment(base_dir, "tmp", "test_sd")
    
    # Call the function with test data
    handle_sd(env, sd_source_type, sd_version, sd_data, sd_delta)
    
    # Compare files
    expected_dir = os.path.join(g_sd_dir, cluster_name, env_name, "Inventory", "solution-descriptor")
    expected_file, sd_filename = find_yaml_file(expected_dir, "sd")
    files_to_compare = [sd_filename]
    
    sd_output_dir = os.path.join(g_output_dir, "Inventory", "solution-descriptor")
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
    else:
        logger.info(f"Errors: {dump_as_yaml_format(errors)}")
    
    assert len(mismatch) == 0, f"Files from expected and actual result mismatch: {dump_as_yaml_format(mismatch)}"
    assert len(errors) == 0, f"Error during comparing expected and actual result: {dump_as_yaml_format(errors)}" 