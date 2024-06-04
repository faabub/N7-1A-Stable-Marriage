class StableMarriage:
    def __init__(self, students, schools, serenading="students"):
        self.students = students
        self.schools = schools
        self.serenading = serenading
        self.rounds = 0

    def all_students_matched(self):
        for student in self.students:
            if student.school is None:
                return False
        return True

    def no_more_capacity(self):
        for school in self.schools:
            if not school.is_full():
                return False
        return True

    def run(self):
        while not self.all_students_matched() or self.no_more_capacity():
            # beginning of round/day
            self.rounds += 1

            # morning
            serenaded_schools = set()
            for student in self.students:
                if not student.is_free():
                    continue

                serenaded_school = student.get_next_school()
                while serenaded_school.is_full() and student.has_next_school():
                    serenaded_school = student.get_next_school()

                serenaded_schools.add(serenaded_school)
                serenaded_school.serenading_students.append(student)

            # afternoon
            for school in serenaded_schools:
                school.match_students()

class School:
    def __init__(self, name, capacity):
        self.name = name
        """name of the school"""

        self.capacity = capacity
        """number of students the school can take"""

        self.serenading_students = []
        """students who are serenading this school in the midst of a given round"""

        self.matched_students = set()
        """students who have been matched to this school"""

    def is_full(self):
        return len(self.matched_students) >= self.capacity

    def match_students(self):
        '''
        Match students in `self.serenading_students` to the school.\n
        Sets the student's school to `self` and add the student to `self.matched_students`.
        '''
        if (
            self.capacity == 0
            or len(self.serenading_students) == 0
            or self.is_full()
        ):
            return
        
        for student in self.serenading_students:
            if student in self.matched_students:
                continue

            student.school = self
            self.matched_students.append(student)

        self.serenading_students = []

    def __str__(self):
        return f"{self.name} with {self.capacity} seats"

    def __repr__(self):
        return f"{self.name} with {self.capacity} seats"


class Student:
    def __init__(self, name, preferences):
        self.name = name
        self.preferences = preferences
        self.school = None

    def __str__(self):
        return f"Name: {self.name}"

    def is_free(self):
        return self.school is None

    def get_next_school(self):
        return self.preferences.pop(0)
