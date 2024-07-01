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

## Configuration

### Database Setup

The database schema (DDL) and data (DML) files are located in the database folder.
Update the database configuration in app.py:
Replace placeholder credentials (MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB) with your actual database credentials if deploying in a production environment.

### Database Files

database/schema.sql: Contains the database schema definition (DDL).
database/data.sql: Contains sample data for demonstration purposes (DML).

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

## Author
- Matthew J Paccione (@MattPacc)
- matthew.j.paccione@gmail.com

### Guides Referenced

#### Flask:
https://flask.palletsprojects.com/en/3.0.x/

#### Flask Blueprints:
https://flask.palletsprojects.com/en/3.0.x/blueprints/

#### Github SHH keys:
https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent