-- Disable foreign key checks and autocommit
SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;

-- Drop tables if they exist to avoid errors upon recreation
DROP TABLE IF EXISTS UserPasswords, ExpensesCategoriesLink, Expenses, Categories, IncomeSources, Accounts, Users;

-- Creating Users table
CREATE OR REPLACE TABLE Users (
    userID INT AUTO_INCREMENT NOT NULL,
    userName VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    PRIMARY KEY (userID)
);

-- Creating Accounts table
CREATE OR REPLACE TABLE Accounts (
    accountID INT AUTO_INCREMENT NOT NULL,
    userID INT UNIQUE NOT NULL,
    currentBalance DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    FOREIGN KEY (userID) REFERENCES Users(userID) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (accountID)
);

-- Creating Categories table
CREATE OR REPLACE TABLE Categories (
    categoryID INT AUTO_INCREMENT,
    categoryName VARCHAR(255) NOT NULL,
    PRIMARY KEY (categoryID)
);

-- Creating Expenses table
CREATE OR REPLACE TABLE Expenses (
    expenseID INT AUTO_INCREMENT UNIQUE NOT NULL,
    accountID INT NOT NULL,
    userID INT NOT NULL,
    amount DECIMAL(10, 2),
    dateSpent DATE,
    description TEXT,
    FOREIGN KEY (userID) REFERENCES Users(userID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (accountID) REFERENCES Accounts(accountID) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (expenseID)
);

-- Creating IncomeSources table
CREATE OR REPLACE TABLE IncomeSources (
    incomeID INT AUTO_INCREMENT UNIQUE NOT NULL,
    userID INT NOT NULL,
    accountID INT NOT NULL,
    sourceName VARCHAR(255),
    amount DECIMAL(10, 2),
    dateReceived DATE,
    FOREIGN KEY (userID) REFERENCES Users(userID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (accountID) REFERENCES Accounts(accountID) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (incomeID)
);

-- Creating UserPasswords table
CREATE OR REPLACE TABLE UserPasswords (
    userID INT UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    FOREIGN KEY (userID) REFERENCES Users(userID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Creating ExpensesCategoriesLink table for many-to-many relationship between Expenses and Categories
CREATE OR REPLACE TABLE ExpensesCategoriesLink (
    expenseID INT,
    categoryID INT NULL,
    FOREIGN KEY (expenseID) REFERENCES Expenses(expenseID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (categoryID) REFERENCES Categories(categoryID) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (expenseID, categoryID)
);

-- Inserting sample data into Users
INSERT INTO Users (userName, email) 
VALUES 
('JeanLucPicard', 'picard@starfleet.com'),
('JamesTKirk', 'kirk@starfleet.com'),
('Spock', 'spock@starfleet.com'),
('Data', 'data@starfleet.com');

-- Inserting sample data into Accounts
INSERT INTO Accounts (userID, currentBalance) 
VALUES
(
    (SELECT userID FROM Users WHERE userName = 'JeanLucPicard'), 
    1000.00
),
(
    (SELECT userID FROM Users WHERE userName = 'JamesTKirk'), 
    1200.00
),
(
    (SELECT userID FROM Users WHERE userName = 'Spock'), 
    1150.00
),
(
    (SELECT userID FROM Users WHERE userName = 'Data'), 
    1300.00
);

-- Inserting sample data into Categories
INSERT INTO Categories (categoryName) 
VALUES 
('Travel'),
('Repairs'),
('Supplies'),
('Entertainment');

-- Inserting sample data into Expenses
INSERT INTO Expenses (userID, accountID, amount, dateSpent, description) 
VALUES 
(
    (SELECT userID FROM Users WHERE userName = 'JeanLucPicard'), 
    (SELECT accountID FROM Accounts WHERE userID = (SELECT userID FROM Users WHERE userName = 'JeanLucPicard')), 
    250.00, '2024-05-01', 'Transport to Starbase 12'
),
(
    (SELECT userID FROM Users WHERE userName = 'JamesTKirk'), 
    (SELECT accountID FROM Accounts WHERE userID = (SELECT userID FROM Users WHERE userName = 'JamesTKirk')), 
    300.00, '2024-04-30', 'Engineering repairs'
),
(
    (SELECT userID FROM Users WHERE userName = 'Spock'), 
    (SELECT accountID FROM Accounts WHERE userID = (SELECT userID FROM Users WHERE userName = 'Spock')), 
    150.00, '2024-06-01', 'Research materials'
),
(
    (SELECT userID FROM Users WHERE userName = 'Data'), 
    (SELECT accountID FROM Accounts WHERE userID = (SELECT userID FROM Users WHERE userName = 'Data')), 
    200.00, '2024-06-02', 'Android maintenance'
);

-- Inserting sample data into IncomeSources
INSERT INTO IncomeSources (userID, accountID, sourceName, amount, dateReceived) 
VALUES 
(
    (SELECT userID FROM Users WHERE userName = 'Spock'), 
    (SELECT accountID FROM Accounts WHERE userID = (SELECT userID FROM Users WHERE userName = 'Spock')), 
    'Science Grants', 2000.00, '2024-05-01'
),
(
    (SELECT userID FROM Users WHERE userName = 'JeanLucPicard'), 
    (SELECT accountID FROM Accounts WHERE userID = (SELECT userID FROM Users WHERE userName = 'JeanLucPicard')), 
    'Starfleet Salary', 3000.00, '2024-05-01'
),
(
    (SELECT userID FROM Users WHERE userName = 'JamesTKirk'), 
    (SELECT accountID FROM Accounts WHERE userID = (SELECT userID FROM Users WHERE userName = 'JamesTKirk')), 
    'Starfleet Pension', 2500.00, '2024-05-01'
),
(
    (SELECT userID FROM Users WHERE userName = 'Data'), 
    (SELECT accountID FROM Accounts WHERE userID = (SELECT userID FROM Users WHERE userName = 'Data')), 
    'Research Funding', 2200.00, '2024-05-01'
);

-- Inserting sample data into UserPasswords (remember to hash these in production)
INSERT INTO UserPasswords (userID, password) 
VALUES 
(
    (SELECT userID FROM Users WHERE userName = 'JeanLucPicard'), 
    'enterpriseD123'
),
(
    (SELECT userID FROM Users WHERE userName = 'JamesTKirk'), 
    'finalFrontier456'
),
(
    (SELECT userID FROM Users WHERE userName = 'Spock'), 
    'logicIsKey789'
),
(
    (SELECT userID FROM Users WHERE userName = 'Data'), 
    'positronicBrain101'
);

-- Inserting sample data into ExpensesCategoriesLink
INSERT INTO ExpensesCategoriesLink (expenseID, categoryID)
VALUES
(
    (SELECT expenseID FROM Expenses WHERE description = 'Transport to Starbase 12'), 
    (SELECT categoryID FROM Categories WHERE categoryName = 'Travel')
),
(
    (SELECT expenseID FROM Expenses WHERE description = 'Engineering repairs'), 
    (SELECT categoryID FROM Categories WHERE categoryName = 'Repairs')
),
(
    (SELECT expenseID FROM Expenses WHERE description = 'Research materials'), 
    (SELECT categoryID FROM Categories WHERE categoryName = 'Supplies')
),
(
    (SELECT expenseID FROM Expenses WHERE description = 'Android maintenance'), 
    (SELECT categoryID FROM Categories WHERE categoryName = 'Repairs')
);

-- Re-enable foreign key checks and commit the transaction
SET FOREIGN_KEY_CHECKS = 1;
COMMIT;