ADI Lab Technical Challenge Project Description
-----------------------------------------------

Author information
------------------
Name: Yuanyuting Wang
Email: yw3241@columbia.edu

Project Description:
--------------------
	The project is implemented to accommodate two types of queries:

	1. Query about density information in a specified building: by going to
	/localhost:5000/information/<building_name>, the user can receive a list
	of statistics representing the crowdedness, represented in percentage,
	of the registered rooms in this building.

	2. Query about the least crowded k placed on campus: by going to
	/localhost:5000/information/<k>, with k being a positive integer, the
	user can check out a list of k least crowded placed on campus according to
	the latest data.

Running the Project:
--------------------
	1. go to http://density.adicu.com/auth, and obtain the authentication token by
	logging in using the user's own Columbia email.
	2. go to project directory, and edit the .env file to contain the following line:
		API_KEY=<the_token_you_just_acquired>
	3. $ export FLASK_APP=app.py
	4. $ flask run
	5. enter queries with respect to /localhost:5000 in a new web page

Design Features:
----------------
	1. The building name is not case sensitive, but assumes that all spaces
	are replaced by underscores. If received invalid building name or negative
	integers, an error message will pop up to notify the user.

	2. The app interfaces with Density API through two urls:
	http://density.adicu.com/latest and
	http://density.adicu.com/latest/building/<building_name>. Before all requests,
	a dictionary of building name-key pairs is compiled and stored to ensure later
	direct interaction specifically with the second url.

	3. The authentication token is saved in .env in the project folder and referenced
	in app.py through using the package dotenv. The .env is not publicly shared,
	which means users are required to set up their own environment following the steps
	delineated in <Running the Project> and using their own Columbia emails. After much
	thought, this is deemed as the best practice compared to other practices that
	may involve web driver etc, for reasons of security and technical complexity.
