import smtplib
import imaplib
import email
import base64

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
  		recv_server: server imap address for receiving connection

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


	# base64 decoder function
	def base64_decoder(self, sample_item):

		splited_items = sample_item.split("?")

		if len(splited_items) < 4:
			return sample_item

		return base64.decodestring(splited_items[3].encode()).decode("utf")


	def recv_server_connect(self):
		"""
		Server receive function:

		Server receive function which receives email from custom email address
		using IMAP and receiving it from Mail.ru server

		Attributes:
	
	   		server: server variable, providing all further actions with the server
	   		mail: server connection variable


	    Args:
	        recv_server (str): server imap address for receiving connection
	    """

	    # user's email address
		self.email = self.user.email_address

		# user's email address password
		self.password = self.user.decrypted_email_password	

		# connection to server
		mail = imaplib.IMAP4_SSL(self.recv_server)
		mail.login(self.email, self.password)

		mail.list()
		mail.select("inbox")

		# getting the email data as list, consisting of emails
		result, data = mail.search(None, "ALL")

		# saving email id's 
		# for example data = [b'1 2 3 4 5']
		# so ids are b'1 2 3 4 5'
		ids = data[0]

		# spliting the list of email ids
		id_list = ids.split()

		counter = 1

		print("Which email you want to read?\n")

		# printing out last 10 emails, or if they are less than 10
		# printing the all existing emails
		if len(id_list) < 10:

			for email_ids in range(-1, -len(id_list) - 1, -1):
				
				# saving the last(newest) id of the email in box
				latest_email_id = id_list[email_ids]

				# getting the latest(newest) email in the box
				result, data = mail.fetch(latest_email_id, "(RFC822)")

				# saving unprocessed email in raw_email variable
				# example raw_email = b'Delivered-To: test.mail974@mail.ru\r\nReturn-path: <ernest.keryan@mail.ru>'
				raw_email = data[0][1]

				# decoding unprocessed email and saving it
				raw_email_string = raw_email.decode('utf-8')

				# getting the titles from the email(To, From, Date, Subject, Body, Message-ID)
				email_message = email.message_from_string(raw_email_string)

				# splitting from subject to get `From` header
				from_subject = email_message["From"].split(" ")

				main_from = self.base64_decoder(from_subject[0])

				email_subject = self.base64_decoder(email_message["Subject"])

				print(f"No.: {counter}) Message from: ({main_from}, \
					address: {from_subject[1]}), Subject is: {email_subject}, Date: {email_message['Date']}")
				
				counter += 1

			# user's choice to read email
			user_choice = int(input("Which mail?: \n"))

			# checking for user's correct answer
			while True:

				if user_choice > len(id_list):
					print("Please enter a valid choice")
					user_choice = int(input("Which mail?: \n"))
				else:
					break

			# saving the email under user's choosen id 
			email_id = id_list[user_choice * -1]

			# getting the latest(newest) email in the box
			result, data = mail.fetch(email_id, "(RFC822)")

			# saving unprocessed email in raw_email variable
			# example raw_email = b'Delivered-To: test.mail974@mail.ru\r\nReturn-path: <ernest.keryan@mail.ru>'
			raw_email = data[0][1]

			# decoding unprocessed email and saving it
			raw_email_string = raw_email.decode('utf-8')

			# getting the titles from the email(To, From, Date, Subject, Body, Message-ID)
			email_message = email.message_from_string(raw_email_string)

			# splitting from subject to get `From` header
			from_subject = email_message["From"].split(" ")

			main_from = self.base64_decoder(from_subject[0])

			email_subject = self.base64_decoder(email_message["Subject"])

			print(40 * "--" + "\n")

			print(f"Message is to: {email_message['To']}")
			print(f"Message is from: {main_from}, Address: {from_subject[1]}")
			print(f"Date: {email_message['Date']}")
			print(f"Subject: {email_subject}")
			print(f"Message ID: {email_message['Message-Id']}")

			print(40 * "--" + "\n")
		
			# checking if the email is multipart, 
			# if so we print each component, else, just printing out context
			if email_message.is_multipart():
			    for payload in email_message.get_payload():
			        body = payload.get_payload(decode=True).decode('utf-8')
			        print(body)
			else:
			    body = email_message.get_payload(decode=True).decode('utf-8')
			    print(body)

		else:

			# managing the last 10 emails 
			for email_ids in range(-1, -11, -1):
				
				# saving the last(newest) id of the email in box
				latest_email_id = id_list[email_ids]

				# getting the latest(newest) email in the box
				result, data = mail.fetch(latest_email_id, "(RFC822)")

				# saving unprocessed email in raw_email variable
				# example raw_email = b'Delivered-To: test.mail974@mail.ru\r\nReturn-path: <ernest.keryan@mail.ru>'
				raw_email = data[0][1]

				# decoding unprocessed email and saving it
				raw_email_string = raw_email.decode('utf-8')

				# getting the titles from the email(To, From, Date, Subject, Body, Message-ID)
				email_message = email.message_from_string(raw_email_string)

				# splitting from subject to get `From` header
				from_subject = email_message["From"].split(" ")

				main_from = self.base64_decoder(from_subject[0])

				email_subject = self.base64_decoder(email_message["Subject"])

				print(f"Number: {counter}) - Message from: ({main_from},  \
					address: {from_subject[1]}) , Subject is: {email_subject} , Date: {email_message['Date']}")
				
				counter += 1

			
			# user's choice to read email
			user_choice = int(input("Which mail?: \n"))

			# checking for user's correct answer
			while True:

				if user_choice > 10:
					print("Please enter a valid choice")
					user_choice = int(input("Which mail?: \n"))
				else:
					break

			# saving the email under user's choosen id 
			email_id = id_list[user_choice * -1]

			# getting the latest(newest) email in the box
			result, data = mail.fetch(email_id, "(RFC822)")

			# saving unprocessed email in raw_email variable
			# example raw_email = b'Delivered-To: test.mail974@mail.ru\r\nReturn-path: <ernest.keryan@mail.ru>'
			raw_email = data[0][1]

			# decoding unprocessed email and saving it
			raw_email_string = raw_email.decode('utf-8')

			# getting the titles from the email(To, From, Date, Subject, Body, Message-ID)
			email_message = email.message_from_string(raw_email_string)

			# splitting from subject to get `From` header
			from_subject = email_message["From"].split(" ")

			main_from = self.base64_decoder(from_subject[0])

			email_subject = self.base64_decoder(email_message["Subject"])

			print(40 * "--" + "\n")

			print(f"Message is to: {email_message['To']}")
			print(f"Message is from: {main_from}, Address: {from_subject[1]}")
			print(f"Date: {email_message['Date']}")
			print(f"Subject: {email_subject}")
			print(f"Message ID: {email_message['Message-Id']}")

			print(40 * "--" + "\n")

			# checking if the email is multipart, 
			# if so we print each component, else, just printing out context
			if email_message.is_multipart():
			    for payload in email_message.get_payload():
			        body = payload.get_payload(decode=True).decode('utf-8')
			        print(body)
			else:
			    body = email_message.get_payload(decode=True).decode('utf-8')
			    print(body)

