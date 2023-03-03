# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class MusicabcItem(Item):
    id = Field()
    title = Field()
    link = Field()
    abc = Field()
    abc_link = Field()
    musicxml = Field()
    musicxml_link = Field()
    has_midi = Field()
    midi_link = Field()
