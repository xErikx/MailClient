
import json
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart



# creating and saving configuration data for users in json format
def save_config(data):
	with open("users_json_config.json", "w") as json_config_file:
		json.dump(json_config_file, data)


# loading users json configuration file
def load_config():
	with open ("users_json_config.json") as json_config_file:
		data = json.load(json_config_file)

	return data	


# creating User class		
class User:

	def __init__(self, users_config):
		self.users_config = users_config

	# initial functions wich will ask the user if they want to
	# Login/Register	

	def registration(self):


		self.nickname = input("Please enter your nickname: ")
		self.__password = input("Please enter your password: ")
		self.email_address = input("Enter your mail address which will be used, \
			for email client")

		# adding user to configuration
		self.users_config["users"].append({"nickname": self.nickname, "password": self.__password, "email_address": self.email_address})


	def login(self):
		# user's input
		self.nickname = input("Enter your nickname")
		self.__password = input("Enter your password")

		while True:

			for name in self.users_config["users"]:

				if self.nickname == name["nickname"] and self.__password == name["password"]:
					print("The nickname and password are correct")
					break

				else:
					print("Either the password or the nickname are incorrect")
					self.nickname = input("Enter your nickname")
					self.__password = input("Enter your password")




	# main Register, Login function
	def connect(self):

		# ask user if register or login 

		print("Would You like to register or login? \n",
			"if you want to register press `r` \n"
			"if you want to login press `l`")

		# user's choice
		choice = str(input())

		# loop for executing the login/register process,
		# and in case if user write's wrong initial,
		# programm will work untill it executes properly

		while choice != "r" and choice != "l":

			if choice == "r":
				self.registration()
				break

			elif choice == "l":
				self.login()
				break

			else:
				print("Please enter valid choice")
				choice = str(input())



class Email:

	def __init__(self, user):
		self.user = user

	# user's email and password to login into server
	def email_server_login(self):
		#user's email adress for sending and receiving
		self.mail_adress = self.user.email_address
		print(f"The mail will be sent from {self.mail_adress} adress") 
		self.__email_password = input("Enter your email password to login to server: ")

	# email object to for send() function
	def creating_email_object(self):
		
		self.to_addr = input("Enter the address where to sent: ")
		self.subject = input("What's the subject?: ")
		self.body = input("Print the body: ")


# creating server class for further communication
class Server:
	def __init__(self, email, ip="smtp.mail.ru", port=465):
		self.ip = ip
		self.port = port
		self.email = email

	# server connection function
	def server_connection(self):
		self.server = smtplib.SMTP_SSL(self.ip, self.port)
		print("connected to server")

		self.server.ehlo()
		print("started server")

		self.email.email_server_login()

		self.server.login(email.mail_adress, email.__email_password)
		print("logged in")



	# sending fucntion for the server
	def server_mail_send(self):
		# creating multipart for our email
		self.msg = MIMEMultipart()

		# address of the receiver
		self.msg["From"] = email.mail_adress

		# address of the sender
		self.msg["To"] = email.to_addr	 

		# the subject of the email
		self.msg["Subject"] = email.subject

		# attaching the text of the email
		self.msg.attach(MIMEText(email.body, "plain"))

		# formatting email as str to send
		self.text = msg.as_string()

		# eventual email send
		self.server.sendmail(email.mail_adress, email.to_addr, text) 