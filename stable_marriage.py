class School:
    def __init__(self, name, students, capacity):
        self.name = name
        self.students = students
        self.capacity = capacity


class Student:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class StableMarriage:
    def __init__(self, data, serenader="student", verbose=False):
        self.serenader = serenader
        self.rounds = 0
        if self.serenader not in {"student", "school"}:
            raise ValueError("serenading must be either 'student' or 'school'")

        if self.serenader == "student":
            # students serenade schools
            # init schools as a set of Serenadees
            self.serenadees = {
                Serenadee(
                    school["name"],
                    school["preferences"],
                    school["capacity"],
                    verbose=verbose,
                )
                for school in data["schools"]
            }

            # init students as a set of Serenaders
            self.serenaders = {
                Serenader(student["name"], student["preferences"])
                for student in data["students"]
            }
        else:
            # schools serenade students
            # init students as a set of Serenadees
            self.serenadees = {
                Serenadee(student["name"], student["preferences"], verbose=verbose)
                for student in data["students"]
            }

            # init schools as a set of Serenaders
            self.serenaders = {
                Serenader(school["name"], school["preferences"], school["capacity"])
                for school in data["schools"]
            }

        # debugging
        self.verbose = verbose

    def get_rounds(self):
        return self.rounds

    def get_schools(self):
        if self.serenader == "student":
            return {
                School(
                    serenadee.name,
                    [Student(s.name) for s in serenadee.matched_serenaders],
                    serenadee.capacity,
                )
                for serenadee in self.serenadees
            }
        else:
            return {
                School(
                    serenader.name,
                    [Student(s.name) for s in serenader.matched],
                    serenader.capacity,
                )
                for serenader in self.serenaders
            }

    def get_unmatched_students(self):
        if self.serenader == "student":
            return {
                Student(serenader.name)
                for serenader in self.serenaders
                if not serenader.is_fulfilled()
            }
        else:
            return {
                Student(serenadee.name)
                for serenadee in self.serenadees
                if not serenadee.is_fulfilled()
            }

    def all_serenaders_fulfilled(self):
        return all(serenader.is_fulfilled() for serenader in self.serenaders)

    def all_serenadees_fulfilled(self):
        return all(serenadee.is_fulfilled() for serenadee in self.serenadees)

    def run(self):
        # exit conditions:
        # - all serenaders are fulfilled
        #   - schools: all schools are full
        #   - students: all students have found a school
        # - all serenadees are fulfilled
        #   - students: all students have found a school
        #   - schools: all schools are full
        while (
            not self.all_serenaders_fulfilled() and not self.all_serenadees_fulfilled()
        ):
            # beginning of round/day
            self.rounds += 1
            if self.verbose:
                print()
                print("---------------------------------")
                print(f"Round {self.rounds} begins")

            # morning: serenaders go serenade who they like
            if self.verbose:
                print("--------")
                print("Morning:")
                print("--------")
            for serenader in self.serenaders:
                if self.verbose:
                    print(f"- {serenader.name} serenades:")

                if self.verbose:
                    # these checks are not necessary and are already accounted for in "serenader.pop_next_preferences()"

                    if serenader.is_fulfilled():
                        print(f"{serenader.name} is already fulfilled")

                    if len(serenader.preferences) == 0:
                        print(f"{serenader.name} has no more preferences")

                # serenade the n=capacity first preferences
                for serenadee_name in serenader.pop_next_preferences():
                    # find the serenadee from its name
                    serenadee = next(
                        serenadee
                        for serenadee in self.serenadees
                        if serenadee.name == serenadee_name
                    )
                    serenadee.new_serenaders.add(serenader)

                    if self.verbose:
                        print(f"{serenader.name} serenades {serenadee.name}")

            # afternoon/evening: serenadees match the n=capacity most preferred serenaders and rejects the rest
            if self.verbose:
                print("------------------")
                print("Afternoon/Evening:")
                print("------------------")
            for serenadee in self.serenadees:
                # match and reject serenaders for serenadees that have new serenaders
                if len(serenadee.new_serenaders) > 0:
                    if self.verbose:
                        print(f"- {serenadee.name} matches and rejects serenaders:")
                    serenadee.match_and_reject()

            if self.verbose:
                print()
                print(f"Round {self.rounds} ends")
                print("---------------------------------")


class Serenadee:
    def __init__(self, name, preferences, capacity=1, verbose=False):
        self.name = name
        self.preferences = preferences
        self.capacity = capacity
        self.verbose = verbose

        self.new_serenaders = set()
        """new serenaders from a round"""
        self.matched_serenaders = []
        """serenaders who are temporarily matched to the serenadee (and that are carried over to the next round)"""

    def is_fulfilled(self):
        return len(self.matched_serenaders) >= self.capacity

    def match_and_reject(self):
        """
        Match serenaders to the serenadee, given the serenadee's preferences.\n

        Match the first `self.capacity` serenaders and reject the rest.\n
        Matched serenaders are added to `self.matched_serenaders` and have their `matched` updated to include `self`.\n
        Rejected serenaders have their `matched` updated to remove `self`.
        """
        if len(self.new_serenaders) == 0:
            # no new serenaders this round
            # shouldn't happen since this function is only called on serenadees with new serenaders
            if self.verbose:
                print(f"{self.name} has no new serenaders this round")
            return

        if self.verbose:
            print(f"current serenaders for {self.name}: {self.matched_serenaders}")
            print(f"new serenaders for {self.name}: {self.new_serenaders}")

        # all serenaders that are matched to the serenadee (temporarily over capacity)
        self.matched_serenaders = list(
            set(self.matched_serenaders).union(self.new_serenaders)
        )
        self.new_serenaders.clear()

        if len(self.matched_serenaders) <= self.capacity:
            # all new serenaders can be matched
            if self.verbose:
                print(f"enough capacity: all serenaders can be matched to {self.name}")
            for serenader in self.matched_serenaders:
                serenader.matched.add(self)
        else:
            # not all new serenaders can be matched
            # match the first `self.capacity` preferred serenaders
            if self.verbose:
                print(
                    f"not enough capacity: only the first {self.capacity} preferred serenaders can be matched to {self.name}"
                )

            # sort the serenaders by their preference (index in the preferences list)
            self.matched_serenaders.sort(
                key=lambda serenader: self.preferences.index(serenader.name)
            )

            if self.verbose:
                print(f"sorted serenaders by preference: {self.matched_serenaders}")

            # reject the serenaders that are not in the first `self.capacity`
            for serenader in self.matched_serenaders[self.capacity :]:
                serenader.matched.discard(self)

                if self.verbose:
                    print(f"{serenader.name} is rejected from {self.name}")

            # delete the rejected serenaders
            del self.matched_serenaders[self.capacity :]

            # match the first `self.capacity` serenaders
            for serenader in self.matched_serenaders:
                serenader.matched.add(self)

        if self.verbose:
            print(f"matched serenaders for {self.name}: {self.matched_serenaders}")


class Serenader:
    def __init__(self, name, preferences, capacity=1):
        self.name = name
        self.preferences = preferences
        """
        List of preferences from most to least preferred.\n
        The preferences are the names of the serenadees.\n
        When a preference is gotten, it is removed from this list.
        """

        self.capacity = capacity

        self.matched = set()

    def is_fulfilled(self):
        return len(self.matched) >= self.capacity

    def available_capacity(self):
        return self.capacity - len(self.matched)

    def pop_next_preferences(self):
        """
        Get the next preferences to serenade that the serenader has not serenaded yet.\n
        There will be `min(len(self.preferences), self.available_capacity())` preferences returned.\n
        They are removed from `self.preferences`.\n
        """
        available_capacity = self.available_capacity()
        result = self.preferences[:available_capacity]
        del self.preferences[:available_capacity]
        return result

    def __repr__(self):
        return self.name
