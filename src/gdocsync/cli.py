import click

from .sync import sync_johnny_decimal_drive_files


@click.command()
@click.argument('base_dir')
def cli(base_dir):
    """Simple program that greets NAME for a total of COUNT times."""
    sync_johnny_decimal_drive_files(base_dir)


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
