# -*- coding: utf-8 -*-
import scrapy
from fang.items import NewHouseItem,ESFHouseItem
import re

class FangtianxiaSpider(scrapy.Spider):
    name = 'fangtianxia'
    allowed_domains = ['fang.com']
    start_urls = ['http://www.fang.com/SoufunFamily.htm']
    def parse(self, response):
        trs = response.xpath('//div[@class="outCont"]//tr[@id]')
        province_name = None
        for tr in trs:
            province = tr.xpath('./td[not(@class)]/strong/text()').get("")
            if province == "其它":
                continue
            if province and province != " ":
                province_name = province
            city_tds = tr.xpath('./td[last()]/a')
            for city in city_tds:
                city_name = city.xpath('./text()').get()
                city_url = city.xpath('./@href').get()

                if "bj." in city_url:
                    new_house_url = "http://newhouse.fang.com/house/s/"
                    esf_house_url = "http://esf.fang.com/"
                else:
                    house_url = city_url.split("//")
                    new_house_url = house_url[0] + "//newhouse."+house_url[1]+"/house/s/"
                    esf_house_url = house_url[0]+"//esf."+house_url[1]

                yield scrapy.Request(url=new_house_url, callback=self.parse_new_house, meta = {"info":(province_name, city_name)})
                yield scrapy.Request(url=esf_house_url, callback=self.parse_esf_house, meta={"info": (province_name, city_name)})

    def parse_new_house(self, response):
        province, city = response.meta.get('info')
        lis = response.xpath('//div[@id="newhouse_loupai_list"]/ul/li[not(@class)]')
        for li in lis:
            name = li.xpath('.//div[@class="nlcd_name"]/a/text()').get("").strip()
            number = li.xpath('.//div[@class="nhouse_price"]/span/text()').get("")
            per = li.xpath('.//div[@class="nhouse_price"]/em/text()').get("")
            price = number+per
            rooms = ",".join(li.xpath('.//div[@class="house_type clearfix"]/a/text()').getall())
            area = ",".join(li.xpath('.//div[@class="house_type clearfix"]/text()').getall())
            try:
                area = re.search("\d+.*米",area).group()
            except Exception:
                area = ""
            address = li.xpath('//div[@class="address"]/a/@title').get()
            district = ",".join(li.xpath('.//div[contains(@class,"fangyuan")]/a//text()').getall())
            sale = li.xpath('.//div[contains(@class,"fangyuan")]/span/text()').get()
            origin_url = response.url
            item = NewHouseItem(province = province,city = city,name = name,price = price,rooms = rooms,\
                                area = area,address = address,district = district,sale = sale,origin_url = origin_url)
            yield item
        next_page = response.xpath('//a[@class="next"]/@href').get()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse_new_house, meta={"info":(province, city)})

    def parse_esf_house(self, response):
        province, city = response.meta.get('info')
        dls = response.xpath('//div[@class="houseList"]/dl')
        for dl in dls:
            name = dl.xpath('.//p[@class="title"]/a/@title').get()
            describe = dl.xpath('.//p[@class="mt12"]/text()').getall()
            try:
                rooms = describe[0].strip()
            except Exception:
                rooms = ""
            try:
                floor = describe[1].strip()
            except Exception:
                floor = ""
            try:
                toward = describe[2].strip()
            except Exception:
                toward = ""
            try:
                year = describe[3].strip().split("：")[1]
            except Exception:
                year = ""
            address = dl.xpath('.//p[@class="mt10"]/span/@title').get()
            area = dl.xpath('.//div[contains(@class,"area")]/p/text()').get()
            price = "".join(dl.xpath('.//div[@class="moreInfo"]/p/span/text()').getall()[0:2])
            unit = "".join(dl.xpath('.//div[@class="moreInfo"]/p[last()]//text()').getall())
            origin_url = response.url
            item = ESFHouseItem(province=province,city=city,name=name,rooms=rooms,floor=floor,toward=toward,\
                                year=year,address=address,area=area,price=price,unit=unit,origin_url=origin_url)
            yield item
        next_page = response.xpath('//a[@id="PageControl1_hlk_next"]/@href').get()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page),callback=self.parse_esf_house, meta = {"info":(province, city)})

