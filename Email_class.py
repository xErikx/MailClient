from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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