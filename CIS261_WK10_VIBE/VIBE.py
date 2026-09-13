# Mia Smothers
# CIS261
# WK10 VIBE Coding

from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent.parent / "student_grades.txt"


class Student:
	"""Store one student's information and calculated grade."""

	def __init__(self, name, student_id, test1, test2, test3):
		self.name = name
		self.student_id = student_id
		self.test1 = float(test1)
		self.test2 = float(test2)
		self.test3 = float(test3)
		self.average = (self.test1 + self.test2 + self.test3) / 3
		self.grade = self.calculate_grade()

	def calculate_grade(self):
		if self.average >= 90:
			return "A"
		if self.average >= 80:
			return "B"
		if self.average >= 70:
			return "C"
		if self.average >= 60:
			return "D"
		return "F"

	def to_file_line(self):
		return (f"{self.name}|{self.student_id}|{self.test1:.2f}|"
			    f"{self.test2:.2f}|{self.test3:.2f}|{self.average:.2f}|"
			    f"{self.grade}\n")

	@classmethod
	def from_file_line(cls, line):
		fields = line.strip().split("|")
		if len(fields) != 7:
			raise ValueError("record must contain 7 pipe-delimited fields")
		return cls(fields[0], fields[1], fields[2], fields[3], fields[4])


def load_students():
	students = []
	try:
		with DATA_FILE.open("r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				if not line.strip():
					continue
				try:
					students.append(Student.from_file_line(line))
				except ValueError as error:
					print(f"Skipped invalid record on line {line_number}: {error}")
	except FileNotFoundError:
		print(f"{DATA_FILE.name} was not found. Starting with no records.")
	except OSError as error:
		print(f"Could not load {DATA_FILE.name}: {error}")
	return students


def save_students(students):
	try:
		with DATA_FILE.open("w", encoding="utf-8") as file:
			for student in students:
				file.write(student.to_file_line())
		print(f"Saved {len(students)} student record(s) to {DATA_FILE.name}.")
	except OSError as error:
		print(f"Could not save {DATA_FILE.name}: {error}")


def prompt_text(message):
	value = input(message)
	if value == "\x1b":
		return None
	return value.strip()


def prompt_score(test_number):
	while True:
		value = prompt_text(f"Test {test_number} score (0-100): ")
		if value is None:
			return None
		try:
			score = float(value)
			if 0 <= score <= 100:
				return score
			print("Enter a score between 0 and 100.")
		except ValueError:
			print("Enter a valid number.")


def add_student(students):
	print("\nAdd Student. Press ESC at any prompt to cancel.")
	name = prompt_text("Student name: ")
	if name is None:
		return
	student_id = prompt_text("Student ID: ")
	if student_id is None:
		return
	if not name or not student_id:
		print("Name and student ID cannot be blank.")
		return

	scores = []
	for test_number in range(1, 4):
		score = prompt_score(test_number)
		if score is None:
			return
		scores.append(score)
	students.append(Student(name, student_id, *scores))
	print("Student record added.")


def display_students(students):
	if not students:
		print("\nNo student records found.")
		return
	print("\nStudent Records")
	print("-" * 88)
	print(f"{'Name':<22}{'ID':<12}{'Test 1':>10}{'Test 2':>10}{'Test 3':>10}{'Average':>10}{'Grade':>8}")
	print("-" * 88)
	for student in students:
		print(f"{student.name:<22.22}{student.student_id:<12.12}"
			  f"{student.test1:>10.2f}{student.test2:>10.2f}"
			  f"{student.test3:>10.2f}{student.average:>10.2f}"
			  f"{student.grade:>8}")
	print("-" * 88)


def display_statistics(students):
	if not students:
		print("\nNo student records available for statistics.")
		return
	averages = [student.average for student in students]
	print("\nClass Statistics")
	print(f"Highest average: {max(averages):.2f}")
	print(f"Lowest average:  {min(averages):.2f}")
	print(f"Class average:   {sum(averages) / len(averages):.2f}")


def search_student(students):
	search_name = prompt_text("Search by name (press ESC to cancel): ")
	if search_name is None:
		return
	matches = [student for student in students
		       if search_name.lower() in student.name.lower()]
	if matches:
		display_students(matches)
	else:
		print("No matching students found.")


def show_menu():
	print("\nStudent Grade Calculator")
	print("1. Add student")
	print("2. Display all students")
	print("3. Display class statistics")
	print("4. Search by student name")
	print("5. Save and exit")
	print("Press ESC to save and exit")


def main():
	students = load_students()
	print(f"Loaded {len(students)} student record(s).")
	while True:
		show_menu()
		choice = input("Select an option: ").strip()
		if choice == "\x1b" or choice == "5":
			save_students(students)
			print("Goodbye!")
			return
		if choice == "1":
			add_student(students)
		elif choice == "2":
			display_students(students)
		elif choice == "3":
			display_statistics(students)
		elif choice == "4":
			search_student(students)
		else:
			print("Invalid choice. Select 1, 2, 3, 4, 5, or ESC.")


if __name__ == "__main__":
	main()






