import scrapy



class CancerSpider(scrapy.Spider):
    allowed_subwords=["Terveys","Paikkakunnat"]
    name="cancer_spider"
    start_urls=['https://keskustelu.suomi24.fi/haku?keyword=sy%C3%B6p%C3%A4']

    def parse(self, response):
        for thread in response.css('li.thread-list-item'):
            subcheck = thread.css('div.thread-list-item-breadcrumb ::text').extract()
            if subcheck:
                subword = subcheck[0].split(">")[0].rstrip()
                if subword in self.allowed_subwords:
                        link = thread.css('a.thread-list-item-container ::attr(href)').extract_first()
                        yield {
                            'subword': subword
                        }
                        yield response.follow(link,self.parseThread)

        next_link=response.css('p.pagination').css('a ::attr(href)').extract()[1]
        if next_link:
            yield response.follow(next_link,self.parse)

    def parseThread(self,response):
        yield {
            'title': response.css('h1.thread-header ::text').extract_first(),
            'timestamp': response.css('div.user-info-big.p.user-info-timestamp ::text').extract_first(),
            'user': response.css('div.user-info-big.p.user-info-name ::text').extract_first(),
            'thread-body': response.css('div.thread-text ::text').extract_first(),
        }
        for answer in response.css('div.answer-container'):
            yield {
                'user': answer.css('p.user-info-name ::text').extract_first(),
                'timestamp': answer.css('p.user-info-timestamp ::text').extract_first(),
                'answer-body': answer.css('div.answer-text ::text').extract_first()
            }
            if response.css('div.comments-list'):
                for comment in response.css('div.comment'):
                    yield {
                        'user' : comment.css('p.user-info-name ::text').extract_first(),
                        'timestamp': comment.css('p.user-info-timestamp ::text').extract_first(),
                        'comment-body': comment.css('div.comment-text ::text').extract_first()
                    }
