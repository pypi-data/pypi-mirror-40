heap-analytics-python-client
----------------------------

[![Build Status](https://travis-ci.org/m-vdb/heap-analytics-python-client.svg?branch=master)](https://travis-ci.org/m-vdb/heap-analytics-python-client)
[![Coverage Status](https://coveralls.io/repos/github/m-vdb/heap-analytics-python-client/badge.svg?branch=master)](https://coveralls.io/github/m-vdb/heap-analytics-python-client?branch=master)
[![Pypi version](https://img.shields.io/pypi/v/heapapi.svg)](https://pypi.python.org/pypi/heapapi)

A Python3 client library for the Heap Analytics server-side API.

It supports both the **track** and **identify** APIs. See [Heap documentation](https://docs.heapanalytics.com/reference#track-1).

Installation
------------
```
pip install git+git://github.com/m-vdb/heap-analytics-python-client.git@v0.0.3
```

Usage
-----

```python
from heapapi import HeapAPIClient

heap_client = HeapAPIClient("app_id")

heap_client.identify(
    identity="user@email.com",
    properties={"age": 30, "country": "USA"}
)

heap_client.track(
    identity="user@email.com",
    event="Purchase",
    properties={"cost": 20, "currency": "usd"}
)
```
