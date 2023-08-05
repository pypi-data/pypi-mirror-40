import click

from nbless import nbexec, nbsave


@click.command()
@click.argument("in_file")
@click.option("-k", "--kernel", "kernel")
@click.option("-o", "--out_file", "out_file")
def nbexec_click(in_file: str, kernel: str, out_file: str) -> None:
    nb_name, nb = nbexec(in_file, kernel) if kernel else nbexec(in_file)
    nbsave(out_file, nb) if out_file else nbsave(nb_name, nb)
