# CharityBase Client Library (Python)

A Python client library for interacting with the CharityBase REST API. Tested on python 3.7.1

Modelled on the [official charitybase JavaScript client](https://github.com/charity-base/charity-base-client-js).

## Authorisation

Log in to the [CharityBase API Portal](https://charitybase.uk/api-portal) and create an API key.

## Example

Search for "homeless" charities with income range £100k - £1m, sorted by descending income:

```python
from charitybase import CharityBase


charityBase = CharityBase(apiKey='my-api-key')

res = charityBase.charity.list({
  'fields': ['income.latest.total'],
  'search': 'homeless',
  'incomeRange': [100000, 1000000],
  'sort': 'income.latest.total:desc',
  'limit': 10,
  'skip': 0,
})
print(res.charities)
```

(Remember to replace `my-api-key` with your actual key, copied from the [CharityBase API Portal](https://charitybase.uk/api-portal))
