import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import DanskebanknoItem
from itemloaders.processors import TakeFirst


class DanskebanknoSpider(scrapy.Spider):
	name = 'danskebankno'
	start_urls = ['https://danskebank.com/no/nyheter-og-presse']

	def parse(self, response):
		post_links = response.xpath('//ul[@class="listing"]/li/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath(
			'//p[@class="article-subheadline"]/text()|//div[@class="article"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="article-meta"]/text()').get()
		if date:
			date = re.findall(r'\d+.\s[a-z]+.\s\d{4}', date)

		item = ItemLoader(item=DanskebanknoItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
