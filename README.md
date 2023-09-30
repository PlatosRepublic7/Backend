This repo assumes you have a MySQL server installed, as well as having the sakila database active on that server.

This project is a basic web application for performing various simple operations with the sakila database.

In order to run the server you need to perform the following steps:
1. Set up a virtual environment within the main directory.
    - Command: py -m venv .venv
2. Activate the virtual environment (named .venv in the previous step).
    - Command: .venv/scripts/activate
3. Install the required libraries.
    - Command: pip install -r requirements.txt
4. Edit credentials.cfg for database connection.
    - Enter your Username, password, localhost for HOST, and the port for your MySQL server.
    - Save the file.
5. Start the Web Server.
    - Command: flask --app movieapp run
    - Add the --debug flag to the above command should you wish.

