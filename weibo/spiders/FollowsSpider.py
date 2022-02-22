import json
import scrapy
from weibo.items import FollowItem


class FollowsspiderSpider(scrapy.Spider):
    name = 'FollowsSpider'
    allowed_domains = ['m.weibo.cn']
    # 关注列表
    follow_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&page={page}'
    # 用户列表
    start_users = ['1776448504']  # 社会你鸡哥
    # 从第一页开始
    page = 1

    def start_requests(self):
        for uid in self.start_users:
            yield scrapy.Request(self.follow_url.format(uid=uid, page=self.page),
                                 callback=self.parse_follows, meta={'page': self.page, 'uid': uid})

    def parse_follows(self, response):
        """
        解析用户关注
        :param response:
        :return:
        """
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards') \
                and len(result.get('data').get('cards')) \
                and result.get('data').get('cards')[-1].get('card_group'):
            # 解析用户
            follows = result.get('data').get('cards')[-1].get('card_group')
            for follow in follows:
                if follow.get('user'):
                    follow_info = follow.get('user')
                    follow_item = FollowItem()
                    follow_item['user_id'] = follow_info.get('id')
                    follow_item['name'] = follow_info.get('screen_name')
                    follow_item['avatar'] = follow_info.get('avatar_hd')
                    follow_item['cover'] = follow_info.get('cover_image_phone')
                    follow_item['gender'] = follow_info.get('gender')
                    follow_item['description'] = follow_info.get('description')
                    follow_item['fans_count'] = follow_info.get('followers_count')
                    follow_item['follows_count'] = follow_info.get('follow_count')
                    follow_item["weibos_count"] = follow_info.get('statuses_count')
                    if follow_info.get('verified') == 'false':
                        follow_item['verified'] = follow_info.get('verified')
                        follow_item['verified_reason'] = 'None'
                    else:
                        follow_item['verified'] = follow_info.get('verified')
                        follow_item['verified_reason'] = follow_info.get('verified_reason')
                    follow_item['verified_type'] = follow_info.get('verified_type')
                    yield follow_item

            uid = response.meta.get('uid')
            # 下一页关注
            page = response.meta.get('page') + 1
            yield scrapy.Request(self.follow_url.format(uid=uid, page=page),
                                 callback=self.parse_follows, meta={'page': page, 'uid': uid})
