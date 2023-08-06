"""
docstring

Usage:
  docstring <file> <name> [-tmj] [-T=<tpl>]
  docstring -h | --help
  docstring --version

Options:
  -h --help                         Show help (this screen).
  --version                         Show version.
  -m --markdown                     Output extracted docstring as Markdown.
  -t --text                         Output extracted docstring as plain-text.
  -j --json                         Output extracted docstring as JSON.
  -T=<tpl> --template=<tpl>         Set template for Markdown output.

Examples:
  Extract the module docstring
    docstring module.py . --markdown
  Extract a module function docstring
    docstring module.py function --markdown
  Extract a class docstring
    docstring module.py Class --markdown
  Extract a method docstring
    docstring module.py Class.method --markdown

Help:
  Please see the issue tracker for the Github repository:
  https://github.com/ooreilly/docstring
"""
from docopt import docopt
from . import command

def main():
    """
    Program main
    """
    options = docopt(__doc__)
    cmd = command.Command(options)

    for opt in options:
        if options[opt]:
            cmd(opt)

