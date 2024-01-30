# 详细使用方法

## 1. Fork 本仓库

<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/1.png" style="zoom:60%;" />
<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/2.png" style="zoom:60%;" />

## 2. 开启工作流读写权限

<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/3.png" style="zoom:60%;" />
<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/4.png" style="zoom:60%;" />
<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/5.png" style="zoom:60%;" />

## 3. 添加 Secrets

> Name = Name，Secret = 例子

| Name     | 例子                       | 说明              |
| -------- | -------------------------- | ----------------- |
| URL      | https://www.nianbroken.top | 教务系统地址      |
| USERNAME | 2971802058                 | 教务系统用户名    |
| PASSWORD | Y3xhaCkb5PZ4               | 教务系统密码      |
| TOKEN    | J65KWMBfyDh3YPLpcvm8       | Pushplus 的 token |

<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/6.png" style="zoom:60%;" />
<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/7.png" style="zoom:60%;" />

### 获取 TOKEN

[登录 Pushplus ](https://www.pushplus.plus/login.html)

<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/17.png" style="zoom:60%;" />

[获取 Token](https://www.pushplus.plus/api/open/user/token)

打开页面后，你会得到一个类似下列所示的 Json 代码块，`data`中的值就是 TOKEN

```json
{
	"code": 200,
	"msg": "请求成功",
	"data": "cd735c356aa14d16b1452aa932ac89cc",
	"count": null
}
```

[相关文档](https://www.pushplus.plus/doc/guide/openApi.html#_1-%E8%8E%B7%E5%8F%96token)

当你的 Secrets 添加完成后，你的页面应该是类似下图所示
<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/8.png" style="zoom:60%;" />

## 4. 开启 Actions

<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/9.png" style="zoom:60%;" />
<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/10.png" style="zoom:60%;" />

## 5. 运行程序

<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/11.png" style="zoom:60%;" />
<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/12.png" style="zoom:60%;" />
<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/13.png" style="zoom:60%;" />

## 6. 查看运行结果

当你的页面类似下图所示时则表示程序正常运行且未报错
<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/14.png" style="zoom:60%;" />
<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/15.png" style="zoom:60%;" />
在此之后，程序将会每隔 30 分钟自动运行一次

## 7. 成绩更新通知

当检测到成绩更新时，你的页面应该是类似下图所示
<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/16.png" style="zoom:60%;" />
