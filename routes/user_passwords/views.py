from flask import Blueprint, request, redirect, flash, render_template, current_app
from . import user_passwords_bp

@user_passwords_bp.route("/", methods=["POST", "GET"])
def manage_passwords():
    mysql = current_app.extensions['mysql']
    
    if request.method == "POST":
        cur = mysql.connection.cursor()
        user_id = request.form["userID"]
        password = request.form["password"]

        query = "INSERT INTO UserPasswords (userID, password) VALUES (%s, %s);"
        cur.execute(query, ( user_id, password))
        mysql.connection.commit()
        flash("Password added successfully!", "success")
        return redirect("/passwords")

    if request.method == "GET":
        query = """
            SELECT UserPasswords.userID, UserPasswords.password, Users.userName
            FROM UserPasswords
            JOIN Users ON UserPasswords.userID = Users.userID;

        """
        cur = mysql.connection.cursor()
        cur.execute(query)
        user_passwords = cur.fetchall()

        query2 = "SELECT userID FROM Users;"
        cur.execute(query2)
        users = cur.fetchall()
        
        return render_template("user_passwords.j2",user_passwords=user_passwords, users=users)