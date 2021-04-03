from Classes import User, load_config, save_config, Email, Server


def main():
	# loading user configuration from json
	configuration = load_config()

	#creating user object
	user = User(configuration)
	user.connect()

	#creating server
	server = Server(email_object)

	# starting server
	server.server_connection()

	save_config(configuration)


if __name__ == '__main__':
	main()