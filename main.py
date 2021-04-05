from Classes import User, load_config, save_config, Email, Server


def main():
	# loading user configuration from json
	configuration = load_config()	# 1)

	#creating user object
	user = User(configuration)		# 2)

	# user's login/registration
	user.connect()					# 3)

	# creating mail login and password to connect to server
	email_object = Email(user)	# 4)

	#creating server object
	server = Server(email_object)		# 4)

	# starting server
	server.server_connection()			# 4)

	# Action loop trigger
	trigger = True

	while trigger:						# 5)

		print("Select from options: \n",
			"To send mail press `s` \n",
			"To receieve mail press `r` \n",
			"To exit the programm type `!exit")

		user_choice = input(": ")

		if user_choice == "!exit":

			print("Closing the client, goodbye")
			trigger = False

		elif user_choice == "s":
			server.email_object.creating_email_object()
			server.server_mail_send()	

		elif user_choice == "r":
			pass
			
	save_config(configuration)


if __name__ == '__main__':
	main() 
