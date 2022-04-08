### 启动cookie获取接口

nohup /usr/bin/python3  cookies.py >/dev/null 2>&1 &

### 查看cookie日志

tail -f log/cookies.log

### 启动程序

python3 wechat.py

### 解决思路	

```
注册一个微信公众号账号，登录以后：图文素材--新建图文素材--超链接--选择你需要的公众号--抓包
就可以看到公众号所有的文章，所有的链接都是ajax请求，请求所需要携带的参数只有这几个：
data = {
        "token": token,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
        "action": "list_ex",
        "begin": 5 * page,
        "count": "5",
        "query": "",
        "fakeid": fakeid,
        "type": "9",
 }
url = "https://mp.weixin.qq.com"
content_json = requests.get(url, headers=headers, params=data）

其中变量只有验证登陆状态的token和begin页码，另外还需要登录后的cookie，cookie的过期时间比较久,大约48小时
至于模拟登录肯定是不行的，输入账号密码以后还是需要微信扫码才能登录成功。因此只能用插件发送cookie。
其中的fakeid是一个base64编码后的字符串，例如fakenid = {'MzAxNjUyOTExOQ==': '统战新语'},
可以采用字典和真实的公众号名称一一对应，这个是固定的，可以通过search输入公众号名字，搜索拿到
fakeid和名字
                            
```

### token过期和程序错误
```
返回json结果为： {'base_resp': {'err_msg': 'freq control', 'ret': 200013}}

出现这个错误，账号被封了，需要等待几个小时解禁，账号cookie和token会过期需要及时更新
如果需要大量数据，需要多个账号

```