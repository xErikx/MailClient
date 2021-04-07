
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
		self.email_address = input("Enter your mail address which will be used for email client: ")
		self.__email_address_password = input("Enter your email password to login to server: ")

		# adding user to configuration
		self.users_config["users"].append({"nickname": self.nickname, "password": self.__password, "email_address": self.email_address, "email_address_password": self.__email_address_password})


	def login(self):
		# user's input
		self.nickname = input("Enter your nickname")


		# checking if the user's nickname is in the json list "users"
		if self.nickname not in self.users_config["users"]:
			print("Your nickname is incorrect, please insert correct nickname")
			self.nickname = input("Enter your nickname")
		else:

			# user's password input 
			self.__password = input("Enter your password")

			# if nickname is in the list
			for name in self.users_config["users"]:

				if self.nickname == name["nickname"] and self.__password == name["password"]:

					print("The nickname and password are correct")
					print(f"Hi {self.nickname}!")
					break

				elif self.nickname == name["nickname"] and self.__password != name["password"]:

					print("Your password is incorrect, please enter correct password")
					self.__password = self.__password = input("Enter your password")




	# main Register, Login function
	def connect(self):

		# ask user if register or login 

		print("Would You like to register or login? \n",
			"if you want to register press `r` \n",
			"if you want to login press `l` \n",
			"If you want to close the programm type `!exit`")

		# user's choice
		choice = str(input())

		# loop for executing the login/register process,
		# and in case if user write's wrong initial,
		# programm will work untill it executes properly

		while choice:

			# register option
			if choice == "r":
				self.registration()
				break

			# login option
			elif choice == "l":
				self.login()
				break

			# programm exit option
			elif choice == "!exit":
				print("Closing the programm...")
				print("Goodbye!")
				break

			else:
				print("Please enter valid choice")
				choice = str(input())



class Email:

	def __init__(self, user, server):
		self.user = user
		self.server = server

	# email object to for send() function
	def creating_email_object(self):
		
		self.source = self.user.email_address
		self.to_addr = input("Enter the address where to sent: ")
		self.subject = input("What's the subject?: ")
		self.body = input("Print the body: ")

	# creating the mail to pass it to server.send() function and send the email
	def multipart_mail(self):
		# creating multipart for our email
		self.msg = MIMEMultipart()

		# address of the receiver
		self.msg["From"] = self.source

		# address of the sender
		self.msg["To"] = self.to_addr	 

		# the subject of the email
		self.msg["Subject"] = self.subject

		# attaching the text of the email
		self.msg.attach(MIMEText(self.body, "plain"))

		# formatting email as str to send
		self.text = self.msg.as_string()

		return self.text



# creating server class for further communication
class Server:
	def __init__(self, user, ip="smtp.mail.ru", port=465):
		self.user = user
		self.ip = ip
		self.port = port
		

	# server connection function
	def server_connection(self):
		self.server = smtplib.SMTP_SSL(self.ip, self.port)
		print("connected to server")

		self.server.ehlo()
		print("started server")

		self.server.login(self.user.email_address, "kohoioki11")
		print("logged in")



	# sending fucntion for the server
	def server_mail_send(self, to, msg):
		self.to = to
		self.msg = msg

		# eventual email send
		self.server.sendmail(self.user.email_address, self.to, self.msg) 
		print("Mail send!")