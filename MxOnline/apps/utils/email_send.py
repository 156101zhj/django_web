from random import Random

from users.models import EmailVerifyRecord

#django 内置的邮件函数
from django.core.mail import send_mail
from MxOnline.settings import EMAIL_FROM



# 生成随机字符串
def random_str(random_length=8):
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email,send_type="register"):
    email_record = EmailVerifyRecord()
    if send_type == 'update_email':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "it网注册激活链接"
        email_body = "请点击下面的链接激活你的帐号：http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = "it网密码重置链接"
        email_body = "请点击下面的链接重置你的密码：http://127.0.0.1:8000/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass


    elif send_type == "update_email":

        email_title = "it网邮箱修改验证码"

        email_body = "你的邮箱验证码为{0}".format(code)

        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，从哪里发，接受者list

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

        # 如果发送成功

        if send_status:
            pass



def generate_random_str():
    pass