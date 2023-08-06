
# Datasets in Local Mode


```python
%run ./00_setup.ipynb
```

## Initiate Local Session
...


```python
cortex = Cortex.local()
builder = cortex.builder()
```

## Create a Dataset from a CSV file using the local builder
...


```python
ds = builder.dataset('c12e/sp500_5y_daily').title('5Y Daily S&P 500 Data').from_csv('./sample-data/sp500_5y_daily_10312018.csv').build()
print('{} v{}'.format(ds.title, ds.version))
df = ds.as_pandas()
df.tail()
```

## Reload the dataset
...


```python
ds = cortex.dataset('c12e/sp500_5y_daily')
print('{} v{}'.format(ds.title, ds.version))
df = ds.as_pandas()
df.tail()
```


```python

```
