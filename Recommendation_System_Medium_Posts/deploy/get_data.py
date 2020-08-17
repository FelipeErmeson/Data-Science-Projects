import requests as rq
import bs4 as bs4
import re
import time

def download_post_page(query, date):
    url = "https://medium.com/tag/{query}/archive/{date}"
    urll = url.format(query=query, date=date)
    response = rq.get(urll)

    return response.text

def parse_post_page(page_html):
    post_list = []
    parsed = bs4.BeautifulSoup(page_html, 'html.parser')
    tags = parsed.select(".streamItem")

    for e in tags:
        if not e.select(".graf--title"):
            continue
        if not e.select("div > span > button"):
            palms = '0'
        else:
            palms = e.select("div > span > button")[0].text
        if not e.select("div.buttonSet.u-floatRight > a"):
            comments = '0'
        else:
            comments = e.select("div.buttonSet.u-floatRight > a")[0].text
        
        link = e.findAll("a")[3]['href']
        title = e.select(".graf--title")[0].text
        reading_time = e.select("span.readingTime")[0]['title']
        data = {"link": link, "comments": comments, "palms": palms, "reading_time": reading_time, "title": title}
        post_list.append(data)

    return post_list