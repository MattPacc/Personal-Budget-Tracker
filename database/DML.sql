-- =============================================
-- Users Page Queries
-- =============================================

-- Insert a new user
INSERT INTO Users (userName, email) VALUES (:userName, :email);

-- Select all users to view in the table
SELECT userId, userName, email FROM Users;


-- =============================================
-- Accounts Page Queries
-- =============================================

-- Insert a new account
INSERT INTO Accounts (userId, currentBalance) VALUES (:userId, :currentBalance);

-- Select all accounts to view their balances
SELECT accountId, userId, currentBalance FROM Accounts;

-- Select all accounts with user details
SELECT Accounts.accountID, Accounts.userID, Accounts.currentBalance, Users.userName
FROM Accounts
JOIN Users ON Accounts.userID = Users.userID;

-- Select all users to populate userID dropdown
SELECT userID FROM Users;


-- =============================================
-- Income Sources Page Queries
-- =============================================

-- Insert a new income source
INSERT INTO IncomeSources (userId, accountId, sourceName, amount, dateReceived) VALUES (:userId, :accountId, :sourceName, :amount, :dateReceived);

-- Select all income sources to view
SELECT userID, sourceName, amount, dateReceived FROM IncomeSources;

-- Select all users to populate userID dropdown
SELECT userID FROM Users;

-- Select all accounts to populate accountID dropdown
SELECT accountID FROM Accounts;


-- =============================================
-- Categories Page Queries
-- =============================================

-- Insert a new category
INSERT INTO Categories (categoryName) VALUES (:categoryName);

-- Select all categories and their linked expenses
SELECT c.categoryID, c.categoryName, 
       ecl.expenseID, e.amount as expenseAmount, e.dateSpent, e.description as expenseDescription
FROM Categories c
LEFT JOIN ExpensesCategoriesLink ecl ON c.categoryID = ecl.categoryID
LEFT JOIN Expenses e ON ecl.expenseID = e.expenseID;

-- Select a specific category by categoryID
SELECT * FROM Categories WHERE categoryID = :categoryID;

-- Update a category
UPDATE Categories SET categoryName = :categoryName WHERE categoryID = :categoryID;

-- Delete a category
DELETE FROM Categories WHERE categoryID = :categoryID;

-- Delete a specific link between category and expense
DELETE FROM ExpensesCategoriesLink WHERE categoryID = :categoryID AND expenseID = :expenseID;

-- Insert a new record into the join table ExpensesCategoriesLink
INSERT INTO ExpensesCategoriesLink (expenseID, categoryID) VALUES (:expenseID, :categoryID);

-- Select all expenses (to populate the dropdown)
SELECT * FROM Expenses;


-- =============================================
-- Expenses Page Queries
-- =============================================

-- Insert a new expense
INSERT INTO Expenses (userID, accountID, amount, dateSpent, description)
VALUES (:userID, :accountID, :amount, :dateSpent, :description);

-- Insert a new record into the join table ExpensesCategoriesLink
INSERT INTO ExpensesCategoriesLink (expenseID, categoryID) 
VALUES (:expenseID, :categoryID);

-- Select all expenses along with their category names
SELECT e.expenseID, e.amount, e.dateSpent, e.description, 
       ecl.categoryID, c.categoryName
FROM Expenses e
LEFT JOIN ExpensesCategoriesLink ecl ON e.expenseID = ecl.expenseID
LEFT JOIN Categories c ON ecl.categoryID = c.categoryID;

-- Select all categories (to populate the dropdown)
SELECT * FROM Categories;

-- Select all users (to populate the dropdown)
SELECT userID, userName FROM Users;

-- Select all accounts (to populate the dropdown)
SELECT accountID FROM Accounts;

-- Update an expense
UPDATE Expenses 
SET amount = :amount, dateSpent = :dateSpent, description = :description 
WHERE expenseID = :expenseID AND userID = :userID AND accountID = :accountID;

-- Replace the link between expense and category
REPLACE INTO ExpensesCategoriesLink (expenseID, categoryID) 
VALUES (:expenseID, :categoryID);

-- Delete the link between expense and category if categoryID is NULL
DELETE FROM ExpensesCategoriesLink WHERE expenseID = :expenseID AND (categoryID IS NULL OR categoryID = '');

-- Delete an expense
DELETE FROM Expenses WHERE expenseID = :expenseID;

-- Select expenses with a filter by categoryId
SELECT e.expenseID, e.amount, e.dateSpent, e.description, 
       ecl.categoryID, c.categoryName
FROM Expenses e
LEFT JOIN ExpensesCategoriesLink ecl ON e.expenseID = ecl.expenseID
LEFT JOIN Categories c ON ecl.categoryID = c.categoryID
WHERE ecl.categoryID = :category_id_filter OR ecl.categoryID IS NULL;


-- =============================================
-- User Passwords Page Queries
-- =============================================

-- Insert a new user password
INSERT INTO UserPasswords (userId, password) VALUES (:userId, :password);

-- Select all user passwords along with user names
SELECT UserPasswords.userID, UserPasswords.password, Users.userName
FROM UserPasswords
JOIN Users ON UserPasswords.userID = Users.userID;

-- Select all users to populate userID dropdown
SELECT userID FROM Users;
