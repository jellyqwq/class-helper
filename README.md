# class-helper
主要是用来提醒上课的个性化工具

# 2022.5.21-23:10
## API说明
### 领导讲话
> http://www.hnkjedu.cn/posthome.aspx
#### request data
|参数|栗子|类型|说明|
|--|--|--|--|
|id|374|int|领导讲话id|
|type|news|str||
|cid|1|int|获取的条数|
|count|26|int|暂不明确|

#### response data
```json
[
    {
        "News_id": "12530",
        "News_title": "海南科技职业大学2022年五一劳动节慰问信",
        "News_titleall": "海南科技职业大学2022年五一劳动节慰问信",
        "News_time": "2022.05.01"
    },
    {
        "News_id": "12238",
        "News_title": "海南科技职业大学2022年新年贺词",
        "News_titleall": "海南科技职业大学2022年新年贺词",
        "News_time": "2021.12.31"
    }
]
```
> http://www.hnkjedu.cn/column_show.aspx?id=31&zid=News_id

### 海科新闻
> http://www.hnkjedu.cn/posthome.aspx

#### request data
|参数|栗子|类型|说明|
|--|--|--|--|
|id|12|int|海科新闻id|
|type|news|str||
|cid|2|int|获取的条数|
|count|26|int|暂不明确|

#### response data
```json
[
    {
        "News_id": "12629",
        "News_title": "海南科技职业大学举办2022届毕业生春季校园招聘会",
        "News_titleall": "海南科技职业大学举办2022届毕业生春季校园招聘会",
        "News_time": "2022.05.19"
    },
    {
        "News_id": "12628",
        "News_title": "海南科技职业大学举行2020-2021学年度国家奖学...",
        "News_titleall": "海南科技职业大学举行2020-2021学年度国家奖学金和国家助学金颁奖典礼",
        "News_time": "2022.05.19"
    }
]
```
> http://www.hnkjedu.cn/show.aspx?id=News_id

### 通知公告
> http://www.hnkjedu.cn/posthome.aspx

#### request data
|参数|栗子|类型|说明|
|--|--|--|--|
|id|22|int|通知公告id|
|type|news|str||
|cid|2|int|获取的条数|
|count|26|int|暂不明确|

#### response data
```json
[
    {
        "News_id": "12630",
        "News_title": "关于5·19海科大安全教育日的一封信",
        "News_titleall": "关于5·19海科大安全教育日的一封信",
        "News_time": "2022.05.19"
    },
    {
        "News_id": "12512",
        "News_title": "关于2022年“五一”劳动节放假的通知",
        "News_titleall": "关于2022年“五一”劳动节放假的通知",
        "News_time": "2022.04.21"
    }
]
```
> http://www.hnkjedu.cn/show.aspx?id=News_id

### 媒体报道
> http://www.hnkjedu.cn/posthome.aspx

#### request data
|参数|栗子|类型|说明|
|--|--|--|--|
|type|mtbd|str|媒体报道(返回数量不可选,固定十条)|

#### response data(照顾版面,省略8条,展示两条)
```json
[
    {
        "News_title": "【中国民办教育协会】海南科技职业大学党委书记带队开展...",
        "News_titleall": "【中国民办教育协会】海南科技职业大学党委书记带队开展访企拓岗促就业工作",
        "News_time": "2022.05.20",
        "mtbd_link": "https://www.canedu.org.cn/site/content/6732.html#10006-weixin-1-52626-6b3bffd01fdde4900130bc5a2751b6d1"
    },
    {
        "News_title": "【中新网】海南科技职业大学组织学习《中华人民共和国职...",
        "News_titleall": "【中新网】海南科技职业大学组织学习《中华人民共和国职业教育法》",
        "News_time": "2022.05.11",
        "mtbd_link": "http://www.hi.chinanews.com.cn/hnnew/2022-05-11/638513.html?bsh_bid=5761683638"
    }
]
```
> mtbd_link

### 教务通知
> http://www.hnkjedu.cn/posthome.aspx

#### request data
|参数|栗子|类型|说明|
|--|--|--|--|
|id|108|int|教务通知id|
|type|news|str||
|cid|2|int|获取的条数|
|count|26|int|暂不明确|

#### response data
```json
[
    {
        "News_id": "12631",
        "News_title": "海南科技职业大学关于做好2022届毕业生离校工作的通...",
        "News_titleall": "海南科技职业大学关于做好2022届毕业生离校工作的通知",
        "News_time": "2022.05.20"
    },
    {
        "News_id": "12614",
        "News_title": "海南科技职业大学“产教融合课改试验项目”课程开发工作...",
        "News_titleall": "海南科技职业大学“产教融合课改试验项目”课程开发工作坊结业式专家报告会圆满结束",
        "News_time": "2022.05.16"
    }
]
```
> http://jwc.hnkjedu.cn/shownews.aspx?id=News_id

### 科研通知
> http://www.hnkjedu.cn/posthome.aspx

#### request data
|参数|栗子|类型|说明|
|--|--|--|--|
|id|111|int|科研通知id|
|type|news|str||
|cid|2|int|获取的条数|
|count|26|int|暂不明确|

#### response data
```json
[
    {
        "News_id": "12519",
        "News_title": "关于提名2022年度高等学校科学研究优秀成果奖 （科...",
        "News_titleall": "关于提名2022年度高等学校科学研究优秀成果奖 （科学技术）提名的公示",
        "News_time": "2022.04.28"
    },
    {
        "News_id": "12457",
        "News_title": "关于组织申报2022年度教育部产学合作协同育人项目的...",
        "News_titleall": "关于组织申报2022年度教育部产学合作协同育人项目的通知",
        "News_time": "2022.04.19"
    }
]
```
> http://kyzx.hnkjedu.cn/show.aspx?id=News_id

# 2022年5月21日22:05
计划增加海科官网的海科新闻, 通知公告, 媒体报道, 领导讲话, 教务通知, 科研通知的推送(当然, 和之前一样有开关)

# 2022年5月18日
实现了删除账号, 忘记密码, 以及可选的提交立即推送的功能

# 2022年5月15日
基本完成-除了忘记密码和删除账号

# 2022年5月8日
开始进行2.0的开发

