# -*- coding: utf-8 -*-
# @File  : mail.py
# @Author: TT
# @Email : tt.jiaqi@gmail.com
# @Date  : 2019/3/3
# @Desc  :

import smtplib
from email.mime.text import MIMEText


class Email(object):

    def __init__(self):

        self.mail_user = "1329429689@qq.com"  # 用户名
        self.mail_pass = "noloatwjimzghgba"  # 密码  网易邮箱需要使用授权码
        self.mail_postfix = "qq.com"  # 邮箱的后缀，网易就是163.com
        self.me = "<1329429689@qq.com>"

        self.wy_port = 994
        self.wy_host = "smtp.163.com"

        self.qq_port = 465
        self.qq_host = "smtp.qq.com"

    def send_mail(self,to,sub,content):
        mailto_list = [to]  # 收件人(列表)
        msg = MIMEText(content, "plain", "utf-8")
        msg['Subject'] = sub
        msg['From'] = self.me
        msg['To'] = ";".join(mailto_list)  # 将收件人列表以‘；’分隔
        try:
            server = smtplib.SMTP_SSL(self.qq_host, self.qq_port)
            server.login(self.mail_user, self.mail_pass)  # 登录操作
            server.sendmail(self.me, mailto_list, msg.as_string())
            server.close()
            return True
        except Exception as e:
            print( str(e) )
            return False


if __name__ == "__main__":
    em = Email()
    em.send_mail(to="smile@smilehacker.net",sub="新年快乐",content="新年快乐")