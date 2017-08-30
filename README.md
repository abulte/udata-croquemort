# uData-croquemort

This plugin provide integration between uData and Croquemort link checker.

## Compatibility

**udata-croquemort** requires Python 2.7+ and [uData][].

## Installation

Install [uData][].

Remain in the same virtual environment (for Python) and use the same version of npm (for JS).

Install **udata-croquemort**:

```shell
pip install udata-croquemort
```

Modify your local configuration file of **udata** (typically, `udata.cfg`) as following:

```python
PLUGINS = ['croquemort']
CROQUEMORT = {
    'url': 'http://localhost:8000',
    'delay': 1,
    'retry': 10,
}
CROQUEMORT_IGNORE = []
```

[uData]: https://github.com/opendatateam/udata
