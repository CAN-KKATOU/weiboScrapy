# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
import time

from weibo.items import UserItem, FanItem, FollowItem, WeiboItem, WeiboListItem, CommentUserItem
from twisted.internet.threads import deferToThread
import pymongo


class CommentTextPipeline:
    def process_item(self, item, spider):
        """
        评论文本清理
        清除超话链接、话题链接、网页链家、emoji链接等等
        :param item:
        :param spider:
        :return:
        """
        if item.get('comment_text'):
            raw_text = item.get('comment_text')
            label_filter_1 = re.compile(r'<a  href=.*?class="surl-text">', re.S)
            label_filter_2 = re.compile(r'<span class="url-icon"><img alt=', re.S)
            label_filter_3 = re.compile(r'src=.*?</span>', re.S)
            label_filter_4 = re.compile(r'</span></a>', re.S)
            raw_text = re.sub(label_filter_1, '', raw_text)
            raw_text = re.sub(label_filter_2, '', raw_text)
            raw_text = re.sub(label_filter_3, '', raw_text)
            raw_text = re.sub(label_filter_4, '', raw_text)
            item['comment_text'] = raw_text
        return item


class WeiboTextPipeline:
    def process_item(self, item, spider):
        """
        微博文本清理
        清除超话链接、话题链接、网页链家、emoji链接等等
        :param item:
        :param spider:
        :return:
        """
        if item.get('text'):
            raw_text = item.get('text')
            label_filter_1 = re.compile(r'<a  href=.*?class="surl-text">', re.S)
            label_filter_2 = re.compile(r'<span class="url-icon"><img alt=', re.S)
            label_filter_3 = re.compile(r'src=.*?</span>', re.S)
            label_filter_4 = re.compile(r'</span></a>', re.S)
            label_filter_5 = re.compile(r'<a.*>', re.S)
            label_filter_6 = re.compile(r'</a>', re.S)
            label_filter_7 = re.compile(r'<br />', re.S)
            raw_text = re.sub(label_filter_1, '', raw_text)
            raw_text = re.sub(label_filter_2, '', raw_text)
            raw_text = re.sub(label_filter_3, '', raw_text)
            raw_text = re.sub(label_filter_4, '', raw_text)
            raw_text = re.sub(label_filter_5, '', raw_text)
            raw_text = re.sub(label_filter_6, '', raw_text)
            raw_text = re.sub(label_filter_7, '', raw_text)
            item['text'] = raw_text
        return item


class MongoDBPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        cls.mongo_url = crawler.settings.get('MONGODB_CONNECTION_URL')
        cls.mongo_db = crawler.settings.get('MONGODB_DATABASE')
        return cls()

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]
        self.db[UserItem.collection].create_index([('id', pymongo.ASCENDING)])
        self.db[FanItem.collection].create_index([('id', pymongo.ASCENDING)])
        self.db[FollowItem.collection].create_index([('id', pymongo.ASCENDING)])
        self.db[WeiboItem.collection].create_index([('id', pymongo.ASCENDING)])
        self.db[WeiboListItem.collection].create_index([('id', pymongo.ASCENDING)])
        self.db[CommentUserItem.collection].create_index([('id', pymongo.ASCENDING)])

    def close_spider(self, spider):
        self.client.close()

    def _process_item(self, item, spider):
        """
        将数据存入MongoDB
        :param item:
        :param spider:
        :return:
        """
        if isinstance(item, UserItem) or isinstance(item, FanItem) or isinstance(item, FollowItem) \
                or isinstance(item, CommentUserItem):
            self.db[item.collection].update_one({'user_id': item.get('user_id')}, {'$set': dict(item)}, True)
        elif isinstance(item, WeiboListItem) or isinstance(item, WeiboItem):
            self.db[item.collection].update_one({'weibo_id': item.get('weibo_id')}, {'$set': dict(item)}, True)
        return item

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)


class LargePicsPipeline:
    def process_item(self, item, spider):
        """
        将略缩图url更改为大图url
        :param item:
        :param spider:
        :return:
        """
        if item.get('pics'):
            pics_urls = item.get('pics')
            new_urls = []
            for url in pics_urls:
                url = re.sub('/orj360/', '/large/', url)
                new_urls.append(url)

            item['pics'] = new_urls

        return item


class TimePipeline:
    def process_item(self, item, spider):
        if item.get('create_at'):
            date = item.get('create_at')
            if re.match('刚刚', date):
                date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
            if re.match('\d+分钟前', date):
                minute = re.match('(\d+)', date).group(1)
                date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - float(minute) * 60))
            if re.match('\d+小时前', date):
                hour = re.match('(\d+)', date).group(1)
                date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - float(hour) * 60 * 60))
            if re.match('昨天.*', date):
                date = re.match('昨天(.*)', date).group(1).strip()
                date = time.strftime('%Y-%m-%d', time.localtime() - 24 * 60 * 60) + ' ' + date
            if re.match('\d{2}-\d{2} \d{2}:\d{2}', date):
                date = time.strftime('%Y-', time.localtime()) + date
            if re.match('\d{2}-\d{2}', date):
                date = time.strftime('%Y-', time.localtime()) + date + ' 00:00'
            if re.match('\d-\d{2} \d{2}:\d{2}', date):
                date = time.strftime('%Y-', time.localtime()) + date
            if re.match('\d-\d{2}', date):
                date = time.strftime('%Y-', time.localtime()) + date + ' 00:00'
            if re.match('\d{2}-\d \d{2}:\d{2}', date):
                date = time.strftime('%Y-', time.localtime()) + date
            if re.match('\d{2}-\d', date):
                date = time.strftime('%Y-', time.localtime()) + date + ' 00:00'

            item['create_at'] = date

        return item


class CountPipeline:
    def str_to_value(self, value_str):
        value_str = str(value_str)
        value_str = re.sub('\+', '', value_str)
        idxOfYi = value_str.find('亿')
        idxOfWan = value_str.find('万')
        if idxOfYi != -1 and idxOfWan != -1:
            return int(float(value_str[:idxOfYi]) * 1e8 + float(value_str[idxOfYi + 1:idxOfWan]) * 1e4)
        elif idxOfYi != -1 and idxOfWan == -1:
            return int(float(value_str[:idxOfYi]) * 1e8)
        elif idxOfYi == -1 and idxOfWan != -1:
            return int(float(value_str[idxOfYi + 1:idxOfWan]) * 1e4)
        elif idxOfYi == -1 and idxOfWan == -1:
            return float(value_str)

    def process_item(self, item, spider):
        if item.get('fans_count'):
            value_str = item.get('fans_count')
            value = self.str_to_value(value_str)
            item['fans_count'] = value

        if item.get('follows_count'):
            value_str = item.get('follows_count')
            value = self.str_to_value(value_str)
            item['follows_count'] = value

        if item.get('weibos_count'):
            value_str = item.get('weibos_count')
            value = self.str_to_value(value_str)
            item['weibos_count'] = value

        if item.get('comments_count'):
            value_str = item.get('comments_count')
            value = self.str_to_value(value_str)
            item['comments_count'] = value

        if item.get('reposts_count'):
            value_str = item.get('reposts_count')
            value = self.str_to_value(value_str)
            item['reposts_count'] = value

        if item.get('attitudes_count'):
            value_str = item.get('attitudes_count')
            value = self.str_to_value(value_str)
            item['attitudes_count'] = value

        return item


class SourcePipeline:
    def process_item(self, item, spider):
        if item.get('source'):
            source = item.get('source')
            source = re.sub('来自 ', '', source)
            item['source'] = source

        return item
