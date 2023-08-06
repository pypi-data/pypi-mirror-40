

```python
import os
import sys
import platform
import json
import re
import time
import datetime
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
import cortex
from cortex import Cortex, Message
```


```python
# Matplotlib configuration
%matplotlib inline
plt.rcParams['figure.figsize'] = [18,9]
```


```python
# Seaborn configuration
sns.set_style('darkgrid')
```


```python
# Fix random seed for reproducibility
np.random.seed(7)
```


```python
# Pandas configuration
# Limit float output to 3 decimal places
pd.set_option('display.float_format', lambda x: '{:.3f}'.format(x))
```


```python
print('Python version: {}'.format(platform.python_version()))
print('Pandas version: {}'.format(pd.__version__))
print('Numpy version: {}'.format(np.__version__))
print('Cortex SDK version: {}'.format(cortex.__version__))
```


```python
import warnings
warnings.filterwarnings('ignore')
```


```python

```
