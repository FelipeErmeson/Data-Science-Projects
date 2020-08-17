import scrapy
import itertools

class MediumsearchSpider(scrapy.Spider):
    name = 'mediumSearch'

    def __init__(self, max_page, *args, **kwargs):
        super(MediumsearchSpider, self).__init__(*args, **kwargs)
        self.download_delay = 1.5
        self.allowed_domains = ['medium.com']
        self.key_words = ['Data%20Science', 'Machine%20Learning', 'Deep%20Learning', 'Kaggle']
        self.current_page = 1
        self.max_page = int(max_page)
        self.i = 0
        self.aux = False
        self.url = 'https://medium.com/search/posts?q={}&page={}'
        self.start_urls = [self.url.format(self.key_words[self.i], self.current_page)] 

    def parse(self, response):
        links = response.css("div.postArticle-content > a::attr(href)").getall()
        titles = response.css('.graf--title::text').getall() #response.css('.graf--title::text, .graf--title > strong::text').getall()
        reading_times = response.css("span.readingTime::attr(title)").getall()
        palms = response.css("div > span > button::text").getall()
        comments = response.css("div.buttonSet.u-floatRight > a::text").getall() #Responses

        if len(titles) != 10:
            self.current_page += 1
            yield scrapy.Request(self.url.format(self.key_words[self.i], self.current_page), self.parse)
        else:
            for link, title, r_time, palm, comment in itertools.zip_longest(links, titles, reading_times, palms, comments, fillvalue=''):
                yield {"link": link, "title": title, "reading_time": r_time, "palms": palm, "comments": comment,
                "key_word": self.key_words[self.i], "page": self.current_page}
            if self.current_page <= self.max_page: #<
                self.current_page += 1
                if self.current_page >= self.max_page: #==
                    self.i += 1
                    self.current_page = 1
                yield scrapy.Request(self.url.format(self.key_words[self.i], self.current_page), self.parse)
