# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

print(pd.read_sql("""SELECT * FROM sqlite_master""", conn))

# STEP 1
# Replace None with your code
df_boston = pd.read_sql("""
    SELECT e.firstName, e.jobTitle
    FROM employees e
    JOIN offices o ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston'
""", conn)

# STEP 2
# Replace None with your code
df_zero_emp = pd.read_sql("""
    SELECT o.city
    FROM offices AS o
    LEFT JOIN employees AS e ON o.officeCode = e.officeCode
    WHERE e.employeeNumber IS NULL
""", conn)

# STEP 3
# Replace None with your code
df_employee = pd.read_sql("""
    SELECT e.firstName, e.lastName, o.city, o.state
    FROM employees AS e
    LEFT JOIN offices AS o ON e.officeCode = o.officeCode
    ORDER BY e.firstName, e.lastName
""", conn)

# STEP 4
# Replace None with your code
df_contacts = pd.read_sql("""
    SELECT c.contactLastName, c.contactFirstName, c.phone, c.salesRepEmployeeNumber
    FROM customers AS c
    LEFT JOIN orders AS o ON c.customerNumber = o.customerNumber
    WHERE o.customerNumber IS NULL
    ORDER BY c.contactLastName ASC
""", conn)

# STEP 5
# Replace None with your code
df_payment = pd.read_sql("""
    SELECT c.contactLastName, c.contactFirstName, p.amount, p.paymentDate
    FROM customers AS c
    JOIN payments AS p ON c.customerNumber = p.customerNumber
    ORDER BY CAST(p.amount AS DECIMAL) DESC
""", conn)

# STEP 6
# Replace None with your code
df_credit = pd.read_sql("""
    SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(c.customerNumber) AS totalCustomers
    FROM employees AS e
    JOIN customers AS c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY e.employeeNumber, e.firstName, e.lastName
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY totalCustomers DESC
""", conn)

# STEP 7
# Replace None with your code
df_product_sold = pd.read_sql("""
    SELECT p.productName, COUNT(DISTINCT od.orderNumber) AS numorders, SUM(od.quantityOrdered) AS totalunits
    FROM products AS p
    JOIN orderdetails AS od ON p.productCode = od.productCode
    GROUP BY p.productName
    ORDER BY totalunits DESC
""", conn)

# STEP 8
# Replace None with your code
df_total_customers = pd.read_sql("""
    SELECT p.productName, p.productCode, COUNT(DISTINCT o.customerNumber) AS numpurchasers
    FROM products AS p
    JOIN orderdetails AS od ON p.productCode = od.productCode
    JOIN orders AS o ON od.orderNumber = o.orderNumber
    GROUP BY p.productName, p.productCode
    ORDER BY numpurchasers DESC
""", conn)

# STEP 9
# Replace None with your code
df_customers = pd.read_sql("""
    SELECT o.officeCode, o.city, COUNT(c.customerNumber) AS n_customers
    FROM offices AS o
    JOIN employees AS e ON o.officeCode = e.officeCode
    JOIN customers AS c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY o.officeCode, o.city
""", conn)

# STEP 10
# Replace None with your code
df_under_20 = pd.read_sql("""
    SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName, o.city, o.officeCode
    FROM employees AS e
    JOIN offices AS o ON e.officeCode = o.officeCode
    JOIN customers AS c ON e.employeeNumber = c.salesRepEmployeeNumber
    JOIN orders AS ord ON c.customerNumber = ord.customerNumber
    JOIN orderdetails AS od ON ord.orderNumber = od.orderNumber
    WHERE od.productCode IN (
        SELECT p.productCode
        FROM products p
        JOIN orderdetails od ON p.productCode = od.productCode
        JOIN orders o ON od.orderNumber = o.orderNumber
        GROUP BY p.productCode
        HAVING COUNT(DISTINCT o.customerNumber) < 20
    )
    ORDER BY e.lastName, e.firstName
""", conn)

conn.close()