import pyodbc

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=ARUHI;'
    'DATABASE=StudentDB;'
    'Trusted_Connection=yes;'
)

print("Connected successfully")





