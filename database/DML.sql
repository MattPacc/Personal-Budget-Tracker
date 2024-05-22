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

-- =============================================
-- Income Sources Page Queries
-- =============================================

-- Insert a new income source
INSERT INTO IncomeSources (userId, sourceName, amount, dateReceived) VALUES (:userId, :sourceName, :amount, :dateReceived);

-- Select all income sources to view
SELECT incomeId, userId, sourceName, amount, dateReceived FROM IncomeSources;

-- =============================================
-- Expenses and Categories Management Page Queries
-- =============================================

-- Insert a new expense into the Expenses table
INSERT INTO Expenses (userId, amount, dateSpent, categoryId) 
VALUES (:userId, :amount, :dateSpent, :categoryId);

-- Insert a new category into the Categories table
INSERT INTO Categories (categoryName) 
VALUES (:categoryName);

-- Insert a new record into the join table ExpenseCategories
INSERT INTO ExpenseCategories (expenseId, categoryId) 
VALUES (:expenseId, :categoryId);

-- Select all expenses along with their category names
SELECT Expenses.expenseId, Expenses.userId, Expenses.amount, Expenses.dateSpent, Categories.categoryName
FROM Expenses
LEFT JOIN Categories ON Expenses.categoryId = Categories.categoryId;

-- Select expenses with a filter by categoryId
SELECT Expenses.expenseId, Expenses.userId, Expenses.amount, Expenses.dateSpent, Categories.categoryName
FROM Expenses
LEFT JOIN ExpenseCategories ON Expenses.expenseId = ExpenseCategories.expenseId
LEFT JOIN Categories ON ExpenseCategories.categoryId = Categories.categoryId
WHERE Categories.categoryId = :categoryIdFilter;

-- Update an expense, potentially setting its category to NULL
UPDATE Expenses
SET amount = :amount, dateSpent = :dateSpent, categoryId = (:categoryId IS NULL ? NULL : :categoryId)
WHERE expenseId = :expenseId;

-- Delete an expense based on its expenseId and its references in ExpenseCategories
DELETE FROM ExpenseCategories WHERE expenseId = :expenseId;
DELETE FROM Expenses WHERE expenseId = :expenseId;

-- Delete a category based on its categoryId and its references in ExpenseCategories
DELETE FROM ExpenseCategories WHERE categoryId = :categoryId;
DELETE FROM Categories WHERE categoryId = :categoryId;

-- Update Expenses setting categoryId to NULL where previously deleted categoryId was referenced
-- Ensures that no expense is left referencing the deleted category
UPDATE Expenses
SET categoryId = NULL
WHERE categoryId = :categoryId;

-- =============================================
-- User Passwords Page Queries
-- =============================================

-- Insert a new user password
INSERT INTO userPasswords (userId, passwordHash) VALUES (:userId, :passwordHash);

-- Select all user passwords to view in the table
SELECT userId, passwordHash FROM userPasswords;