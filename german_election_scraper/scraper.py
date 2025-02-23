import requests
from bs4 import BeautifulSoup

def fetch_federal_states():
    url = "https://www.bundeswahlleiterin.de/bundestagswahlen/2025/ergebnisse/bund-99.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    states = soup.find_all('a')
    for state in states:
        print(state.text, state['href'])

if __name__ == "__main__":
    fetch_federal_states()
