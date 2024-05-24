from flask import Blueprint, request, redirect, flash, render_template, current_app
from flask_mysqldb import MySQLdb
from . import categories_bp

@categories_bp.route("/", methods=["POST", "GET"])
def manage_categories():
    mysql = current_app.extensions['mysql']
    if request.method == "POST":
        category_name = request.form["categoryName"]
        query = "INSERT INTO Categories (categoryName) VALUES (%s);"
        cur = mysql.connection.cursor()
        cur.execute(query, (category_name,))
        mysql.connection.commit()
        flash("Category added successfully!", "success")
        return redirect("/categories")


    if request.method == "GET":
        query = """
            SELECT c.categoryID, c.categoryName, 
                   ecl.expenseID, e.description as expenseDescription
            FROM Categories c
            LEFT JOIN ExpensesCategoriesLink ecl ON c.categoryID = ecl.categoryID
            LEFT JOIN Expenses e ON ecl.expenseID = e.expenseID;
        """
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        categories = {}
        category_expense_links = []
        for row in data:
            if row['categoryID'] not in categories:
                categories[row['categoryID']] = {'categoryID': row['categoryID'], 'categoryName': row['categoryName']}
            if row['expenseID']:
                category_expense_links.append({'categoryID': row['categoryID'], 'categoryName': row['categoryName'],
                                               'expenseID': row['expenseID'], 'expenseDescription': row['expenseDescription']})

        categories = list(categories.values())

        query2 = "SELECT * FROM Expenses;"
        cur.execute(query2)
        expenses = cur.fetchall()

        return render_template("categories.j2", categories=categories, category_expense_links=category_expense_links, expenses=expenses)

@categories_bp.route("/update_category/<int:categoryID>", methods=["POST", "GET"])
def update_category(categoryID):
    mysql = current_app.extensions['mysql']
    if request.method == "GET":
        query = "SELECT * FROM Categories WHERE categoryID = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (categoryID,))
        category = cur.fetchone()
        return render_template("update_category.j2", category=category)

    if request.method == "POST":
        category_name = request.form["categoryName"]
        query = "UPDATE Categories SET categoryName = %s WHERE categoryID = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (category_name, categoryID))
        mysql.connection.commit()
        flash("Category updated successfully!", "success")
        return redirect("/categories")

@categories_bp.route("/delete_category/<int:categoryID>", methods=["POST", "GET"])
def delete_category(categoryID):
    mysql = current_app.extensions['mysql']
    cur = mysql.connection.cursor()

    # Delete associated entries in ExpensesCategoriesLink
    delete_expenses_categories_link_query = "DELETE FROM ExpensesCategoriesLink WHERE categoryID = %s;"
    cur.execute(delete_expenses_categories_link_query, (categoryID,))

    # Delete the category
    delete_category_query = "DELETE FROM Categories WHERE categoryID = %s;"
    cur.execute(delete_category_query, (categoryID,))

    mysql.connection.commit()
    flash("Category deleted successfully!", "success")

    cur.close()

    return redirect("/categories")

@categories_bp.route("/delete_category_expense_link/<int:categoryID>/<int:expenseID>", methods=["POST"])
def delete_category_expense_link(categoryID, expenseID):
    mysql = current_app.extensions['mysql']
    query = "DELETE FROM ExpensesCategoriesLink WHERE categoryID = %s AND expenseID = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (categoryID, expenseID))
    mysql.connection.commit()
    return redirect("/categories")

@categories_bp.route("/link_expense_to_category", methods=["POST"])
def link_expense_to_category():
    mysql = current_app.extensions['mysql']
    expenseID = request.form["expenseID"]
    categoryID = request.form["categoryID"]
    try:
        query = "INSERT INTO ExpensesCategoriesLink (expenseID, categoryID) VALUES (%s, %s);"
        cur = mysql.connection.cursor()
        cur.execute(query, (expenseID, categoryID))
        mysql.connection.commit()
    except MySQLdb.IntegrityError as e:
        if e.args[0] == 1062:  # Duplicate entry error
            flash("This expense is already linked to the category.", "error")
        else:
            flash("An error occurred while linking the expense to the category.", "error")
    return redirect("/categories")