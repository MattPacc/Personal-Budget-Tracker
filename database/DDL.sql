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
    FOREIGN KEY (userID) REFERENCES Users(userID),
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
    FOREIGN KEY (userID) REFERENCES Users(userID),
    FOREIGN KEY (accountID) REFERENCES Accounts(accountID),
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
    FOREIGN KEY (userID) REFERENCES Users(userID),
    FOREIGN KEY (accountID) REFERENCES Accounts(accountID),
    PRIMARY KEY (incomeID)
);


-- Creating UserPasswords table
CREATE OR REPLACE TABLE UserPasswords (
    userID INT UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    FOREIGN KEY (userID) REFERENCES Users(userID)
);


-- Creating ExpensesCategoriesLink table for many-to-many relationship between Expenses and Categories
CREATE OR REPLACE TABLE ExpensesCategoriesLink (
    expenseID INT,
    categoryID INT,
    FOREIGN KEY (expenseID) REFERENCES Expenses(expenseID),
    FOREIGN KEY (categoryID) REFERENCES Categories(categoryID),
    PRIMARY KEY (expenseID, categoryID)
);


-- Inserting sample data into Users----------------------------
INSERT INTO Users (userName, email) 
VALUES 
('JeanLucPicard', 'picard@starfleet.com'),
('JamesTKirk', 'kirk@starfleet.com'),
('Spock', 'spock@starfleet.com');


-- Inserting sample data into Accounts, assuming a starting balance for each
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
);


-- Inserting sample data into Categories ----------------------------------------------
INSERT INTO Categories (categoryName) 
VALUES 
('Travel'),
('Repairs');


-- Inserting sample data into Expenses
INSERT INTO Expenses (userID, accountID, amount, dateSpent, description) 
VALUES ((SELECT userID FROM Users WHERE userName = 'JeanLucPicard'), 
        (SELECT accountID FROM Accounts WHERE userID = (SELECT userID FROM Users WHERE userName = 'JeanLucPicard')), 
        250.00, '2024-05-01', 'Transport to Starbase 12');

INSERT INTO Expenses (userID, accountID, amount, dateSpent, description) 
VALUES ((SELECT userID FROM Users WHERE userName = 'JamesTKirk'), 
        (SELECT accountID FROM Accounts WHERE userID = (SELECT userID FROM Users WHERE userName = 'JamesTKirk')), 
        300.00, '2024-04-30', 'Engineering repairs');


-- Inserting sample data into IncomeSources---------------------------------------------
INSERT INTO IncomeSources (userID, accountID, sourceName, amount, dateReceived) 
VALUES ((SELECT userID FROM Users WHERE userName = 'Spock'), 
        (SELECT accountID FROM Accounts WHERE userID = (SELECT userID FROM Users WHERE userName = 'Spock')), 
        'Science Grants', 2000.00, '2024-05-01');


-- Inserting sample data into UserPasswords (remember to hash these in production)-----------------------------------
INSERT INTO UserPasswords (userID, password) 
VALUES 
(
    (SELECT userID FROM Users WHERE userName = 'JeanLucPicard'), 
    'enterpriseD123'
),
(
    (SELECT userID FROM Users WHERE userName = 'JamesTKirk'), 
    'finalFrontier456'
);

-- Re-enable foreign key checks and commit the transaction
SET FOREIGN_KEY_CHECKS = 1;
COMMIT;