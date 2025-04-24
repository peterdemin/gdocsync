import logging

import click

from .docs_importer import build_docs_importer


@click.command()
@click.argument("base_dir")
@click.option("-e", "--email", help="Email for Google Workspace delegated authentication.")
def cli(base_dir, email):
    """Imports Google Docs documents to ReST files."""
    logging.basicConfig(level=logging.INFO)
    docs_importer = build_docs_importer(email)
    docs_importer(base_dir)


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
