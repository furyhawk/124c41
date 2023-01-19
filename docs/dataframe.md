# Dataframe

`df["cancer"].value_counts().plot(kind='barh')`
`df[["patient_id", "image_id"]].astype(str).apply(lambda x: 'data/rsna/'+'/'.join(x)+'.png', axis=1)`
`list(mapping.keys())[list(mapping.values()).index(x)]`
``

import logging
from configs import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)  # pylint: disable=invalid-name

logger.info