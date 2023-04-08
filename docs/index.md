# Welcome to 124c41

type: short summary

  │            │

  │            └─⫸ Summary in present tense. Not capitalized.

  │

  └─⫸ Commit Type: build|cicd|docs|feat|fix|node|refactor|test

## Team Fight Tactics Strategy Application

http://tftchamp.duckdns.org:3000/

### Datasets

publish @ https://www.kaggle.com/datasets/teckmengwong/team-fight-tactics-matches

![tftfi00](https://github.com/furyhawk/tftchamp/raw/master/assets/XGBRegressor_feature_importances.png)

[furyhawk/tftchamp: teamfight-tactics Data Analysis (github.com)](https://github.com/furyhawk/tftchamp)

#### About this dataset

Team Fight Tactics highest ELO challengers games scrape by https://github.com/furyhawk/tftchamp.

Using https://developer.riotgames.com/ API.

- 8 players FFA in one game.

- **Target Label**: *placement*

- 1 is best. Lower is better.

- Top 4 placement is a Win.

- Alternative prediction is to group Top 4 placement as Binary Win, bottom 4 as Binary Lost.

- Only team traits and augments/items chosen included in datasets.

- Stats like *game_length*, *players_eliminated* are excluded. This is to prevent the model from learning obvious predictor.

```sh
sudo ./scripts/run_pipeline.sh -nrci
```

## Web Scraping With Python

### Objective

This tutorial aims to show how to use the Python programming language to web scrape a website. Specifically, we will use the `requests` and `Beautiful Soup` libraries to scrape and parse data from [companiesmarketcap.com](https://companiesmarketcap.com/) and retrieve the “*Largest Companies by Market Cap*”. Finance details are scrape and parse from [finance.yahoo.com](https://finance.yahoo.com/quote/).

We will learn how to scale the web scraping process by first retrieving the first company/row of the table, then all companies on the website’s first page, and finally, all 6024 companies from multiple pages. Once the scraping process is complete, we will preprocess the dataset and transform it into a more readable format before using `matplotlib` to visualise the most important information.
