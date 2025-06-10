import scrapy
from fotodiskont_scraper.items import FotodiskontItem


class FotodiskontSpider(scrapy.Spider):
    name = "fotodiskont"
    allowed_domains = ["fotodiskont.rs"]
    start_urls = ["https://fotodiskont.rs/"]

    def parse(self, response):
        category_links = response.css("ul.dropdown-menu a.dropdown-item::attr(href)").getall()
        for link in category_links:
            yield response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        subcategory_links = response.css("div.category-wrapper-grid a::attr(href)").getall()

        if subcategory_links:
            for link in subcategory_links:
                yield response.follow(link, callback=self.parse_category)
        else:
            category = response.css("h1::text").get()
            category = category.strip() if category else "Неизвестно"
            products = response.css("div.col-xs-6.col-sm-4")

            for product in products:
                item = FotodiskontItem()
                item["category"] = category
                item["title"] = product.css("span.vsCMS3compareButton::attr(data-producttitle)").get()
                item["url"] = product.css(".product-title a::attr(href)").get()
                item["price"] = product.css("div.product-price span.price::text").get()
                yield item

            next_page = response.xpath('//a[span/img[@src="/design/pagination-arrow-right.png"]]/@href').get()
            if next_page:
                yield response.follow(next_page, callback=self.parse_category)
