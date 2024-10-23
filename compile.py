#!/usr/bin/env python3
"""
Main script to compile YAML definitions into SQL files.
"""

import click
from src.compiler import Compiler


@click.command()
@click.option('--definitions-dir', default='definitions',
              help='Directory containing YAML definition files.')
@click.option('--config-dir', default='config',
              help='Directory containing configuration files.')
@click.option('--includes-dir', default='includes',
              help='Directory containing files to be included in SQL.')
@click.option('--output-dir', default='output',
              help='Directory to save compiled SQL files.')
@click.option('--log-dir', default='compilation_log',
              help='Directory to save compilation logs.')
@click.option('--verbose', is_flag=True, default=False,
              help='Enable verbose logging.')
def main(definitions_dir, config_dir, includes_dir, output_dir, log_dir, verbose):
    """
    Compiles YAML definitions into a single SQL file.
    """
    compiler = Compiler(
        definitions_dir=definitions_dir,
        config_dir=config_dir,
        includes_dir=includes_dir,
        output_dir=output_dir,
        log_dir=log_dir,
        verbose=verbose
    )
    compiler.run()


if __name__ == '__main__':
    main()

"""
Example usage:
python compile.py
python compile.py --definitions-dir definitions --config-dir config --includes-dir includes --output-dir output --log-dir compilation_log --verbose
"""
