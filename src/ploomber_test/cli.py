from pathlib import Path
import click

from ploomber_test.runner import CodeRunner


@click.group()
def cli():
    pass


@cli.command()
@click.argument("file_path", type=click.Path(exists=True), help="The markdown file with the python code to run")
@click.argument("python_version", default="3.12.2", help="The python version to use, default is 3.12.2")
def run(file_path, python_version):
    """
       Run python code blocks from a markdown file.

       The markdown block should use the python language identifier, example:
       ```python
            print("This is python")
        ```

       Example usage:
       \b
       python cli.py ../../examples/print-python-version.md 3.12.2
    """
    CodeRunner(Path(file_path).read_text(), python_version).run()
