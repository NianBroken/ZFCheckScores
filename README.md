# 正方教务系统成绩推送

## 作用

**使用本项目前：**

睡醒看一遍教务系统、上厕所看一遍教务系统、刷牙看一遍教务系统、洗脸看一遍教务系统、吃早餐看一遍教务系统、吃午饭看一遍教务系统、睡午觉前看一遍教务系统、午觉醒来看一遍教务系统、吃完晚饭看一遍教务系统、洗澡看一遍教务系统、睡觉之前看一遍教务系统。

**使用本项目后：**

成绩更新后自动发通知到微信 以节省您宝贵的时间

## 测试环境

正方教务系统 版本 V8.0.0

## 目前支持的功能

1. 每隔 30 分钟自动检测成绩是否更新 若更新则向微信推送通知

2. 显示成绩提交时间（何时将成绩录入教务系统）

3. 显示成绩提交人姓名（何人将成绩录入教务系统）

## 使用方法

### 1. Fork 本仓库

<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/1.png" style="zoom:40%;" />
<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/2.png" style="zoom:40%;" />

### 2. 开启工作流读写权限

<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/3.png" style="zoom:40%;" />
<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/4.png" style="zoom:40%;" />
<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/5.png" style="zoom:40%;" />

### 3. 添加 Secrets

| Name     | 例子                       | 说明              |
| -------- | -------------------------- | ----------------- |
| URL      | https://www.nianbroken.top | 教务系统地址      |
| USERNAME | 2971802058                 | 教务系统用户名    |
| PASSWORD | Y3xhaCkb5PZ4               | 教务系统密码      |
| TOKEN    | J65KWMBfyDh3YPLpcvm8       | Pushplus 的 token |

<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/6.png" style="zoom:40%;" />
<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/7.png" style="zoom:40%;" />

获取 TOKEN：

- [登录 Pushplus ](https://www.pushplus.plus/login.html)
  <img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/17.png" style="zoom:40%;" />

- [获取 Token](https://www.pushplus.plus/api/open/user/token)

打开页面后，你会得到一个类似下列所示的 Json 代码块，`data`中的值就是 TOKEN

```json
{
	"code": 200,
	"msg": "请求成功",
	"data": "cd735c356aa14d16b1452aa932ac89cc",
	"count": null
}
```

- [相关文档](https://www.pushplus.plus/doc/guide/openApi.html#_1-%E8%8E%B7%E5%8F%96token)

当你的 Secrets 添加完成后，你的页面应该是类似下图所示
<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/8.png" style="zoom:40%;" />

### 4. 开启 Actions

<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/9.png" style="zoom:40%;" />
<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/10.png" style="zoom:40%;" />

### 5. 运行程序

<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/11.png" style="zoom:40%;" />
<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/12.png" style="zoom:40%;" />

当你的页面应该是类似下图所示时则表示程序运行结束且未报错
<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/13.png" style="zoom:40%;" />
在此之后 程序将会每隔 30 分钟自动运行一次

### 6. 查看运行结果

<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/14.png" style="zoom:40%;" />
<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/15.png" style="zoom:40%;" />

### 7. 成绩更新通知

当检测到成绩更新时，你的页面应该是类似下图所示
<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/16.png" style="zoom:40%;" />
