# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from musicabc.db import Db


class MusicabcPipeline:

    def process_item(self, item, spider):
        for field in item.fields:
            item.setdefault(field, None)

        Db.cur().execute("""
            insert into sheets (id, link, title, abc, abc_link, musicxml_link, midi_link)
            values (%s,%s,%s,%s,%s,%s,%s);""", (
                item['id'],
                item['link'],
                item['title'],
                item['abc'],
                item['abc_link'],
                item['musicxml_link'],
                item['midi_link']
            )
        )
        Db.conn().commit()
        return item

    def close_spider(self, spider):
        Db.conn().close()
