import pandas as pd
import plotly.express as px

df = pd.read_csv("student_data.csv")

# Gender vs Marks
gender_avg = df.groupby("sex")["G3"].mean().reset_index()

fig = px.bar(gender_avg, x="sex", y="G3", title="Average Marks by Gender")

fig.show()


study_avg = df.groupby("studytime")["g3"].mean().reset_index()

fig2 = px.line(study_avg, x="studytime", y="G3", title="Study Time vs Marks")

fig2.show()



fig3 = px.histogram(df, x="G3", nbins=10, title="Marks Distribution")

fig3.show()

