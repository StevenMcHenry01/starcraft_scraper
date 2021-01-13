import scrapy
import re


class LeaderboardSpider(scrapy.Spider):
    name = "leaderboard_spider"

    start_urls = [
        "https://www.rankedftw.com/ladder/lotv/1v1/mmr/"
    ]

    def get_region(self, region_img_name):
        attr_string = region_img_name.css('img::attr(srcset)').get()
        return re.search('regions/(.*)-16', attr_string).group(1)

    def get_league(self, league_img_name):
        attr_string = league_img_name.css('img::attr(src)').get()
        return re.search('leagues/(.*)-128', attr_string).group(1)

    def get_race(self, race_img_name):
        attr_string = race_img_name.css('img::attr(src)').get()
        return re.search('races/(.*).svg', attr_string).group(1)

    def parse(self, response):
        data_array = []
        for row in response.css('a.row'):
            # print(row.css('div')[1].get())
            data_array.append({
                'rank': int(row.css('div::text')[0].get()),
                'region': self.get_region(row.css('div')[1]),
                'league': self.get_league(row.css('div')[2]),
                'race': self.get_race(row.css('div')[4]),
                'name': row.css('div')[4].css('span::text').get(),
                'mmr': int(row.css('div::text')[5].get()),
                'points': int(row.css('div::text')[6].get()),
                'wins': int(row.css('div::text')[7].get()),
                'losses': int(row.css('div::text')[8].get()),
                'games_played': int(row.css('div::text')[9].get()),
                'win_rate': row.css('div::text')[10].get(),
            })
        print(data_array)
        next_page = response.urljoin(response.css('ul.pagination li')[
                                     1].css('a::attr(href)').get())
        yield scrapy.Request(next_page, callback=self.parse)
