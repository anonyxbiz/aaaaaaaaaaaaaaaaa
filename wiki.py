# wiki.py
from requests import Session, get
from bs4 import BeautifulSoup as bs4
from re import sub

p = print

def rmp(text):
    pattern = r'\([^)]*\)|\[[^\]]*\]'
    stripped_text = sub(pattern, '', text).replace('  ', ' ').strip()
    return stripped_text

def wiki(keyword):
    full_article = ''

    cookies = {
        'GeoIP': 'KE:30:Nairobi:-1.28:36.82:v4',
        'enwikimwuser-sessionId': '5502b21ef9c20da1291a',
        'WMF-Last-Access': '13-Mar-2024',
        'WMF-Last-Access-Global': '13-Mar-2024',
        'NetworkProbeLimit': '0.001',
        'WMF-DP': '441,c04,765',
    }
    headers = {
        'authority': 'en.m.wikipedia.org',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://en.m.wikipedia.org/w/index.php?fulltext=search&search=Eminem+American+rapper&title=Special%3ASearch&ns0=1',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'action': 'opensearch',
        'format': 'json',
        'formatversion': '2',
        'search': keyword,
        'namespace': '0',
        'limit': '10',
    }

    try:
        res = get('https://en.m.wikipedia.org/w/api.php', params=params, cookies=cookies, headers=headers)
        if res.status_code == 200:
            url = res.json()[3][0]
            res = get(url, cookies=cookies, headers=headers, allow_redirects=True)
            if res.status_code == 200:
                r = res.text
                soup = bs4(r, 'html.parser')
                summary = soup.find_all("p")
                for a in summary:
                    a = a.text.strip()
                    if a == '\n':
                        pass
                    elif len(a) < 50:
                        pass
                    else:
                        full_article+=f'{a}'
                        break
            else:
                full_article = 'I don\'t know '+keyword+' yet.'
    except:
        pass
    
    full_article = rmp(full_article)
    return full_article

if __name__ == "__main__":
    pass