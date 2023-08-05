AkuLaku Client
==============

[![Build status](https://gramediadigital.visualstudio.com/Open%20Source/_apis/build/status/AkuLaku%20Build)](https://gramediadigital.visualstudio.com/Open%20Source/_build/latest?definitionId=104)

**INCOMPLETE.  DO NOT USE**

This is a small python client for integrating applications with the AkuLaku API.

[Documentation @ ReadTheDocs](https://akulaku.readthedocs.io/en/latest/)


Quickstart
----------

This library will work with Python 3.6+.

```python

from akulaku import AkuLakuGateway

gateway = AkuLakuGateway(app_id='myapp', secret_key='s3cr3t')

# get a redirect url for frontend to complete payment

# capture order (after redirect?)

# check the order status

```

Development
-----------

```bash
# install requirements
pip install -r requirements.txt

# add sources directory to the search path
PYTHONPATH=$PYTHONPATH:$(pwd)/src

# run tests
behave
```
