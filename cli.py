import click

from .trend import trend


@click.group()
def cli():
    """Command line interface for Neem CLI"""

cli.add_command(trend)

if __name__ == '__main__':
    cli()