import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


server = smtplib.SMTP_SSL("smtp.mail.ru", 465)
print("connected to server")

server.ehlo()
print("started server")


server.login("sample_mail", "password")
print("logged in")

msg = MIMEMultipart()
msg["From"] = "sample_mail"
msg["To"] = "sample_mail"	 #"df-fdf-2004@mail.ru"
msg["Subject"] = "Testing"

with open("message.txt", "r") as f:
	message = f.read()


msg.attach(MIMEText(message, "plain"))

text = msg.as_string()

server.sendmail("sample_mail", "sample_mail", text)


if __name__ == '__main__':
	main()

