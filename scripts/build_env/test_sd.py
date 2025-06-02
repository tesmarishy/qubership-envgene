# Standard library imports
import filecmp
import difflib
import os

# Third party imports
import pytest
from ruamel.yaml import YAML
import json

# Local imports
from env_inventory_generation import handle_sd, Environment
from envgenehelper import *

# Initialize YAML parser
yaml = YAML()

# Test data configuration
TEST_CASES = [
    # (cluster_name, environment_name, test_case_name)
    ("test-solution-structure", "test-solution-structure-case-01", "test_001")
]

# Directory paths configuration
TEST_SD_DIR = getAbsPath("../../test_data/test_sd")               # Directory with test SD files
ETALON_ENV_DIR = getAbsPath("../../test_data/test_environments")  # Directory with etalon environments
OUTPUT_DIR = getAbsPath("../../tmp/test_sd")                      # Directory for test output

def find_yaml_file(directory, base_name):
    """
    Find a YAML file with either .yaml or .yml extension.
    
    Args:
        directory (str): Directory to search in
        base_name (str): Base name of the file without extension
        
    Returns:
        tuple: (full_path, filename) of the found file
        
    Raises:
        FileNotFoundError: If no matching file is found
    """
    logger.debug(f"Searching for YAML file:"
                f"\n\tDirectory: {directory}"
                f"\n\tBase name: {base_name}")
    
    for ext in ['yaml', 'yml']:
        file_path = os.path.join(directory, f"{base_name}.{ext}")
        if os.path.exists(file_path):
            logger.debug(f"Found YAML file: {file_path}")
            return file_path, f"{base_name}.{ext}"
    
    error_msg = f"YAML file '{base_name}' not found in directory: {directory}"
    logger.error(error_msg)
    raise FileNotFoundError(error_msg)

def load_yaml_file(file_path):
    """
    Load and parse YAML file.
    
    Args:
        file_path (str): Path to the YAML file
        
    Returns:
        dict: Parsed YAML content
    """
    logger.debug(f"Loading YAML file: {file_path}")
    with open(file_path, 'r') as f:
        return yaml.load(f)

def load_test_sd_data(test_case_name):
    """
    Load and parse test SD data from YAML file.
    
    Args:
        test_case_name (str): Name of the test case file (without extension)
        
    Returns:
        tuple: SD data parameters (sd_data, sd_source_type, sd_version, sd_delta)
    """
    logger.info(f"Loading test data for case: {test_case_name}")
    test_file, _ = find_yaml_file(TEST_SD_DIR, test_case_name)
    test_data = load_yaml_file(test_file)
    
    # Extract SD parameters with defaults
    sd_data = test_data.get("SD_DATA", "{}")
    sd_source_type = test_data.get("SD_SOURCE_TYPE", "")
    sd_version = test_data.get("SD_VERSION", "")
    sd_delta = test_data.get("SD_DELTA", "")
    
    logger.info(f"Loaded SD parameters:"
               f"\n\tSource type: {sd_source_type}"
               f"\n\tVersion: {sd_version}"
               f"\n\tDelta mode: {sd_delta}")
    
    return sd_data, sd_source_type, sd_version, sd_delta

def compare_sd_files(expected_dir, actual_dir, sd_filename):
    """
    Compare SD files between expected and actual directories.
    
    Args:
        expected_dir (str): Path to directory with expected SD file
        actual_dir (str): Path to directory with actual SD file
        sd_filename (str): Name of the SD file to compare
        
    Returns:
        bool: True if files match, False otherwise
    """
    logger.info(f"Comparing SD files:"
               f"\n\tExpected dir: {expected_dir}"
               f"\n\tActual dir: {actual_dir}"
               f"\n\tFilename: {sd_filename}")
    
    files_to_compare = [sd_filename]
    match, mismatch, errors = filecmp.cmpfiles(expected_dir, actual_dir, files_to_compare, shallow=False)
    
    # Log comparison results
    logger.info(f"Comparison results:"
               f"\n\tMatching files: {dump_as_yaml_format(match)}"
               f"\n\tMismatched files: {dump_as_yaml_format(mismatch)}"
               f"\n\tErrors: {dump_as_yaml_format(errors)}")
    
    # Show detailed diff for mismatches
    if len(mismatch) > 0:
        for file in mismatch:
            file1 = os.path.join(expected_dir, file)
            file2 = os.path.join(actual_dir, file)
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
                    logger.error(f"Differences found in {file}:\n{diff_text}")
            except Exception as e:
                logger.error(f"Error reading files for diff: {file1}, {file2}. Error: {e}")
    
    # Show file contents on errors
    if len(errors) > 0:
        for file in errors:
            file1 = os.path.join(expected_dir, file)
            file2 = os.path.join(actual_dir, file)
            logger.info(f"File existence check:"
                       f"\n\tExpected file exists: {os.path.exists(file1)}"
                       f"\n\tActual file exists: {os.path.exists(file2)}")
            
            if os.path.exists(file1):
                with open(file1, 'r') as f:
                    logger.info(f"Expected file contents:\n{f.read()}")
            if os.path.exists(file2):
                with open(file2, 'r') as f:
                    logger.info(f"Actual file contents:\n{f.read()}")
    
    return len(mismatch) == 0 and len(errors) == 0

@pytest.mark.parametrize("cluster_name, env_name, test_case_name", TEST_CASES)
def test_sd(cluster_name, env_name, test_case_name):
    """
    Test SD file generation and comparison.
    
    Args:
        cluster_name (str): Name of the cluster
        env_name (str): Name of the environment
        test_case_name (str): Name of the test case
    """
    logger.info(f"Starting SD test:"
               f"\n\tCluster: {cluster_name}"
               f"\n\tEnvironment: {env_name}"
               f"\n\tTest case: {test_case_name}")
    
    # Load test data
    sd_data, sd_source_type, sd_version, sd_delta = load_test_sd_data(test_case_name)
    
    # Create Environment object for output
    env = Environment(OUTPUT_DIR, test_case_name, "")
    
    # Generate SD file
    logger.info("Generating SD file...")
    handle_sd(env, sd_source_type, sd_version, sd_data, sd_delta)
    
    # Compare generated SD with etalon
    expected_dir = os.path.join(ETALON_ENV_DIR, cluster_name, env_name, "Inventory", "solution-descriptor")
    expected_file, sd_filename = find_yaml_file(expected_dir, "sd")
    actual_dir = os.path.join(env.env_path, "Inventory", "solution-descriptor")
    
    # Verify files match
    assert compare_sd_files(expected_dir, actual_dir, sd_filename), \
        "Generated SD file does not match the expected one" 