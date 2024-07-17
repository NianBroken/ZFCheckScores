# 详细使用方法

推荐使用电脑查看该页面

## 1. Fork 本仓库

<table>
	<tr>
		<td>
			<img src="https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/img/10.png" />
		</td>
		<td>
			<img src="https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/img/11.png" />
		</td>
	</tr>
</table>

## 2. 开启工作流读写权限

<table>
	<tr>
		<td>
			<img src="https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/img/12.png" />
		</td>
		<td>
			<img src="https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/img/13.png" />
		</td>
        <td>
			<img src="https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/img/14.png" />
		</td>
	</tr>
</table>

## 3. 添加 Secrets

> Name = Name，Secret = 例子

| Name     | 例子                        | 说明                                                 |
| -------- | --------------------------- | ---------------------------------------------------- |
| URL      | https://www.nianbroken.top/ | 教务系统地址                                         |
| USERNAME | 2971802058                  | 教务系统用户名                                       |
| PASSWORD | Y3xhaCkb5PZ4                | 教务系统密码                                         |
| TOKEN    | J65KWMBfyDh3YPLpcvm8        | [PushPlus 的 token](#获取-token "PushPlus 的 token") |

<table>
	<tr>
		<td>
			<img src="https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/img/15.png" />
		</td>
		<td>
			<img src="https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/img/16.png" />
		</td>
        <td>
			<img src="https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/img/17.png" />
		</td>
	</tr>
</table>

### 获取 TOKEN

<p>1. <a href="https://www.pushplus.plus/login.html">登录 PushPlus </a></p>

<img src="https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/img/18.png" width="60%" />

<p>2. <a href="https://www.pushplus.plus/api/open/user/token">获取 Token</a></p>

打开“获取 Token”的页面后，你会得到一个与下列所示几乎一致的 Json 代码块，`data`中的值就是 TOKEN

```json
{
	"code": 200,
	"msg": "请求成功",
	"data": "cd735c356aa14d16b1452aa932ac89cc",
	"count": null
}
```

当你的 Secrets 添加完成后，你的页面应该与下图所示的页面完全一致或几乎一致

<img src="https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/img/19.png" width="60%"/>

<p>3. <a href="https://www.pushplus.plus/doc/guide/openApi.html#_1-%E8%8E%B7%E5%8F%96token">相关文档</a></p>

## 4. 开启 Actions

<table>
	<tr>
		<td>
			<img src="https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/img/20.png" />
		</td>
		<td>
			<img src="https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/img/21.png" />
		</td>
	</tr>
</table>

## 5. 运行程序

<table>
	<tr>
		<td>
			<img src="https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/img/22.png" />
		</td>
		<td>
			<img src="https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/img/23.png" />
		</td>
	</tr>
</table>

## 6. 查看运行结果

<table>
	<tr>
		<td>
			<img src="https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/img/24.png" />
		</td>
		<td>
			<img src="https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/img/25.png" />
		</td>
	</tr>
</table>

当你的页面与上图所示的页面完全一致或几乎一致，则代表程序正常运行且未报错

在此之后，程序将会每隔 30 分钟自动检测一次成绩是否有更新

## 7. 成绩更新通知

当检测到成绩更新时，你的页面应该与下图所示的页面完全一致或几乎一致

<img src="https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/img/26.png" width="60%" />
