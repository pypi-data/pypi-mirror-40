
# Experiments in Local Mode
This notebook require scikit-learn.  Please install using `pip install scikit-learn` or equivalent in your environment.


```python
%run ./00_setup.ipynb
```


```python
from sklearn.datasets.california_housing import fetch_california_housing
houses = fetch_california_housing()
```


```python
print(houses.DESCR)
```


```python
df = pd.DataFrame(data=houses.data, columns=houses.feature_names)
df.head()
```


```python
cortex = Cortex.local()
builder = cortex.builder()
```


```python
ds = builder.dataset('c12e/cal-housing').title('California Housing dataset').from_df(df).build()
print('{} v{}'.format(ds.name, ds.version))
```


```python
from sklearn.linear_model import LinearRegression, RidgeCV, LassoCV, ElasticNetCV
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
```


```python
def train(x, y, **kwargs):
    alphas = kwargs.get('alphas', [1, 0.1, 0.001, 0.0001])
    # Select alogrithm "
    mtype = kwargs.get('model_type')
    if mtype == 'Lasso':
        model = LassoCV(alphas=alphas)
    elif mtype == 'Ridge':
        model = RidgeCV(alphas=alphas)
    elif mtype == 'ElasticNet':
        model = ElasticNetCV(alphas=alphas)
    else:
        model = LinearRegression()

    # Train model
    model.fit(x, y)
    
    return model
```


```python
def predict_and_score(model, x, y):
    predictions = model.predict(x)
    rmse = np.sqrt(mean_squared_error(predictions, y))
    return [predictions, rmse]
```


```python
X_train, X_test, y_train, y_test = train_test_split(df, houses.target, test_size=0.30, random_state=10)
```


```python
%%time

best_model = None
best_model_type = None
best_rmse = 1.0

exp = cortex.experiment('c12e/cal-housing-regression')
exp.reset()
exp.set_meta('style', 'supervised')
exp.set_meta('function', 'regression')

with exp.start_run() as run:
    alphas = [1, 0.1, 0.001, 0.0005]
    for model_type in ['Linear', 'Lasso', 'Ridge', 'ElasticNet']:
        print('---'*30)
        print('Training model using {} regression algorithm'.format(model_type))
        model = train(X_train, y_train, model_type=model_type, alphas=alphas)
        [predictions, rmse] = predict_and_score(model, X_train, y_train)
        print('Training error:', rmse)
        [predictions, rmse] = predict_and_score(model, X_test, y_test)
        print('Testing error:', rmse)

        if rmse < best_rmse:
            best_rmse = rmse
            best_model = model
            best_model_type = model_type

    r2 = best_model.score(X_test, y_test)
    run.log_metric('r2', r2)
    run.log_metric('rmse', best_rmse)
    run.log_param('model_type', best_model_type)
    run.log_param('alphas', alphas)
    run.log_artifact('model', best_model)

print('---'*30)
print('Best model: ' + best_model_type)
print('Best testing error: %.6f' % best_rmse)
print('R2 score: %.6f' % r2)
```


```python
exp
```


```python

```
