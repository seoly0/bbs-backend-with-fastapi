import smtplib
from ast import literal_eval
from email.mime.text import MIMEText
from os.path import abspath, dirname, join

import jinja2

from core.entity import Mail
from settings import ENV


def get_client() -> smtplib.SMTP:
    smtp = smtplib.SMTP(ENV.SMTP_HOST, ENV.SMTP_PORT)
    smtp.starttls()  # TLS 사용시 필요
    smtp.login(ENV.SMTP_USER, ENV.SMTP_KEY)

    return smtp


def get_builder() -> jinja2.Environment:
    path = join(dirname(abspath(__file__)), "template")
    loader = jinja2.FileSystemLoader(searchpath=path)
    return jinja2.Environment(loader=loader)


def send_bulk(mail_list: list[Mail]):
    client = get_client()
    builder = get_builder()  # 원래 for문 안에 있었음. 문제시 되돌리기.

    for mail in mail_list:
        template = builder.get_template(mail.template)
        context = literal_eval(mail.context)
        content = template.render(**context)

        msg = MIMEText(content, "html")
        msg["Subject"] = mail.title
        client.sendmail(ENV.SMTP_SENDER, mail.target, msg.as_string())

    client.quit()


def send(mail: Mail):
    client = get_client()

    builder = get_builder()
    template = builder.get_template(mail.template)
    context = literal_eval(mail.context)
    content = template.render(**context)

    msg = MIMEText(content, "html")
    msg["Subject"] = mail.title
    client.sendmail(ENV.SMTP_SENDER, mail.target, msg.as_string().encode("utf-8"))

    client.quit()
