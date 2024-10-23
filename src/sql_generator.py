# src/sql_generator.py

"""
SQLGenerator module to generate SQL statements from definitions.
"""

import os
from typing import Dict, Any, List

from jinja2 import Template

from .logger import logging


class SQLGenerator:
    """
    Generates SQL statements from YAML definitions.
    """

    def __init__(self, template: Template, mappings: Dict[str, Any], includes_dir: str):
        """
        Initializes the SQLGenerator with a Jinja2 template, mappings, and includes directory.
        
        :param template: Jinja2 template for SQL generation.
        :param mappings: Dictionary of mappings to be used in the template.
        :param includes_dir: Directory where include files are stored.
        """
        self.template = template
        self.mappings = mappings
        self.includes_dir = includes_dir

    def generate_sql(self, definition: Dict[str, Any]) -> str:
        """
        Generates a SQL statement from a definition.
        
        :param definition: Dictionary containing the SQL definition.
        :return: Generated SQL statement as a string.
        """
        try:
            # Process includes in values
            resolved_values = self._resolve_includes(definition.get('values', []))

            # Prepare context for template rendering
            context = {
                'definition': {
                    'table': definition['table'],
                    'fields': definition['fields'],
                    'values': resolved_values
                },
                'mappings': self.mappings,
                'metadata': definition.get('metadata', {})
            }

            # Log the context for debugging purposes
            logging.debug(f"Context for template rendering: {context}")

            # Render the template with the context
            sql = self.template.render(context)
            return sql.strip()
        except Exception as e:
            # Log any errors that occur during SQL generation
            logging.error(f"Error generating SQL: {e}", exc_info=True)
            raise

    def _resolve_includes(self, values: List[Any]) -> List[Any]:
        """
        Resolves include directives in values.
        
        :param values: List of values that may contain include directives.
        :return: List of values with includes resolved.
        """
        resolved_values = []
        for value in values:
            if isinstance(value, dict) and 'include' in value:
                # If the value is a dictionary with an 'include' key, load the include file
                include_filename = value['include']
                include_content = self._load_include(include_filename)
                resolved_values.append(include_content)
            else:
                # Escape single quotes in strings to prevent SQL injection
                if isinstance(value, str):
                    value = value.replace("'", "''")
                resolved_values.append(value)
        return resolved_values

    def _load_include(self, filename: str) -> str:
        """
        Loads the content of an include file.
        
        :param filename: Name of the include file to load.
        :return: Content of the include file as a string.
        """
        include_path = os.path.join(self.includes_dir, filename)
        if not os.path.exists(include_path):
            # Log an error if the include file does not exist
            logging.error(f"Include file not found: {include_path}")
            raise FileNotFoundError(f"Include file not found: {include_path}")
        try:
            # Read the content of the include file
            with open(include_path, 'r') as f:
                content = f.read()
            logging.debug(f"Included content from: {include_path}")
            # Escape single quotes in the content
            return content.replace("'", "''")
        except Exception as e:
            # Log any errors that occur while reading the include file
            logging.error(f"Error reading include file {include_path}: {e}", exc_info=True)
            raise
