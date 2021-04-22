import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from muamalat.items import Article


class muamalatSpider(scrapy.Spider):
    name = 'muamalat'
    start_urls = ['https://www.muamalat.com.my/press-release-archive/']

    def parse(self, response):
        articles = response.xpath('//div[@class="card mb-0"]')
        for article in articles:
            item = ItemLoader(Article())
            item.default_output_processor = TakeFirst()

            title = article.xpath('.//span[@class="press_release_title mb-0"]/text()').get()
            if title:
                title = title.strip()

            date = article.xpath('.//span[@class="press_release_date mb-0"]/text()').get()
            if date:
                date = " ".join(date.split())

            content = article.xpath('./div[@id]/p//text()').getall()
            content = [text.strip() for text in content if text.strip() and '{' not in text]
            content = " ".join(content).strip()

            item.add_value('title', title)
            item.add_value('date', date)
            item.add_value('content', content)

            yield item.load_item()



