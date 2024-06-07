# Citation for the following code:
# Date: 05/22/2024
# Adapted from:
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
# Exploration - Developing in Flask: https://canvas.oregonstate.edu/courses/1958399/pages/exploration-developing-in-flask?module_item_id=24181857
from flask import Blueprint, request, redirect, flash, render_template, current_app
from . import accounts_bp

@accounts_bp.route("/", methods=["POST", "GET"])
def manage_accounts():
    mysql = current_app.extensions['mysql']
    
    if request.method == "POST":
        # Retrieve form data
        cur = mysql.connection.cursor()
        user_id = request.form["userID"]
        balance = request.form["currentBalance"]

        # Insert a new account into the Accounts table
        query = "INSERT INTO Accounts (userID, currentBalance) VALUES (%s, %s);"
        cur.execute(query, ( user_id, balance ))
        mysql.connection.commit()
        flash("Account added successfully!", "success")
        return redirect("/accounts")

    if request.method == "GET":
        # Retrieve all accounts along with user names
        query = """
            SELECT Accounts.accountID, Accounts.userID, Accounts.currentBalance, Users.userName
            FROM Accounts
            JOIN Users ON Accounts.userID = Users.userID;
        """
        cur = mysql.connection.cursor()
        cur.execute(query)
        accounts = cur.fetchall()

        # Retrieve all users to populate the userID dropdown
        query2 = "SELECT userID FROM Users;"
        cur.execute(query2)
        users = cur.fetchall()
        
        return render_template("accounts.j2",accounts=accounts, users=users)