# Dataframe

`df["cancer"].value_counts().plot(kind='barh')`
`df[["patient_id", "image_id"]].astype(str).apply(lambda x: 'data/rsna/'+'/'.join(x)+'.png', axis=1)`
`list(mapping.keys())[list(mapping.values()).index(x)]`
``

import logging
from configs import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)  # pylint: disable=invalid-name

logger.info

## Rows of a pandas dataframe df
```py
def __len__(self) -> int:
        """Return the length of the dataset."""
        return len(self.df.index)
```

```sh
In [7]: timeit len(df.index)
1000000 loops, best of 3: 248 ns per loop

In [8]: timeit len(df)
1000000 loops, best of 3: 573 ns per loop
```