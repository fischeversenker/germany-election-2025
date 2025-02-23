import requests
from bs4 import BeautifulSoup

def fetch_federal_states():
    base_url = "https://www.bundeswahlleiterin.de/bundestagswahlen/2025/strukturdaten/"
    url = base_url + "bund-99.html"
    print(f"Fetching federal states from {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch federal states: {response.status_code}")
        return
    soup = BeautifulSoup(response.content, 'html.parser')
    states = soup.find_all('a', href=True)
    print("Federal states found:")
    for state in states:
        if "bund-99/land-" in state['href']:
            print(state.text, state['href'])
            print(f"Fetching constituencies for {state.text}")
            fetch_constituencies(base_url + state['href'])

def fetch_constituencies(state_url):
    print(f"Fetching constituencies from {state_url}")
    response = requests.get(state_url)
    if response.status_code != 200:
        print(f"Failed to fetch constituencies: {response.status_code}")
        return
    soup = BeautifulSoup(response.content, 'html.parser')
    constituencies = soup.find_all('a', href=True)
    for constituency in constituencies:
        if "wahlkreis" in constituency['href']:
            print(constituency.text, constituency['href'])

if __name__ == "__main__":
    fetch_federal_states()
