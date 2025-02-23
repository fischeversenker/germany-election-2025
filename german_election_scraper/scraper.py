import requests
import json
from bs4 import BeautifulSoup

def fetch_federal_states():
    base_url = "https://www.bundeswahlleiterin.de/en/bundestagswahlen/2025/strukturdaten/"
    url = base_url + "bund-99.html"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch federal states: {response.status_code}")
        return
    soup = BeautifulSoup(response.content, 'html.parser')
    states = soup.find_all('a', href=True)
    for state in states:
        if "bund-99/land-" in state['href']:
            fetch_constituencies(base_url + state['href'])

def fetch_constituencies(state_url):
    response = requests.get(state_url)
    if response.status_code != 200:
        print(f"Failed to fetch constituencies: {response.status_code}")
        return
    soup = BeautifulSoup(response.content, 'html.parser')
    constituencies = soup.find_all('a', href=True)
    for constituency in constituencies:
        if "/land-" in constituency['href'] and "/wahlkreis-" in constituency['href']:
            print(f"Fetching data for {constituency.text}")
            fetch_constituency_data(state_url.rsplit('/', 1)[0] + '/' + constituency['href'])
            break

def fetch_constituency_data(constituency_url):
    response = requests.get(constituency_url)
    if response.status_code != 200:
        print(f"Failed to fetch constituency data: {response.status_code}")
        return
    soup = BeautifulSoup(response.content, 'html.parser')
    main_section = soup.find('main')
    if not main_section:
        print("No main section found.")
        return

    data = {}
    figures = main_section.find_all('figure')
    for figure in figures:
        caption = figure.find('caption')
        table = figure.find('table')
        if caption and table:
            caption_text = caption.get_text(strip=True)
            data[caption_text] = {}
            for row in table.find_all('tr'):
                th = row.find('th')
                td = row.find('td')
                if th and td:
                    data[caption_text][th.get_text(strip=True)] = td.get_text(strip=True)

    # Extract the wahlkreis number from the URL
    wahlkreis_number = constituency_url.split('-')[-1].split('.')[0]
    json_filename = f"strukturdaten-{wahlkreis_number}.json"
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print(f"Data saved to {json_filename}")

if __name__ == "__main__":
    fetch_federal_states()
