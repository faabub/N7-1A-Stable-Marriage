class StableMarriage:
    def __init__(self, data, serenading="student", verbose=False):
        self.serenaders = serenading
        self.rounds = 0
        if self.serenaders not in {"student", "school"}:
            raise ValueError("serenading must be either 'student' or 'school'")
        
        if self.serenaders == "student":
            # students serenade schools
            # init students as a set of Serenaders
            self.serenaders = {Serenader(student['name'], student['preferences']) for student in data['students']}

            # init schools as a set of Serenadees
            self.serenadees = {Serenadee(school['name'], school['preferences'], school['capacity']) for school in data['schools']}
        else:
            # schools serenade students
            # init students as a set of Serenadees
            self.serenadees = {Serenadee(student['name'], student['preferences']) for student in data['students']}

            # init schools as a set of Serenaders
            self.serenaders = {Serenader(school['name'], school['preferences'], school['capacity']) for school in data['schools']}

        # debugging
        self.verbose = verbose

    def all_serenaders_matched(self):
        for serenader in self.serenaders:
            if serenader.is_free():
                return False
        return True

    def all_serenadees_full(self):
        for serenadee in self.serenadees:
            if not serenadee.is_full():
                return False
        return True

    def run(self):
        # exit conditions:
        # - all serenaders are matched
        #   - schools: all schools are not free -> all schools are full
        #   - students: all students are not free -> all students have a school
        # - all serenadees are full
        #   - students: all students have found a school
        #   - schools: all schools are full
        while not (self.all_serenaders_matched() or self.all_serenadees_full()):
            # beginning of round/day
            self.rounds += 1
            if self.verbose:
                print(f"Round {self.rounds}")
                print("---------------------------------")

            # morning: serenaders go serenade serenadees
            round_serenadees = set() # serenadees that are serenaded in the current round
            for serenader in self.serenaders:
                if self.verbose:
                    print(f"{serenader.name} serenades:")

                # serenade as long as the serenader is free and has preferences
                while

                if not serenader.is_free():
                    # serenader is already matched: school is full or student has a school
                    if self.verbose:
                        print(f"{serenader.name} is already matched, and keeps serenading")
                    continue

                if not serenader.has_next_preference():
                    # free serenader has no more preferences, should be impossible since it would mean serenadees are all full and thus would have stopped the loop
                    if self.verbose:
                        print(f"{serenader.name} has no more preferences")
                    continue

                # get the next serenadee to serenade
                serenadee_name = serenader.get_next_preference()
                serenaded = next(serenadee for serenadee in self.serenadees if serenadee.name == serenadee_name)

                round_serenadees.add(serenaded)
                serenaded.serenaders.add(serenader)

                if self.verbose:
                    print(f"{serenader.name} serenades {serenaded.name}")
                    print("---------------------------------")

            # afternoon/evening: serenadees keep the n = capacity most preferred serenaders and kicks the rest
            for serenadee in round_serenadees:
                serenadee.keep_and_kick_serenaders()

class Serenadee:
    def __init__(self, name, preferences, capacity=1):
        self.name = name
        self.preferences = preferences
        self.capacity = capacity

        self.serenaders = set()
        """serenaders in the midst of a given round"""
        self.matched = set()
        """serenaders who are temporarily matched to the serenadee"""

    def is_full(self):
        return len(self.matched) >= self.capacity

    def keep_and_kick_serenaders(self):
        '''
        Match serenaders in `self.serenaders` to the serenadee.\n
        Adds `self` to `serenader.matched` and add the serenadee to `self.matched`.
        '''
        if (
            self.capacity == 0
            or len(self.serenaders) == 0
            or self.is_full()
        ):
            if self.verbose:
                print(f"{self.name} is full or has no serenaders to match")
            return
        
        for serenader in self.serenaders:
            if serenader in self.matched:
                # serenader is already matched to the serenadee, should be impossible since serenaders are removed from serenadee.serenaders after being matched
                if self.verbose:
                    print(f"{serenader.name} is already matched to {self.name}")
                continue

            if len(self.matched) >= self.capacity:
                # serenadee is full
                if self.verbose:
                    print(f"{self.name} is full: {serenader.name} is not matched")
                break

            self.matched.add(serenader)
            serenader.matched.add(self)

        self.serenaders = set()

class Serenader:
    def __init__(self, name, preferences, capacity=1):
        self.name = name
        self.preferences = preferences
        self.capacity = capacity

        self.matched = set()

    def is_free(self):
        return len(self.matched) <= self.capacity

    def get_next_preference(self):
        return self.preferences.pop(0)

    def has_next_preference(self):
        return len(self.preferences) > 0
