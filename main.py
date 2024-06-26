import stable_marriage as sm, json

if __name__ == "__main__":
    f = open("data.json")

    data = json.load(f)

    # main program
    print("Welcome to the School Allocation System")
    answer = 0
    while answer not in range(1, 5):
        try:
            print("Please select an option from the following:")
            print("-------------------------------------------")
            print("1. Students serenade schools")
            print("2. Schools serenade students")
            print("3. Students serenade schools (verbose)")
            print("4. Schools serenade students (verbose)")
            answer = int(input("Enter your choice: "))
        except:
            continue

    if answer == 1:
        serenading = "student"
        verbose = False
    elif answer == 2:
        serenading = "school"
        verbose = False
    elif answer == 3:
        serenading = "student"
        verbose = True
    elif answer == 4:
        serenading = "school"
        verbose = True

    stable_marriage = sm.StableMarriage(data, serenader=serenading, verbose=verbose)

    stable_marriage.run()

    rounds = stable_marriage.get_rounds()
    schools = stable_marriage.get_schools()
    unmatched_students = stable_marriage.get_unmatched_students()

    print(f"\nSchool Allocation completed in {rounds} rounds\n")
    print("The students have been allocated to the following schools:")
    for school in schools:
        print(
            f"{school.name} ({len(school.students)}/{school.capacity}):\n {school.students}"
        )

    print()
    if len(unmatched_students) == 0:
        print("All students have been allocated to a school")
    else:
        print("The following students could not be allocated to any school:")
        print(unmatched_students)

    f.close()
