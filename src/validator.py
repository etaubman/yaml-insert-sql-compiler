"""
Validator module to validate YAML definitions against a schema.
"""

from jsonschema import validate, ValidationError
from typing import Dict, Any

from .logger import logging


class Validator:
    """
    Validates YAML definitions using a JSON schema.
    """

    def __init__(self, schema: Dict[str, Any]):
        self.schema = schema

    def validate(self, data: Dict[str, Any]):
        """
        Validates data against the schema.
        """
        try:
            validate(instance=data, schema=self.schema)
        except ValidationError as e:
            logging.error(f"Validation error: {e.message}")
            raise
