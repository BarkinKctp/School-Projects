import os

STUDENT_FILE = 'students.txt'
DELETED_STUDENTS_FILE = 'deleted_students.txt'

def main():
    initialize_files()
    while True:
        print("\n===== Student Management System =====")
        print("1. Show all students")
        print("2. Add a new student")
        print("3. Remove a student")
        print("4. Update a student's grade")
        print("5. Show class average")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            show_all_students()
        elif choice == "2":
            add_student()
        elif choice == "3":
            remove_student()
        elif choice == "4":
            update_student_grade()
        elif choice == "5":
            show_class_average()
        elif choice == "6":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()


def initialize_files():
    #Initialize the student and deleted student files if they don't exist.
    if not os.path.exists(STUDENT_FILE):
        with open(STUDENT_FILE, 'w') as file:
            file.write("John Smith, 85\n")
            file.write("Emily Johnson, 90\n")
            file.write("Michael Brown, 78\n")
    if not os.path.exists(DELETED_STUDENTS_FILE):
        open(DELETED_STUDENTS_FILE, 'w').close()


def read_students():
    try:
        #Read and return the list of students from the student file.
        with open(STUDENT_FILE, 'r') as file:
            students = [line.strip() for line in file.readlines()]
        return students
    except FileNotFoundError:
        print("Student file not found.")
        return []


#Write the list of students to the student file.
def write_students(students):
    with open(STUDENT_FILE, 'w') as file:
        for student in students:
            file.write(student + '\n')


#Display all students and their grades.
def show_all_students():
    students = read_students()
    if not students:
        print("No students found in the file.")
        return
    print("Student List:")
    for student in students:
        name, grade = student.split(', ')
        print(f"Name: {name}, Grade: {grade}")


#Add a new student to the student file.
def add_student():
    name = input("Enter student name: ")
    grade = input("Enter student grade: ")
    with open(STUDENT_FILE, 'a') as file:
        file.write(f"{name}, {grade}\n")
    print(f"Student {name} added successfully.")


#Delete a student from the student file and log the deletion.
def remove_student():
    name_to_remove = input("Enter the name of the student to remove: ")
    students = read_students()
    updated_students = []
    found = None

    for student in students:
        name, grade = student.split(', ')
        if name.strip().lower() == name_to_remove.strip().lower():
            found = student
            with open(DELETED_STUDENTS_FILE, 'a') as del_file:
                del_file.write(student + '\n')
            print(f"Student {name} deleted and backed up successfully.")
        else:
            updated_students.append(student)

    if not found:
        print(f"Student {name_to_remove} not found.")
    else:
        write_students(updated_students)


#Update the grade of an existing student.
def update_student_grade():   
    name_to_update = input("Enter the name of the student to update: ")
    new_grade = input("Enter the new grade: ").strip()
    if not new_grade.isdigit():
        print("Invalid grade input. Please enter a number.")
        return

    students = read_students()
    updated_students = []
    found = False

    for student in students:
        name, grade = student.split(', ')
        if name.strip().lower() == name_to_update.strip().lower():
            updated_students.append(f"{name}, {new_grade}")
            found = True
            print(f"Student {name}'s grade updated to {new_grade}.")
        else:
            updated_students.append(student)

    if not found:
        print(f"Student {name_to_update} not found.")
    else:
        write_students(updated_students)


#Calculate and display the average grade of the class.
def show_class_average():
    students = read_students()
    if not students:
        print("No students found to calculate average.")
        return
    try: 
        grades = [int(student.split(', ')[1]) for student in students]
        avg = sum(grades) / len(grades)
        print(f"Class Average Grade: {avg:.2f}")
    except ValueError:
        print("Invalid grade data found. Cannot calculate average.")
