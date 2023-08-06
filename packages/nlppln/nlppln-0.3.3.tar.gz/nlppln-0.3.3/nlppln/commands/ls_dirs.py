#!/usr/bin/env python
import click
import json
import os

from ..utils import cwl_dir


@click.command()
@click.argument('dir_in', type=click.Path(exists=True))
def command(dir_in):
    dirs_out = [os.path.join(dir_in, f) for f in os.listdir(dir_in)]
    dirs_out = list(filter(lambda d: os.path.isdir(d), dirs_out))
    dirs_out = sorted(dirs_out)

    dirs_out = [cwl_dir(d) for d in dirs_out]

    stdout_text = click.get_text_stream('stdout')
    stdout_text.write(json.dumps({'dirs_out': dirs_out}))


if __name__ == '__main__':
    command()
