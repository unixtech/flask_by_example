import requests
import re
import nltk
import operator
from collections import Counter
from lxml import html
from bs4 import BeautifulSoup as bs
from stop_words import stops
import os
import models
from app import db
import json
from flask import jsonify

#Count and dev func
def count_and_save_words(url):
    errors = []
    try:
        r = requests.get(url)
    except:
        errors.append('Unable to get URL')
        return {'error': errors}
    raw = bs(r.text, 'lxml').get_text()
    tokens = nltk.word_tokenize(raw)
    text = nltk.Text(tokens)
    nonPunct = re.compile('.*[A-Za-z].*')
    raw_words = [w for w in text if nonPunct.match(w)]
    raw_words_count = Counter(raw_words)
    #Stop words
    no_stop_words = [w for w in raw_words if w.lower() not in stops]
    no_stop_words_count = Counter(no_stop_words)
    no_stop_words_count_d = dict(no_stop_words_count)
    with open('/root/python/flask_by_example/t.txt', 'w') as f:
        json.dump(no_stop_words_count_d, f)
    return no_stop_words_count

    #Save the results
    # try:
        # result = models.Result(url=url, result_all=dict(raw_words_count), result_no_stop_words=dict(no_stop_words_count))
        # print(str(result.result_no_stop_words))
        # db.session.add(result)
        # db.session.commit()
        # return result.id
    # except:
        # errors.append('Unable to add Items to DB')
        # return {"error": errors}
