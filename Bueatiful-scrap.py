import requests
from bs4 import BeautifulSoup

def scrape_tag(url, tag_name):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.find_all(tag_name)
        return tag_name, [element.get_text() for element in elements]
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return tag_name, []

def scrape_sequentially(url, tags):
    for tag in tags:
        tag_name, content = scrape_tag(url, tag)
        
        print(f"Content for <{tag_name}> tag:")
        for text in content:
            print(text)
        print("-" * 40)

url = 'https://jalammar.github.io/illustrated-transformer/'

tags = ['p', 'h1', 'div', 'a'] 

scrape_sequentially(url, tags)
