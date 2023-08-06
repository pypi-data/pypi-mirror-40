# -*- coding: utf-8 -*-


"""vsc.vsc: provides entry point main()."""


__version__ = "0.1.0"


import sys
from .stuff import Stuff
import click


@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('Hello %s!' % name)


def main():
    hello()
