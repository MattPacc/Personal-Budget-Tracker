from flask import Blueprint, request, redirect, flash, render_template, current_app, url_for
from flask_mysqldb import MySQLdb
from . import expenses_bp

@expenses_bp.route("/", methods=["POST", "GET"])
def manage_expenses():
    mysql = current_app.extensions['mysql']
    if request.method == "POST":
        cur = mysql.connection.cursor()
        user_id = request.form["userID"]
        account_id = request.form["accountID"]
        category_id = request.form["expenseCategory"]
        amount = request.form["expenseAmount"]
        date_spent = request.form["expenseDate"]
        description = request.form["description"]
        expense_id = request.form.get("expenseID")

        query = """
        INSERT INTO Expenses (userID, accountID, amount, dateSpent, description)
        VALUES (%s, %s, %s, %s, %s);
        """
        cur.execute(query, (user_id, account_id, amount, date_spent, description))

        expense_id = cur.lastrowid

        query2 = "INSERT INTO ExpensesCategoriesLink (expenseID, categoryID) VALUES (%s, %s);"
        cur.execute(query2, (expense_id, category_id))

        mysql.connection.commit()
        flash("Expense added successfully!", "success")

        return redirect("/expenses")

    if request.method == "GET":
        query = """
            SELECT e.expenseID, e.amount, e.dateSpent, e.description, 
                   ecl.categoryID, c.categoryName
            FROM Expenses e
            LEFT JOIN ExpensesCategoriesLink ecl ON e.expenseID = ecl.expenseID
            LEFT JOIN Categories c ON ecl.categoryID = c.categoryID;
        """
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        expenses = {}
        expense_category_links = []
        for row in data:
            if row['expenseID'] not in expenses:
                expenses[row['expenseID']] = {'expenseID': row['expenseID'], 'amount': row['amount'], 
                                              'dateSpent': row['dateSpent'], 'description': row['description'], 'categoryName': row['categoryName']}
            if row['categoryID']:
                expense_category_links.append({'expenseID': row['expenseID'], 'amount': row['amount'],
                                               'dateSpent': row['dateSpent'], 'description': row['description'],
                                               'categoryID': row['categoryID'], 'categoryName': row['categoryName']})

        expenses = list(expenses.values())

        query2 = "SELECT * FROM Categories;"
        cur.execute(query2)
        categories = cur.fetchall()

        query3 = "SELECT userID, userName FROM Users;"
        cur.execute(query3)
        users = cur.fetchall()

        query4 = "SELECT accountID FROM Accounts;"
        cur.execute(query4)
        accounts = cur.fetchall()


        return render_template("expenses.j2", expenses=expenses, expense_category_links=expense_category_links, categories=categories, users=users, accounts=accounts)


@expenses_bp.route("/update_expense/<int:expenseID>/", methods=["POST", "GET"])
def update_expense(expenseID):
    mysql = current_app.extensions['mysql']
    if request.method == "GET":
        query = """
            SELECT e.expenseID, e.amount, e.dateSpent, e.description, ecl.categoryID
            FROM Expenses e
            LEFT JOIN ExpensesCategoriesLink ecl ON e.expenseID = ecl.expenseID
            WHERE e.expenseID = %s;
        """
        cur = mysql.connection.cursor()
        cur.execute(query, (expenseID,))
        expense = cur.fetchone()

        query2 = "SELECT * FROM Categories;"
        cur.execute(query2)
        categories = cur.fetchall()

        return render_template("update_expense.j2", expense=expense, categories=categories)

    if request.method == "POST":
        amount = request.form["expenseAmount"]
        date_spent = request.form["expenseDate"]
        description = request.form["description"]
        category_id = request.form["expenseCategory"]
        user_id = request.form["userID"]
        account_id = request.form["accountID"]
        expense_id = request.form["expenseID"]

        query = """
        UPDATE Expenses 
        SET amount = %s, dateSpent = %s, description = %s 
        WHERE expenseID = %s AND userID = %s AND accountID = %s;
        """
        cur = mysql.connection.cursor()
        cur.execute(query, (amount, date_spent, description, expense_id, user_id, account_id))

        query2 = "REPLACE INTO ExpensesCategoriesLink (expenseID, categoryID) VALUES (%s, %s);"
        cur.execute(query2, (expense_id, category_id))

        mysql.connection.commit()
        flash("Expense updated successfully!", "success")
        return redirect("/expenses")



@expenses_bp.route("/delete_expense/<int:expenseID>", methods=["POST", "GET"])
def delete_expense(expenseID):
    mysql = current_app.extensions['mysql']
    cur = mysql.connection.cursor()
    delete_expense_query = "DELETE FROM Expenses WHERE expenseID = %s;"
    cur.execute(delete_expense_query, (expenseID,))

    mysql.connection.commit()
    flash("Expense deleted successfully!", "success")

    cur.close()
    return redirect("/expenses")


@expenses_bp.route("/filter", methods=["GET"])
def filter_expenses():
    mysql = current_app.extensions['mysql']
    category_id_filter = request.args.get("categoryIdFilter")

    cur = mysql.connection.cursor()

    query = """
        SELECT e.expenseID, e.amount, e.dateSpent, e.description, 
               ecl.categoryID, c.categoryName
        FROM Expenses e
        LEFT JOIN ExpensesCategoriesLink ecl ON e.expenseID = ecl.expenseID
        LEFT JOIN Categories c ON ecl.categoryID = c.categoryID
    """

    if category_id_filter == "0":
        return redirect(url_for('expenses_bp.manage_expenses'))
    elif category_id_filter == "1":
        query += " WHERE ecl.categoryID IS NULL"
        cur.execute(query)
    else:
        query += " WHERE ecl.categoryID = %s"
        cur.execute(query, (category_id_filter,))

    expenses = cur.fetchall()

    # Query to fetch all expense-category links
    query_links = """
        SELECT ecl.expenseID, e.amount, e.dateSpent, e.description, 
               ecl.categoryID, c.categoryName
        FROM ExpensesCategoriesLink ecl
        JOIN Expenses e ON ecl.expenseID = e.expenseID
        JOIN Categories c ON ecl.categoryID = c.categoryID
    """
    cur.execute(query_links)
    expense_category_links = cur.fetchall()

    # Fetch categories, users, and accounts for dropdowns
    query2 = "SELECT * FROM Categories;"
    cur.execute(query2)
    categories = cur.fetchall()

    query3 = "SELECT userID, userName FROM Users;"
    cur.execute(query3)
    users = cur.fetchall()

    query4 = "SELECT accountID FROM Accounts;"
    cur.execute(query4)
    accounts = cur.fetchall()

    return render_template("expenses.j2", expenses=expenses, expense_category_links=expense_category_links, categories=categories, users=users, accounts=accounts, selected_category=category_id_filter)
