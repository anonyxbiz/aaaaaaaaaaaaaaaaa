from requests import get, post
from bs4 import BeautifulSoup as bs4
from threading import Thread
from json import dump, load

headers = {
    'authority': 'tech.co',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
}

p = print

articles = {'posts': []}

def articler(link):
    r = get(link, headers=headers).text
    
    soup = bs4(r, "html.parser")
    
    h1 = soup.find_all('p')
    
    article = ''
    for a in h1:
        data = a.text.strip()
        if data.startswith('Stay informed'):
            pass
        else:
            if len(data) > 200:
                article+='{}\n\n'.format(data)
        
    # p(article)
    articles['posts'].append(article)

def updater():
    link = 'https://tech.co/news'
    r = get(link, headers=headers).text
        
    soup = bs4(r, "html.parser")
    
    a = soup.find_all(class_="post-link")
    
    links = []
    for a_ in a:
        links.append(a_.attrs['href'])
    
    threads = []
    for link in links:
        thread = Thread(target = articler, args = (link,))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    
    p('Scraped {} Articles'.format(len(articles['posts'])))
    
    try:
        with open('news.json', 'w') as f:
            dump(articles, f, indent=2)
        p('Articles Dumped')
    except Exception as e:
        p(f'{e}')

while True:
    try:
        updater()
    except KeyboardInterrupt:
        break
    except Exception as e:
        p(e)
        break