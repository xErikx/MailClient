
import json
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import hashlib
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import imaplib
import email


# loading users json configuration file
def load_config():

	"""
    Loading configuration function:

    Loading json file configuration function for user's creds availability

    Attributes:
    	data: data variable consisting of json configuration file data

    Returns:
    
    ----------
    	Returns data as a container of user's creds

	"""

	with open ("users_json_config.json") as json_config_file:
		data = json.load(json_config_file)

	return data	


# creating and saving configuration data for users in json format
def save_config(data):

	"""
    Saving configuration function:

    Saving json file configuration function which saves
    user's creds as a json config. file in PC's memory

    Args:
	    data (str): user's creds
	        

	"""

	with open("users_json_config.json", "w") as json_config_file:
		json.dump(data, json_config_file)
		json_config_file.close()



# creating User class		
class User:

	"""
    A class used to represent User in email client

    ...

    Attributes
    ----------
    nickname : str
        user's nickname for client
    password : str
        user's client password
    email_address : str
        user's email address to login to server
    email_address_password : str
        user's email address password to login to server

    Methods
    -------
    registration:
        User's registration to client
    login:
		User's login to client
    connect:
		User's options for logins/registration to client


    """

	def __init__(self, users_config):

		"""
        Parameters
        ----------
        users_config: user's creds in configuration file

        Attributes
		
		users_config: user config file
		key: key for encryption/decryption of the email address password
		salt: salt option for generation and use of the same key in the future


        """

		self.users_config = users_config
		self.key = None
		self.salt = b'\x85\xb2\xa5\xd9\xf8\x90\xd5\xd3\xfb\x0ct\xfd`\xb3z\xc2'

	# initial functions wich will ask the user if they want to
	# Login/Register	

	def registration(self):
		
		"""
	    Registration function:

	    Registration function, which stores user's creds
	    to configuration json file

	    Attributes:
        
	    ----------
	    self.nickname: user's nickname variable
	    self.password: user's mail client variable
	    self.email_address: user's email address to connect to server
	    self.email_address_password: ser's mail account password to login to mail server
	    self.password1: provided password, encoded for the further use as email password encryption/decryption key
	    self.key: key to decrypt and encrypt mail password
	 

    	"""

		# user's nickname attribute
		self.nickname = input("Please enter your nickname: ")
		# user's client password attribute
		self.password = input("Please enter your password: ")

		# user's email address password
		self.email_address = input("Enter your mail address which will be used for email client: ")

		# user's mail account password to login to mail server
		self.email_address_password = input("Enter your email password to login to server: ")

		# provided password, encoded for the further use as email password encryption/decryption key
		self.password1 = self.password.encode()

		self.kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
							 length=32,
							 salt=self.salt,
							 iterations=100000,
							 backend = default_backend())
		
		# this will be our key to decrypt and encrypt mail password
		self.key = base64.urlsafe_b64encode(self.kdf.derive(self.password1))


		# here will be our crypting variable
		self.crypter = Fernet(self.key)

		# this is our encrypted mail password to connect to server
		self.crypted_email_password = self.crypter.encrypt(self.email_address_password.encode())

		# decrypted email password to login to mail server
		self.decrypted_email_password = self.email_address_password
		

		# hashing our client password
		self.bytes_password = str.encode(self.password)
		self.hashed_password = hashlib.sha1(self.bytes_password)

		# our client password hashed
		self.hex_dig = self.hashed_password.hexdigest()

		

		# adding user's creds to configuration file
		self.users_config["users"].append({"nickname": self.nickname, "password": self.hex_dig, "email_address": self.email_address, "email_address_password": base64.encodestring(self.crypted_email_password).decode()})

	# logging in dunction for email client login
	def login(self):

		"""
	    Login function:

	    Login function, which provides logging in into client with user's creds
	    from json configuration file

	    Attributes:
        
	    ----------
	    self.nickname: user's nickname variable
	    self.password: user's mail client variable
	    self.email_address: user's email address to connect to server
	    self.email_address_password: ser's mail account password to login to mail server
	    self.password1: provided password, encoded for the further use as email password encryption/decryption key
	    self.key: key to decrypt and encrypt mail password
	 

    	"""

		# user's input
		self.nickname = input("Enter your nickname: ")

		# user's password input 
		self.password = input("Enter your password: ")

		# hashing our client password
		self.bytes_password = str.encode(self.password)
		self.hashed_password = hashlib.sha1(self.bytes_password)

		# our client password hashed
		self.hex_dig = self.hashed_password.hexdigest()


		connected = False

		while not connected:

			self.user_object = None

			# checking if the user's nickname is in the json list "users"
			for user_nickname in self.users_config["users"]:

				# if statement for user's nickname presence
				if self.nickname == user_nickname["nickname"]:
					print("Found the nickname")

					self.user_object = user_nickname


					# checking password
					if self.hex_dig == self.user_object["password"]:

						print("Login success")
						print(f"Hi {self.nickname}!")

						# our key reassigned to decrypt the password
						self.password1 = self.password.encode()

						self.kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
											 length=32,
											 salt=self.salt,
											 iterations=100000,
											 backend = default_backend())

						# import ipdb; ipdb.set_trace()
						
						# this will be our key to decrypt and encrypt mail password
						self.key = base64.urlsafe_b64encode(self.kdf.derive(self.password1))

						self.crypter = Fernet(self.key)

						# decrypted email account password
						self.decrypted_email_password = self.crypter.decrypt(base64.decodestring(user_nickname["email_address_password"].encode())).decode()

						# user's email address to login to email server
						self.email_address = user_nickname[ "email_address"]

						connected = True

					break

			if self.user_object == None:
				print("Sorry, your creds are wrong")
				self.nickname = input("Enter your nickname: ")

				self.password = input("Enter your password: ")

				# hashing our password
				self.bytes_password = str.encode(self.password)
				self.hashed_password = hashlib.sha1(self.bytes_password)
				
				# our password hashed
				self.hex_dig = self.hashed_password.hexdigest()
			

		



	# main Register, Login function
	def connect(self):

		"""
	    Connect function:

	    Connect function, which activates as the programm starts
	    providing Login?/Register option for user

	    Attributes:
        
	    ----------
	    choice: user's choice variable
	 

    	"""

		# ask user if register or login 

		print("Would You like to register or login? \n",
			"if you want to register press `r` \n",
			"if you want to login press `l` \n",
			"If you want to close the programm type `!exit`")

		# user's choice
		choice = str(input(": "))

		# loop for executing the login/register process,
		# and in case if user write's wrong initial,
		# programm will work untill it executes properly

		while True:

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

	"""
    A class used to represent Email object

    ...

    Attributes
    ----------
    msg: Email object which eventually will be send
	msg["From"]: user's email address, from which the mail will be sent in str() format inside the mail
	msg["To"]:  email address destination to send in str() format inside the mail 
	msg["Subject"]: email's subject in str() format inside the mail
	text: The main and complete email to send

    Methods
    -------
    creating_email_object:
        Email object create function
    multipart_mail:
		Multipart Email object function

    """

	def __init__(self, user, server):
		self.user = user
		self.server = server

	# email object to for send() function
	def creating_email_object(self):

		"""
	    Email object create function:

	    Function which creates email object to send it 
	    to a specific email address as user chooses

	    Attributes:
        
	    ----------
	    self.source: user's email address, from which the mail will be sent
		self.to_addr: email address destination to send
		self.subject: = email's subject
		self.body: = email's body
	 

    	"""
		
		self.source = self.user.email_address
		self.to_addr = input("Enter the address where to sent: ")
		self.subject = input("What's the subject?: ")
		self.body = input("Print the body: ")

	# creating the mail to pass it to server.send() function and send the email
	def multipart_mail(self):

		"""
	    Multipart Email object function:

	    Function which multiparts email object to send it 
	    to a specific email address as user chooses

	    Attributes:
        
	    ----------
	   	msg: Email object which eventually will be send
		msg["From"]: user's email address, from which the mail will be sent in str() format inside the mail
		msg["To"]:  email address destination to send in str() format inside the mail 
		msg["Subject"]: email's subject in str() format inside the mail
		text: The main and complete email to send

		Returns:
            Returns text varialbe as complete email to send
	 

    	"""

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

	"""
    A class used to represent Server object

    ...

    Attributes
    ----------
    msg: Email object which eventually will be send
	msg["From"]: user's email address, from which the mail will be sent in str() format inside the mail
	msg["To"]:  email address destination to send in str() format inside the mail 
	msg["Subject"]: email's subject in str() format inside the mail
	text: The main and complete email to send

    Methods
    -------
    server_connection:
        server connection function
    server_mail_send:
		sending function for server

    """

	def __init__(self, user, ip="smtp.mail.ru", port=465, recv_server="imap.mail.ru"):

		"""
  		Parameters
  		----------
  		user: user's parameter for using user creds
  		ip: server ip for connection
  		port: server port for connection

		"""

		self.user = user
		self.ip = ip
		self.port = port
		self.recv_server = recv_server
		

	# server connection function
	def server_connection(self):

		"""
	    Server connection function:

	    Function which connects email client to the email server
	    and logs in user's email adress to server for further actions

	    Attributes:
        
	    ----------
	   	server: server variable, providing all further actions with the server
	 

    	"""

		self.server = smtplib.SMTP_SSL(self.ip, self.port)
		print("connected to server")

		self.server.ehlo()
		print("started server")

		
		self.server.login(self.user.email_address, self.user.decrypted_email_password)
		print("logged in")



	# sending fucntion for the server
	def server_mail_send(self, to, msg):

		"""
		Server send function:

		Server send function which sends the email to the custom email address

		Attributes:
	
	   		server: server variable, providing all further actions with the server

	    Args:
	        to (str): destination parameter
	        msg (str): email parameter.

	    """
		self.to = to
		self.msg = msg



		# eventual email send
		self.server.sendmail(self.user.email_address, self.to, self.msg) 
		print("Mail send!")

	# receiving email server connection
	def recv_server_connect(self):

		self.email = self.user.email_address
		self.password = self.user.decrypted_email_password	

		mail = imaplib.IMAP4_SSL(self.recv_server)
		mail.login(self.email, self.password)

		mail.list()
		mail.select("inbox")

		result, data = mail.search(None, "ALL")

		ids = data[0]
		id_list = ids.split()
		latest_email_id = id_list[-1]

		result, data = mail.fetch(latest_email_id, "(RFC822)")
		raw_email = data[0][1]
		raw_email_string = raw_email.decode('utf-8')


		email_message = email.message_from_string(raw_email_string)

		print(40 * "--" + "\n")

		print(f"Message is to: {email_message['To']}")
		print(f"Message is from: {email_message['From']}")
		print(f"Date: {email_message['Date']}")
		print(f"Subject: {email_message['Subject']}")
		print(f"Message ID: {email_message['Message-Id']}")

		print(40 * "--" + "\n")


		if email_message.is_multipart():
		    for payload in email_message.get_payload():
		        body = payload.get_payload(decode=True).decode('utf-8')
		        print(body)
		else:
		    body = email_message.get_payload(decode=True).decode('utf-8')
		    print(body)