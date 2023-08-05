# ACRCloud-py

An ACRCloud API Python client library

## Installation
```
$ pip nstall git+https://github.com/andriyor/acrcloud-py.git#egg=acrcloud-py
```

### Requirements
* Python 3.6 and up

### Installation from source
```
$ git clone https://github.com/andriyor/acrcloud-py.git
$ cd acrcloud-py
$ python setup.py install
```

## Usage

Before you can begin identifying audio with ACRCloud's API, you need to sign up for a free trial over at 
https://www.acrcloud.com and create an Audio & Video recognition project. 
This will generate a `host`, `access_key`, and `access_secret` for you to use.

```
from acrcloud import ACRCloud
import os

acr = ACRCloud('eu-west-1.api.acrcloud.com', 'access_key', 'access_secret')
metadata = acr.identify('path-to-file.ogg')
print(metadata)
```

## Development
Install [Pipenv](https://docs.pipenv.org/)   
```
$ pipenv install --dev -e .
```