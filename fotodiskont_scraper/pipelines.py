# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class FotodiskontScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Price convert to float
        price_value = adapter.get("price")
        if price_value and price_value != "Kontakt za cenu":
            price_value = price_value.replace("RSD", "").replace(".", "").strip()
            adapter["price"] = float(price_value)
        else:
            adapter["price"] = None

        # Add full url
        relative_url = adapter.get("url")
        if relative_url:
            adapter["url"] = "https://fotodiskont.rs" + relative_url

        return item
