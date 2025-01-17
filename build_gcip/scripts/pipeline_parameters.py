from os import getenv
from dataclasses import dataclass, field


@dataclass
class PipelineParameters:
    env_names: str = getenv("ENV_NAMES", "")
    env_build: bool = getenv("ENV_BUILDER") == "true"
    get_passport: bool = getenv("GET_PASSPORT") == "true"
    cmdb_import: bool = getenv("CMDB_IMPORT") == "true"
    generate_effective_set: bool = getenv("GENERATE_EFFECTIVE_SET", "false") == "true"
    env_template_version: str = getenv("ENV_TEMPLATE_VERSION", "")
    env_template_test: bool = getenv("ENV_TEMPLATE_TEST") == "true"
    is_template_test: bool = getenv("ENV_TEMPLATE_TEST") == "true"
    is_offsite: bool = getenv("IS_OFFSITE") == "true"
    ci_commit_ref_name: str = getenv("CI_COMMIT_REF_NAME", "")
    json_schemas_dir: str = getenv("JSON_SCHEMAS_DIR", "/module/schemas")
    env_inventory_generation_params: dict[str, str | None] = field(
        default_factory=lambda: {
            "SD_SOURCE_TYPE": getenv("SD_SOURCE_TYPE"),
            "SD_VERSION": getenv("SD_VERSION"),
            "SD_DATA": getenv("SD_DATA"),
            "SD_DELTA": getenv("SD_DELTA"),
            "ENV_INVENTORY_INIT": getenv("ENV_INVENTORY_INIT"),
            "ENV_SPECIFIC_PARAMETERS": getenv("ENV_SPECIFIC_PARAMS"),
            "ENV_TEMPLATE_NAME": getenv("ENV_TEMPLATE_NAME"),
            "ENV_TEMPLATE_VERSION": getenv("ENV_TEMPLATE_VERSION"),
        }
    )
