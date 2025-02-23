import requests
from bs4 import BeautifulSoup

def fetch_federal_states():
    base_url = "https://www.bundeswahlleiterin.de/bundestagswahlen/2025/ergebnisse/"
    url = base_url + "bund-99.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    states = soup.find_all('a', href=True)
    for state in states:
        if "bund-99/land-" in state['href']:
            print(f"Fetching constituencies for {state.text}")
            fetch_constituencies(base_url + state['href'])

def fetch_constituencies(state_url):
    response = requests.get(state_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    constituencies = soup.find_all('a', href=True)
    for constituency in constituencies:
        if "wahlkreis" in constituency['href']:
            print(constituency.text, constituency['href'])

if __name__ == "__main__":
    fetch_federal_states()
