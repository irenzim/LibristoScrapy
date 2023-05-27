import scrapy
import pandas as pd
from timeit import default_timer as timer

start = timer()

page_limit = True

class Book(scrapy.Item):
    title = scrapy.Field()
    author_year = scrapy.Field()
    lang = scrapy.Field()
    cover = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    discount = scrapy.Field()


class LibristoSpider(scrapy.Spider):
    name = "bookSpider"
    allowed_domains = ["www.libristo.pl"]
    start_urls = ["http://www.libristo.pl/"]

    try:
        with open("links.csv", "rt") as f:
            start_urls= [url.strip() for url in f.readlines()][1:]
            print('Category links to be crawled:', start_urls)
    except: 
        start_urls = []

    def __init__(self): 
        self.books = []
    
    def parse(self, response):
        b = Book()

        title_xpath = '//div[@class = "LST_inf"]/h3/a/text()'
        author_year_xpath = '//div[@class = "LST_inf"]/h4/text()'
        lang_xpath = '//div[@class = "LST_inf"]/p[1]/text()'
        cover_xpath = '//div[@class = "LST_inf"]/p[2]/text()'
        link_xpath = '//div[@class = "LST_inf"]/h3/a//@href'
        price_xpath = '//div[@class = "LST_buy"]/p/strong/text()'
        discount_xpath = '//li/div[@class="LST_buy"]/div[1]/text()'

        title = response.xpath(title_xpath).getall()
        author_year = response.xpath(author_year_xpath).getall()
        lang = response.xpath(lang_xpath).getall()
        cover = response.xpath(cover_xpath).getall()
        link = response.xpath(link_xpath).getall()
        price = response.xpath(price_xpath).getall()
        discount = response.xpath(discount_xpath).getall()
        
        self.books.extend(list(zip(title, author_year, lang, cover, link, price, discount)))

        b['title'] = response.xpath(title_xpath).getall()
        b['author_year'] = response.xpath(author_year_xpath).getall()
        b['lang'] = response.xpath(lang_xpath).getall()
        b['cover'] = response.xpath(cover_xpath).getall()
        b['link'] = response.xpath(link_xpath).getall()
        b['price'] = response.xpath(price_xpath).getall()
        b['discount'] = response.xpath(discount_xpath).getall()

        yield b

    def closed(self, reason):
        # Create a DataFrame using the scraped data
        df = pd.DataFrame(self.books, columns=['Title', 'Author/Year', 'Language', 'Cover', 'Link', 'Price', 'Discount'])

        # Save the DataFrame to a CSV file without the index column
        df.to_csv('book_data.csv', index=False)

        

end = timer()
print(end - start)



