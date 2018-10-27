# -*- coding: utf-8 -*-
import scrapy


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['yorkshire.com']
    start_urls = ['https://www.yorkshire.com/accommodation/listings']

    def parse(self, response):
        urls = response.xpath('//article[@class="block block--blue block--hasimage"]/a[@class="block__link"]/@href').extract()
        for url in urls:
            full_url = response.urljoin(url)
            yield scrapy.Request(full_url, callback=self.individual_page)
        # Calling next page
        next_page_url = response.xpath('//a[@class="button button--blue button--chevronr "]/@href').extract_first()
        yield scrapy.Request(next_page_url, callback=self.parse)

    def individual_page(self, response):
        url = response.url
        name = response.xpath('//h1[@class="heading--primary"]/a/text()').extract_first().strip()
        description = response.xpath('//div[@class="description"]/p/text()').extract_first()
        address = response.xpath('//p[@class="location blue"]/text()').extract_first().strip()
        website = response.xpath('//a[@class="button button--chevronr outgoing-link button--blue"]/@href').extract_first()

        fields = dict(name=name, description=description, address=address, website=website, url=url)

        yield fields