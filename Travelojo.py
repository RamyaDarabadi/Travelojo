from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
import MySQLdb

class Travelojo_Spider(BaseSpider):
    name = 'travelojo'
    start_urls = ['http://www.travelojo.in/India-tour.html']
    
    def __init__(self, *args, **kwargs):
        self.conn = MySQLdb.connect(host="localhost", user="root", passwd='01491a0237db', db="travelojodb", charset='utf8', use_unicode=True)
        self.cur = self.conn.cursor()

    def parse(self, response):
        sel = Selector(response)
        nodes = sel.xpath('//div[@class="container"]/div[@class="banner-bottom-grids"]//div[@class="col-md-4 weekend-grids"]/div[@class="weekend-grid"]//div[@class="weekend-grid-info"]//h6[@class="package_h6"]')
        for node in nodes:
            title = "".join(node.xpath('./a/text()').extract())
            price = "".join(node.xpath('./a/i[@class="price"]').extract())
            link =  "".join(node.xpath('./a/@href').extract())
            qry = 'insert into travel(title, link, price) values (%s,%s, %s)on duplicate key update title = %s'
            values = (title ,link, price,title)
            print qry%values
            self.cur.execute(qry, values)
            self.conn.commit()                                                       
