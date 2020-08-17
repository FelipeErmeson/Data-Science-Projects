from get_data import download_post_page, parse_post_page
from ml_utils import compute_prediction
import time
from datetime import date
import sqlite3 as sql 
import json

#Words for scrapping
queries = ["machine-learning", "deep-learning", "data-science", "kaggle"]
db_name = "posts.db"

#Scraping three days before the current date
now = date.today()
date_back = date.fromordinal(now.toordinal()-3).strftime("%Y/%m/%d")

def update_db():
    with sql.connect(db_name) as conn:
        for query in queries:
            post_page = download_post_page(query, date_back)
            post_json_data_list = parse_post_page(post_page)

            for post_json in post_json_data_list:
                p = compute_prediction(post_json)

                post_url = post_json['link']
                post_title = post_json['title'].replace("'", "")
                data_front = {"title": post_title, "score": float(p), "link": post_url}
                data_front['update_time'] = time.ctime(time.time())

                print(post_url, json.dumps(data_front))
                c = conn.cursor()
                c.execute("INSERT INTO posts VALUES ('{title}', '{link}', {score}, '{update_time}')".format(**data_front))
                conn.commit()
    return True