import os
import requests
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time


def requests_get(url, submit=False, apply=False, checken=False, page=False, referer=None, cookies=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        
    }
    session = requests.Session()
    if (apply and cookies) or (submit and cookies):
        session.cookies.update(cookies)

    if page:
        headers['Referer'] = referer
        response = session.get(url, headers=headers)

    if checken:
        referer = 'https://forum.h3dhub.com/forum-36-1.html'
        headers['Referer'] = referer
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            print("签到成功")
        else :
            print("签到失败")

    if apply or submit :
        referer = 'https://forum.h3dhub.com/home.php?mod=task'
        headers['Referer'] = referer
        response = session.get(url, headers=headers)
        if apply :
            if response.status_code == 302 :
                return '任务仅接取'

    return response.text


def get_formhash(response_text):
    match = re.search(r'name="formhash" value="([^"]+)', response_text)
    if match:
        return match.group(1)
    else:
        result_str = "没有找到formhash\r\n"
        # 发送邮件通知
        subject = "论坛签到结果通知"
        send_email(subject, result_str, from_email, to_email, smtp_server, smtp_port, smtp_user, smtp_password)
        exit('没有找到formhash')


def apply_task(task_id,isVip=False,isAnnual_Vip=False):

    if isAnnual_Vip:
        print("开始年费会员任务签到")
    elif isVip:
        print("开始Vip任务签到")
    else:
        print("开始执行任务签到")

    # 任务申请地址
    task_apply_url = 'https://forum.h3dhub.com/home.php?mod=task&do=apply&id={}'.format(task_id)

    # 申请任务
    response = requests_get(task_apply_url, apply=True, cookies=cookies)

    # 正常情况下申请任务后就会自动提交，但是可能有不提交的情况
    if response == '任务仅接取' :
        print("开始提交任务")
        # 提交任务
        response = submit_task(task_id)

    return response


def submit_task(task_id):
    # 任务提交地址
    task_submit_url = 'https://forum.h3dhub.com/home.php?mod=task&do=draw&id={}'.format(task_id)
    # 提交任务
    response = requests_get(task_submit_url, submit=True, cookies=cookies)
    return response


def result(response,isVip=False,isAnnual_Vip=False):
    
    sign_result = re.search(r'class="alert_(error|info)">\n<p>(.*?)<', response)
    
    #print(f"Sign result: {sign_result}")
    if sign_result and '任务' in sign_result.group(2):
        result_str = sign_result.group(2)
    elif isAnnual_Vip:
        result_str = "年费会员签到失败!\r\n"
    elif isVip:
        result_str = "vip签到失败!\r\n"
    else :
        result_str = "论坛签到失败!\r\n"
        # 发送邮件通知
        subject = "论坛签到结果通知"
        send_email(subject, result_str, from_email, to_email, smtp_server, smtp_port, smtp_user, smtp_password)

    print(result_str)


def send_email(subject, body, from_email, to_email, smtp_server, smtp_port, smtp_user, smtp_password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()


# 从环境变量中获取Cookies字符串
cookies_str = os.getenv('COOKIES')  # 论坛的Cookies字符串
# 从环境变量中获取任务id
isTuanYuan = os.getenv('TUANYUAN','false')
if isTuanYuan == 'true':
    task_id = '14'
else:
    task_id = '22'

isVip = os.getenv('VIP','false')
isAnnual_Vip = os.getenv('ANNUAL_VIP','false')


# 邮件相关环境变量
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = os.getenv('SMTP_PORT', 587)
smtp_user = os.getenv('SMTP_USER')
smtp_password = os.getenv('SMTP_PASSWORD')
from_email = os.getenv('FROM_EMAIL')
to_email = os.getenv('TO_EMAIL')


# 将Cookies字符串解析为字典
cookies = {item.split('=')[0]: item.split('=')[1] for item in re.split(r';\s*', cookies_str)}

# 任务页面地址
task_page_url = 'https://forum.h3dhub.com/home.php?mod=task'

print("Starting the sign-in process")

# 访问任务页面
response = requests_get(task_page_url, page=True, cookies=cookies)
#print(f"Sign page response: {response[:500]}")  # 打印前500个字符以避免过多输出

# 获取formhash验证串
formhash = get_formhash(response)
print(f"Sign formhash: {formhash}")

#获取当前时间戳
timestamp = int(time.time())

# 每日签到提交地址
sign_submit_url = 'https://forum.h3dhub.com/home.php?mod=spacecp&ac=pm&op=checknewpm&rand={}'.format(timestamp)

# 每日签到
print("开始执行每日登录")
requests_get(sign_submit_url, checken=True, cookies=cookies)

# 申请任务
response = apply_task(task_id)
#print(f"Sign submit response: {response[:500]}")  # 打印前500个字符以避免过多输出

# 获取任务结果
result(response)

# vip额外任务
if isAnnual_Vip == 'true':
    task_id = '20'
    response = apply_task(task_id,isVip=True)
    result(response,isVip=True)

#年费额外任务
if isVip == 'true':
    task_id = '19'
    response = apply_task(task_id,isAnnual_Vip=True)
    result(response,isVip=True)

