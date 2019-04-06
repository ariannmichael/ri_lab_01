# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class BrasilElpaisSpider(scrapy.Spider):
    name = 'brasil_elpais'
    allowed_domains = ['brasil.elpais.com']
    start_urls = []

    def __init__(self, *a, **kw):
        super(BrasilElpaisSpider, self).__init__(*a, **kw)
        with open('seeds/brasil_elpais.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())


    def parse_urls(self, response):
        for artigo in response.css('div.articulo__interior'):
            url = artigo.css('h2.articulo-titulo a::attr(href)').get()
            url = 'https:' + str(url)
            yield response.follow(url, callback=self.parse_content)
            
    def parse(self, response):
        
        yield response.follow(response.url, callback=self.parse_urls)
    
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        
    def parse_content(self, response):
        for item in response.css('div.contenedor'):
            title = str(item.css('h1.articulo-titulo::text').get().encode('utf-8'))
            

            yield {
                'title': title
            }

            
