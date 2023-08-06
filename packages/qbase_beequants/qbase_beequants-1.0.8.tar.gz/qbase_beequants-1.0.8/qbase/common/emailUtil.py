
# coding: utf-8

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from qbase.common import configer as cf




# 通过Header对象编码的文本，包含utf-8编码信息和Base64编码信息。以下中文名测试ok
# subject = '中文标题'
# subject=Header(subject, 'utf-8').encode()

# 构造邮件对象MIMEMultipart对象


# 构造图片链接
#sendimagefile =open(r'D:\pythontest\testimage.png' ,'rb').read()
#image = MIMEImage(sendimagefile)
#image.add_header('Content-ID' ,'<image1>')
#image["Content-Disposition"] = 'attachment; filename="testimage.png"'
#msg.attach(image)

# 构造html
# 发送正文中的图片:由于包含未被许可的信息，网易邮箱定义为垃圾邮件，报554 DT:SPM ：<p><img src="cid:image1"></p>
#html = """
#<html>
#  <head></head>
#  <body>
#    <p>Hi!<br>
#       How are you?<br>
#       Here is the <a href="http://www.baidu.com">link</a> you wanted.<br>
#    </p>
#  </body>
#</html>
#"""
#text_html = MIMEText(html, 'html', 'utf-8')
#text_html["Content-Disposition"] = 'attachment; filename="texthtml.html"'
#msg.attach(text_html)

# 构造附件
#file = r'C:\\Users\\mynam\\Desktop\\Coinsuper_Test\\iovcusdt.log'
#sendfile =open(file, 'rb').read()
#text_att = MIMEText(sendfile, 'base64', 'utf-8')
#text_att["Content-Type"] = 'application/octet-stream'
# 以下附件可以重命名成aaa.txt
# text_att["Content-Disposition"] = 'attachment; filename="aaa.txt"'
# 另一种实现方式
# text_att.add_header('Content-Disposition', 'attachment', filename='aaa.txt')
# 以下中文测试不ok
# text_att["Content-Disposition"] = u'attachment; filename="中文附件.txt"'.decode('utf-8')
#msg.attach(text_att)

# 发送邮件


def sendMail(subject, text, attach_file=''):
    conf = cf.configer()
    # 设置smtplib所需的参数
    # 下面的发件人，收件人是用于邮件传输的。
    smtpserver = conf.getValueByKey("email", "smtpserver")
    sender = conf.getValueByKey("email", "sender")
    password = conf.getValueByKey("email", "password")
    receiver = eval(conf.getValueByKey("email", "receivers"))
    msg = MIMEMultipart('mixed')
    msg.attach(MIMEText(text, 'plain', 'utf-8'))
    if attach_file:
        with open(attach_file, 'rb') as f:
            # 设置附件的MIME和文件名，这里是png类型:
            text_att = MIMEText(f.read(), 'base64', 'utf-8')
            text_att["Content-Type"] = 'application/octet-stream'
            file = attach_file.split('\\')[-1]
            text_att.add_header('Content-Disposition', 'attachment', filename=('gbk', '', file))
            msg.attach(text_att)
    msg['Subject'] = Header(subject, 'utf-8')
    msg['from'] = sender
    msg['to'] = ';'.join(receiver)
    server = smtplib.SMTP_SSL()  # server = smtplib.SMTP()

    # server.set_debuglevel(1)

    server.connect(smtpserver, 465)

    # server = smtplib.SMTP_SSL(smtp_server,465)

    server.ehlo(smtpserver)

    server.login(sender, password)

    server.sendmail(sender, receiver, msg.as_string())

    server.quit()

    print('email has send out !')

    return True


