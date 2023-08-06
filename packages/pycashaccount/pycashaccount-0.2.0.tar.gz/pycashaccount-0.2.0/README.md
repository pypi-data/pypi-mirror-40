# Cash Account Helper

A helper library + cli to help you create a [cash account](https://gitlab.com/cash-accounts/specification).


## Installation

Requires python3 for now.

`pip install pycashaccount`


## Status / ToDo

It is very basic still.

- ~~OP_RETURN output for electron-cash op_return markdown~~
- ~~OP_RETURN hex-like output~~
- ~~p2sh output~~
- support payment codes
- generate raw hex output that common node CLIs can use


## CLI (command line interface) usage after installation

For example, get the information required for a key hash and script hash accounts:

```bash
cashaccount keyhash emergent_reasons bitcoincash:qrme8l598x49gmjhn92dgwhk5a3znu5wfcf5uf94e9 --opreturn-hex
cashaccount scripthash some_name bitcoincash:pp4d24pemra2k3mths8cjxpuu6yl3a5ctvcp8mdkm9 --opreturn-hex
```

Generally:

```bash
cashaccount payment_type name payment_info --formatting
```

Get help:

```bash
cashaccount --help

cashaccount address --help
```


## CLI usage directly from repository

Same usage as the installed cli, except you can call it from the `cli` script at the repository root:

```bash
./cli --help
```


## Library usage

Look at `cashaccount/cli.py` for usage.

For example, create a registration from a name and payment information.

```python
from cashaccount import PaymentKeyHash, Registration, opreturn_hexlike

name = 'emergent_reasons'
info = PaymentKeyHash('bitcoincash:qrme8l598x49gmjhn92dgwhk5a3znu5wfcf5uf94e9')
registration = Registration(name, info)
print(registration)
print(opreturn_hexlike(registration))
```


## Contributions

Contributions are welcome:

- Fork the repository and submit a pull request from your fork.
- Install test requirements `pip install -r requirements-test.txt`
- Update tests to cover any changes
- Confirm all tests pass before submitting a Pull Request (e.g. `pytest --cov -v`)
