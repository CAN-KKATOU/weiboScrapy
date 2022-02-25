import json
import scrapy
from weibo.items import WeiboListItem


class WeibospiderSpider(scrapy.Spider):
    name = 'WeiboSpider'
    allowed_domains = ['m.weibo.cn']
    weibo_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={user_id}&containerid=107603{user_id}'
    start_users = ['1627500245']

    custom_settings = {
        'ITEM_PIPELINES': {
            'weibo.pipelines.WeiboTextPipeline': 300,
            'weibo.pipelines.MongoDBPipeline': 301,
        }
    }

    def start_requests(self):
        for uid in self.start_users:
            yield scrapy.Request(f'{self.weibo_url}{uid}&containerid=107603{uid}', callback=self.parse_weibo_list,  meta={'uid': uid})

    def parse_weibo_list(self, response):
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards') \
                and len(result.get('data').get('cards')):
            weibos = result.get('data').get('cards')
            for weibo in weibos:
                if weibo.get('mblog'):
                    weiboItem = WeiboListItem()
                    weibo = weibo.get('mblog')

                    weiboItem['user_id'] = weibo.get('user').get('id')
                    weiboItem['user_name'] = weibo.get('user').get('screen_name')
                    weiboItem['weibo_id'] = weibo.get('id')
                    # 是否转发
                    if weibo.get('repost_type') == 1:
                        weiboItem['is_repost'] = 'true'
                        weiboItem['text'] = weibo.get('raw_text')
                    else:
                        weiboItem['is_repost'] = 'false'
                        weiboItem['text'] = weibo.get('text')
                    # 微博是否有图片
                    if weibo.get('pics'):
                        urls = weibo.get('pics')
                        pics = []
                        for url in urls:
                            url = url.get('large').get('url')
                            pics.append(url)
                        weiboItem['pics'] = pics
                    else:
                        weiboItem['pics'] = ''

                    weiboItem['reposts_count'] = weibo.get('reposts_count')
                    weiboItem['comments_count'] = weibo.get('comments_count')
                    weiboItem['attitudes_count'] = weibo.get('attitudes_count')
                    yield weiboItem

        if result.get('ok') and result.get('data').get('cardlistInfo'):
            since_id = result.get('data').get('cardlistInfo').get('since_id')
            uid = response.meta.get('uid')
            yield scrapy.Request(f'{self.weibo_url}{uid}&containerid=107603{uid}&since_id={since_id}',
                                 callback=self.parse_weibo_list,  meta={'uid': uid})
