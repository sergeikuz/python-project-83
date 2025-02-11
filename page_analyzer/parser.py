from bs4 import BeautifulSoup
import lxml

def get_data(content: str) -> dict:
    soup = BeautifulSoup(content, 'lxml')
    data = {}
    data['title'] = soup.title.text if soup.title else None
    data['h1'] = soup.h1.text if soup.h1 else None
    data['description'] = None
    if soup.find('meta', attrs={'name': 'description'}):
        meta = soup.find('meta', attrs={'name': 'description'})
        data['description'] = meta.get('content', None)
    
    return data