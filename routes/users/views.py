from flask import Blueprint, request, redirect, flash, render_template, current_app
from . import users_bp

@users_bp.route("/", methods=["POST", "GET"])
def manage_users():
    mysql = current_app.extensions['mysql']
    
    if request.method == "POST":
        cur = mysql.connection.cursor()
        user_name = request.form["userName"]
        email = request.form["email"]

        query = "INSERT INTO Users (userName, email) VALUES (%s, %s);"
        cur.execute(query, ( user_name, email))
        mysql.connection.commit()
        flash("Income source added successfully!", "success")
        return redirect("/users")

    if request.method == "GET":
        query = "SELECT userID, userName, email FROM Users;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        users = cur.fetchall()

        return render_template("users.j2",users=users)