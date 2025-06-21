-- Drop tables if they exist
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS OrderItems;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Suppliers;

-- Create tables
CREATE TABLE Customers (
    CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Email TEXT UNIQUE,
    Phone TEXT
);

CREATE TABLE Suppliers (
    SupplierID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    ContactName TEXT,
    Phone TEXT
);

CREATE TABLE Categories (
    CategoryID INTEGER PRIMARY KEY AUTOINCREMENT,
    CategoryName TEXT NOT NULL
);

CREATE TABLE Products (
    ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductName TEXT NOT NULL,
    CategoryID INTEGER,
    SupplierID INTEGER,
    Price REAL,
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID),
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID)
);

CREATE TABLE Orders (
    OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
    CustomerID INTEGER,
    OrderDate TEXT,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE OrderItems (
    OrderItemID INTEGER PRIMARY KEY AUTOINCREMENT,
    OrderID INTEGER,
    ProductID INTEGER,
    Quantity INTEGER,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

-- Insert sample data
INSERT INTO Customers (Name, Email, Phone) VALUES
('Alice Smith', 'alice@example.com', '555-1234'),
('Bob Johnson', 'bob@example.com', '555-5678');

INSERT INTO Suppliers (Name, ContactName, Phone) VALUES
('Acme Corp', 'John Doe', '555-1111'),
('Global Supplies', 'Jane Roe', '555-2222');

INSERT INTO Categories (CategoryName) VALUES
('Electronics'),
('Books');

INSERT INTO Products (ProductName, CategoryID, SupplierID, Price) VALUES
('Laptop', 1, 1, 999.99),
('Smartphone', 1, 2, 499.99),
('Novel', 2, 2, 19.99);

INSERT INTO Orders (CustomerID, OrderDate) VALUES
(1, '2024-06-21'),
(2, '2024-06-22');

INSERT INTO OrderItems (OrderID, ProductID, Quantity) VALUES
(1, 1, 1),
(1, 3, 2),
(2, 2, 1);

-- Script ends here
