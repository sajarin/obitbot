import glob
from typing import List
from core.scrape import load_page, save_page
from core.parse import load_html, parse_html
from bs4 import BeautifulSoup

def generate_url_list(url: str, num_of_pages: int) -> List:
    url_list = []
    for i in range(0, num_of_pages):
        url_to_scrape = url + str(i)
        raw_html = load_page(url_to_scrape)
        soup = BeautifulSoup(raw_html, 'lxml')
        links = soup.find_all('h3', {"class": "c-list__item-title"})
        for link in links:
            link = link.a
            url_list.append('https://news.uchicago.edu' + link['href'])
    return url_list

def parse_uchicago_pages(page_soup: BeautifulSoup) -> str:
    title = page_soup.find('h1', {"class": "c-hero__heading"})
    text_container = page_soup.find('section', {"class": "c-article__content"})
    text = ''.join(text_container.get_text(strip=True)).replace('\n', '')
    title = title.text.replace('\n', '')
    print(repr(title))
    return title.replace(",", " ") + ',' + text.replace(",", " ") + '\n'

def run_bot(): 
    BASE_URL = 'https://news.uchicago.edu/tag/obituary?all=on&type%5Bstory%5D=story&type%5Bpodcast%5D=podcast&type%5Bvideo%5D=video&page='
    NUM_OF_PAGES = 19 

    # list_of_obituaries = generate_url_list(BASE_URL, NUM_OF_PAGES)
    # for i, obituary in enumerate(list_of_obituaries, start=1): 
    #     print(i, obituary)
    #     save_page(f'data/uchicago/saved_pages/{i}.html', obituary)

    filename = "data/uchicago/uchicago.csv"
    f = open(filename, "a+", encoding="utf-8")
    for file in sorted(glob.glob('data/uchicago/saved_pages/*.html')):
        page_soup = load_html(file)
        extracted_data = parse_html(page_soup, parse_uchicago_pages)
        f.write(extracted_data)

run_bot()