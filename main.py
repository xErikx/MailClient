# import ipdb; ipdb.set_trace()
from Classes import User, load_config, save_config, Email, Server



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
			"To exit the programm type `!exit")

		user_choice = input(": ")

		if user_choice == "!exit":

			print("Closing the client, goodbye")
			trigger = False

		elif user_choice == "s":
			# creating email object
			email_object = Email(user, server)
			email_object.creating_email_object()
			email_object.server.server_mail_send(email_object.multipart_mail())	

		elif user_choice == "r":
			pass
			
	save_config(configuration)


if __name__ == '__main__':
	main() 
