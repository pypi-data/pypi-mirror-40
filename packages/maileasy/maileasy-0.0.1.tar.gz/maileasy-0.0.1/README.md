Simple mail sending
## Installation
### Using pip (Recommended)
`pip install maileasy`
### From source
1. Clone this repository
1. `python setup.py install`

## First use
To ensure the module works, create a .json configuration file like the template `maileasy_config.json`, then run this python code:
```python
import maileasy
maileasy.send("maileasy test", "success", config=<CONFIG FILE>))
```


This module is still in *very* early stages.
Please open an issue if you have encounter any bugs.
