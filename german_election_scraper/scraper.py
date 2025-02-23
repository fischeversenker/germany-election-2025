import os
import requests
import json
from bs4 import BeautifulSoup


def fetch_federal_states():
    base_url = "https://www.bundeswahlleiterin.de/en/bundestagswahlen/2025/strukturdaten/"
    url = base_url + "bund-99.html"
    print(f"Fetching federal states from {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch federal states: {response.status_code}")
        return
    soup = BeautifulSoup(response.content, 'html.parser')
    states = soup.find_all('a', href=True)
    for state in states:
        if "bund-99/land-" in state['href']:
            print(f"Processing federal state: {state.text}")
            fetch_constituencies(base_url + state['href'])
            break  # Only process the first federal state for now


def fetch_constituencies(state_url):
    print(f"Fetching constituencies from {state_url}")
    response = requests.get(state_url)
    if response.status_code != 200:
        print(f"Failed to fetch constituencies: {response.status_code}")
        return
    soup = BeautifulSoup(response.content, 'html.parser')
    constituencies = soup.find_all('a', href=True)
    for constituency in constituencies:
        if "land-" in constituency['href'] and "/wahlkreis-" in constituency['href']:
            print(f"Processing constituency: {constituency.text}")
            fetch_constituency_data(state_url.rsplit(
                '/', 1)[0] + '/' + constituency['href'])
            break


def fetch_constituency_data(constituency_url):
    debug = os.getenv('DEBUG') == '1'
    if debug:
        print(f"Fetching constituency data from {constituency_url}")
        print("Starting data extraction process...")
    response = requests.get(constituency_url)
    if response.status_code != 200:
        print(f"Failed to fetch constituency data: {response.status_code}")
        return
    soup = BeautifulSoup(response.content, 'html.parser')
    main_section = soup.find('main')
    if not main_section:
        if debug:
            print("No main section found.")
        return
    if debug:
        print("Main section found.")

    data = {}
    figures = main_section.find_all('figure')
    if debug:
        if figures:
            print(f"Found {len(figures)} figures.")
        else:
            print("No figures found in the main section.")
    for figure in figures:
        caption = figure.find('caption')
        table = figure.find('table')
        if debug:
            if caption:
                print(f"Caption found: {caption.get_text(strip=True)}")
            else:
                print("No caption found in figure.")
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
                if debug:
                    print(f"Extracted row: {th_text} -> {td_text}")
                if current_subheading:
                    data[caption_text][current_subheading][th_text] = td_text
                else:
                    data[caption_text][th_text] = td_text

    # Extract the wahlkreis number from the URL
    wahlkreis_number = constituency_url.split('-')[-1].split('.')[0]
    json_filename = f"strukturdaten-{wahlkreis_number}.json"
    if debug:
        print(f"Extracted data: {data}")
        print(f"Saving data to {json_filename}")
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    if debug:
        print(f"Data successfully saved to {json_filename}")


if __name__ == "__main__":
    fetch_federal_states()
