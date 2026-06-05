#python se csv load krega or insert krega

import pandas as pd
import pyodbc

# Read CSV

df = pd.read_csv("student_data_150.csv")
print(df.columns)
# Connect SQL
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=ARUHI;'
    'DATABASE=StudentDashboard;'
    'Trusted_Connection=yes;'
)

cursor = conn.cursor()

# Insert rows
for index, row in df.iterrows():
    cursor.execute(
        "INSERT INTO Students VALUES (?,?,?,?,?)",
        index + 1,
        row["school"],
        row["sex"],
        int(row["G3"]),
        row["sex"]
    )

conn.commit()
print("Data inserted successfully")