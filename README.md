## 微博爬虫模块(Spider)


### 微博评论爬虫(CommentsSpider)

博客ID(weibo_id)

#### 内容(content)

- 文字(raw_text)
- 图片(pics)



评论数(comments_count)

转发数(reposts_count)

点赞数(attitudes_count)

微博发布时间(created_at)

来源(source)

<!--来源表示发布微博终端型号，例如“来自 Iphone 13”、“来自 vivo S12”或“来自微博网页客户端”，以下来源同理-->

#### 评论用户信息(conmment_users_info)

- ID
- 头像(avatar)
- 封面(cover)
- 名字(name)
- 性别(gender)
- 描述(description)
- 粉丝数量(fans_count)
- 关注数量(follows_count)
- 微博数量(weibos_count)
- 是否认证(verified)
- 认证理由(verified_reason)
- 认证类型(verified_type)

### 粉丝爬虫(FansSpider)

- ID
- 名字(name)
- 头像(avatar)
- 封面(cover)
- 性别(gender)
- 描述(description)
- 粉丝数量(fans_count)
- 关注数量(follows_count)
- 微博数量(weibos_count)
- 是否认证(verified)
- 认证理由(verified_reason)
- 认证类型(verified_type)

### 关注列表爬虫(FollowsSpider)

- ID
- 名字(name)
- 头像(avatar)
- 封面(cover)
- 性别(gender)
- 描述(description)
- 粉丝数量(fans_count)
- 关注数量(follows_count)
- 微博数量(weibos_count)
- 是否认证(verified)
- 认证理由(verified_reason)
- 认证类型(verified_type)

### 用户爬虫(UserSpider)

- ID
- 名字(name)
- 头像(avatar)
- 封面(cover)
- 性别(gender)
- 描述(description)
- 粉丝数量(fans_count)
- 关注数量(follows_count)
- 微博数量(weibos_count)
- 是否认证(verified)
- 认证理由(verified_reason)
- 认证类型(verified_type)

### 微博爬虫（WeibosSpider）

- 用户ID(user_id)
- 用户名称(user_name)
- 微博ID(weibo_id)
- 是否转发(is_repost)
- 文字(text)
- 图片(pics)
- 点赞数(attitudes_count)
- 转发数(reposts_count)
- 评论数(comments_count)
- 发布时间(created_at)
- 来源(source)



## 中间件模块(Middleware)

### 代理中间件

访问代理池，获取代理IP地址：端口信息，添加到request请求

### 随机User-Agent中间件

随机设置请求头(headers)中User-Agent的值，模拟浏览器请求



## 管道(Pipeline)

### 数据清洗

包含以下清洗

- 微博文字清洗

- 评论文字清洗

  <!--文字清洗包括去除话题链接，超话链接，emoji链接等-->

- 微博图片略缩图url改为大图url

- 时间清洗

- 数目清洗

  <!--将类似“xx万”的字符串转化为对应数字-->
