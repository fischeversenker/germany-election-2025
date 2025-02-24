# German Election Data Project


This project consists of two main components:

1. **Scraper**: A Python script that collects data about the German election from the official government website.
2. **Visualizer**: A Flask-based web application that visualizes the collected data.

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

## Visualizer

The visualizer is a web application built with Flask. It aims to provide a dashboard to display the election data in a user-friendly manner. Currently, it includes a basic setup to display the number of municipalities per constituency.

### How to Run the Visualizer

1. Navigate to the visualizer directory.
2. Set up a Python virtual environment and install Flask:

```bash
python3 -m venv venv
source venv/bin/activate
pip install flask
```

3. Run the Flask application:

```bash
export FLASK_APP=strukturdaten-visualizer/app.py
flask run
```

4. Open a web browser and go to `http://127.0.0.1:5000/` to view the dashboard.

### Next Steps

- Expand the dashboard to include more visualizations and data insights.
- re-think Flask. Is it the right choice for a feature-rich good-looking dashboard?
- put json files into folders for their state. So there should be a folder per state that has the strukturdaten and the election results
- pull election results for each wahlkreis from https://www.bundeswahlleiterin.de/en/bundestagswahlen/2025/ergebnisse/bund-99/land-9/wahlkreis-213.html. Find the election results (Zweitstimme) in the figure with an id that starts with "stimmentabellexxxx".
