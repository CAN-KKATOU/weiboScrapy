import json
import scrapy
from weibo.items import UserItem


class UserspiderSpider(scrapy.Spider):
    name = 'UserSpider'
    allowed_domains = ['m.weibo.cn']
    # 用户信息
    user_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}type=uid&value={uid}&containerid=100505{uid}'
    # 用户列表
    start_users = ['1776448504']  # 社会你鸡哥

    def start_requests(self):
        for uid in self.start_users:
            yield scrapy.Request(self.user_url.format(uid=uid), callback=self.parse_user)

    def parse_user(self, response):
        """
        解析用户信息
        :param response:
        :return:
        """
        result = json.loads(response.text)
        if result.get('data').get('userInfo'):
            user_info = result.get('data').get('userInfo')
            user_item = UserItem()

            user_item['user_id'] = user_info.get('id')
            user_item['name'] = user_info.get('screen_name')
            user_item['avatar'] = user_info.get('avatar_hd')
            user_item['cover'] = user_info.get('cover_image_phone')
            user_item['gender'] = user_info.get('gender')
            user_item['description'] = user_info.get('description')
            user_item['fans_count'] = user_info.get('followers_count')
            user_item['follows_count'] = user_info.get('follow_count')
            user_item["weibos_count"] = user_info.get('statuses_count')
            if user_info.get('verified') == 'false':
                user_item['verified'] = user_info.get('verified')
                user_item['verified_reason'] = 'None'
            else:
                user_item['verified'] = user_info.get('verified')
                user_item['verified_reason'] = user_info.get('verified_reason')
            user_item['verified_type'] = user_info.get('verified_type')

            yield user_item
