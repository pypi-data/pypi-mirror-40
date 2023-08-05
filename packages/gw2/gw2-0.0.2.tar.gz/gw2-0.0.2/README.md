Guild Wars 2 API client for Python.

## Installation

```sh
pip install gw2
```

It is recommended to use a [virtual environment].

## Usage

```py
import gw2

client = gw2.Client()

client.get('achievements/daily')

client.get('achievements', ids=[1, 2])  # pass query parameters as keyword arguments

client.auth('YOUR-API-KEY')  # set api key for authenticated endpoints

client.get('account')
```

To handle error responses:

```py
try:
    client.get('...')
except gw2.HTTPError as e:
    print(e.response.status_code, e.response.json())
```

## License

[MIT][license]

[license]: /LICENSE
[virtual environment]: https://docs.python.org/3/library/venv.html
