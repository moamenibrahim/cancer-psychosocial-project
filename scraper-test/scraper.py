import scrapy
from pathlib import Path


class CancerSpider(scrapy.Spider):
    filenum = 0
    allowed_subwords=["Terveys","Paikkakunnat"]
    custom_settings={
        'DOWNLOAD_DELAY':'0.75'
    }
    name="cancer_spider"
    start_urls=['https://keskustelu.suomi24.fi/haku?keyword=sy%C3%B6p%C3%A4']
    filePath = Path('./scrapes/')

    def parse(self, response):
        for thread in response.css('li.thread-list-item'):
            subcheck = thread.css('div.thread-list-item-breadcrumb ::text').extract()
            if subcheck:
                subword = subcheck[0].split(">")[0].rstrip()
                if subword in self.allowed_subwords:
                        link = thread.css('a.thread-list-item-container ::attr(href)').extract_first()
                        yield response.follow(link,self.parseThread,subword)

        next_link=response.css('p.pagination').css('a ::attr(href)').extract()[1]
        if next_link:
            yield response.follow(next_link,self.parse)

    def parseThread(self,response,subword):
        filenum+=1
        filename=subword+filenum+'.txt'
        f = open(filepath/filename,'w')
        datastore={}
        datastore['title']=response.css('h1.thread-header ::text').extract_first()
        datastore['timestamp']=response.css('div.user-info-big.p.user-info-timestamp ::text').extract_first()
        datastore['user']=response.css('div.user-info-big.p.user-info-name ::text').extract_first()
        datastore['thread-body']=response.css('div.thread-text ::text').extract_first()
        datastore['answers']={}
        for answer in response.css('div.answer-container'):
            answer={}
            answer['answer-body']=answer.css('div.answer-text ::text').extract_first()
            answer['timestamp']=answer.css('p.user-info-timestamp ::text').extract_first()
            answer['user']=answer.css('p.user-info-name ::text').extract_first()
            answer['comments']={}
            if response.css('div.comments-list'):
                for comment in response.css('div.comment'):
                    comment={}
                    comment['comment-body']=comment.css('div.comment-text ::text').extract_first()
                    comment['timestamp']=comment.css('p.user-info-timestamp ::text').extract_first()
                    comment['user']=comment.css('p.user-info-name ::text').extract_first()
                    answer['comments'].append(comment)
            datastore['answers'].append(answer)
        f.write(datastore)
        f.close()
