import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

st.set_page_config(page_title="CIMAGE Dashboard", page_icon="🎓", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
* { font-family: 'Poppins', sans-serif; }

div.stButton > button {
    background: linear-gradient(135deg, #00BFFF, #0080ff);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 8px 20px;
    font-weight: 600;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px #00BFFF55;
}
.sidebar-info {
    background: #00BFFF11;
    border-left: 3px solid #00BFFF;
    padding: 10px 14px;
    border-radius: 0 8px 8px 0;
    font-size: 13px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ── session state 
if "page"          not in st.session_state: st.session_state.page          = "landing"
if "logged_in"     not in st.session_state: st.session_state.logged_in     = False
if "role"          not in st.session_state: st.session_state.role          = None
if "username"      not in st.session_state: st.session_state.username      = ""
if "notifications" not in st.session_state: st.session_state.notifications = []

# login page 
USERS = {
    "admin":   {"password": "1234", "role": "admin",   "display": "Admin"},
    "student": {"password": "pass", "role": "student", "display": "Student"},
}



# LANDING PAGE

if st.session_state.page == "landing":
    st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1523050854058-8df90110c9f1");
        background-size: cover; background-position: center;
    }
    .main-title {
        text-align: center; margin-top: 150px; color: white;
        background-color: rgba(0,0,0,0.6);
        padding: 30px 40px; border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.15);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="main-title">
        <h1 style="font-size:72px; margin:0;">🎓 CIMAGE</h1>
        <h2 style="margin:8px 0;">Student Performance Dashboard</h2>
        <p style="font-size:16px; opacity:0.85;">Track. Analyze. Improve.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Get Started"):
            st.session_state.page = "login"
            st.rerun()
    st.stop()



# 1. LOGIN PAGE
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "login":
    st.markdown("<style>.block-container{max-width:420px;margin-top:80px;}</style>",
                unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center;'>🔐 Login</h1>", unsafe_allow_html=True)

    # FIX 1: show both roles clearly so tester knows credentials
   # st.info("**Admin login:** username `admin` | password `1234`\n\n"
     #       "**Student login:** username `student` | password `pass`")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("LOGIN", use_container_width=True):
            user = USERS.get(username)
            if user and user["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username  = username
                st.session_state.role      = user["role"]
                st.session_state.page      = "dashboard"
                st.session_state.notifications.append(
                    f"✅ {user['display']} logged in at {datetime.now().strftime('%H:%M')}"
                )
                # FIX 1: use user['display'] — key now exists
                st.success(f"Welcome {user['display']}!")
                st.rerun()
            else:
                st.error("❌ Wrong username or password")

    with col2:
        if st.button("Forgot pass?", use_container_width=True):
            st.info("Contact: admin@cimage.in")

    st.stop()



# 2. SIDEBAR

if st.session_state.page not in ["landing", "login"]:
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center; padding:10px 0;'>
            <div style='font-size:36px;'></div>
            <div style='font-size:18px; font-weight:700; color:#00BFFF;'>CIMAGE</div>
            <div style='font-size:11px; opacity:0.6;'>Academic Insight Platform</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='sidebar-info'>
            👤 <b>{st.session_state.username.title()}</b><br>
            Role: <b>{st.session_state.role.title()}</b>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.role == "admin":
            options = ["Dashboard", "Analysis", "Student Profile", "Teacher Profile",
                       "Attendance", "Add Student", "Reports", "Notifications", "Settings", "About"]
        else:
            options = ["Dashboard", "Analysis", "Student Profile", "Attendance", "About"]

        choice = st.radio("Navigation", options, label_visibility="collapsed")

        page_map = {
            "Dashboard": "dashboard", "Analysis": "analysis",
            "Student Profile": "profile", "Teacher Profile": "teacher",
            "Attendance": "attendance", "Add Student": "add",
            "Reports": "reports", "Notifications": "notifications",
            "Settings": "settings", "About": "about"
        }
        st.session_state.page = page_map[choice]

        st.divider()
        n = len(st.session_state.notifications)
        if n > 0:
            st.markdown(f"🔔 **{n} notification(s)**")

        if st.button("Logout", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()


# 3. LOAD DATA

@st.cache_data
def load_data():
    try:
        data = pd.read_csv("student_data_150.csv")
    except FileNotFoundError:
        import numpy as np
        np.random.seed(42)
        n = 150
        names = ["Rahul","Ankit","Priya","Sneha","Ravi","Amit",
                 "Pooja","Raj","Neha","Vikram","Sita","Geeta"]
        depts = ["BCA","BBA","BCom","BScIT"]
        data = pd.DataFrame({
            "name":       [names[i % len(names)] + str(i) for i in range(n)],
            "department": [depts[i % len(depts)]          for i in range(n)],
            "marks":      np.random.randint(20, 100, n),
        })
    data.columns = data.columns.str.strip().str.lower()
    return data

df = load_data()

att_cycle = [88, 75, 92, 81, 67, 95, 70, 83, 60, 98]
df["attendance"] = [att_cycle[i % len(att_cycle)] for i in range(len(df))]
df["rank"]   = df["marks"].rank(ascending=False, method="dense").astype(int)
df["result"] = df["marks"].apply(lambda x: "Pass" if x >= 40 else "Fail")
df["grade"]  = df["marks"].apply(
    lambda x: "A+" if x >= 90 else "A"  if x >= 80 else "B" if x >= 70 else
              "C"  if x >= 60 else "D"  if x >= 50 else "E" if x >= 40 else "F"
)

student_images = {
    "Rahul": "https://cdn-icons-png.flaticon.com/512/2202/2202112.png",
    "Ankit": "https://cdn-icons-png.flaticon.com/512/4140/4140048.png",
    "Priya": "https://cdn-icons-png.flaticon.com/512/4140/4140051.png",
    "Sneha": "https://cdn-icons-png.flaticon.com/512/6997/6997662.png",
}



# 4.  DASHBOARD suru
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "dashboard":
    st.title("Student Performance Dashboard")
    st.caption("Academic Insight Platform")
    st.divider()

    dept        = st.sidebar.selectbox("Department", ["All"] + sorted(df["department"].unique().tolist()))
    search      = st.sidebar.text_input("Search Student")
    min_m, max_m = int(df["marks"].min()), int(df["marks"].max())
    marks_range = st.sidebar.slider("Marks Range", min_m, max_m, (min_m, max_m))

    fdf = df.copy()
    if dept   != "All": fdf = fdf[fdf["department"].eq(dept)]
    if search:          fdf = fdf[fdf["name"].str.contains(search, case=False)]
    fdf = fdf[(fdf["marks"] >= marks_range[0]) & (fdf["marks"] <= marks_range[1])]

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Total Students", len(fdf))
    c2.metric("Avg Marks",  round(fdf["marks"].mean(),1) if len(fdf) else 0)
    c3.metric("Highest",    fdf["marks"].max() if len(fdf) else 0)
    c4.metric("Lowest",     fdf["marks"].min() if len(fdf) else 0)
    pass_rate = round((fdf["result"].eq("Pass").sum()/len(fdf))*100,1) if len(fdf) else 0
    c5.metric("Pass Rate",  f"{pass_rate}%")

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Department Performance")
        dept_avg = fdf.groupby("department")["marks"].mean().reset_index()
        fig1 = px.bar(dept_avg, x="department", y="marks", color="department",
                      color_discrete_sequence=px.colors.qualitative.Bold,
                      labels={"marks":"Avg Marks"})
        fig1.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Grade Distribution")
        grade_data = fdf["grade"].value_counts().reset_index()
        grade_data.columns = ["grade","count"]
        fig_pie = px.pie(grade_data, names="grade", values="count",
                         color_discrete_sequence=px.colors.qualitative.Pastel, hole=0.4)
        fig_pie.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("Pass vs Fail by Department")
    pf = fdf.copy()
    pf["status"] = pf["marks"].apply(lambda x: "Pass" if x >= 40 else "Fail")
    pf_group = pf.groupby(["department","status"]).size().reset_index(name="count")
    fig_pf = px.bar(pf_group, x="department", y="count", color="status", barmode="group",
                    color_discrete_map={"Pass":"#00c853","Fail":"#ff1744"})
    fig_pf.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_pf, use_container_width=True)

    st.subheader("Topper Student")
    if len(fdf) > 0:
        topper = fdf.sort_values("marks", ascending=False).iloc[0]
        t1, t2 = st.columns([1,2])
        with t1: st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=160)
        with t2:
            st.markdown(f"""
            ## {topper['name']}
            **Department:** {topper['department']}
            **Marks:** {topper['marks']}
            **Grade:** {topper['grade']}
            """)

    st.divider()
    st.subheader("Marks Distribution")
    fig2 = px.histogram(fdf, x="marks", nbins=10, color_discrete_sequence=["#00BFFF"])
    fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Student Data Table")
    st.dataframe(fdf, use_container_width=True)



# 5. ANALYSIS (student comparison  )

if st.session_state.page == "analysis":
    st.title("Detailed Analysis")
    tab1, tab2, tab3 = st.tabs(["Rankings","Trends","Compare Departments"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Top 10 Students")
            st.dataframe(df.sort_values("marks", ascending=False).head(10)
                           [["name","department","marks","grade","rank"]],
                         use_container_width=True)
        with c2:
            st.subheader("Bottom 10 Students")
            st.dataframe(df.sort_values("marks").head(10)
                           [["name","department","marks","grade","rank"]],
                         use_container_width=True)

    with tab2:
        st.subheader("Marks Spread per Department")
        fig_box = px.box(df, x="department", y="marks", color="department",
                         color_discrete_sequence=px.colors.qualitative.Bold)
        fig_box.update_layout(plot_bgcolor="rgba(0,0,0,0)", showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)

        st.subheader("Marks vs Attendance")
        fig_sc = px.scatter(df, x="attendance", y="marks", color="department",
                            hover_name="name",
                            color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_sc.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_sc, use_container_width=True)

    with tab3:
        st.subheader("Compare Two Departments")
        dept_list = df["department"].unique().tolist()
        d1 = st.selectbox("Department A", dept_list, index=0)
        d2 = st.selectbox("Department B", dept_list, index=min(1, len(dept_list)-1))
        comp = df[df["department"].isin([d1,d2])]
        fig_comp = px.histogram(comp, x="marks", color="department",
                                barmode="overlay", nbins=10, opacity=0.7)
        fig_comp.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_comp, use_container_width=True)
        stats = comp.groupby("department")["marks"].agg(["mean","median","std","min","max"]).round(2)
        stats.columns = ["Mean","Median","Std Dev","Min","Max"]
        st.dataframe(stats, use_container_width=True)



# 6. STUDENT PROFILE

if st.session_state.page == "profile":
    st.title("Student Profile")
    name_input = st.text_input("Enter Student Name")

    if name_input:
        results = df[df["name"].str.contains(name_input, case=False)]
        if not results.empty:
            if len(results) > 1:
                chosen_name = st.selectbox("Multiple found, pick one:", results["name"].tolist())
                student = results[results["name"] == chosen_name].iloc[0]
            else:
                student = results.iloc[0]

            c1, c2 = st.columns([1,2])
            with c1:
                img = student_images.get(student["name"],
                                         "https://cdn-icons-png.flaticon.com/512/3135/3135715.png")
                st.image(img, width=220)
            with c2:
                st.markdown(f"""
                ## {student['name']}
                **Department:** {student['department']}
                **Marks:** {student['marks']} &nbsp; **Grade:** `{student['grade']}`
                **Attendance:** {student['attendance']}%
                **Rank:** #{student['rank']}
                **Result:** {student['result']}
                """)
                st.progress(int(student["attendance"]),
                            text=f"Attendance: {student['attendance']}%")
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number", value=int(student["marks"]),
                    gauge={"axis":{"range":[0,100]},"bar":{"color":"#00BFFF"},
                           "steps":[{"range":[0,40],"color":"#ff1744"},
                                    {"range":[40,70],"color":"#ffd600"},
                                    {"range":[70,100],"color":"#00c853"}]},
                    title={"text":"Score out of 100"}
                ))
                fig_gauge.update_layout(height=220, margin=dict(t=30,b=0,l=0,r=0))
                st.plotly_chart(fig_gauge, use_container_width=True)
        else:
            st.error("Student not found")



# 7. TEACHER PROFILE  (FACULTY INFO)

if st.session_state.page == "teacher":
    st.title("Teacher Profiles")

    if st.session_state.role != "admin":
        st.warning("Admin access required.")
        st.stop()


    default_teachers = [
        {"name": "Neeraj Poddar",   "photo": "1.Neeraj poddar.jpeg",     "department": "HOD",                    "subject": "English",        "experience": "10 Years", "email": "neeraj@cimage.in"},
        {"name": "Nitish Kumar",    "photo": "2.Nitish kr sir.jpeg",      "department": "HOD",                    "subject": "English",        "experience": "8 Years",  "email": "nitish@cimage.in"},
        {"name": "Amit Shukla",     "photo": "3.Amit shukla sir.jpeg",    "department": "HOD",                    "subject": "DBMS",           "experience": "9 Years",  "email": "amit@cimage.in"},
        {"name": "Raju Sir",        "photo": "4.Raju sir.jpeg",           "department": "Information Technology", "subject": "JAVA",           "experience": "9 Years",  "email": "raju@cimage.in"},
        {"name": "Neeraj Kumar",    "photo": "5.Neeraj kumar sir.jpeg",   "department": "Information Technology", "subject": "Web Technology", "experience": "7 Years",  "email": "neerajk@cimage.in"},
        {"name": "Murli Sir",       "photo": "6.Murli sir.jpeg",          "department": "Information Technology", "subject": "Python",         "experience": "6 Years",  "email": "murli@cimage.in"},
        {"name": "Sanjeev Kumar",   "photo": "7.Sanjeev kumar sir.jpeg",  "department": "Management",             "subject": "Power BI",       "experience": "7 Years",  "email": "sanjeevkr@cimage.in"},
        {"name": "Nilanjan Sir",    "photo": "8.Nilanjan sir.jpeg",       "department": "Management",             "subject": "Finance",        "experience": "5 Years",  "email": "nilanjan@cimage.in"},
        {"name": "Pawan Sir",       "photo": "9.Pawan sir.jpeg",          "department": "BCA",                    "subject": "C Programming",  "experience": "8 Years",  "email": "pawan@cimage.in"},
        {"name": "Ravi Soni",       "photo": "10.Ravi soni sir.jpeg",     "department": "BCA",                    "subject": "Networking",     "experience": "6 Years",  "email": "ravisoni@cimage.in"},
    ]

    if "teachers" not in st.session_state:
        st.session_state.teachers = default_teachers

    FALLBACK_ICON = "https://cdn-icons-png.flaticon.com/512/4140/4140048.png"

    cols = st.columns(3)
    for i, t in enumerate(st.session_state.teachers):
        with cols[i % 3]:
            # FIX 2b: try to load local photo; fall back to icon if file missing
            photo_path = t.get("photo", "")
            if photo_path and os.path.exists(photo_path):
                st.image(photo_path, width=120)
            else:
                st.image(FALLBACK_ICON, width=100)

            # FIX 2c: show real name, not filename
            st.markdown(f"""
            **{t['name']}**  
            🏢 Dept: {t['department']}  
            📚 Subject: {t['subject']}  
            🕐 Experience: {t['experience']}  
            ✉️ {t['email']}
            """)
            st.divider()

    with st.expander("➕ Add New Faculty"):
        fn  = st.text_input("Full Name *",    key="fn")
        fd  = st.selectbox("Department",      ["BCA","BBA","BCom","BScIT","IT","Management","HOD"], key="fd")
        fs  = st.text_input("Subject *",      key="fs")
        fe  = st.text_input("Experience",     key="fe")
        fem = st.text_input("Email",          key="fem")

        if st.button("Add Faculty"):
            if fn and fs:
                st.session_state.teachers.append({
                    "name": fn, "photo": "", "department": fd,
                    "subject": fs, "experience": fe, "email": fem
                })
                st.session_state.notifications.append(f"Faculty '{fn}' added")
                st.success(f"{fn} added!")
                st.rerun()
            else:
                st.error("Name and Subject are required.")


# 8. ATTENDANCE (sab 85prct)


if st.session_state.page == "attendance":
    st.title("Attendance Management")
    att_df = df[["name","department","attendance"]].copy()

    threshold = st.slider("Flag students below (%)", 50, 90, 75)
    flagged   = att_df[att_df["attendance"] < threshold]

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("All Students")
        st.dataframe(att_df.head(20), use_container_width=True)
    with c2:
        st.subheader(f"Below {threshold}% ({len(flagged)} students)")
        if not flagged.empty:
            st.dataframe(flagged, use_container_width=True)
        else:
            st.success("All students are above threshold!")

    fig_att = px.bar(att_df.groupby("department")["attendance"].mean().reset_index(),
                     x="department", y="attendance", color="department",
                     labels={"attendance":"Avg Attendance %"},
                     color_discrete_sequence=px.colors.qualitative.Safe)
    fig_att.add_hline(y=threshold, line_dash="dash", line_color="red",
                      annotation_text=f"Threshold {threshold}%")
    fig_att.update_layout(plot_bgcolor="rgba(0,0,0,0)", showlegend=False)
    st.plotly_chart(fig_att, use_container_width=True)

    if st.session_state.role == "admin":
        with st.expander("Mark Today's Attendance"):
            sel_student = st.selectbox("Student", df["name"].unique())
            status = st.radio("Status", ["Present","Absent"], horizontal=True)
            if st.button("Save"):
                st.session_state.notifications.append(f"{sel_student} marked {status}")
                st.success(f"Saved: {sel_student} — {status}")



# 9.ADD STUDENT

if st.session_state.page == "add":
    st.title("Add New Student")

    if st.session_state.role != "admin":
        st.warning("Admin access required.")
        st.stop()

    with st.form("add_student"):
        name       = st.text_input("Student Name *")
        department = st.selectbox("Department *", ["BCA","BBA","BCom","BScIT"])
        marks      = st.number_input("Marks *", min_value=0, max_value=100, step=1)
        attendance = st.number_input("Attendance % *", min_value=0, max_value=100, step=1, value=80)
        done       = st.form_submit_button("Add Student")

    if done:
        if name.strip():
            new_row = pd.DataFrame([[name.strip(), department, marks, attendance]],
                                   columns=["name","department","marks","attendance"])
            updated = pd.concat([df, new_row], ignore_index=True)
            updated.to_csv("student_data_150.csv", index=False)
            load_data.clear()
            st.session_state.notifications.append(f"Student '{name}' added")
            st.success(f"{name} added successfully!")
            st.balloons()
        else:
            st.error("Please enter student name.")



# 10. REPORTS

if st.session_state.page == "reports":
    st.title("Report Generation")

    if st.session_state.role != "admin":
        st.warning("Admin access required.")
        st.stop()

    dept_f   = st.selectbox("Department",    ["All"] + df["department"].unique().tolist())
    result_f = st.selectbox("Result Filter", ["All","Pass","Fail"])

    report = df.copy()
    if dept_f   != "All": report = report[report["department"].eq(dept_f)]
    if result_f != "All": report = report[report["result"].eq(result_f)]

    st.markdown(f"**{len(report)} records found**")
    st.dataframe(report, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.download_button("Download CSV",
                           data=report.to_csv(index=False).encode("utf-8"),
                           file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                           mime="text/csv", use_container_width=True)
    with c2:
        summary = report.groupby("department")["marks"].describe().round(2)
        st.download_button("Download Summary",
                           data=summary.to_csv().encode("utf-8"),
                           file_name="dept_summary.csv",
                           mime="text/csv", use_container_width=True)

    st.subheader("Department Summary")
    st.dataframe(summary, use_container_width=True)



# 11. NOTIFICATIONS

if st.session_state.page == "notifications":
    st.title("Notifications")

    if not st.session_state.notifications:
        st.info("No notifications yet.")
    else:
        for note in reversed(st.session_state.notifications):
            st.markdown(f"• {note}")

    if st.button("Clear All"):
        st.session_state.notifications = []
        st.rerun()



# 12. SETTINGS


if st.session_state.page == "settings":
    st.title("Settings")

    st.subheader("Account Info")
    st.write(f"**Username:** {st.session_state.username}")
    st.write(f"**Role:** {st.session_state.role.title()}")

    st.subheader("Change Password")
    with st.form("change_pass"):
        old_p  = st.text_input("Current Password", type="password")
        new_p  = st.text_input("New Password",     type="password")
        conf_p = st.text_input("Confirm Password", type="password")
        save   = st.form_submit_button("Update")

    if save:
        user = USERS.get(st.session_state.username)
        if user and user["password"] == old_p:
            if new_p == conf_p and len(new_p) >= 4:
                USERS[st.session_state.username]["password"] = new_p
                st.success("Password updated!")
            else:
                st.error("Passwords don't match or too short.")
        else:
            st.error("Current password is wrong.")

    st.subheader("Data")
    if st.button("Reload Data"):
        load_data.clear()
        st.success("Data reloaded.")


# 13. ABOUT my project

if st.session_state.page == "about":
    st.title("About This Project")
    c1, c2 = st.columns([2,1])
    with c1:
        st.markdown("""
        ### CIMAGE Student Performance Dashboard

        Built to help teachers and admin staff track student performance,
        attendance, and grades in one place.

        **Technologies Used:** Python · Streamlit · Pandas · Plotly

        **Features:**
        - Admin & Student login (role-based access)
        - Live KPI dashboard
        - Grade & pass/fail charts
        - Student profile with score gauge
        - Teacher profiles with local photos
        - Attendance tracker & flagging
        - Add new students
        - Downloadable CSV reports
        - Notifications log
        """)
    with c2:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=180)
        st.markdown("""
        **Version:** 2.1  
        **College:** CIMAGE, Patna  
        **Contact:** admin@cimage.in
        """)
        
        # this is not the end -------- aage ka in phase 3 !!!!!!!
