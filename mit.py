import glob
from typing import List
from core.scrape import load_page, save_page
from core.parse import load_html, parse_html
from bs4 import BeautifulSoup

def generate_url_list(url: str, num_of_pages: int) -> List:
    url_list = []
    for i in range(1, num_of_pages):
        url_to_scrape = url + str(i)
        raw_html = load_page(url_to_scrape)
        soup = BeautifulSoup(raw_html, 'lxml')
        links = soup.find_all('a', {"class": "term-page--news-article--item--title--link"})
        for link in links:
            url_list.append('https://news.mit.edu' + link['href'])
    return url_list

def parse_mit_pages(page_soup: BeautifulSoup) -> str:
    title = page_soup.find('span', itemprop="name headline")
    text_container = page_soup.find('div', {"class": "paragraph--type--content-block-text"})
    text = ''.join(text_container.get_text(strip=True))
    title = title.text
    print(title)
    return title.replace(",", " ") + ',' + text.replace(",", " ") + '\n'

def run_bot(): 
    BASE_URL = 'https://news.mit.edu/topic/obituaries?type=1&page='
    NUM_OF_PAGES = 68 

    # list_of_obituaries = generate_url_list(BASE_URL, NUM_OF_PAGES)
    # for i, obituary in enumerate(list_of_obituaries, start=1): 
    #     print(i, obituary)
    #     save_page(f'data/mit/saved_pages/{i}.html', obituary)

    filename = "data/mit/mit.csv"
    f = open(filename, "a+", encoding="utf-8")
    for file in sorted(glob.glob('data/mit/saved_pages/*.html'), key=lambda x: int(x.split('pages\\')[1][:-5])):
        print(file + '\n')
        page_soup = load_html(file)
        extracted_data = parse_html(page_soup, parse_mit_pages)
        f.write(extracted_data)

run_bot()