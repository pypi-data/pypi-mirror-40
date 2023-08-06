# Grow Recipe Python Wrapper

A python module to provide functionality to the [Grow Recipe Schema](https://github.com/njason/grow-recipe-schema)


## Installation

[pip](https://pip.pypa.io/en/stable/):

`$ pip install grow-recipe`


## Usage

```
from datetime import datetime

import grow_recipe

# keep track of the start of the grow
start_time = datetime(2018, 12, 17)

with open('some_file.xml') as xml_file:
    temperature_range = grow_recipe.get_metric(
        xml_file, 'air', 'temperature', start_time, datetime.now())

print('Temperature minimum ' + temperature_range.min)
print('Temperature maximum ' + temperature_range.max)
```


## Development

Setup with pip:
`$ pip install -r requirements.txt`

To run tests, run `$ pytest`

Unfortunately, setuptools does not support submodules (to my knowledge). So the [XML schema](grow_recipe/grow-recipe.xsd) must be kept updated with the [source](https://github.com/njason/grow-recipe-schema/blob/master/grow-recipe.xsd)
