import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import EMAIL_LOGIN, EMAIL_PASSWORD


def send_reset_password_mail(email, token):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Восстановление пароля"
    msg['From'] = EMAIL_LOGIN
    msg['To'] = email

    html = f"""\
    <html>
      <head></head>
      <body>
        <p>
            <a href="http://localhost:5173/reset-password?token={token}">Нажмите сюда чтобы восстановить пароль</a>
        </p>
      </body>
    </html>
    """

    part2 = MIMEText(html, 'html')

    msg.attach(part2)

    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.login(EMAIL_LOGIN, EMAIL_PASSWORD)
    server.sendmail(EMAIL_LOGIN, email, msg.as_string())
    server.quit()
