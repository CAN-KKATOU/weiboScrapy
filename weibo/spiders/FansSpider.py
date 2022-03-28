import json
import time

import scrapy
from weibo.items import FanItem


class FansspiderSpider(scrapy.Spider):
    name = 'FansSpider'
    allowed_domains = ['m.weibo.cn']
    # 粉丝列表
    fan_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_'
    # 用户列表
    start_users = ['5886191812']
    # 从第一页开始

    def start_requests(self):
        for uid in self.start_users:
            yield scrapy.Request(f'{self.fan_url}{uid}',
                                 callback=self.parse_fans, meta={'uid': uid})


    def parse_fans(self, response):
        """
        解析粉丝列表
        :param response:
        :return:
        """
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards') \
                and len(result.get('data').get('cards')) \
                and result.get('data').get('cards')[-1].get('card_group'):
            # 解析用户
            fans = result.get('data').get('cards')[-1].get('card_group')
            for fan in fans:
                if fan.get('user'):
                    fan_info = fan.get('user')
                    fan_item = FanItem()

                    fan_item['user_id'] = fan_info.get('id')
                    fan_item['name'] = fan_info.get('screen_name')
                    fan_item['avatar'] = fan_info.get('avatar_hd')
                    fan_item['cover'] = fan_info.get('cover_image_phone')
                    fan_item['gender'] = fan_info.get('gender')
                    fan_item['description'] = fan_info.get('description')
                    fan_item['fans_count'] = fan_info.get('followers_count')
                    fan_item['follows_count'] = fan_info.get('follow_count')
                    fan_item["weibos_count"] = fan_info.get('statuses_count')
                    if fan_info.get('verified') == 'false':
                        fan_item['verified'] = fan_info.get('verified')
                        fan_item['verified_reason'] = 'None'
                    else:
                        fan_item['verified'] = fan_info.get('verified')
                        fan_item['verified_reason'] = fan_info.get('verified_reason')
                    fan_item['verified_type'] = fan_info.get('verified_type')
                    yield fan_item

            uid = response.meta.get('uid')
            # 下一页粉丝
            if result.get('data').get('cardlistInfo').get('since_id'):
                since_id = result.get('data').get('cardlistInfo').get('since_id')
            else:
                # 第一个ajax请求返回json报文没有since_id
                since_id = 20

            yield scrapy.Request(f'{self.fan_url}{uid}&since_id={since_id}',
                                 callback=self.parse_fans, meta={'uid': uid})
