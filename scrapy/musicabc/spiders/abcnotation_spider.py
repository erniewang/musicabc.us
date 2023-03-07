from pathlib import Path
from hashlib import sha1

from scrapy.spiders import Spider
# from scrapy.linkextractors import LinkExtractor
from musicabc.items import MusicabcItem
from musicabc.db import Db

NUM_INDEX_PAGES = 1  # 1 for testing, 1758 for real
START_INDEX_PAGE = 0


class AbcnotationComSpider(Spider):
    name = "abcnotation_com"
    allowed_domains = ['abcnotation.com']
    start_urls = [
        'https://abcnotation.com/browseTunes?n={:04d}'.format(i)
        for i in range(START_INDEX_PAGE, START_INDEX_PAGE + NUM_INDEX_PAGES)
    ]

    def get_file_path(self, url) -> Path:
        a = url.split("?")[-1][2:]
        sha1ed = sha1(a.encode('utf-8')).hexdigest()
        return Path(f'save/{sha1ed}.html')

    def get_hash(self, url) -> Path:
        # get the part after 'tunePage?a='
        a = url.split("?")[-1][2:]
        sha1ed = sha1(a.encode('utf-8')).hexdigest()
        return sha1ed

    def sheet_exists(self, hash) -> bool:
        cur = Db.cur()
        cur.execute("""select * from sheets where id = %s;""", (hash,))
        return bool(cur.fetchone())

    def parse(self, response):
        for href in response.css("section > pre > a::attr(href)"):
            url = response.urljoin(href.extract())
            if not self.sheet_exists(self.get_hash(url)):
                yield response.follow(url, self.parse_item)

    def parse_item(self, response):
        id = self.get_hash(response.url)
        item = MusicabcItem(id=id, link=response.url)
        item['title'] = response.css('main > section > div.row > section > h4 ::text').extract_first()
        for a in response.css('main > section > div.row > section > div > a'):
            txt = a.css("::text").extract_first()
            link = response.urljoin(a.css("::attr(href)").extract_first())
            if txt == "abc":
                item['abc_link'] = link
            elif txt == "musicxml":
                item['musicxml_link'] = link
            elif txt == "midi":
                item['midi_link'] = link
        item['abc'] = response.css('main > section > div.row > section > pre ::text').extract_first()
        yield item
