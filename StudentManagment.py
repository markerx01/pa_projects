class Student:
    def __init__(self, id, name, grade, age):
        self.id = id
        self.name = name
        self.grade = grade
        self.age = age

    def __str__(self): #ToString
        return f"ID: {self.id}, Name: {self.name}, Grade: {self.grade}, Age: {self.age}"

class StudentManagementSystem:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)
        print(f"Student {student.name} added successfully.")

    def remove_student(self, student_id):
        for student in self.students:
            if student.id == student_id:
                self.students.remove(student)
                print(f"Student with ID {student_id} removed successfully.")
                return
        print(f"Student with ID {student_id} not found.")

    def view_students(self):
        if not self.students:
            print("No students in the system.")
        else:
            for student in self.students:
                print(student)

    def search_student(self, student_id):
        for student in self.students:
            if student.id == student_id:
                print(student)
                return
        print(f"Student with ID {student_id} not found.")

    def run(self):
        while True:
            print("\nStudent Management System")
            print("1. Add Student")
            print("2. Remove Student")
            print("3. View All Students")
            print("4. Search Student")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                id = input("Enter student ID: ")
                name = input("Enter student name: ")
                grade = input("Enter student grade: ")
                age = input("Enter student age: ")
                student = Student(id, name, grade, age)
                self.add_student(student)
            elif choice == '2':
                id = input("Enter student ID to remove: ")
                self.remove_student(id)
            elif choice == '3':
                self.view_students()
            elif choice == '4':
                id = input("Enter student ID to search: ")
                self.search_student(id)
            elif choice == '5':
                print("Exiting the system.")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    sms = StudentManagementSystem()
    sms.run()
#אני פשוט ראיתי שאמרתם שלא הגשתי את הפרויקט ואני לא מצאתי איפה הוא אז ניחשתי