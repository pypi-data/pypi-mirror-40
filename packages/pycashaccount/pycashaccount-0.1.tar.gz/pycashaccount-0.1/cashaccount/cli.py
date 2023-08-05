import click

from . import electron_markdown as em
from . import PaymentKeyHash
from . import Registration


@click.group()
def run():
    pass


@run.command()
@click.argument('name')
@click.argument('cash_or_legacy_address')
@click.option('--electron-markdown', is_flag=True, default=False)
def address(name, cash_or_legacy_address, electron_markdown):
    info = PaymentKeyHash(cash_or_legacy_address)
    registration = Registration(name, info)

    if electron_markdown:
        result = em(registration)
    else:
        result = str(registration)
    click.echo(result)
