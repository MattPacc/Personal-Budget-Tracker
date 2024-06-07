# CS340_database_project
# Personal Budget Tracker

## Overview

The **Personal Budget Tracker** is a web application built with Flask, designed to help users manage their personal finances by tracking income and expenses. It provides a user-friendly interface for setting budgets, monitoring transactions, and gaining financial insights.

## Features

- Track Income and Expenses
- Manage Expense Categories and their Associations
- View Accounts and Manage Income Sources
- Support for Multiple Users and High Transaction Volumes

## Installation

### Prerequisites

- Python 3.x
- pip
- Virtual environment (optional but recommended)

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/personal-budget-tracker.git
    ```

2. Navigate to the project directory:
    ```bash
    cd personal-budget-tracker
    ```

3. Create a virtual environment (optional but recommended):
    ```bash
    python3 -m venv venv
    ```

4. Activate the virtual environment:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

5. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

6. Set up the database:
    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

7. Run the application:
    ```bash
    flask run
    ```

## Usage

1. Open a web browser and navigate to `http://127.0.0.1:55308`.
2. Add your income sources and expenses.
3. Set your budget goals.
4. Monitor your financial status.

## Database Schema

### Users
  - `userID`: int, auto_increment, unique, PK
  - `userName`: varchar, unique, not NULL
  - `email`: varchar, unique, not NULL

### Accounts
  - `accountID`: int, auto_increment, unique, PK
  - `userID`: int, FK to Users (ON DELETE CASCADE, ON UPDATE CASCADE)
  - `currentBalance`: decimal(10,2), default 0.00

### Expenses
  - `expenseID`: int, auto_increment, unique, PK
  - `userID`: int, FK to Users (ON DELETE CASCADE, ON UPDATE CASCADE)
  - `accountID`: int, FK to Accounts (ON DELETE CASCADE, ON UPDATE CASCADE)
  - `amount`: decimal
  - `dateSpent`: date
  - `description`: text

### IncomeSources
  - `incomeID`: int, auto_increment, unique, PK
  - `userID`: int, FK to Users (ON DELETE CASCADE, ON UPDATE CASCADE)
  - `accountID`: int, FK to Accounts (ON DELETE CASCADE, ON UPDATE CASCADE)
  - `sourceName`: varchar
  - `amount`: decimal
  - `dateReceived`: date

### UserPasswords
  - `userID`: int, FK to Users (ON DELETE CASCADE, ON UPDATE CASCADE)
  - `password`: varchar, not NULL

### Categories
  - `categoryID`: int, auto_increment, unique, PK
  - `categoryName`: varchar, not NULL

### ExpensesCategoriesLink
  - `expenseID`: int, FK to Expenses (ON DELETE CASCADE, ON UPDATE CASCADE)
  - `categoryID`: int, FK to Categories (ON DELETE CASCADE, ON UPDATE CASCADE)


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Rajan Patel (TA) for feedback and guidance
- Peer reviewers for their constructive feedback and suggestions

## Citations

Code was Adapted from:

Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app

Exploration - Developing in Flask: https://canvas.oregonstate.edu/courses/1958399/pages/exploration-developing-in-flask?module_item_id=24181857

The code was mostly from these sources but has been modified in many different ways. The templating code is the most similar to the starter code for the Flask application. The Flask blueprinting configuration is original. However the routes are based on the starter app particularly the bsg_people_app portion. Citations are used where code was adapted and modified from the original.

The majority of the code in this project is based on the CS340 starter app. The templating code follows the structure of the starter code for the Flask application and the route implementations are largely adapted from the starter app as well, particularly from the `bsg_people_app` portion. Citations are provided wherever code has been adapted and modified from the original sources.


### Guides Referenced

#### Flask:
https://flask.palletsprojects.com/en/3.0.x/

#### Flask Blueprints:
https://flask.palletsprojects.com/en/3.0.x/blueprints/

#### Github SHH keys:
https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

