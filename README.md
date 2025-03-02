# German Election Data Project

 ## Project Overview

 This project consists of two main components:

 1. **Scraper**: A Python script that collects data about the German election from the official government website.
 2. **Visualizer**: A Python script that analyzes and visualizes the collected data to provide insights into voting patterns and correlations with various socio-economic
 factors.

 ## Setup

 To set up the project, ensure you have `pipenv` installed. If not, you can install it using:

 ```bash
 pip install pipenv
 ```

 Then, navigate to the `german_election_scraper` directory and install the dependencie

 ```bash
 pipenv install
 ```

 ## Scraper

 The scraper is responsible for fetching data from the German election website and saving it as JSON files. It processes each federal state and its constituencies to extract relevant data.

 ### How to Run the Scraper

 ```bash
 python3 german_election_scraper/scraper.py
 ```

 The data will be saved in the `strukturdaten` directory as JSON files and are part of this repository.

 ## Visualizer

 The visualizer analyzes the collected data to provide insights into various correlations and voting patterns.

 ### How to Run the Visualizer

 ```bash
 python3 german_election_scraper/visualizer.py
 ```
The visualizer provides correlation analyses for:

 - **Education and Voting Patterns**: Analyze how the level of education in a constituency correlates with voting preferences, particularly for parties that emphasize education policies.
 - **Economic Indicators and Election Results**: Investigate the relationship between economic factors such as unemployment rates or average income and the election outcom in different constituencies.
 - **Demographic Influence**: Examine how demographic factors like age distribution an population density affect voting behavior and party support.

 These analyses can provide valuable insights into the socio-political landscape and help in understanding the factors influencing voter behavior in Germany.

