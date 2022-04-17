from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app # to display flash messages
# Import other models as needed:
from flask import flash
from flask_app.models import recipe
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
# PASSWORD REGEX = re.compile() # https://www.ocpsoft.org/tutorials/regular-expressions/password-regular-expression/
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)
# Import other models as needed:

class User:
    schema_name = "recipe"

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = [] # List because one user can make many games. 

    @classmethod 
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.schema_name).query_db(query, data)


    @classmethod 
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.schema_name).query_db(query, data)
        print(results)
        if len(results) == 0:
            return None
        else: 
            return cls(results[0])

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.schema_name).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    #Grabs all the recipes by one user - we're grabbing a specific user's recipe which is why we are starting with the user's table. 
    # Now that we are starting with the user's table, we have to LEFT JOIn because it is possible that a user has not added recipe yet. 
    # view/recipe/<int:id>
    @ classmethod
    def user_with_all_games(cls, data):
        query = "SELECT * FROM users LEFT JOIN recipes on users.id = recipes.user_id  WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.schema_name).query_db(query, data) 
        if len(results) < 1: # No usersare found 
            return None
        else:
            this_user = cls(results[0])
            # Loop through each recipe made by the user
            for row in results: # Each item is a dictionary holding info about a recipe and the user who added it 
                # Grab the data for the uder 
                row = {
                    "id": row["recipes.id"], # change it from user to recipes because recipes is the table we are joining 
                    "name": row["name"],
                    "under30": row["under30"],
                    "description": row["description"],
                    "instructions": row["instructions"],
                    "date_made": row["date_made"],
                    "created_at": row["recipes.created_at"],
                    "updated_at": row["recipes.updated_at"],
                }
                # Create the recipe
                this_recipe_instance = recipe.Recipe(row)
                # Link the user to the recipe
                this_user.recipes.append(this_recipe_instance)
            return this_user 

# What kind of method do we need into order to perform our validations? check our data looks good first before we allow a new user ot be registered in our database 
    @staticmethod 
    def validate_registration(form_data):
        is_valid = True # Assume for now everything in the form is good 
            #  first name 
        if len(form_data['first_name']) < 3:
            is_valid = False 
            flash("First name must be atleast 3 characters.", "register")
            # last name
        if len(form_data['last_name']) < 3:
            is_valid = False 
            flash("Last name must be atleast 3 characters.", "register")
            # email
        if len(form_data['email']) < 3:
            is_valid = False 
            flash("Email must be atleast 3 characters.", "register")
        if not EMAIL_REGEX.match(form_data['email']): # if email pattern doesn't match ??????
            is_valid = False
            flash("Email is invalid !")
        # Checking to make sure email is unique
        data = {
            "email": form_data["email"]
        }
        found_user_or_false = User.get_by_email(data)
        if found_user_or_false != False: 
            is_valid = False 
            flash("Email is aready registered.", "register")
        # Check to see if the password is long enough
        if len(form_data['password']) < 8:
            is_valid = False 
            flash("Password must be atleast 8 characters.", "register") 
            #check to see if the passwords match
        if form_data["password"] != form_data["confirm_password"]:
            is_valid = False
            flash("Passwords must agree.", "register")
        return is_valid 

    @staticmethod
    def validate_login(form_data):
        is_valid = True # Assume for now everything in the form is good 
        # Check to see if the email exists in the database 
        email_data = {
            "email": form_data["email"]
        }
        found_user_or_false = User.get_by_email(email_data)
        # if we dont find anybody, who cares about the password. 
        if found_user_or_false == False:
            is_valid = False
            flash("Invalid login credentials.", "login")
            return is_valid 
        #if we do find somebody, then check the password
        if not bcrypt.check_password_hash(found_user_or_false.password, form_data['password']):
            # if we get False after checking the password
            is_valid = False 
            flash("Invalid login credentials.", "login")
        return is_valid