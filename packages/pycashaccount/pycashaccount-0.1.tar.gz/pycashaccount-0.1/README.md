# Cash Account Helper

A helper library + cli to help you create a [cash account](https://gitlab.com/cash-accounts/specification).


## Installation

Requires python3 for now.

`pip install pycashaccount`


## Status / ToDo

It is very basic for now.

- ~~OP_RETURN output for electron-cash op_return markdown~~
- OP_RETURN hex-like output
- additional payment types
- generate raw hex output that common node CLIs can use


## CLI (command line interface) usage after installation

For example, get the information required for a key hash account (it uses a simple address):

```bash
cashaccount address emergent_reasons bitcoincash:qrme8l598x49gmjhn92dgwhk5a3znu5wfcf5uf94e9
```

Generally:

```bash
cashaccount payment_type name payment_info
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
from cashaccount import PaymentKeyHash, Registration, electron_markdown

name = 'emergent_reasons'
info = PaymentKeyHash('bitcoincash:qrme8l598x49gmjhn92dgwhk5a3znu5wfcf5uf94e9')
registration = Registration(name, info)
print(registration)
print(electron_markdown(registration))
```


## Contributions

Contributions are welcome:

- Fork the repository and submit a pull request from your fork.
- Install test requirements `pip install -r requirements-test.txt`
- Update tests to cover any changes
- Confirm all tests pass before submitting a Pull Request (e.g. `pytest --cov -v`)
