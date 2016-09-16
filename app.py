from flask import Flask, render_template, request, url_for, jsonify
from config import Config, DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy
import os
import word_counter
import operator
import operator
import nltk
import json




#Worker imports
from rq import Queue
from rq.job import Job
from worker import conn



app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
import models
q = Queue(connection=conn)




@app.route('/', methods=['GET', 'POST'])
def hello():
    results = {}
    if request.method == "POST":
        url = request.form['url']
        if 'http://' not in url[:7]:
            url = 'http://' + url
        job = q.enqueue_call(
                func=word_counter.count_and_save_words, args=(url,), result_ttl=5000
                )
        print(job.get_id())
    return render_template('index.html', results=results)

@app.route('/start', methods=['POST'])
def get_counts():
    print(request.data)
    data = json.loads(request.data.decode())
    print(data)
    url = data['url']
    if 'http://' not in url[:7]:
        url = 'http://' + url
    job = q.enqueue_call(func=word_counter.count_and_save_words, args=(url,)
, result_ttl=5000 )
    return job.get_id()


@app.route('/results/<job_key>', methods=['GET'])
def get_results(job_key):
    job = Job.fetch(job_key, connection=conn)
    if job.is_finished:
        # result = models.Result.query.filter_by(id=job.result).first()
        with open('t.txt', 'r') as f:
            result = json.load(f)
        results = sorted(
                result.items(),
                key=operator.itemgetter(1),
                reverse=True
                )[:10]
        return jsonify(results)
    else:
        return "Nay!", 202



if __name__ == '__main__':
    app.run(host="10.0.10.32", port=8000)
