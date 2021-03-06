import scrapy
import pymongo
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy import Request
from snap.items import SnaptItem
from snap.items import SnapdealItem
from time import gmtime, strftime
import sys
class SnapSpider(BaseSpider):
    name = "snap"
    global client
    client=MongoClient()
    global db
    db=client.my_db
    global coll
    global slug
    global cat
    slug=''
    cat=''
    for arg in sys.argv: 1
    ass=arg.split('=')
    asd=ass[1].replace('"',"")
    args=asd.split(',')
    slug=args[0]
    cat=args[1]
    coll=db.crawl_data
    print slug
    print cat
    price=''
    image=''
    c=0
    d=50
    url = "www.snapdeal.com/acors/json/product/get/search/"+slug+"/"+str(c)+"/"+str(d)+"?q=&sort=soldout&keyword=&clickSrc=&viewType=List&lang=en&snr=false"
    r  = requests.get("http://" +url)
    data = r.text
    soup = BeautifulSoup(data)
    count=''
    counts=soup.findAll("div", { "class" : "numberFound" })
    for bount in counts:
        count=bount.get_text()
    start_urls=[]
    count=int(count)
    
    allowed_domains = ["www.snapdeal.com"]
    while d<=count:
        url="http://www.snapdeal.com/acors/json/product/get/search/"+slug+"/"+str(c)+"/"+str(d)+"?q=&sort=soldout&keyword=&clickSrc=&viewType=List&lang=en&snr=false"
        start_urls.append(url)
        c=d
        d=d+50
    def chunks(self,l, n):
     n = max(1, n)
     return [l[i:i + n] for i in range(0, len(l), n)]
    def parse(self, response):
       zv=[]
       hxs=HtmlXPathSelector(response)
       item = SnaptItem()
       item ['product_name'] = hxs.select('//p[@class="product-title"]/text()').extract()
       item ['price']=hxs.select("//div[contains(@class, 'product_grid_cont')]/@price").extract()
       item ['url']=hxs.select("//div[contains(@class, 'product-image')]/a/@href").extract()
       item ['image']=hxs.select("//img[contains(@class, 'gridViewImage')]/@src").extract()
       item ['excerpts']=hxs.select("//ul[contains(@id, 'highLights')]/li/text()").extract()
       y=len(item ['product_name'])
       v=item ['excerpts']
       zv=self.chunks(v,5)
       for i in range(0,y):
           print item ['product_name'][i]
           print item ['price'][i]
           print item ['url'][i]
           print item ['image'][i]
           request =  Request(item ['url'][i],  callback = self.parse_statdetail)
           yield request
           
        
           try:
            print zv[i]
           except:
             pass
    def parse_statdetail(self, response):
       hxs=HtmlXPathSelector(response)
       title= hxs.select("//div[contains(@class, 'comp-product-description')]")
       decsi= hxs.select('//*[@class="detailssubbox"]')
       item = SnapdealItem()
       item ['product_name'] = title.select("//h1[contains(@itemprop, 'name')]/text()").extract()
       item ['desc']=decsi.select('.//p/text()').extract()
       item ['specs']=decsi.select('.//table[@class="product-spec"]/tr/td//text()').extract()
       item['price']=hxs.select("//input[contains(@id, 'productPrice')]/@value").extract()
       item['cod']=hxs.select("//input[contains(@id, 'codValidOnCategory')]/@value").extract()
       item['sold_out']=hxs.select("//input[contains(@id, 'soldOut')]/@value").extract()
       item['prebook']=hxs.select("//input[contains(@id, 'prebook')]/@value").extract()
       item['rating']=hxs.select("//input[contains(@id, 'avgRating')]/@value").extract()
       item['rating_count']=hxs.select("//input[contains(@id, 'noOfRatings')]/@value").extract()
       item['image']=hxs.select("//img[contains(@itemprop, 'image')]/@src").extract()
       item['images']=hxs.select("//ul[contains(@id, 'bx-slider-left-image-panel')]/li/img/@src").extract()
       item['offer_texts']=hxs.select(".//span[contains(@class, 'offer-title')]/text()").extract()
       item['offer_codes']=hxs.select(".//div[contains(@class, 'offerHeadBox')]/@title").extract()
       item['excerpts']=hxs.select("//div[contains(@class, 'pdp-e-i-keyfeatures')]/ul/li/@title").extract()
       item ['url'] = response.url
       coll.insert({"product":item['product_name'][0],"price":item['price'][0],"desc":item['desc'],"specs":item['specs'],"store":"snapdeal","url":item['url'],"image":item['image'][0],"images":item['images'],"cod":item['cod'][0],"sold_out":item['sold_out'][0],"prebook":item['prebook'][0],"rating":item['rating'][0],"rating_count":item['rating_count'][0],"offer_texts":item['offer_texts'],"offer_codes":item['offer_codes'],"category":cat,"excerpts":item['excerpts']})
       yield item        
db.crawl_log.insert({"text":"Finished Crawling Snapdeal - " + cat,"time":strftime("%Y-%m-%d %H:%M:%S", gmtime())})
