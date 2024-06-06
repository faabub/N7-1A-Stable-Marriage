class StableMarriage:
    def __init__(self, data, serenaders="students", verbose=False):
        self.students = set(Student(student['name'], student['preferences']) for student in data['students'])
        self.schools = set(School(school['name'], school['preferences'], school['capacity']) for school in data['schools'])
        self.serenaders = serenaders
        self.rounds = 0

        #
        self.serenaders = self.students if serenaders == "students" else self.schools
        self.serenadees = self.schools if serenaders == "schools" else self.students
        # debugging
        self.verbose = verbose

    def all_students_matched(self):
        for student in self.students:
            if student.school is None:
                return False
        return True

    def all_schools_full(self):
        for school in self.schools:
            if not school.is_full():
                return False
        return True

    def run(self):
        while not self.all_students_matched() or self.all_schools_full():
            # beginning of round/day
            self.rounds += 1

            # morning: serenaders go serenade serenadees
            serenaded_serenadees = set()
            for serenader in self.serenaders:
                if not serenader.is_free():
                    continue

                serenaded_name = serenader.get_next()
                serenaded = next(element for element in self.serenadees if element.name == serenaded_name)

                serenaded_serenadees.add(serenaded)
                serenaded.serenaders.add(serenader)

            # afternoon/evening: serenadees keep the n=capacity most preferred serenaders and kicks the rest
            for serenadee in serenaded_serenadees:
                serenadee.keep_and_kick_serenaders()

class Serenadee:
    def __init__(self, name, preferences, capacity=1):
        self.name = name
        self.preferences = preferences
        self.capacity = capacity

        self.serenaders = set()
        """serenaders in the midst of a given round"""
        self.matched = set()
        """serenaders who are temporarily matched to this school"""

    def is_full(self):
        return len(self.matched) >= self.capacity

    def match_students(self):
        '''
        Match students in `self.serenading_students` to the school.\n
        Sets the student's school to `self` and add the student to `self.matched_students`.
        '''
        if (
            self.capacity == 0
            or len(self.serenaders) == 0
            or self.is_full()
        ):
            return
        
        for serenader in self.serenaders:
            if serenader in self.matched:
                continue

            serenader.school = self
            self.matched.append(serenader)

        self.serenaders = set()

class Serenader:
    def __init__(self, name, preferences, capacity=1):
        self.name = name
        self.preferences = preferences
        self.capacity = capacity

        self.serenadees = set()

    def is_free(self):
        return len(self.serenadees) != self.capacity

    def get_next(self):
        return self.preferences.pop(0)

    def has_next(self):
        return len(self.preferences) > 0
