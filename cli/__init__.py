import click

from .trend import trend
from .crawl import crawl
from .incomplete import incomplete_kw


@click.group()
def cli():
    """Command line interface for Neem CLI"""


cli.add_command(trend)
cli.add_command(crawl)
cli.add_command(incomplete_kw)

if __name__ == "__main__":
    cli()
