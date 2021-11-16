import requests

def load_page(url:str) -> str:
    response = requests.get(url)
    html = response.text
    return html

def save_page(storage_path: str, url: str) -> None:
    response = requests.get(url)
    html = response.text
    with open(f'{storage_path}', 'w', encoding="utf-8") as f:
        f.write(html)