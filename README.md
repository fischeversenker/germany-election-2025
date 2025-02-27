# German Election Data Project


This project consists of two main components:

1. **Scraper**: A Python script that collects data about the German election from the official government website.

## Scraper

The scraper is responsible for fetching data from the German election website and saving it as JSON files. It processes each federal state and its constituencies to extract relevant data.

### How to Run the Scraper

1. Navigate to the scraper directory.
2. Ensure you have the necessary Python packages installed.
3. Run the scraper script:

```bash
python3 german_election_scraper/scraper.py
```

The data will be saved in the `strukturdaten` directory as JSON files.

### Analysis of the Data

This section explores potential correlations and insights that can be derived from the collected election and structural data:

- **Education and Voting Patterns**: Analyze how the level of education in a constituency correlates with voting preferences, particularly for parties that emphasize education policies.
- **Urban vs. Rural Voting Trends**: Compare voting patterns between urban and rural constituencies to identify any significant differences in party support.
- **Economic Indicators and Election Results**: Investigate the relationship between economic factors such as unemployment rates or average income and the election outcomes in different constituencies.
- **Demographic Influence**: Examine how demographic factors like age distribution and population density affect voting behavior and party support.
- **Historical Voting Trends**: Analyze changes in voting patterns over time to identify shifts in political alignment or emerging trends in specific regions.

These analyses can provide valuable insights into the socio-political landscape and help in understanding the factors influencing voter behavior in Germany.

- Expand the dashboard to include more visualizations and data insights.
- Evaluate if Flask is the best choice for a feature-rich, visually appealing dashboard.
- Organize JSON files into folders by state, ensuring each state has its own directory for `strukturdaten` and election results.
- Automate the process of pulling election results for each constituency (Wahlkreis) from the official website, specifically targeting the "Zweitstimme" results in figures with IDs starting with "stimmentabellexxxx".
