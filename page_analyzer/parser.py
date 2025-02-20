from bs4 import BeautifulSoup


def get_data(content: str) -> dict:
    soup = BeautifulSoup(content, 'lxml')
    data = {}
    title = soup.title.text
    data['title'] = title if title and len(title) <= 70 else None
    data['h1'] = soup.h1.text if soup.h1 and len(soup.h1) <= 65 else None
    data['description'] = None
    meta = soup.find('meta', attrs={'name': 'description'})
    if meta and len(meta) <= 300:  
        data['description'] = meta.get('content', None)
    
    return data