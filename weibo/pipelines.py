# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
from weibo.items import UserItem, FanItem, FollowItem, WeiboItem, WeiboListItem, CommentUserItem
from twisted.internet.threads import deferToThread
import pymongo


class CommentTextPipeline:
    def process_item(self, item, spider):
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
        main processor
        :param item:
        :param spider:
        :return:
        """
        if isinstance(item, UserItem) or isinstance(item, FanItem) or isinstance(item, FollowItem) \
                or isinstance(item, WeiboItem) or isinstance(WeiboListItem) or isinstance(CommentUserItem):
            self.db[item.collection].update({'id': item.get('id')}, {'$set': item}, True)
        return item

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)
