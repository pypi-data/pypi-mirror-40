import os
import click
from urllib.parse import urlencode, quote
from AppKit import NSWorkspace, NSURL, NSWorkspaceLaunchWithoutActivation
import yaml
from pathlib import Path

CREATE_URL = {'bear': 'bear://x-callback-url/create?',
              'ulysses': 'ulysses://x-callback-url/new-sheet?'}
RC_PATH = str(Path.home()) + '/.noterc'
# QUERY = {'text': ''}

class Notes:

    def __init__(self, text):
        self.CONTENTS = {}
        self.CONTENTS['text'] = text

    def upload(self, app):
        if app == 'local':
            pass
        else:
            url = CREATE_URL[app] + urlencode(self.CONTENTS, quote_via=quote)
            ws = NSWorkspace.sharedWorkspace()
            ws.openURL_options_configuration_error_(NSURL.URLWithString_(url), NSWorkspaceLaunchWithoutActivation, None, None)


class Config:

    def __init__(self):
        open(RC_PATH, 'a').close()

    def read(self, key):
        with open(RC_PATH, 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        try:
            return cfg[key]
        except TypeError:
            print("Please run notes mode to set where to save note.")
            exit()

    def write(self, app):
        with open(RC_PATH, 'w') as ymlfile:
            yaml.dump({'app': app}, ymlfile, default_flow_style=False)


@click.group()
def cli():
    """A command line note!!!"""

@cli.command('create', short_help='create a note')
@click.option('-e', '--editor', is_flag=True)
@click.option('--vim', is_flag=True)
@click.argument('text', default='')
def create(editor, text, vim):
    """Simple command line tool to write note"""
    if editor or vim:
        text = click.edit(text, editor='vim' if vim else None)
    app = Config().read('app')
    note = Notes(text)
    note.upload(app)


@cli.command('mode', short_help='select the mode')
@click.option('--app', type=click.Choice(['local', 'bear', 'ulysses']), prompt='Please choose where to save your note')
def mode(app):
    cfg = Config().write(app)




if __name__ == '__main__':
    cli()
