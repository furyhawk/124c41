<img src="assets/logo.png" alt="logo" width="20%">

# Welcome to 124c41



type: short summary

  │            │

  │            └─⫸ Summary in present tense. Not capitalized.

  │

  └─⫸ Commit Type: build|cicd|docs|feat|fix|node|refactor|test

## AGI

- Humanity achieve AGI.
- Basic computing skills lost.
- NSFW content filtered for everyone.
- 1 Human decide to learn computing skills.
- NSFW content accessed.

## Home Server

- [Chat](https://chat.furyhawk.lol/): Chat with AI, RAG chatbot. 
- [Bot](https://bot.furyhawk.lol/): AI assistant using GROQ, llama3 70B, RAG and web search.
- [Stock Analysis Assistant](https://fin.furyhawk.lol/): AI assistant using GROQ and llama3.
- ~~[Redlib](https://redlib.furyhawk.lol/): Reddit libre.~~ (killed by bots)
- [Blog](https://info.furyhawk.lol/)
- [Ghost](https://ghost.furyhawk.lol/): Ghost blog.
- [Beyond All Information](https://bai.furyhawk.lol/): analyse your [Beyond All Reason](https://www.beyondallreason.info/) games.
- [CheatSheets](https://cheat.furyhawk.lol/): Collection of cheatsheets.
- [Cookbook](https://cook.furyhawk.lol/): Collection of tech recipes.
- ~~[Forum](https://forum.furyhawk.lol/): Host your own forum.~~ (deprecated)
- [Neural Network Playground](https://furyhawk.github.io/playground): Understand neural network visually.
- [Note](https://note.furyhawk.lol/): Notepad Online. Use cookie storage only.
- [linx](https://linx.furyhawk.lol/): Image pastebin.
- [pastebin](https://bin.furyhawk.lol/): text/file Pastebin.
- [speedtest](https://speed.furyhawk.lol/): Speedtest.
- [Home server](https://github.com/furyhawk/cloudy): Build for ARM64 platform using Docker swarm mode.
- [Team Fight Tactics ML](https://github.com/furyhawk/tftchamp): Analyse the current meta.

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
