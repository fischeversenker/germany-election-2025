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

## Results

This is the analysis of Gemini Flash to the correlation matrices produced and printed by the visualizer.py.

### Overall Trends:
#### Education:
- Higher education levels correlate with increased support for SPD, Grüne, and Die Linke.
- Lower education levels correlate strongly with increased support for AfD.
- CDU's support shows a weak positive correlation with higher education.
#### Age:
- Younger voters (18-34) favor SPD and Grüne, with some support for Die Linke.
- Older voters (60+) strongly support AfD, with less support for SPD and Grüne.
- CDU's support is relatively age-neutral.
#### Unemployment:
- Higher unemployment areas correlate with increased support for SPD and Die Linke.
- Higher unemployment correlates with decreased support for AfD.
- Unemployment has little impact on CDU and Grüne support.
#### Income:
- Higher income areas strongly favor Grüne.
- Higher income areas correlate with decreased support for AfD and Die Linke.
- Income has minimal impact on SPD and CDU support.
#### Foreigners:
- Areas with a higher percentage of foreigners show increased support for Grüne and Die Linke.
- Areas with a higher percentage of foreigners show decreased support for AfD.
- SPD has a moderate positive correlation with areas that have a higher percentage of foreigners.
- CDU support is not significantly impacted by the percentage of foreigners.

### Key Party Takeaways:
- **AfD**: Strongest support from older, less-educated, and lower-income demographics, and in areas with fewer foreigners.
- **Grüne**: Strongest support from younger, highly educated, and higher-income demographics, and in areas with more foreigners.
- **SPD**: Moderate support across younger, higher-educated, and higher-unemployment demographics, and areas with more foreigners.
- **Die Linke**: Moderate support from higher educated and higher unemployment demographics, and areas with more foreigners. Lower support from higher income demographics.
- **CDU**: Support is less influenced by the analyzed demographic factors, showing relatively weak correlations across the board.
