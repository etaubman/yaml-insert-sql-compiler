# src/compiler.py

"""
Compiler module that processes YAML definitions and generates SQL files.
"""

import os
import glob
import datetime
from typing import List

from .config_loader import ConfigLoader
from .validator import Validator
from .sql_generator import SQLGenerator
from .logger import setup_logging, logging


class Compiler:
    """
    Orchestrates the compilation of YAML definitions into SQL files.
    """

    def __init__(self, definitions_dir: str, config_dir: str, includes_dir: str,
                 output_dir: str, log_dir: str, verbose: bool):
        """
        Initializes the Compiler with directory paths and verbosity setting.
        Sets up logging and ensures required directories exist.
        Loads configurations, validator, and SQL generator.
        """
        self.definitions_dir = definitions_dir
        self.config_dir = config_dir
        self.includes_dir = includes_dir
        self.output_dir = output_dir
        self.log_dir = log_dir
        self.verbose = verbose

        # Create a timestamp for log and output file names
        self.timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_filename = os.path.join(self.log_dir, f'compilation_{self.timestamp}.log')
        
        # Set up logging
        setup_logging(self.log_filename, self.verbose)

        # Ensure all required directories exist
        self._ensure_directories()

        # Load configurations
        self.config_loader = ConfigLoader(self.config_dir)
        
        # Initialize the validator with the loaded schema
        self.validator = Validator(self.config_loader.schema)
        
        # Initialize the SQL generator with the loaded template and mappings
        self.sql_generator = SQLGenerator(
            template=self.config_loader.template,
            mappings=self.config_loader.mappings,
            includes_dir=self.includes_dir
        )

    def _ensure_directories(self):
        """
        Ensures that required directories exist.
        Creates them if they do not exist.
        """
        required_dirs = [self.definitions_dir, self.config_dir,
                         self.includes_dir, self.output_dir, self.log_dir]
        for directory in required_dirs:
            if not os.path.exists(directory):
                os.makedirs(directory)
                logging.debug(f"Created directory: {directory}")

    def run(self):
        """
        Executes the compilation process.
        Processes each YAML definition file, validates it, generates SQL statements,
        and writes them to the output file.
        """
        logging.info("Starting compilation process.")
        sql_statements = []

        # Find all YAML definition files in the definitions directory
        definition_files = glob.glob(os.path.join(self.definitions_dir, '*.yaml'))
        if not definition_files:
            logging.warning(f"No YAML files found in {self.definitions_dir}.")
            return

        # Process each YAML file
        for filepath in definition_files:
            try:
                # Load the YAML definition
                definition = self.config_loader.load_yaml(filepath)
                logging.info(f"Processing file: {filepath}")

                # Validate the YAML definition
                self.validator.validate(definition)
                logging.debug(f"Validation successful for file: {filepath}")

                # Generate SQL statement from the definition
                sql = self.sql_generator.generate_sql(definition)
                sql_statements.append(sql)
                logging.debug(f"SQL statement generated for file: {filepath}")

            except Exception as e:
                # Log any errors that occur during processing
                logging.error(f"Error processing file {filepath}: {e}", exc_info=True)

        # Write the generated SQL statements to the output file
        if sql_statements:
            self._write_output(sql_statements)
            logging.info("Compilation process completed successfully.")
        else:
            logging.warning("No SQL statements were generated.")

    def _write_output(self, sql_statements: List[str]):
        """
        Writes the SQL statements to the output file.
        """
        output_filename = os.path.join(self.output_dir, f'compiled_{self.timestamp}.sql')
        try:
            # Open the output file and write each SQL statement
            with open(output_filename, 'w') as f:
                for statement in sql_statements:
                    f.write(statement + '\n\n')
            logging.info(f"Compiled SQL written to {output_filename}")
            print(f"Compilation successful. Output written to {output_filename}")
        except IOError as e:
            # Log any errors that occur during file writing
            logging.error(f"Failed to write output file {output_filename}: {e}", exc_info=True)
            raise
