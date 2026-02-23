# DevHomesRepo
DevHomes is a real estate listing Django project. It holds multiple apartments and houses for sale, has a credit calculator function, and supports a message board for customers.


--- Tech Stack:---
  * Python 3.13+
  * Django (latest stable)
  * PostgreSQL
  * HTML / CSS
  * Django ORM
  * psycopg2-binary

--- Key features:---

The project contains three main apps:
  // Listings //
Users can create, edit and delete listings for properties for sale. They can also link them to messages and credit requests. 
-Property CRUD
-City and District relationships
-Many-to-many Amenities
-Dynamic search filtering
-Pagination

  //Accounts//
Users can create messages and link existing listings to their message.
-Contact inquiry submission
-Inquiry dashboard
-Status tracking (New, In Progress, Closed)
-CRUD for inquiries

  //Credit Calculator//
Users can estimate their monthly payment for their property credit.
-Loan calculation form
-Stores credit requests
-Dashboard for submitted requests

  //Homepage//
The homepage of the site offers statistics and key listings to the users. It also has a search field for easy call-to-action. 

--- Repo setup and Venv ---
1. Clone the repository
    * git clone <(https://github.com/marina-atanasova/DevHomesRepo)>
    * cd DevHomesDjango
2. Create and activate virtual environment
     * python -m venv venv
    * source venv/bin/activate   # macOS/Linux
    * venv\Scripts\activate      # Windows

--- DB Setup ---
1. Create a PostgreSQL instance locally:
    *createdb devhomes
2. Define the following variables (in a .env folder, or modify the db settings to use credentials there directly):
    * export DB_NAME=devhomes
    * export DB_USER=postgres
    * export DB_PASSWORD=yourpassword
    * export DB_HOST=localhost
    * export DB_PORT=5432
3. Run migrations:
   * python manage.py migrate

--- Requirements and startup ---
1. Set up the PostgreSQL and credentials as desctibed above.
2. Run 'pip install -r requirements.txt' to install the requirements file
   * for MAC ARM architecture the setup is psycopg2-binary. For other OS you can use psycopg2 directly.
3. (Optional) Populate the DB with sample data:
    * python manage.py seed_locations
    * python manage.py seed_amenities
    * python manage.py populate_db
    * python manage.py populate_inquiries
4. Run the server:
   * python manage.py runserver

--- Custom 404 Page ---
A custom 404 template is implemented (templates/404.html).
Django displays it only when Debug mode is false (by default, debug mode is True):
  DEBUG = False

To preview locally with styling, switch Debug mode to False in settings.py and run:
  python manage.py runserver --insecure




