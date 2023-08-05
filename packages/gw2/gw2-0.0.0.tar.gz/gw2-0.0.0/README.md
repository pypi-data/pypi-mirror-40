Guild Wars 2 API client for Python.

## Installation

```sh
pip install <name>
```

It is recommended to use a [virtual environment].

## Usage

```py
import gw2

client = gw2.Client()

client.get('achievements/daily')

client.get('account', token='API-KEY')
```

## License

[MIT][license]

[license]: /LICENSE
[virtual environment]: https://docs.python.org/3/library/venv.html
