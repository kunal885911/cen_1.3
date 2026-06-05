import json
import yaml
from pathlib import Path
from pydantic import ValidationError

from schemas.assembly_schema import AssemblyRequest

class ConfigLoader:
    """
    Loads and validates assembly configurations from JSON or YAML files.
    """
    def load_json(self, filepath: str) -> dict:
        """Load and parse a JSON config file. Raise with clear message on invalid JSON."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON configuration in {filepath}: {str(e)}")
        except Exception as e:
            raise ValueError(f"Failed to load JSON file {filepath}: {str(e)}")

    def load_yaml(self, filepath: str) -> dict:
        """Load and parse a YAML config file. Raise with clear message on invalid YAML."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML configuration in {filepath}: {str(e)}")
        except Exception as e:
            raise ValueError(f"Failed to load YAML file {filepath}: {str(e)}")

    def validate(self, config: dict) -> AssemblyRequest:
        """
        Validate the config dict against AssemblyRequest schema.
        This triggers PartConfig.validate_parameters() for each part,
        which in turn runs the existing per-model Pydantic validation.
        Returns a validated AssemblyRequest or raises ValidationError.
        
        The Pydantic validation guarantees that the configuration adheres to the 
        strict geometry and type constraints defined globally.
        """
        try:
            # This triggers all nested Pydantic validations, including those
            # in PartConfig which delegate to specific model schemas.
            return AssemblyRequest(**config)
        except ValidationError as e:
            raise ValueError(f"Configuration validation failed: {str(e)}")
