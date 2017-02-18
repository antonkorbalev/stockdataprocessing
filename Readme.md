# About
This repo contains scripts for stock data analysis using various machine learning algorithms.

# File structure
* **Conf** folder contains configuration files for robots, stock data downloaders and algoritms.
* **Tests** folder contains unit tests.
* **StockDataDownloader** folder contains classes for downloading stock data. This data is used for back tests and strategies optimization.
* **DbDump.py** - dumps forex data from Oanda broker to configurable PostgreSQL database.
* **FxRobot.py** - a template for forex robot with backlogs support (to be modified).
* **PatternsProcessor.py** - a class for splitting sequental price data into patterns.
* **Readme.md** - readme file.
