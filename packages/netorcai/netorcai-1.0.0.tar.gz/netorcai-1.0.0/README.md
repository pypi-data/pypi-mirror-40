[![Build Status](https://img.shields.io/travis/netorcai/netorcai-client-python/master.svg?maxAge=600)](https://travis-ci.org/netorcai/netorcai-client-python)
[![Coverage Status](https://img.shields.io/codecov/c/github/netorcai/netorcai-client-python/master.svg?maxAge=600)](https://codecov.io/github/netorcai/netorcai-client-python)

netorcai-client-python
====================
Python version of the [netorcai] client library.

Installation
------------

The library can be installed via [pip].

``` bash
# Install latest release from the Python Package Index.
pip install netorcai

# Alternatively, clone this repo then install its latest commit.
git clone https://github.com/netorcai/netorcai-client-python.git
pip install ./netorcai-client-python
```

Usage
-----
Feel free to look at [hello world examples](./examples) to build your own clients.

Running tests
-------------

The tests use [pytest] and [pytest-cov].

``` bash
python -m pytest --cov=netorcai ./tests
```

[netorcai]: https://github.com/netorcai/
[pip]: https://pip.pypa.io/en/stable/
[pytest]: https://docs.pytest.org/en/latest/
[pytest-cov]: https://pypi.org/project/pytest-cov/
