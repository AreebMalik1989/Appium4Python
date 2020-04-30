#!/usr/bin/env python
# coding: utf-8

import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from idna import unicode

from model.Tester import *


def _format_address(s):
    name, address = parseaddr(s)
    return formataddr((
        Header(name, 'utf-8').encode(),
        address.encode('utf-8') if isinstance(address, unicode) else address))


def run():

    sender = 'xxx@163.com'  # sender
    receiver = ['xxx@163.com']  # recipient

    # Sent email service address
    smtp = smtplib.SMTP_SSL("smtp.exmail.qq.com", port=465)
    username = 'xxx@163.com'
    password = 'xxxxxx'

    # Mail object
    msg_root = MIMEMultipart('related')
    msg_root['From'] = _format_address('autotest<%s>' % sender)
    for x in receiver:
        msg_root['to'] = _format_address('<%s>' % x)
    msg_root['Subject'] = '[Monkey]%s' % get_format_current_time()

    # Construct the attachment, that is the body of the message
    for listdir in Tester.lis:
        att = MIMEText(open('%s' % listdir, 'rb').read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="%s"' % listdir
        msg_root.attach(att)

    smtp.connect('smtp.exmail.qq.com')
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg_root.as_string())
    smtp.quit()


if __name__ == '__main__':
    run()
