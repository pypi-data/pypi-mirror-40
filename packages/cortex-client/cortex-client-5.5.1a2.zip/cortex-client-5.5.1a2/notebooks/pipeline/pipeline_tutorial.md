
# Basic Pipeline Example

This notebook shows how to use basic functions of the Cortex Python SDK pipeline. 
In this example you can see how to modify or enrich data sets to make them suitable for training or modeling. 
Data is modified in a sequential series of steps, hence the pipeline anaology.


```python
# First we import cortex and other libraries we will use
import math
from cortex import Cortex

# Create a Builder instance
cortex = Cortex.local()
builder = cortex.builder()
```

In the next step we will create a data set and populate it from a comma separated values file. A pipeline operates on a data set.


```python
data_set = builder.dataset('forest_fires').title('Forest Fire Data')\
    .from_csv('./data/ff.sample.csv').build()
# Create a pandas data frame so we can view the last few lines of the data set
data_frame = data_set.as_pandas()
data_frame.tail(20)
```

A data set can have one or more named pipelines. Each pipeline is a chain of Python functions that transform the dataset.  In the next step we create a pipeline named "prep".


```python
pipeline = data_set.pipeline('prep') # create or retrieve the pipline named 'prep'
pipeline.reset() # removes any previous steps or context for this pipeline
```

A pipeline step may be used to add a new column.

The [documentation](http://piano.dsi.uminho.pt/~pcortez/fires.pdf) on this data set says that it uses components from the Fire Weather Index to make predictions. One element, the Build Up Index, or BUI, is based on a relation of two other columns and is omitted. This step adds that missing element. 


```python
def add_bui(pipeline, df):
    df['BUI'] = (0.8 * df['DMC'] * df['DC'])/(df['DMC'] + 0.4 * df['DC'])

pipeline.add_step(add_bui)
```

You see in the above code that pipeline step functions require a pipeline and a dataframe parameter. The [Pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/dsintro.html#dataframe) provides a rich set of functions for operating on table data.

A pipeline step may be used to modify a column.

The documentation also says that the last column, __area__, is skewed towards zero and should be adjusted logarithmically "to improve regression results for right-skewed targets".


```python
def fix_area(pipeline, df):
    df['area'] = df['area'].map(lambda a: math.log1p(a))
    
pipeline.add_step(fix_area)
```

### Running the Pipeline
After all the steps are added, you can call _run_ on the pipeline. This will invoke each of the steps in order and return a transformed DataFrame instance.


```python
pipeline.run(data_frame)
```


```python

```
