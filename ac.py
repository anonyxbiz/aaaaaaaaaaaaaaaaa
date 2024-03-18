# ac.py
from bs4 import BeautifulSoup as sc
from requests import post, get
from re import sub
from random import choice
from wiki import wiki

p = print

def clean(scrape_site):
    soup = sc(scrape_site, 'html.parser')
    class_name = 'break-words meaning mb-4'
    data = soup.find('div', class_=class_name)
    stuff = data.text
    stuff = sub(r'(\b\d+\.)', r'\n\1', stuff)
    stuff = f'{stuff}\n'.replace('urban dictionary', 'SlangAI')
    stuff = stuff.replace('Urban Dictionary', 'SlangAI')
    stuff = stuff.replace('\n','')
    return stuff

def Gt(term, headers):
    data = {
        'term': term,
    }
    try:
        scrape_site = post('https://www.urbandictionary.com/search.php', headers=headers, data=data, timeout=20, allow_redirects=True).text
    except Exception:
        scrape_site = Exception
    return scrape_site

def Gss(keyword):
    try:
        headers = {
            'authority': 'api.urbandictionary.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'origin': 'https://www.urbandictionary.com',
            'pragma': 'no-cache',
            'referer': 'https://www.urbandictionary.com/',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }

        params = (
            ('term', keyword),
        )

        r = get('https://api.urbandictionary.com/v0/autocomplete-extra', headers=headers, params=params, timeout=20, allow_redirects=True)
        
        if r.status_code == 200:
            check_list = r.json().get('results')
            if check_list:
                term = choice(check_list).get('term')
                answer_ = Gt(term, headers)
                answer = clean(answer_)

                return answer.strip()
            else:
                answer = wiki(keyword)

                return answer
        else:
            pass

    except Exception as e:
        return e

if __name__ == "__main__":
    while True:
        try:
            p(Gss(input('You: ')))
        except KeyboardInterrupt:
            break
        except Exception as e: p(e)