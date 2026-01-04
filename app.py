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

st.sidebar.divider()

# --- DYNAMIC SUBJECTS INPUT ---
st.sidebar.header("Enter Marks")

# 1. Ask how many subjects
num_subjects = st.sidebar.number_input("Number of Subjects", min_value=1, max_value=10, value=5, step=1)

# Default subject names list to pre-fill the first few
default_names = ["Mathematics", "Data Science", "English", "Python Programming", "Artificial Intelligence"]

marks_dict = {}

# 2. Generate inputs dynamically based on the number selected
for i in range(num_subjects):
    st.sidebar.markdown(f"**Subject {i+1}**")
    
    # Pre-fill name if available in defaults, else use "Subject X"
    def_val = default_names[i] if i < len(default_names) else f"Subject {i+1}"
    
    # Create columns for cleaner look: Name (Left) | Marks (Right)
    col1, col2 = st.sidebar.columns([3, 2])
    
    with col1:
        sub_name = st.text_input(f"Name {i+1}", value=def_val, key=f"sub_name_{i}", label_visibility="collapsed")
    with col2:
        sub_marks = st.number_input(f"Marks {i+1}", 0, 100, 75 if i < len(default_names) else 0, key=f"sub_marks_{i}", label_visibility="collapsed")
    
    marks_dict[sub_name] = sub_marks

# --- CALCULATIONS ---
total_obtained = sum(marks_dict.values())
max_possible_marks = num_subjects * 100  # Dynamic total based on subject count
percentage = (total_obtained / max_possible_marks) * 100

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
    col1.metric("Total Marks", f"{total_obtained}/{max_possible_marks}")
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
    # Dynamic colors: Repeat the color list if subjects > 5
    base_colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0', '#ffb3e6', '#c2f0c2']
    colors = base_colors * (num_subjects // len(base_colors) + 1)
    
    ax.bar(df['Subject'], df['Marks Obtained'], color=colors[:num_subjects])
    ax.set_ylabel("Marks")
    ax.set_title("Subject-wise Performance")
    ax.set_ylim(0, 100)
    plt.xticks(rotation=45, ha='right') # Rotate labels if many subjects
    
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