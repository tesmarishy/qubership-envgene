import filecmp
import pytest
import difflib
import os
import yaml
import json
from main import handle_sd
from envgenehelper import *

test_data = [
    ("test_001", "2.1", "deploy")  # test_name, sd_version, sd_source_type
]

g_test_data_dir = getAbsPath("../../test_data/test_sd")
g_expected_dir = getAbsPath("../../test_data/test_environments/test-solution-structure/test-solution-structure-case-01/Inventory/solution-descriptor")
g_output_dir = getAbsPath("../../tmp/test_sd")

@pytest.fixture(autouse=True)
def change_test_dir(request, monkeypatch):
    monkeypatch.chdir(request.fspath.dirname+"/../..")

def load_yaml_file(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

@pytest.mark.parametrize("test_name, sd_version, sd_source_type", test_data)
def test_sd(test_name, sd_version, sd_source_type):
    # Load test data
    test_file = os.path.join(g_test_data_dir, f"{test_name}.yaml")
    test_data = load_yaml_file(test_file)
    sd_data = json.loads(test_data["SD_DATA"])
    
    # Ensure output directory exists
    os.makedirs(g_output_dir, exist_ok=True)
    
    # Generate output file path
    output_file = os.path.join(g_output_dir, "sd.yaml")
    
    # Call the function with test data
    env = "test-env"
    sd_delta = None
    result = handle_sd(env, sd_source_type, sd_version, sd_data, sd_delta)
    
    # Write result to file
    with open(output_file, 'w') as f:
        yaml.dump(result, f, default_flow_style=False)
    
    # Compare files
    expected_file = os.path.join(g_expected_dir, "sd.yaml")
    files_to_compare = ["sd.yaml"]
    
    match, mismatch, errors = filecmp.cmpfiles(g_expected_dir, g_output_dir, files_to_compare, shallow=False)
    
    logger.info(f"Match: {dump_as_yaml_format(match)}")
    if len(mismatch) > 0:
        logger.error(f"Mismatch: {dump_as_yaml_format(mismatch)}")
        for file in mismatch:
            file1 = os.path.join(g_expected_dir, file)
            file2 = os.path.join(g_output_dir, file)
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