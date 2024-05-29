# CS340_database_project
# Personal Budget Tracker

## Overview

The **Personal Budget Tracker** is a web application built with Flask, designed to help users manage their personal finances by tracking income and expenses. It provides a user-friendly interface for setting budgets, monitoring transactions, and gaining real-time financial insights.

## Features

- Track Income and Expenses
- Set and Monitor Budgets
- Real-Time Financial Insights
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

1. Open a web browser and navigate to `http://127.0.0.1:5000`.
2. Add your income sources and expenses.
3. Set your budget goals.
4. Monitor your financial status through the dashboard.

## Database Schema

### Tables and Relationships

- **Users**
  - `userID`: int, auto_increment, unique, PK
  - `userName`: varchar, unique, not NULL
  - `email`: varchar, unique, not NULL

- **Accounts**
  - `accountID`: int, auto_increment, unique, PK
  - `userID`: int, FK to Users
  - `currentBalance`: decimal(10,2), default 0.00

- **Expenses**
  - `expenseID`: int, auto_increment, unique, PK
  - `userID`: int, FK to Users
  - `accountID`: int, FK to Accounts
  - `amount`: decimal
  - `dateSpent`: date
  - `description`: text

- **IncomeSources**
  - `incomeID`: int, auto_increment, unique, PK
  - `userID`: int, FK to Users
  - `accountID`: int, FK to Accounts
  - `sourceName`: varchar
  - `amount`: decimal
  - `dateReceived`: date

- **UserPasswords**
  - `userID`: int, FK to Users
  - `password`: varchar, not NULL

- **Categories**
  - `categoryID`: int, auto_increment, unique, PK
  - `categoryName`: varchar, not NULL

- **ExpensesCategoriesLink**
  - `expenseID`: int, FK to Expenses
  - `categoryID`: int, FK to Categories

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Rajan Patel (TA) for feedback and guidance
- Peer reviewers for their constructive feedback and suggestions

