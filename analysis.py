import pandas as pd

# CSV load
df = pd.read_csv("student_data.csv")

# First 5 rows
print(df.head())

# Columns info
print("\nColumns:")
print(df.columns)

# Dataset info
print("\nInfo:")
print(df.info())


print("this will show where data is missing")
print("\nMissing Values:")
print(df.isnull().sum())


df.fillna(df.mean(numeric_only=True), inplace=True)


df.fillna("Unknown", inplace=True)

df.drop_duplicates(inplace=True)

df.columns = df.columns.str.strip()
df.columns = df.columns.str.lower()

print("\nCleaned Data:")
print(df.head())

import pandas as pd

df = pd.read_csv("student_data.csv")

print("Original Data:")
print(df.head())

print("\nMissing Values:")
print(df.isnull().sum())

df.fillna(df.mean(numeric_only=True), inplace=True)
df.fillna("Unknown", inplace=True)

df.drop_duplicates(inplace=True)

df.columns = df.columns.str.strip()
df.columns = df.columns.str.lower()

print("\nCleaned Data:")
print(df.head())

# Total students
print("\nTotal Students:", len(df))

# Average final grade
print("Average Final Grade:", df["g3"].mean())

# Highest marks
print("Highest Final Grade:", df["g3"].max())

# Lowest marks
print("Lowest Final Grade:", df["g3"].min())

# Top 5 students based on final grade
top_students = df.sort_values(by="g3", ascending=False).head(5)

print("\nTop 5 Students:")
print(top_students[["sex", "age", "g3"]])

# Gender wise average marks
gender_avg = df.groupby("sex")["g3"].mean()

print("\nAverage Marks by Gender:")
print(gender_avg)

# Study time vs marks
study_avg = df.groupby("studytime")["g3"].mean()

print("\nStudy Time vs Marks:")
print(study_avg)


import matplotlib.pyplot as plt

plt.figure(figsize=(12,8))

# Chart 1: Gender
plt.subplot(2,2,1)
df.groupby("sex")["g3"].mean().plot(kind="bar")
plt.title("Gender vs Marks")

# Chart 2: Study time
plt.subplot(2,2,2)
df.groupby("studytime")["g3"].mean().plot(kind="line", marker="o")
plt.title("Study Time vs Marks")

# Chart 3: Distribution
plt.subplot(2,2,3)
plt.hist(df["g3"], bins=10)
plt.title("Marks Distribution")

plt.tight_layout()
plt.show()
