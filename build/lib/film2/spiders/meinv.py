# -*- coding: utf-8 -*-
import scrapy


class MeinvSpider(scrapy.Spider):
    name = 'meinv'
    allowed_domains = ['meinv.com']
    start_urls = ['http://tuku.piaoliang.com/mm/list_1_1.html']

    def parse(self, response):
        urls = response.xpath('//a[re:test(@href,"http://tuku.piaoliang.com/mm/\d+/")]/@href')
        for url in urls:
            # print(url.extract())
            yield scrapy.Request(url=url.extract(), dont_filter=True, method='GET', callback=self.parse_part2)


        next_page = response.xpath('//div[@class="dede_pages3"]/ul[@class="pagelist"]/li/a[text()="下一页"]/@href').extract_first()
        print(next_page)
        # print(next_page,response.url,'12312312312313221312')
        if next_page is not None:
            next_url="http://tuku.piaoliang.com/mm/%s"%next_page
            print(next_url)
            yield scrapy.Request(url=next_url,dont_filter=True, method='GET', callback=self.parse)


    def parse_part2(self, response):
        imgurl = response.xpath('//div[@class="imgbox"]/img/@src').extract_first()
        name = response.xpath('//div[@class="info"]/h1/text()').extract_first()
        # print(imgurl,'-------')
        next_page = response.xpath('//div[@class="dede_pages"]/ul[@class="pagelist"]/li/a[text()="下一页"]/@href').extract_first()
        # if next_page is not None:
        #     temp=str(response.url).split('index')[0]
        #     next_url=temp+next_page
        #     # print(next_url,'----------')
        #     yield scrapy.Request(url=next_url, dont_filter=True, method='GET', callback=self.parse_part2)

        min_img=str(imgurl).split('piaoliang.com')[-1] #/uploads/allimg/180118/2-1P11R03612.jpg
        fin_img_url='http://tuku.piaoliang.com'+min_img
        # print(fin_img_url,name)
        from ..items import MeinvItem
        obj = MeinvItem(name=name, url=fin_img_url)
        yield obj

