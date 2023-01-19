# Hydra

```python

import logging

from omegaconf import OmegaConf, DictConfig
import hydra
from hydra.core.hydra_config import HydraConfig

@hydra.main(
    version_base=None,
    config_path="configs",
    config_name="config",
)
def main(cfg: DictConfig) -> None:
    logger.info(OmegaConf.to_yaml(cfg))
    logger.info(f"runtime.output_dir{HydraConfig.get().runtime.output_dir}")

if __name__ == "__main__":
    main()
```

```python
from hydra import initialize, compose

with initialize(version_base=None, config_path="configs"):
    # config is relative to a module
    cfg = compose(config_name="config")
```

To check current defaults
```sh
python my_app.py --info defaults-tree
```
