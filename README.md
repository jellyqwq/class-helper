# class-helper
主要是用来提醒上课的个性化工具

# 2022.5.2?-??:??
## API说明
### 领导讲话
> http://www.hnkjedu.cn/posthome.aspx
#### request data
|参数|栗子|类型|说明|
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

### 海科新闻
> http://www.hnkjedu.cn/posthome.aspx
#### request data
|参数|栗子|类型|说明|
|id|12|int|海科新闻id|
|type|news|str||
|cid|1|int|获取的条数|
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

# 2022年5月21日22:05
计划增加海科官网的海科新闻, 通知公告, 媒体报道, 领导讲话, 教务通知, 科研通知的推送(当然, 和之前一样有开关)

# 2022年5月18日
实现了删除账号, 忘记密码, 以及可选的提交立即推送的功能

# 2022年5月15日
基本完成-除了忘记密码和删除账号

# 2022年5月8日
开始进行2.0的开发

