import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


server = smtplib.SMTP_SSL("smtp.mail.ru", 465)
print("connected to server")

server.ehlo()
print("started server")


server.login("test.mail974@mail.ru", "kohoioki11")
print("logged in")

msg = MIMEMultipart()
msg["From"] = "test.mail974@mail.ru"
msg["To"] = "chelovek.prostodushnyy@mail.ru"	 #"df-fdf-2004@mail.ru"
msg["Subject"] = "Testing"

with open("message.txt", "r") as f:
	message = f.read()


msg.attach(MIMEText(message, "plain"))

text = msg.as_string()

server.sendmail("test.mail974@mail.ru", "chelovek.prostodushnyy@mail.ru", text)


if __name__ == '__main__':
	main()

