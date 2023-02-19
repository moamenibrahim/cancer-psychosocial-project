import scrapy
from pathlib import Path
import os
import errno


class CancerSpider(scrapy.Spider):
    """
    RETRY_TIMES = 10
    RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]

    DOWNLOADER_MIDDLEWARES = {
        'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
        'scrapy_proxies.RandomProxy': 100,
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    }

    PROXY_LIST = '/home/feilz/workspace/cancerproject/bin/list.txt'
    """

    filenum = 0
    allowed_subwords = ["Terveys", "Paikkakunnat"]

    custom_settings = {
        'DOWNLOAD_DELAY': '0.75'
    }
    name = "cancer_spider"
    start_urls = ['https://keskustelu.suomi24.fi/haku?keyword=sy%C3%B6p%C3%A4']
    try:
        os.makedirs('scrapes')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    filePath = Path('./scrapes/')

    def parse(self, response):
        for thread in response.css('li.thread-list-item'):
            subcheck = thread.css(
                'div.thread-list-item-breadcrumb ::text').extract()
            if subcheck:
                subword = subcheck[0].split(">")[0].rstrip()
                if subword in self.allowed_subwords:
                    link = thread.css(
                        'a.thread-list-item-container ::attr(href)').extract_first()
                    yield response.follow(link, self.parseThread, subword)

        next_link = response.css('p.pagination').css(
            'a ::attr(href)').extract()[1]
        if next_link:
            yield response.follow(next_link, self.parse)

    def parseThread(self, response, subword):
        filenum += 1
        filename = subword+filenum+'.txt'
        f = open(filepath/filename, 'w')
        datastore = {}
        datastore['title'] = response.css(
            'h1.thread-header ::text').extract_first().strip()
        datastore['timestamp'] = response.css(
            'div.user-info-big.p.user-info-timestamp ::text').extract_first().strip()
        datastore['user'] = response.css(
            'div.user-info-big.p.user-info-name ::text').extract_first().strip()
        datastore['thread-body'] = response.css(
            'div.thread-text ::text').extract_first().strip()
        datastore['answers'] = {}
        for answer in response.css('div.answer-container'):
            answer = {}
            answer['answer-body'] = answer.css(
                'div.answer-text ::text').extract_first().strip()
            answer['timestamp'] = answer.css(
                'p.user-info-timestamp ::text').extract_first().strip()
            answer['user'] = answer.css(
                'p.user-info-name ::text').extract_first().strip()
            answer['comments'] = {}
            if response.css('div.comments-list'):
                for comment in response.css('div.comment'):
                    comment = {}
                    comment['comment-body'] = comment.css(
                        'div.comment-text ::text').extract_first().strip()
                    comment['timestamp'] = comment.css(
                        'p.user-info-timestamp ::text').extract_first().strip()
                    comment['user'] = comment.css(
                        'p.user-info-name ::text').extract_first().strip()
                    answer['comments'].append(comment)
            datastore['answers'].append(answer)
        f.write(datastore)
        f.close()
