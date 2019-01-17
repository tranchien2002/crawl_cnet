#  -*- codiing:  utf-8 -*-
import scrapy
import pdb
import re
import os.path
class NewsSpider(scrapy.Spider):
  name = "tech-industry"
  source = "https://www.cnet.com/topics/tech-industry/"
  start_urls = [ source + str(i + 1) + "/" for i in range(200)]

  def parse(self, response):
    source = "https://www.cnet.com"
    list_topic = response.xpath('//section[@id="topicListing"]/div')
    links =  list_topic[1].xpath('//div[@class = "row asset"]/div[@class="col-2 assetThumb"]/a/@href').extract()
    regex = r"\/news\/.*"
    list_news = [x for x in links if re.match(regex,x)]
    for i in list_news:
      yield scrapy.Request(source + i, callback= self.saveFile)

  def saveFile(self, response):
    save_path = '/home/tmc/Documents/NLP/cross_language/tech/cnet_en'
    list_sentences = response.xpath('//article[@id="article-body"]/div[@class="col-7 article-main-body row"]/p/text()').extract()
    doc = "".join(list_sentences)
    title = str(response).split("/")[-2]
    completeName = os.path.join(save_path, title + ".txt")
    file = open(completeName, "w")
    file.write(doc.encode("utf-8"))
    file.close()
