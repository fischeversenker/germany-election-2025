import os
import os.path
import requests
import json
from bs4 import BeautifulSoup


def fetch_federal_states():
    base_url = "https://www.bundeswahlleiterin.de/en/bundestagswahlen/2025/strukturdaten/"
    url = base_url + "bund-99.html"
    # Create the directory for JSON files if it doesn't exist
    os.makedirs("strukturdaten", exist_ok=True)
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch federal states: {response.status_code}")
        return
    soup = BeautifulSoup(response.content, 'html.parser')
    states = soup.find_all('a', href=True)
    processed_states = set()
    for state in states:
        if state['href'] in processed_states:
            continue
        processed_states.add(state['href'])
        if "bund-99/land-" in state['href']:
            print(f"Processing federal state: {state.text}")
            fetch_constituencies(base_url + state['href'])


def fetch_constituencies(state_url):
    print(f"Fetching constituencies from {state_url}")
    response = requests.get(state_url)
    if response.status_code != 200:
        print(f"Failed to fetch constituencies: {response.status_code}")
        return
    soup = BeautifulSoup(response.content, 'html.parser')
    constituencies = soup.find_all('a', href=True)
    processed_constituencies = set()
    for constituency in constituencies:
        if constituency['href'] in processed_constituencies:
            continue
        processed_constituencies.add(constituency['href'])
        if "land-" in constituency['href'] and "/wahlkreis-" in constituency['href']:
            print(f"Processing constituency: {constituency.text}")
            fetch_constituency_data(state_url.rsplit(
                '/', 1)[0] + '/' + constituency['href'])


def fetch_constituency_data(constituency_url):
    response = requests.get(constituency_url)
    if response.status_code != 200:
        print(f"Failed to fetch constituency data: {response.status_code}")
        return
    soup = BeautifulSoup(response.content, 'html.parser')
    main_section = soup.find('main')
    if not main_section:
        return

    data = {}
    figures = main_section.find_all('figure')
    for figure in figures:
        caption = figure.find('caption')
        table = figure.find('table')
        if not (caption and table):
            continue

        caption_text = caption.get_text(separator=" ", strip=True).rstrip(" i")
        data[caption_text] = {}
        current_subheading = None
        for row in table.find_all('tr'):
            th = row.find('th')
            td = row.find('td')
            if th and not td:
                # This is a subheading
                current_subheading = th.get_text(separator=" ", strip=True).rstrip(" i")
                data[caption_text][current_subheading] = {}
            elif th and td:
                # This is a regular row
                th_text = th.get_text(separator=" ", strip=True).rstrip(" i")
                td_text = td.get_text(separator=" ", strip=True)
                # Convert to float if the value is numeric and not a percentage
                if td_text.replace('.', '', 1).isdigit() and not td_text.endswith('%'):
                    td_text = float(td_text)
                if current_subheading:
                    data[caption_text][current_subheading][th_text] = td_text
                else:
                    data[caption_text][th_text] = td_text

    # Extract the state name and wahlkreis number from the URL
    state_number = constituency_url.split('/')[-3].split('-')[-1]
    state_dir = f"strukturdaten/{state_number}"
    os.makedirs(state_dir, exist_ok=True)
    wahlkreis_number = constituency_url.split('-')[-1].split('.')[0]
    json_filename = f"{state_dir}/strukturdaten-{wahlkreis_number}.json"
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    fetch_federal_states()
