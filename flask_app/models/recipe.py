from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app # to display flash messages
from flask_app.models import user 
from flask import flash

class Recipe:
    schema_name = "recipe"

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.under30 = data["under30"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_made = data["date_made"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user = None # Placeholder linking the user to this one game


    # Method to add a recipe to the database
    @classmethod
    def add_recipe(cls, data):
        query = "INSERT INTO recipes (name, under30, description, instructions, date_made, user_id) VALUES (%(name)s, %(under30)s, %(description)s, %(instructions)s, %(date_made)s, %(user_id)s);"
        results = connectToMySQL(cls.schema_name).query_db(query, data)
        return results

        # Get all recipes with the users 
    @classmethod
    def get_all_recipes_with_users(cls):
        # it's a join because we're starting with the recipes table(many side)
        query = "SELECT * FROM recipes JOIN users on users.id = recipes.user_id;" # query the data from the database
        results = connectToMySQL(cls.schema_name).query_db(query)
        if len(results) < 1: # if no recipes are found
            return None
        else: 
            all_recipes = [] # List that will hold Recipes  with Users
            for each_recipe in results: # Each item is a dictionary holding info about a recipe and user who added it 
                recipe_instance = cls(each_recipe)  # This creates a recipe clas ssintance form the information for each database row
                # Grab the data for the user 
                user_data = {
                    "id": each_recipe["users.id"],
                    "first_name": each_recipe["first_name"],
                    "last_name": each_recipe["last_name"],
                    "email": each_recipe["email"],
                    "password": each_recipe["password"],
                    "created_at": each_recipe["users.created_at"],
                    "updated_at": each_recipe["users.updated_at"],
                }
                # Create the User class isntance that's in the user.py model file
                recipe_creator = user.User(user_data)
                # Link the Recipe to this User
                recipe_instance.user = recipe_creator
                # Add this  recipe to the list 
                all_recipes.append(recipe_instance)
            return all_recipes 

    # Get one game made by the user - view recipe 
    @classmethod 
    def get_one_recipe_with_user(cls, data):
        query = "SELECT * from recipes JOIN users on users.id = recipes.user_id WHERE recipes.id = %(id)s;"# query the data from the database
        results = connectToMySQL(cls.schema_name).query_db(query, data) 
        if len(results) < 1: # If no recipes are found 
            return None
        else: 
            #create the recipe class instance
            one_recipe = cls(results[0]) # Need 0 because the variable results is a list; creating the recipe. 
                # Grab the data for the user
            user_data = {
                "id": results[0]["users.id"],
                "first_name": results[0]["first_name"],
                "last_name": results[0]["last_name"],
                "email": results[0]["email"],
                "password": results[0]["password"],
                "created_at": results[0]["users.created_at"],
                "updated_at": results[0]["users.updated_at"]
            }
                # Create the User class instance 
            recipe_creator = user.User(user_data)
            # Link the recipe to this User
            one_recipe.user = recipe_creator 
            # Return the recipe
            return one_recipe

    @classmethod  
    def edit_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, under30 = %(under30)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s  WHERE id = %(id)s;"
        return connectToMySQL(cls.schema_name).query_db(query, data) 

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.schema_name).query_db(query, data) 


    @staticmethod
    def validate_recipe(form_data):
        print(form_data)
        is_valid = True
        # Check to see if game is long enough
        if len(form_data["name"]) < 3: 
            is_valid = False
            flash("Recipe name must be at least 3 characters long")
        if len(form_data["description"]) < 3: 
            is_valid = False
            flash("Description must be at least 3 characters long")
        if len(form_data["name"]) < 3: 
            is_valid = False
            flash("Instructions name must be at least 3 characters long")
        return is_valid
        
        
