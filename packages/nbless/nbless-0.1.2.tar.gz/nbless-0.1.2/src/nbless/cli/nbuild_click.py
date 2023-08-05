from typing import List

import click

from src.nbless import nbuild, nbsave


@click.command()
@click.argument('in_files', nargs=-1)
@click.option('-o', '--out_file', 'out_file')
def nbuild_click(in_files: List[str], out_file: str) -> None:
    nb = nbuild.nbuild(in_files)
    nbsave.nbsave(out_file, nb) if out_file else print(nb)
