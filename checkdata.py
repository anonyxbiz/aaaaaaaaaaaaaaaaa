# checkdata.py
import json_stream
from random import randint as ra

p = print

def s_meaning(meaning):
    meaning = meaning.strip()

    return meaning

def analyzer(keyword, a_type):
    with open('knowledge_base.json', 'r', encoding="utf8") as file:
        knowledge_base: dict = json_stream.load(file)

        for item in knowledge_base["data"]:
            ref = keyword.lower()
            word = item[f'{a_type}']
            meaning = item['answer']

            if ref in word.lower() and len(word) < (len(ref) + ra(0, 10)):
                return s_meaning(meaning)
            else:
                pass
        return None

def define(keyword):
    try:
        meaning = analyzer(keyword, 'keyword')
        if meaning:
            return meaning
        else:
            meaning = analyzer(keyword, 'answer')
            if meaning:
                return meaning
 
 
    except Exception as e:
        p(e)
    return None

if __name__ == "__main__":
    while True:
        try:
            p(define(input('You: ')))
        except KeyboardInterrupt:
            break
        except Exception as e: p(e)
