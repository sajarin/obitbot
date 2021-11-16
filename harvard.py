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
        link_containers = soup.find_all('h2', {"class": "tz-article-image__title"})
        for link in link_containers:
            link = link.a
            url_list.append(link['href'])
    return url_list

def parse_harvard_pages(page_soup: BeautifulSoup) -> str:
    title = page_soup.find('h1', {"class": "article-titles__title"})
    text_container = page_soup.find('div', {"class": "article-body"})
    text = ''.join(text_container.get_text(strip=True))
    title = title.text
    print(title)
    return title.replace(",", " ") + ',' + text.replace(",", " ") + '\n'

def run_bot(): 
    BASE_URL = 'https://news.harvard.edu/gazette/tag/obituary/page/'
    NUM_OF_PAGES = 12

    # list_of_obituaries = generate_url_list(BASE_URL, NUM_OF_PAGES)
    # for i, obituary in enumerate(list_of_obituaries, start=1): 
    #     print(i, obituary)
    #     save_page(f'data/harvard/saved_pages/{i}.html', obituary)

    filename = "data/harvard/harvard.csv"
    f = open(filename, "a+", encoding="utf-8")
    for file in sorted(glob.glob('data/harvard/saved_pages/*.html')):
        page_soup = load_html(file)
        extracted_data = parse_html(page_soup, parse_harvard_pages)
        f.write(extracted_data)

run_bot()