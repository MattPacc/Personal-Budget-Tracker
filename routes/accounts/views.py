from flask import Blueprint, request, redirect, flash, render_template, current_app
from . import accounts_bp

@accounts_bp.route("/", methods=["POST", "GET"])
def manage_accounts():
    mysql = current_app.extensions['mysql']
    
    if request.method == "POST":
        cur = mysql.connection.cursor()
        user_id = request.form["userID"]
        balance = request.form["currentBalance"]


        query = "INSERT INTO Accounts (userID, currentBalance) VALUES (%s, %s);"
        cur.execute(query, ( user_id, balance ))
        mysql.connection.commit()
        flash("Account added successfully!", "success")
        return redirect("/accounts")

    if request.method == "GET":
        query = """
            SELECT Accounts.accountID, Accounts.userID, Accounts.currentBalance, Users.userName
            FROM Accounts
            JOIN Users ON Accounts.userID = Users.userID;
        """
        cur = mysql.connection.cursor()
        cur.execute(query)
        accounts = cur.fetchall()

        query2 = "SELECT userID FROM Users;"
        cur.execute(query2)
        users = cur.fetchall()
        
        return render_template("accounts.j2",accounts=accounts, users=users)