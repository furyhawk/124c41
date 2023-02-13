# Weights & Biases

Machine learning experiment tracking, dataset versioning, and model evaluation

```python
import wandb
from omegaconf import DictConfig
import pandas as pd


class WeightsAndBiases:
    def __init__(self, cfg: DictConfig) -> None:
        self.cfg: DictConfig = cfg
        if cfg.debug:
            wandb.init(mode="disabled")
        else:
            wandb.init(project=cfg.project, entity="peekingduck", config=cfg)

    def watch(self, model) -> None:
        wandb.watch(model)

    def log(self, loss) -> None:
        wandb.log(loss)

    def log_history(self, history) -> None:
        selected_history = {
            key: history[key]
            for key in [
                "train_loss",
                "valid_loss",
                "valid_elapsed_time",
                "val_MulticlassAccuracy",
                "val_MulticlassPrecision",
                "val_MulticlassRecall",
                "val_MulticlassAUROC",
            ]
        }

        df: pd.DataFrame = pd.DataFrame(selected_history)
        for row_dict in df.to_dict(orient="records"):
            wandb.log(row_dict)

    def log_training_loss(self, loss) -> None:
        wandb.log({"train_loss": loss})

    def log_validation_loss(self, loss) -> None:
        wandb.log({"val_loss": loss})
```

Your personal account has 100 GB of free storage and artifacts.

Usage Pricing
Storage
$0.08 per GB up to 10 TB
$0.06 per GB up to 100 TB
$0.05 per GB up to 1000 TB
Over 1000 TB, contact us
Artifact tracking
$0.05 per GB up to 10 TB
$0.03 per GB up to 100 TB
$0.02 per GB up to 1000 TB
Over 1000 TB, contact us

One team, up to 10 users

Email and chat support

100 GB storage and artifacts tracking included. For additional storage, see prices.
