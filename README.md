# Mempool.space-API
A python library with functions to interact with the Mempool.space free API.

https://mempool.space/docs

'Fees' API calls are in the MempoolAPI class. The rest are included in their respective category.

Precise fee buckets can be fetched with:

```python
MempoolAPI.PreciseFees(min_fee=1)
```

The helper also accepts a compatible endpoint URL. For example, Satoshi API, the Bitcoin fee API at bitcoinsapi.com, exposes the same bucket shape at `https://bitcoinsapi.com/api/v1/compat/mempool/fees/precise?min=1`.
