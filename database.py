import sqlite3

# ----------------------------------------
# DATABASE CONNECTION
# ----------------------------------------
# This will create 'sahay.db' if it does not exist
conn = sqlite3.connect("sahay.db")
cursor = conn.cursor()

# ----------------------------------------
# CREATE STUDENT TABLE
# ----------------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    academic_year INTEGER,
    strong_subjects TEXT,
    weak_subjects TEXT,
    availability TEXT,
    role TEXT,
    credits INTEGER DEFAULT 0
)
""")

conn.commit()
print("Student database initialized successfully.")

# ----------------------------------------
# FUNCTION: ADD A STUDENT
# ----------------------------------------
def add_student(name, year, strong_subjects, weak_subjects, availability, role):
    cursor.execute("""
    INSERT INTO students
    (name, academic_year, strong_subjects, weak_subjects, availability, role)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (name, year, strong_subjects, weak_subjects, availability, role))
    
    conn.commit()
    print(f"Student '{name}' added successfully.")

# ----------------------------------------
# FUNCTION: VIEW ALL STUDENTS
# ----------------------------------------
def view_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    print("\n--- STUDENT RECORDS ---")
    for student in students:
        print(student)

# ----------------------------------------
# SAMPLE DATA (for testing)
# ----------------------------------------
if __name__ == "__main__":
    add_student(
        name="Amit Kumar",
        year=1,
        strong_subjects="Maths, Physics",
        weak_subjects="Chemistry",
        availability="Evening",
        role="Both"
    )

    add_student(
        name="Sneha Patil",
        year=2,
        strong_subjects="Chemistry",
        weak_subjects="Maths",
        availability="Morning",
        role="Mentor"
    )

    view_students()

    # Close the database connection
    conn.close()