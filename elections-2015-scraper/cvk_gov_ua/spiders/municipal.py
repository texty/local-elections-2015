# -*- coding: utf-8 -*-
from cvk_gov_ua.items import Municipal
from base import BaseSpider

class MunicipalSpider(BaseSpider):
    name = "municipal"

    def start_requests(self):
      initial_urls = [
        'PVM002?PT001F01=100&pt00_t001f01=100'
      ]

      for url in initial_urls:
        yield self.build_request(url, self.findRegionUrls)

    def findRegionUrls(self, response):
      for row in response.css("#result table.t2")[1].css("tr")[1:]:
        region_urls = row.css("td")[4].css("a").xpath("@href").extract()
        for region_url in region_urls:
          yield self.build_request(region_url, self.findMunicipalUrls)

    def findMunicipalUrls(self, response):
      for url in response.css(".a1").xpath('@href').extract():
        yield self.build_request(url, self.parseMunicipalList)

    def parseMunicipalList(self, response):
        council = response.css(".p2::text")[0].extract()
        for row in response.css("#result table.t2")[2].css("tr")[1:]:
          result = row.css("td::text")[1].extract()
          party = row.css("a::text")[0].extract()
          yield Municipal(result=result,
                               party=party,
                               council=council)
