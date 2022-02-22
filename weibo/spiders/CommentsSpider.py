import json
import re
import scrapy
from gerapy_pyppeteer import PyppeteerRequest
from weibo.items import WeiboItem, CommentUserItem


class CommentsspiderSpider(scrapy.Spider):
    name = 'CommentsSpider'
    allowed_domains = ['m.weibo.cn']
    weibo_url = 'https://m.weibo.cn/detail'
    comment_url = 'https://m.weibo.cn/comments/hotflow?id='
    weibos_id = ['4732124995783072']

    custom_settings = {
        'ITEM_PIPELINES': {
            'weibo.pipelines.CommentTextPipeline': 300,
        }
    }

    def start_requests(self):
        for weibo_id in self.weibos_id:
            yield PyppeteerRequest(f'{self.weibo_url}/{weibo_id}',
                                   callback=self.parse_weibo, wait_for='.f-weibo.card9.m-panel',
                                   meta={'weibo_id': weibo_id})
            yield scrapy.Request(f'{self.comment_url}{weibo_id}&mid={weibo_id}',
                                 callback=self.parse_comments, meta={'weibo_id': weibo_id})

    def parse_weibo(self, response):
        weibo_id = response.meta.get('weibo_id')
        text = response.css('.card9 .weibo-main .weibo-text::text, .card9 .weibo-main a span::text').extract()
        raw_text = ''.join(text)
        pics = response.css('.f-bg-img[data-v-bc38ac84]::attr(src), .m-img-box img::attr(src)').extract()
        info = response.css('.lite-page-tab .tab-item i::text').extract()
        reposts_count = info[1]
        comments_count = info[3]
        attitudes_count = info[5]
        weibo_item = WeiboItem()
        weibo_item['weibo_id'] = weibo_id
        weibo_item['text'] = raw_text
        weibo_item['pics'] = pics
        weibo_item['reposts_count'] = reposts_count
        weibo_item['comments_count'] = comments_count
        weibo_item['attitudes_count'] = attitudes_count
        yield weibo_item

    def parse_comments(self, response):
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('data'):
            comments = result.get('data').get('data')
            for comment in comments:
                comment_user_info = comment.get('user')
                comment_item = CommentUserItem()

                comment_item['weibo_id'] = response.meta.get('weibo_id')
                comment_item['comment_text'] = comment.get('text')
                comment_item['like_count'] = comment.get('like_count')

                comment_item['user_id'] = comment_user_info.get('id')
                comment_item['name'] = comment_user_info.get('screen_name')
                comment_item['avatar'] = comment_user_info.get('avatar_hd')
                comment_item['cover'] = comment_user_info.get('cover_image_phone')
                comment_item['gender'] = comment_user_info.get('gender')
                comment_item['description'] = comment_user_info.get('description')
                comment_item['fans_count'] = comment_user_info.get('followers_count')
                comment_item['follows_count'] = comment_user_info.get('follow_count')
                comment_item["weibos_count"] = comment_user_info.get('statuses_count')
                if comment_user_info.get('verified') == 'false':
                    comment_item['verified'] = comment_user_info.get('verified')
                    comment_item['verified_reason'] = 'None'
                else:
                    comment_item['verified'] = comment_user_info.get('verified')
                    comment_item['verified_reason'] = comment_user_info.get('verified_reason')
                comment_item['verified_type'] = comment_user_info.get('verified_type')

                yield comment_item

        if result.get('data').get('max_id'):
            max_id = result.get('data').get('max_id')
            max_id_type = result.get('data').get('max_id_type')
            weibo_id = response.meta.get('weibo_id')
            yield scrapy.Request(
                f'{self.comment_url}{weibo_id}&mid={weibo_id}&max_id={max_id}&max_id_type={max_id_type}',
                callback=self.parse_comments, meta={'weibo_id': weibo_id})