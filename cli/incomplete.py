from os import path
import sys
import json

import click


@click.command()
def incomplete_kw():
    """Test for incomplete keywords in output.json"""
    if path.exists("../../output.json"):
        with open("../../output.json") as fh:
            data = json.load(fh)

        for d in data:
            if d["keywords"] == "None":
                click.echo(f"No keywords for '{d['title']}'")
    else:
        click.echo("output.json does not exist in root directory")
        sys.exit(1)
