import click

from . import electron_markdown as em
from . import opreturn_hexlike
from . import PaymentKeyHash, PaymentScriptHash
from . import Registration


@click.group()
def run():
    pass


@run.command()
@click.argument('name')
@click.argument('cash_or_legacy_address')
@click.option('--opreturn-hex', is_flag=True, default=False)
@click.option('--electron-markdown', is_flag=True, default=False)
def keyhash(name, cash_or_legacy_address, electron_markdown, opreturn_hex):
    try:
        info = PaymentKeyHash(cash_or_legacy_address)
    except ValueError as e:
        raise click.exceptions.BadParameter(e)
    _handle_address(name, info, electron_markdown, opreturn_hex)


@run.command()
@click.argument('name')
@click.argument('cash_or_legacy_address', type=click.types.STRING)
@click.option('--opreturn-hex', is_flag=True, default=False)
@click.option('--electron-markdown', is_flag=True, default=False)
def scripthash(name, cash_or_legacy_address, electron_markdown, opreturn_hex):
    try:
        info = PaymentScriptHash(cash_or_legacy_address)
    except ValueError as e:
        raise click.exceptions.BadParameter(e)
    _handle_address(name, info, electron_markdown, opreturn_hex)


def _handle_address(name, info, electron_markdown, opreturn_hex):
    registration = Registration(name, info)
    if electron_markdown:
        result = em(registration)
    elif opreturn_hex:
        result = opreturn_hexlike(registration)
    else:
        result = str(registration)
    click.echo(result)
