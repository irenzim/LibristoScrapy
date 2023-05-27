# This program allows for playing with xpaths extraction,
# and testing them for specific sites.
from scrapy import Selector
from urllib import request
import pandas as pd

url = 'https://www.libristo.pl/books-in-english/humanities.html'
html = request.urlopen(url)
sel = Selector(text=html.read(), type="html")

xpath = '//li/div[@class="LST_buy"]/div[1]/text()'
#print(sel.xpath(xpath).getall())


# Create an empty DataFrame with one column
links = pd.DataFrame(columns=['link'])

links['link'] = ['https://www.libristo.pl/books-in-english/humanities.html']
print(links)

