[<img src="https://readthedocs.org/projects/sklearn_dummies/badge/?version=latest">](http://readthedocs.org/projects/sklearn-dummies/)
[![CircleCI](https://circleci.com/gh/gsmafra/sklearn-dummies.svg?style=shield)](https://circleci.com/gh/gsmafra/sklearn-dummies)
[![codecov](https://codecov.io/gh/gsmafra/sklearn-dummies/branch/master/graph/badge.svg)](https://codecov.io/gh/gsmafra/sklearn-dummies)
[![Requirements Status](https://requires.io/github/gsmafra/sklearn-dummies/requirements.svg?branch=master)](https://requires.io/github/gsmafra/sklearn-dummies/requirements/?branch=master)

# sklearn-dummies
Scikit-learn label binarizer with support for missing values

## Usage example

```
import pandas as pd
import sklearn_dummies as skdm

df = pd.DataFrame(['A', 'B', None, 'A'], columns=['val'])

df_dummy = skdm.DataFrameDummies().fit_transform(df)
```

Result:

|     | val_A | val_B |
| --- |:-----:|:-----:|
| 0   |   1.0 |   0.0 |
| 1   |   0.0 |   1.0 |
| 2   |   NaN |   NaN |
| 3   |   1.0 |   0.0 |

## Installing

Sklearn-dummies is available in [PyPI](https://pypi.python.org/pypi/sklearn_dummies). Install via pip:

```
pip install sklearn_dummies
```

## Docs

[They're here](http://sklearn-dummies.readthedocs.io/en/latest/index.html)
