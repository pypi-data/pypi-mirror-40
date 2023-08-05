#!/usr/bin/env python3

import click
from .vocab import Vocab


@click.group()
@click.option('--debug/--no-debug', default=False, envvar='DEBUG')
@click.pass_context
def cli(ctx, debug):
    """A handy helper to manage GRE Vocab preparation"""
    ctx.obj = Vocab(debug)

@click.command()
@click.argument('word', nargs=-1)
@click.pass_obj
def add(vocab, word):
    """Add a word/words to vocabulary"""
    vocab.add(word)

@click.command()
@click.argument('word', nargs=-1)
@click.pass_obj
def remove(vocab, word):
    """Remove a word/words from vocabulary"""
    vocab.remove(word)

@click.command()
@click.argument('word')
@click.pass_obj
def get(vocab, word):
    """Retrieve a word, definiton from vocabulary"""
    vocab.get(word)

@click.command()
@click.pass_obj
def show(vocab):
    """Print entire vocabulary"""
    vocab.show()

@click.command()
@click.pass_obj
def flash(vocab):
    """Flash cards"""
    vocab.flash()

@click.command()
@click.argument('path')
@click.pass_obj
def export(vocab, path):
    """Export vocabulary to file"""
    vocab.export(path)

@click.command()
@click.pass_obj
def nuke(vocab):
    """Delete entire vocabulary"""
    vocab.nuke()


cli.add_command(add)
cli.add_command(get)
cli.add_command(flash)
cli.add_command(remove)
cli.add_command(show)
cli.add_command(export)
cli.add_command(nuke)

cli()
