from Classes import User, load_config, save_config
from Server_class import Server
from Email_class import Email


def main():
	# loading user configuration from json
	configuration = load_config()	# 1)

	#creating user object
	user = User(configuration)		# 2)

	# user's login/registration
	user.connect()					# 3)

	

	# creating server object and connecting to it
	server = Server(user)			# 4)
	server.server_connection()

	# Action loop trigger
	trigger = True

	# send/recv action loop
	while trigger:						# 5)

		print("Select from options: \n",
			"To send mail press `s` \n",
			"To receieve mail press `r` \n",
			"To exit the programm type `!exit`")

		user_choice = input(": ")

		if user_choice == "!exit":

			print("Closing the client, goodbye")
			trigger = False

		elif user_choice == "s":
			# creating email object
			email_object = Email(user, server)	# 6)
			email_object.creating_email_object() # 7)
			mail = email_object.multipart_mail() # 7)
			server.server_mail_send(email_object.to_addr, mail)	# 8)

		elif user_choice == "r":
			server.recv_server_connect()
			

	save_config(configuration)



if __name__ == '__main__':
	main() 
	