# 正方教务系统成绩推送

<img src="https://cdn.jsdelivr.net/gh/NianBroken/ZFCheckScores/img/19.png" style="zoom:60%;" />

## 简介

**使用本项目前：**

早晨睡醒看一遍教务系统、上厕所看一遍教务系统、刷牙看一遍教务系统、洗脸看一遍教务系统、吃早餐看一遍教务系统、吃午饭看一遍教务系统、睡午觉前看一遍教务系统、午觉醒来看一遍教务系统、出门前看一遍教务系统、吃晚饭看一遍教务系统、洗澡看一遍教务系统、睡觉之前看一遍教务系统。

**使用本项目后：**

成绩更新后自动发通知到微信 以节省您宝贵的时间

## 测试环境

正方教务系统 版本 V8.0.0

## 目前支持的功能

1. 主要功能

   1. 每隔 30 分钟自动检测成绩是否更新 若更新则向微信推送通知

2. 相较于教务系统增加了哪些功能？

   1. 显示成绩提交时间（成绩在何时被录入进教务系统）
   2. 显示成绩提交人姓名（成绩被谁录入进教务系统）

## 使用方法

### 1. [Fork](https://github.com/NianBroken/ZFCheckScores/fork "Fork") 本仓库

`Fork` → `Create fork`

### 2. [开启](https://github.com/kekeaiaixueer/ZFCheckScores/settings/actions "开启")工作流读写权限

`Settings` → `Actions` → `General` → `Workflow permissions` →`Read and write permissions` →`Save`

### 3. [添加](https://github.com/kekeaiaixueer/ZFCheckScores/settings/secrets/actions "添加") Secrets

`Settings` → `Secrets and variables` → `Actions` → `Secrets` → `Repository secrets` → `New repository secret`

> Name = Name
>
> Secret = 例子

| Name     | 例子                       | 说明                                                                                                                 |
| -------- | -------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| URL      | https://www.nianbroken.top | 教务系统地址                                                                                                         |
| USERNAME | 2971802058                 | 教务系统用户名                                                                                                       |
| PASSWORD | Y3xhaCkb5PZ4               | 教务系统密码                                                                                                         |
| TOKEN    | J65KWMBfyDh3YPLpcvm8       | [Pushplus 的 token](https://www.pushplus.plus/doc/guide/openApi.html#_1-%E8%8E%B7%E5%8F%96token "Pushplus 的 token") |

### 4. 开启 Actions

`Actions` → `I understand my workflows, go ahead and enable them` → `CheckScores` → `Enable workflow` → `Run workflow`

_在此之后 程序将会每隔 30 分钟自动运行一次_

### 5. 特别感谢

[openschoolcn/zfn_api](https://github.com/openschoolcn/zfn_api "openschoolcn/zfn_api")
