import os.path
from flask import Flask, request, render_template
import os
import json
import run_backend
import time
import get_data 
import ml_utils 
import sqlite3 as sql 

app = Flask(__name__)

def get_predictions():
    posts = []
    predictions = []

    with sql.connect(run_backend.db_name) as conn:
        c = conn.cursor()
        for line in c.execute("SELECT * FROM posts WHERE title NOT IN (SELECT title FROM posts GROUP BY title HAVING COUNT(*) > 1)"):
            line_json = {"title": line[0], "link": line[1], "score": line[2], "update_time": line[3]} 
            posts.append(line_json)
    
    last_update = posts[-1]["update_time"]

    for post in posts:
        predictions.append({"link": post['link'], "title": post['title'], "score": round(float(post['score'])*100, 2)})
    
    predictions = sorted(predictions, key= lambda x: x['score'], reverse=True)[:15]

    return predictions, last_update

@app.route('/')
def main_page():
    preds, last_update = get_predictions()
    
    return render_template("index.html", predictions = preds, last_update=last_update)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
