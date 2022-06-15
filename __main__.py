import sys
import os

from .cli import cli

os.chdir("src/neem")
sys.exit(cli())
