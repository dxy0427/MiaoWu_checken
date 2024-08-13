<div align="center">
<h1 align="center">喵子小屋论坛签到脚本</h1>
</div>
Discuz!论坛 喵子小屋论坛的签到脚本。

通过[Discuz论坛通用签到脚本](https://github.com/shangskr/discuz-checkin)修改而来。

邮箱通知仅在失败时执行。

VIP任务和年费会员任务未经过验证，不确定是否可用。

# 使用方式

1. 右上角 fork 本仓库
2. 点击 Settings -> 左侧栏Secrets and variable -> Actions -> Repository secrets
3. 新增 New Repository secrets 并设置 Secrets:
4. **必须** - 请随便找个文件(例如`README.md`)，加个空格提交一下，否则可能会出现无法定时执行的问题
5. 由于规则更新,可能会 Fork 后会默认禁用,请手动点击 Actions 选择要签到的项目 `enable workflows`激活
6. [定时执行](#定时执行)


# 定时执行

1. 支持手动执行，具体在 Actions 中选中要执行的 Workflows 后再在右侧可以看到 Run workflow，点击即可运行此 workflow。

2. 如需修改执行时间自行修改`.github\workflows\`下面的 yaml 内的`cron:` 执行时间为国际标准时间 [时间转换](http://www.timebie.com/cn/universalbeijing.php) 分钟在前 小时在后 尽量提前几分钟,因为下载安装部署环境需要一定时间

# Secrets 变量设置 

| 名称             | 内容                      |备注                        |
| ---------------- | ------------------------- | ------------------------- |
| `COOKIES`        | 论坛的Cookies字符串        | 必须填                     |
| `TUANYUAN`       | true                      | 如果身份组是团员就填         |
| `VIP`            | true                      | 如果身份组是VIP就填         | 
| `ANNUAL_VIP`     | true                      | 如果身份组是年费会员就填     |
| `SMTP_SERVER`    | SMTP服务器地址             | 不需要推送则不填            |
| `SMTP_PORT`      | SMTP服务器端口             | 不需要推送则不填            |
| `SMTP_USER`      | SMTP服务器用户名           | 不需要推送则不填            |
| `SMTP_PASSWORD`  | SMTP服务器密码（应用码）    | 不需要推送则不填            |
| `FROM_EMAIL`     | 发件人邮箱地址             |  不需要推送则不填            |
| `TO_EMAIL`       | 收件人邮箱地址             |  不需要推送则不填            |

