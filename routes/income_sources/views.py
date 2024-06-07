# Citation for the following code:
# Date: 05/22/2024
# Adapted from:
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
# Exploration - Developing in Flask: https://canvas.oregonstate.edu/courses/1958399/pages/exploration-developing-in-flask?module_item_id=24181857
from flask import Blueprint, request, redirect, flash, render_template, current_app
from . import income_sources_bp

@income_sources_bp.route("/", methods=["POST", "GET"])
def manage_income_sources():
    mysql = current_app.extensions['mysql']
    
    if request.method == "POST":
        # Retrieve form data
        cur = mysql.connection.cursor()
        user_id = request.form["userID"]
        account_id = request.form["accountID"]
        source_name = request.form["sourceName"]
        amount = request.form["amount"]
        date_received = request.form["dateReceived"]

        # Insert a new income source into the IncomeSources table
        query = "INSERT INTO IncomeSources (userID, accountID, sourceName, amount, dateReceived) VALUES (%s, %s, %s, %s, %s);"
        cur.execute(query, (user_id, account_id, source_name, amount, date_received))
        mysql.connection.commit()
        flash("Income source added successfully!", "success")
        return redirect("/income")

    if request.method == "GET":
        # Retrieve all income sources
        query = """
            SELECT userID, sourceName, amount, dateReceived
            FROM IncomeSources;
        """
        cur = mysql.connection.cursor()
        cur.execute(query)
        income_sources = cur.fetchall()

        # Retrieve all users to populate the userID dropdown
        query2 = "SELECT userID FROM Users;"
        cur.execute(query2)
        users = cur.fetchall()

        # Retrieve all accounts to populate the accountID dropdown
        query_accounts = "SELECT accountID FROM Accounts;"
        cur.execute(query_accounts)
        accounts = cur.fetchall()

        return render_template("income_sources.j2", income_sources=income_sources, users=users, accounts=accounts)