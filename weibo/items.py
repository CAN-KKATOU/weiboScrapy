# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class UserItem(Item):
    """
    微博用户信息
    包括ID、姓名、头像、封面、性别、描述、粉丝数量、关注数量、微博数量、是否认证、认证理由、认证类型
    """
    # 数据库名字
    collection = 'user_info'
    # ID
    user_id = Field()
    # 用户名字
    name = Field()
    # 用户头像
    avatar = Field()
    # 用户封面
    cover = Field()
    # 用户性别
    gender = Field()
    # 用户描述
    description = Field()
    # 粉丝数量
    fans_count = Field()
    # 关注数量
    follows_count = Field()
    # 微博数量
    weibos_count = Field()
    # 是否认证
    verified = Field()
    # 认证信息
    verified_reason = Field()
    # 认证类型
    verified_type = Field()


class FollowItem(Item):
    """
    微博关注列表用户信息
    包括ID、姓名、性别、描述、粉丝数量、关注数量、微博数量
    """
    collection = 'follows_info'
    # ID
    user_id = Field()
    # 用户名字
    name = Field()
    # 用户头像
    avatar = Field()
    # 用户封面
    cover = Field()
    # 用户性别
    gender = Field()
    # 用户描述
    description = Field()
    # 粉丝数量
    fans_count = Field()
    # 关注数量
    follows_count = Field()
    # 微博数量
    weibos_count = Field()
    # 是否认证
    verified = Field()
    # 认证信息
    verified_reason = Field()
    # 认证类型
    verified_type = Field()


class FanItem(Item):
    """
    微博粉丝列表用户信息
    包括ID、姓名、性别、描述、粉丝数量、关注数量、微博数量
    """
    collection = 'fans_info'
    # ID
    user_id = Field()
    # 用户名字
    name = Field()
    # 用户头像
    avatar = Field()
    # 用户封面
    cover = Field()
    # 用户性别
    gender = Field()
    # 用户描述
    description = Field()
    # 粉丝数量
    fans_count = Field()
    # 关注数量
    follows_count = Field()
    # 微博数量
    weibos_count = Field()
    # 是否认证
    verified = Field()
    # 认证信息
    verified_reason = Field()
    # 认证类型
    verified_type = Field()


class WeiboItem(Item):
    """
    每条微博信息
    包括微博ID、微博文字和图片内容、评论数、转发数、点赞数
    每个WeiboItem应相对应CommentUserItem合集
    """
    collection = 'weibo'
    # 微博ID（指每一条微博唯一的ID号，非微博账号ID）
    weibo_id = Field()
    # 该微博用户名称
    user_name = Field()
    # 发送时间
    created_at = Field()
    # 来源
    source = Field()
    # 微博文字内容
    text = Field()
    # 微博图片内容
    pics = Field()
    # 评论数
    comments_count = Field()
    # 转发数
    reposts_count = Field()
    # 点赞数
    attitudes_count = Field()


class CommentUserItem(Item):
    """
    微博评论列表用户信息
    包括ID、姓名、性别、描述、粉丝数量、关注数量、微博数量
    相同微博下的评论应对应该WeiboItem
    """
    collection = 'comment_user_info'
    # 对应微博ID
    weibo_id = Field()
    # 评论内容
    comment_text = Field()
    # 评论时间
    comment_time = Field()
    # 该评论点赞数量
    like_count = Field()
    # ID
    user_id = Field()
    # 用户名字
    name = Field()
    # 用户头像
    avatar = Field()
    # 用户封面
    cover = Field()
    # 用户性别
    gender = Field()
    # 用户描述
    description = Field()
    # 粉丝数量
    fans_count = Field()
    # 关注数量
    follows_count = Field()
    # 微博数量
    weibos_count = Field()
    # 是否认证
    verified = Field()
    # 认证信息
    verified_reason = Field()
    # 认证类型
    verified_type = Field()


class WeiboListItem(Item):
    collection = 'weibo_list'
    # 该微博发送用户ID
    user_id = Field()
    # 该微博发送用户名称
    user_name = Field()
    # 微博ID（指每一条微博唯一的ID号，非微博账号ID）
    weibo_id = Field()
    # 是否转发
    is_repost = Field()
    # 微博文字内容
    text = Field()
    # 微博图片内容
    pics = Field()
    # 评论数
    comments_count = Field()
    # 转发数
    reposts_count = Field()
    # 点赞数
    attitudes_count = Field()
    # 发送时间
    created_at = Field()
    # 来源
    source = Field()
