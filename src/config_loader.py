# src/config_loader.py

import os
import yaml
from jinja2 import Environment, FileSystemLoader
from typing import Any, Dict

from .logger import logging

class ConfigLoader:
    """
    Loads mappings, templates, and schema from configuration files.
    """

    def __init__(self, config_dir: str):
        """
        Initializes the ConfigLoader with the given configuration directory.
        Loads mappings, templates, and schema during initialization.
        
        :param config_dir: Path to the configuration directory.
        """
        self.config_dir = config_dir
        self.mappings = self._load_mappings()
        self.env = self._load_template()
        self.template = self.env.get_template('insert_template.sql')
        self.schema = self._load_schema()

    def _load_mappings(self) -> Dict[str, Any]:
        """
        Loads the mappings configuration file from the config directory.
        
        :return: A dictionary containing the mappings configuration.
        """
        mappings_path = os.path.join(self.config_dir, 'mappings.yaml')
        try:
            with open(mappings_path, 'r') as f:
                mappings = yaml.safe_load(f)
            logging.debug("Mappings configuration loaded successfully.")
            return mappings
        except FileNotFoundError:
            logging.error(f"Mappings file not found: {mappings_path}")
            raise
        except yaml.YAMLError as e:
            logging.error(f"Error parsing mappings file: {e}")
            raise

    def _load_template(self) -> Environment:
        """
        Loads the SQL insert template and sets up the Jinja2 environment with custom tests.
        
        :return: A Jinja2 Environment object configured with the template directory and custom tests.
        """
        template_dir = os.path.join(self.config_dir, 'templates')
        try:
            env = Environment(loader=FileSystemLoader(template_dir))

            # Define a custom 'is_string' test
            def is_string(value):
                return isinstance(value, str)

            # Define a custom 'is_raw' test
            def is_raw(value):
                return isinstance(value, dict) and 'raw' in value

            env.tests['is_string'] = is_string
            env.tests['is_raw'] = is_raw

            logging.debug("Insert template loaded successfully with custom 'is_string' and 'is_raw' tests.")
            return env
        except FileNotFoundError:
            logging.error(f"Template directory not found: {template_dir}")
            raise
        except Exception as e:
            logging.error(f"Error loading template environment: {e}")
            raise

    def _load_schema(self) -> Dict[str, Any]:
        """
        Loads the JSON schema for validating YAML definitions from the config directory.
        
        :return: A dictionary containing the schema.
        """
        schema_path = os.path.join(self.config_dir, 'schema.json')
        try:
            with open(schema_path, 'r') as f:
                schema = yaml.safe_load(f)
            logging.debug("Schema loaded successfully.")
            return schema
        except FileNotFoundError:
            logging.error(f"Schema file not found: {schema_path}")
            raise
        except yaml.YAMLError as e:
            logging.error(f"Error parsing schema file: {e}")
            raise

    @staticmethod
    def load_yaml(filepath: str) -> Dict[str, Any]:
        """
        Loads a YAML file from the given filepath.
        
        :param filepath: Path to the YAML file.
        :return: A dictionary containing the data from the YAML file.
        """
        try:
            with open(filepath, 'r') as f:
                data = yaml.safe_load(f)
            logging.debug(f"YAML file loaded: {filepath}")
            return data
        except FileNotFoundError:
            logging.error(f"YAML file not found: {filepath}")
            raise
        except yaml.YAMLError as e:
            logging.error(f"Error parsing YAML file {filepath}: {e}")
            raise
