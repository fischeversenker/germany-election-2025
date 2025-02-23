import requests
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
    table = soup.find('table')
    if table:
        print("Tabular data found:")
    if table:
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            if columns:
                print([col.get_text(strip=True) for col in columns])

if __name__ == "__main__":
    fetch_federal_states()
