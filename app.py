from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_paccionm'
app.config['MYSQL_PASSWORD'] = '1546' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_paccionm'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/categories", methods=["POST", "GET"])
def manage_categories():
    if request.method == "POST":
        if request.form.get("Add_Category"):
            category_name = request.form["categoryName"]
            query = "INSERT INTO categories (name) VALUES (%s);"
            cur = mysql.connection.cursor()
            cur.execute(query, (category_name,))
            mysql.connection.commit()
        return redirect("/categories")

    if request.method == "GET":
        query = "SELECT * FROM categories;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        categories = cur.fetchall()
        return render_template("categories.html", categories=categories)


@app.route("/delete_category/<int:id>")
def delete_category(id):
    query = "DELETE FROM categories WHERE id = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()
    return redirect("/categories")


@app.route("/update_category/<int:id>", methods=["POST", "GET"])
def update_category(id):
    if request.method == "GET":
        query = "SELECT * FROM categories WHERE id = %s;" % id
        cur = mysql.connection.cursor()
        cur.execute(query)
        category = cur.fetchone()
        return render_template("update_category.html", category=category)

    if request.method == "POST":
        if request.form.get("Update_Category"):
            category_name = request.form["categoryName"]
            query = "UPDATE categories SET name = %s WHERE id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (category_name, id))
            mysql.connection.commit()
        return redirect("/categories")


# Listener
if __name__ == "__main__":
    #Start the app on port 55308, it will be different once hosted
    app.run(port=55308, debug=True)