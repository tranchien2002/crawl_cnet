from pymongo import MongoClient
from CNET.article2json import article_json 
import scrapy
import pdb
import re
client = MongoClient('localhost', 27017)
db = client.cross_language 
document = db['document']
paragraph = db['paragraph']
class NewsSpider(scrapy.Spider):
  name = "tech-industry"
  start_urls = [ "https://www.cnet.com/topics/tech-industry/"]

  def parse(self, response):
    source = "https://www.cnet.com"
    list_topic = response.xpath('//section[@id="topicListing"]/div')
    links =  list_topic[1].xpath('//div[@class = "row asset"]/div[@class="col-2 assetThumb"]/a/@href').extract()
    regex = r"\/news\/.*"
    list_news = [x for x in links if re.match(regex,x)]
    exist = False
    for i in list_news:
      if(document.find({"link": source + i}).count() > 0):
        exist = True
        break
      yield scrapy.Request(source + i, callback= self.importMongo)
    if(exist == False):
      next_url = ""
      if((source + "/topics/" + self.name + "/") == response.url):
        next_url = response.url + "2/"
      else: 
        next_url_arr = response.url.split("/")
        next_url_arr[-2] = str(int(next_url_arr[-2]) + 1)
        next_url = "/".join(next_url_arr)
      yield scrapy.Request(next_url, callback= self.parse)        

  def importMongo(self, response):
    # list_sentences = response.xpath('//article[@id="article-body"]/div[@class="col-7 article-main-body row"]/p/text()').extract()
    raw_paragraphs = response.xpath('//article[@id="article-body"]/div[@class="col-7 article-main-body row"]/p').extract()
    paragraphs = [re.sub(r"\<.*?\>", "", item) for item in raw_paragraphs]
    content = "".join(paragraphs)
    title = response.xpath('//div[@id="rbContent"]/div[@class="pageWrapper pageContainer current "]/div[@class="content-header"]/div[@class="hero-content"]/div[@class="container"]/div[@class="col-10 articleHead"]/h1/text()').extract()[0]
    link = response.url
    document_insert = document.insert_one({"title": title,"link": link,"content": content})
    temp = ""
    for item in paragraphs:
      temp += item + " "
      if(len(temp) > 35):
        paragraph.insert_one({"content": temp, "document_id": document_insert.inserted_id})
        temp = ""

