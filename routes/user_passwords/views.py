# Citation for the following code:
# Date: 05/22/2024
# Adapted from:
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
# Exploration - Developing in Flask: https://canvas.oregonstate.edu/courses/1958399/pages/exploration-developing-in-flask?module_item_id=24181857
from flask import Blueprint, request, redirect, flash, render_template, current_app
from . import user_passwords_bp

@user_passwords_bp.route("/", methods=["POST", "GET"])
def manage_passwords():
    mysql = current_app.extensions['mysql']
    
    if request.method == "POST":
        # Retrieve form data
        cur = mysql.connection.cursor()
        user_id = request.form["userID"]
        password = request.form["password"]

        # Insert a new user password into the UserPasswords table
        query = "INSERT INTO UserPasswords (userID, password) VALUES (%s, %s);"
        cur.execute(query, ( user_id, password))
        mysql.connection.commit()
        flash("Password added successfully!", "success")
        return redirect("/passwords")

    if request.method == "GET":
        # Retrieve all user passwords along with their user names
        query = """
            SELECT UserPasswords.userID, UserPasswords.password, Users.userName
            FROM UserPasswords
            JOIN Users ON UserPasswords.userID = Users.userID;

        """
        cur = mysql.connection.cursor()
        cur.execute(query)
        user_passwords = cur.fetchall()

        # Retrieve all users to populate the userID dropdown
        query2 = "SELECT userID FROM Users;"
        cur.execute(query2)
        users = cur.fetchall()
        
        return render_template("user_passwords.j2",user_passwords=user_passwords, users=users)