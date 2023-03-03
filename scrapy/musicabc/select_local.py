import sys
from scrapy import Selector

if len(sys.argv) < 2:
    print("Usage: python select_local.py <path_to_html_file>")
    exit(1)

f = open(sys.argv[1], 'r', encoding='utf-8-sig', newline='')
page = f.read()
data = Selector(text=str(page))
