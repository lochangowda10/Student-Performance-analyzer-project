import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Student Performance Analyzer", page_icon="🎓")

st.title("🎓 Student Performance Analyzer")
st.write("Analyze student marks, calculate grades, and visualize performance.")

# --- SIDEBAR: INPUT DATA ---
st.sidebar.header("Enter Student Details")
name = st.sidebar.text_input("Student Name")
roll_no = st.sidebar.text_input("Roll Number")

st.sidebar.subheader("Enter Marks (out of 100)")
math = st.sidebar.number_input("Mathematics", 0, 100, 75)
science = st.sidebar.number_input("Data Science", 0, 100, 80)
english = st.sidebar.number_input("English", 0, 100, 65)
python = st.sidebar.number_input("Python Programming", 0, 100, 90)
ai = st.sidebar.number_input("Artificial Intelligence", 0, 100, 85)

# --- CALCULATIONS ---
marks_dict = {
    "Mathematics": math,
    "Data Science": science,
    "English": english,
    "Python": python,
    "AI": ai
}

total_marks = sum(marks_dict.values())
average_marks = total_marks / 5
percentage = (total_marks / 500) * 100

# Determine Grade
if percentage >= 90:
    grade = "O (Outstanding)"
elif percentage >= 80:
    grade = "A+ (Excellent)"
elif percentage >= 70:
    grade = "A (Very Good)"
elif percentage >= 60:
    grade = "B (Good)"
elif percentage >= 50:
    grade = "C (Pass)"
else:
    grade = "F (Fail)"

# --- MAIN DASHBOARD ---
if st.sidebar.button("Generate Report"):
    st.divider()
    
    # 1. Student Details Section
    st.subheader("📋 Student Information")
    col_name, col_roll = st.columns(2)
    col_name.write(f"**Name:** {name}")
    col_roll.write(f"**Roll Number:** {roll_no}")
    
    st.divider()
    
    # 2. Summary Section
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Marks", f"{total_marks}/500")
    col2.metric("Percentage", f"{percentage:.2f}%")
    col3.metric("Grade", grade)
    
    st.divider()

    # 3. Detailed Data Table
    df = pd.DataFrame(list(marks_dict.items()), columns=["Subject", "Marks Obtained"])
    st.subheader(f"📄 Report Card")
    st.dataframe(df, use_container_width=True)

    # 4. Visualization (Bar Chart)
    st.subheader("📊 Performance Visualization")
    
    fig, ax = plt.subplots()
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0']
    ax.bar(df['Subject'], df['Marks Obtained'], color=colors)
    ax.set_ylabel("Marks")
    ax.set_title("Subject-wise Performance")
    ax.set_ylim(0, 100)
    
    # Add labels on top of bars
    for i, v in enumerate(df['Marks Obtained']):
        ax.text(i, v + 1, str(v), ha='center', fontweight='bold')
        
    st.pyplot(fig)

    # 5. Success Message
    if percentage >= 50:
        st.success("Result: PASSED 🎉")
    else:
        st.error("Result: FAILED ❌")

else:
    st.info("👈 Please enter details in the sidebar and click 'Generate Report'")