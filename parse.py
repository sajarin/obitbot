from bs4 import BeautifulSoup

def load_html(file_path: str) -> BeautifulSoup:
    try: 
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_html = f.read()
            soup = BeautifulSoup(raw_html, 'lxml')
            return soup
    except OSError as err:
        print("OSError: {0}".format(err))

def parse_html(page_soup: BeautifulSoup) -> str:
    extracted_data = ''
    return extracted_data
