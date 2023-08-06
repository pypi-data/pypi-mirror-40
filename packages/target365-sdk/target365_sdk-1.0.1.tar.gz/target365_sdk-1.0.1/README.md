## Target365 SDK for Python

### Getting started

To get started please send us an email at <support@target365.no> containing your EC public key in DER(ANS.1) format.

If you want, you can generate your EC public/private key-pair here: <https://crypto-utils.com/>

### PIP

```
pip install target365-sdk
```
[![pypi version](https://img.shields.io/pypi/v/target365_sdk.svg)](https://pypi.org/project/target365-sdk/)

### Authors and maintainers
Target365 (<support@target365.no>)

### Issues / Bugs / Questions

Please feel free to raise an issue against this repository if you have any questions or problems.

### Contributing

New contributors to this project are welcome. If you are interested in contributing please
send an email to support@target365.no.

##### Automated Tests

Automated tests requires `pytest` framework. There is a useful script `/test` which you may find helpful
when running tests. In order to use this script, you should make a copy of `test_secrets.example.sh`
and rename it to `test_secrets.sh`. You should then modify the values in `test_secrets.sh` appropriately. Do not
commit `test_secrets.sh` to the repository, it is intentionally included in `.gitignore`.

If you want to run only selected test, you can flag the respective test method with `@pytest.mark.testnow` and
instead run `/test testnow`

### License

This library is released under the MIT license.
