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

<p>1. <a href="https://github.com/NianBroken/ZFCheckScores/fork">点击 Fork</a></p>

<p>2. 点击 Create fork</p>

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

<p>1. 点击 Settings</p>

<p>2. 点击 Actions</p>

<p>3. 点击 General</p>

<p>4. 找到 Workflow permissions</p>

<p>5. 点击 Read and write permissions</p>

<p>6. 点击 Save</p>

## 3. 添加 Secrets

> Name = Name，Secret = 例子

> 程序会自动填充 `URL` 尾部的 `xtgl/login_slogin.html`，因此你无需重复添加

| Name     | 例子                   | 说明                                               |
| -------- | ---------------------- | -------------------------------------------------- |
| URL      | https://www.klaio.top/ | 教务系统地址                                       |
| USERNAME | 2971802058             | 教务系统用户名                                     |
| PASSWORD | Y3xhaCkb5PZ4           | 教务系统密码                                       |
| TOKEN    | J65KWMBfyDh3YPLpcvm8   | [Showdoc 的 token](#获取-token "Showdoc 的 token") |

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

<p>1. 点击 Settings</p>

<p>2. 点击 Secrets and variables</p>

<p>3. 点击 Actions</p>

<p>4. 点击 Secrets 选项卡</p>

<p>5. 找到 Repository secrets</p>

<p>6. 点击 New repository secret</p>

<p>7. 根据上面的表格填写正确的 Name 以及 Secret</p>

<p>8. 点击 Add secret</p>

### 获取 TOKEN

<p>1. <a href="https://push.showdoc.com.cn/#/push">登录 Showdoc 推送服务</a></p>

<p>2. 使用微信扫码关注公众号</p>

<p>3. 红框内的字符就是token</p>

<table>
	<tr>
		<td>
			<img src="https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/img/18.png" />
		</td>
		<td>
			<img src="https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/img/19.png" />
		</td>
        <td>
			<img src="https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/img/20.png" />
		</td>
	</tr>
</table>

当你的 Secrets 添加完成后，你的页面应该与下图所示的页面完全一致或几乎一致

<img src="https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/img/21.png" width="60%"/>

## 4. 开启 Actions

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

<p>1. 点击 Actions</p>

<p>2. 点击 I understand my workflows, go ahead and enable them</p>

<p>3. 点击 CheckScores</p>

<p>4. 点击 Enable workflow</p>

## 5. 运行程序

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

<p>1. 点击 Actions</p>

<p>2. 点击 CheckScores</p>

<p>3. 点击 Run workflow</p>

<p>4. 再次点击 Run workflow</p>

## 6. 查看运行结果

<table>
	<tr>
		<td>
			<img src="https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/img/26.png" />
		</td>
		<td>
			<img src="https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/img/27.png" />
		</td>
	</tr>
</table>

当你的页面与上图所示的页面完全一致或几乎一致，则代表程序正常运行且未报错

在此之后，程序将会每隔 30 分钟自动检测一次成绩是否有更新

## 7. 成绩更新通知

当检测到成绩更新时，你的页面应该与下图所示的页面完全一致或几乎一致

<img src="https://raw.githubusercontent.com/NianBroken/ZFCheckScores/main/img/8.png" width="60%" />
