from pathlib import Path
import click

from ploomber_test.runner import CodeRunner


@click.group()
def cli():
    pass


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
def run(file_path):
    CodeRunner(Path(file_path).read_text()).run()
