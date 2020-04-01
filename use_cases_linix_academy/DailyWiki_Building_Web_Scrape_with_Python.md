### <span style="color: black">&#x1F535; DailyWiki: Building a Web Scraper with Python

```
mkdir daily_wiki
cd daily_wiki
```
Install Pipenv.

```
pip3.7 install --user -U pipenv
```

Install Scrapy.
```
pipenv --python python3.7 install scrapy
```

Activate the virtualenv.
```
pipenv shell
```

Create the project.
```
scrapy startproject daily_wiki .
```

Create an Article Item
Open the daily_wiki/items.py file, and add the following at the end of the file:

```
import scrapy

class Article(scrapy.Item):
   title = scrapy.Field()
   link = scrapy.Field()
Save the file.
Create an Articles Spider
Generate a new spider.
scrapy genspider article en.wikipedia.org
Open article.py, and edit the contents to the following:

# -*- coding: utf-8 -*-
import scrapy

from daily_wiki.items import Article

class ArticleSpider(scrapy.Spider):
   name = 'article'
   allowed_domains = ['en.wikipedia.org']
   start_urls = ['https://en.wikipedia.org/wiki/Wikipedia:Featured_articles']

   def parse(self, response):
       host = self.allowed_domains[0]
       for link in response.css(".featured_article_metadata > a"):
           yield Article(
               title = link.attrib.get("title"),
               link = f"https://{host}{link.attrib.get('href')}"
           )
```

Save the file.
Test the spider by running the following command:
scrapy crawl article
Export Articles as JSON
In the article.py file, add the following beneath the line that begins with start_urls:
```
   custom_settings = {
       'FEED_FORMAT': 'json',
       'FEED_URI': 'file:///tmp/featured-articles-%(time)s.json'
   }
```   

Run the spider.

```
scrapy crawl article
```
View the generated JSON file:

```
ls -al /tmp | grep featured
```
