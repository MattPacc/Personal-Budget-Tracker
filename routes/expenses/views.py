# Citation for the following code:
# Date: 05/22/2024
# Adapted from:
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
# Exploration - Developing in Flask: https://canvas.oregonstate.edu/courses/1958399/pages/exploration-developing-in-flask?module_item_id=24181857
from flask import Blueprint, request, redirect, flash, render_template, current_app, url_for
from . import expenses_bp

@expenses_bp.route("/", methods=["POST", "GET"])
def manage_expenses():
    mysql = current_app.extensions['mysql']
    if request.method == "POST":
        # Retrieve form data
        cur = mysql.connection.cursor()
        user_id = request.form["userID"]
        account_id = request.form["accountID"]
        category_id = request.form["expenseCategory"]
        amount = request.form["expenseAmount"]
        date_spent = request.form["expenseDate"]
        description = request.form["description"]
        expense_id = request.form.get("expenseID")
        # Insert a new expense into the Expenses table
        query = """
        INSERT INTO Expenses (userID, accountID, amount, dateSpent, description)
        VALUES (%s, %s, %s, %s, %s);
        """
        cur.execute(query, (user_id, account_id, amount, date_spent, description))

        expense_id = cur.lastrowid
        # Insert a new record into the join table ExpensesCategoriesLink
        query2 = "INSERT INTO ExpensesCategoriesLink (expenseID, categoryID) VALUES (%s, %s);"
        cur.execute(query2, (expense_id, category_id))

        mysql.connection.commit()
        flash("Expense added successfully!", "success")

        return redirect("/expenses")

    if request.method == "GET":
        # Retrieve all expenses along with their category names
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

        # Retrieve all categories to populate the dropdown
        query2 = "SELECT * FROM Categories;"
        cur.execute(query2)
        categories = cur.fetchall()

        # Retrieve all users to populate the dropdown
        query3 = "SELECT userID, userName FROM Users;"
        cur.execute(query3)
        users = cur.fetchall()

        # Retrieve all accounts to populate the dropdown
        query4 = "SELECT accountID FROM Accounts;"
        cur.execute(query4)
        accounts = cur.fetchall()


        return render_template("expenses.j2", expenses=expenses, expense_category_links=expense_category_links, categories=categories, users=users, accounts=accounts)


@expenses_bp.route("/update_expense/<int:expenseID>/", methods=["POST", "GET"])
def update_expense(expenseID):
    mysql = current_app.extensions['mysql']
    if request.method == "GET":
        # Retrieve the specific expense by expenseID
        query = """
            SELECT e.expenseID, e.amount, e.dateSpent, e.description, ecl.categoryID
            FROM Expenses e
            LEFT JOIN ExpensesCategoriesLink ecl ON e.expenseID = ecl.expenseID
            WHERE e.expenseID = %s;
        """
        cur = mysql.connection.cursor()
        cur.execute(query, (expenseID,))
        expense = cur.fetchone()

        # Retrieve all categories to populate the dropdown
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

        # Update the expense in the Expenses table
        query = """
        UPDATE Expenses 
        SET amount = %s, dateSpent = %s, description = %s 
        WHERE expenseID = %s AND userID = %s AND accountID = %s;
        """
        cur = mysql.connection.cursor()
        cur.execute(query, (amount, date_spent, description, expense_id, user_id, account_id))

        # Handle the link between expense and category
        if category_id == 'NULL' or category_id == '':
            query2 = "DELETE FROM ExpensesCategoriesLink WHERE expenseID = %s;"
            cur.execute(query2, (expense_id,))
        else:
            query2 = "REPLACE INTO ExpensesCategoriesLink (expenseID, categoryID) VALUES (%s, %s);"
            cur.execute(query2, (expense_id, category_id))

        mysql.connection.commit()
        flash("Expense updated successfully!", "success")
        return redirect("/expenses")



@expenses_bp.route("/delete_expense/<int:expenseID>", methods=["POST", "GET"])
def delete_expense(expenseID):
    mysql = current_app.extensions['mysql']
    cur = mysql.connection.cursor()

    # Delete the expense from the Expenses table
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

    # Base query to retrieve expenses
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
