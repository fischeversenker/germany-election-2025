import os
import os.path
import requests
import json
from bs4 import BeautifulSoup


def fetch_strukturdaten():
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
            fetch_strukturdaten_constituencies(base_url + state['href'])


def fetch_strukturdaten_constituencies(state_url):
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
            fetch_constituency_strukturdaten(state_url.rsplit(
                '/', 1)[0] + '/' + constituency['href'])


def fetch_constituency_strukturdaten(constituency_url):
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
                current_subheading = th.get_text(
                    separator=" ", strip=True).rstrip(" i")
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
    state_number = constituency_url.split('/')[-2].split('-')[-1]
    state_dir = f"strukturdaten/{state_number}"
    os.makedirs(state_dir, exist_ok=True)
    wahlkreis_number = constituency_url.split('-')[-1].split('.')[0]
    json_filename = f"{state_dir}/strukturdaten_{wahlkreis_number}.json"
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def fetch_election_results():
    base_url = "https://www.bundeswahlleiterin.de/en/bundestagswahlen/2025/ergebnisse/"
    for state_id in range(1, 17):  # Assuming state IDs range from 1 to 16
        state_url = f"{base_url}bund-99/land-{state_id}.html"
        response = requests.get(state_url)
        if response.status_code != 200:
            print(
                f"Failed to fetch election results for state {state_id}: {response.status_code}")
            continue
        soup = BeautifulSoup(response.content, 'html.parser')
        constituencies = soup.find_all('a', href=True)
        for constituency in constituencies:
            if "wahlkreis-" in constituency['href']:
                constituency_id = constituency['href'].split(
                    '-')[-1].split('.')[0]
                print(
                    f"Fetching election results for state {state_id}, constituency {constituency_id}")
                fetch_constituency_election_results(state_id, constituency_id)


def fetch_constituency_election_results(state_id, constituency_id):
    url = f"https://www.bundeswahlleiterin.de/en/bundestagswahlen/2025/ergebnisse/bund-99/land-{state_id}/wahlkreis-{constituency_id}.html"
    response = requests.get(url)
    if response.status_code != 200:
        print(
            f"Failed to fetch election results for constituency {constituency_id}: {response.status_code}")
        return
    soup = BeautifulSoup(response.content, 'html.parser')
    figure = soup.find(
        'figure', id=lambda x: x and x.startswith('stimmentabelle'))
    if not figure:
        print(f"No election results found for constituency {constituency_id}.")
        return
    results = {}
    table = figure.find('table', attrs={'role': None})
    tbodies = table.find_all('tbody')
    if len(tbodies) < 2:
        print(
            f"Expected two tbody elements for constituency {constituency_id}.")
        return
    general_tbody, parties_tbody = tbodies
    results['general'] = {}
    for row in general_tbody.find_all('tr'):
        th = row.find('th')
        cells = row.find_all('td')
        if th and len(cells) >= 6:
            label = th.get_text(strip=True)
            absolute_votes = int(
                cells[-3].get_text(strip=True).replace(',', ''))
            percent_votes = cells[-2].get_text(strip=True)
            results['general'][label] = {
                "absolute_votes": absolute_votes,
                "percent_votes": percent_votes
            }
    results['parties'] = {}
    for row in parties_tbody.find_all('tr'):
        th = row.find('th')
        cells = row.find_all('td')
        if th and len(cells) >= 6:
            label = th.get_text(strip=True)
            absolute_votes = int(
                cells[-3].get_text(strip=True).replace(',', ''))
            percent_votes = cells[-2].get_text(strip=True)
            results['parties'][label] = {
                "absolute_votes": absolute_votes,
                "percent_votes": percent_votes
            }
    state_dir = f"strukturdaten/{state_id}"
    os.makedirs(state_dir, exist_ok=True)
    json_filename = f"{state_dir}/election_results_{constituency_id}.json"
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # fetch_strukturdaten()
    fetch_election_results()
