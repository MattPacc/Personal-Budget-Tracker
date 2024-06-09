# Citation for the following code:
# Date: 05/22/2024
# Adapted from:
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
# Exploration - Developing in Flask: https://canvas.oregonstate.edu/courses/1958399/pages/exploration-developing-in-flask?module_item_id=24181857
from flask import Blueprint, request, redirect, flash, render_template, current_app
from flask_mysqldb import MySQLdb
from . import users_bp

@users_bp.route("/", methods=["POST", "GET"])
def manage_users():
    mysql = current_app.extensions['mysql']
    
    if request.method == "POST":
        try:
            # Retrieve form data
            cur = mysql.connection.cursor()
            user_name = request.form["userName"]
            email = request.form["email"]

            # Insert a new user into the Users table
            query = "INSERT INTO Users (userName, email) VALUES (%s, %s);"
            cur.execute(query, ( user_name, email))
            mysql.connection.commit()
            
            flash("Income source added successfully!", "success")
            return redirect("/users")
    
        except MySQLdb.IntegrityError as e:
            mysql.connection.rollback()
            if e.args[0] == 1062:  # Duplicate entry error
                flash("This username already exists, please use another.", "error")
            else:
                flash("An error occurred while creating a new user.", "error")
            return redirect("/users")

    if request.method == "GET":
        # Retrieve all users
        query = "SELECT userID, userName, email FROM Users;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        users = cur.fetchall()

        return render_template("users.j2",users=users)