
# -*- coding: utf-8 -*-
import scrapy
import json

import pdb
from datetime import datetime

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



    def parse(self, response):

        yield response.follow(response.url, callback=self.parse_urls)

        
        page = response.url.split("/")[-2]
        filename = 'quotes-page-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


    def parse_urls(self, response):

        for artigo in response.css('div.articulo__interior'):
            href = artigo.css('h2.articulo-titulo a::attr(href)').get()
            href = 'https:' + str(href)

            yield response.follow(href, callback=self.parse_content)     
   
    def parse_content(self, response):

        
        for content in response.css('div.contenedor'):
                        
            date = content.css('div.articulo-datos time::attr(datetime)').get()
            date = date[:-6]
            date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
            date = datetime.strftime(date,'%d/%m/%Y %H:%M:%S')

            text = content.css('div.articulo__contenedor p *::text').getall()
            text = "".join(text).replace(',', '').replace('\n', ' ')

            url = response.request.url
            
            section = str(url.split("/")[-2])

            
            yield {
                'title': str(content.css('h1.articulo-titulo::text').get().encode('utf-8')).replace(',', '').replace('\n', ' '),
                'sub_title': content.css('div.articulo-subtitulos h2.articulo-subtitulo::text').get().replace(',', '').replace('\n', ' '),
                'author': str(content.css('div.firma div.autor div.autor-texto span.autor-nombre a::text').get().encode('utf-8')).replace(',', '').replace('\n', ''),
                'date': date,
                'section': section,
                'text': text,
                'url': url                  
            }