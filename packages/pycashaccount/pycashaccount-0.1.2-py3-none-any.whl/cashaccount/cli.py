import click

from . import electron_markdown as em
from . import opreturn_hexlike
from . import PaymentKeyHash
from . import Registration


@click.group()
def run():
    pass


@run.command()
@click.argument('name')
@click.argument('cash_or_legacy_address')
@click.option('--opreturn-hex', is_flag=True, default=False)
@click.option('--electron-markdown', is_flag=True, default=False)
def address(name, cash_or_legacy_address, electron_markdown, opreturn_hex):
    info = PaymentKeyHash(cash_or_legacy_address)
    registration = Registration(name, info)

    if electron_markdown:
        result = em(registration)
    elif opreturn_hex:
        result = opreturn_hexlike(registration)
    else:
        result = str(registration)
    click.echo(result)
