from flask_app import app
from flask import render_template, redirect, request, session, flash
# Import your models
from flask_app.models import user, recipe 
from flask_bcrypt import Bcrypt       


# Route that will show the add form - visible route
@app.route("/recipes/new")
def  add_recipe_page():
    #1. Check to see if someone is logged in 
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    return render_template("add_recipe.html", user = user.User.get_by_id(data)) 

@app.route("/recipes/add_to_db", methods=["POST"]) 
def add_recipe_to_database():
        #1. Check to see if someone is logged in 
    if "user_id" not in session:
        return redirect("/")
    #2. Validate 
    if not recipe.Recipe.validate_recipe(request.form):
        # Always redirect to the route you were at last!!
        return redirect("/recipes/new")
    #3 Create data dictionary 
    data = {
        "name": request.form["name"],
        "under30": request.form["under30"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_made": request.form["date_made"],
        "user_id": session["user_id"] # IMPORTANT: REMEMBER to link the logged in user when creating the game 
    }
    # 4 Call on the query to edit to the database
    recipe.Recipe.add_recipe(data)
    #5 Redirect back to the dashboard
    return redirect("/dashboard")


    #Route that will show individual recipe. 
@app.route("/recipes/<int:id>")
def view_one_recipe_page(id):
    #1 Check to see if someone is logged in 
    if "user_id" not in session:
        return redirect("/")
    recipe_data ={
        "id": id,
    }
    return render_template("view_recipe.html", this_recipe = recipe.Recipe.get_one_recipe_with_user(recipe_data))


@app.route("/recipes/<int:id>/edit")
def edit_recipe_page(id):
    #1 Check to see if someone is logged in 
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id,
    }
    return render_template("edit_recipe.html", this_recipe = recipe.Recipe.get_one_recipe_with_user(data))


@app.route("/recipes/<int:id>/edit_in_db", methods=["POST"])
def edit_recipe_to_database(id):
        #1. Check to see if someone is logged in 
    if "user_id" not in session:
        return redirect("/")
        #2. Validate 
    if not recipe.Recipe.validate_recipe(request.form):
        # Always redirect to the route you were at last!!!
        return redirect(f"/recipes/{id}/edit")
    #3 Create data dictionary 
    data = {
        "name": request.form["name"],
        "under30": request.form["under30"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_made": request.form["date_made"],
        "id": id,
    }
    # 4 Call on the query to edit to the database
    recipe.Recipe.edit_recipe(data)
    #5 Redirect back to the dashboard
    return redirect("/dashboard")


@app.route("/recipes/<int:id>/delete")
def delete_recipe(id):
    #1 check t o see if someone is logged in 
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id, #ID of recipe
    }
    recipe.Recipe.delete(data)
    return redirect("/dashboard")