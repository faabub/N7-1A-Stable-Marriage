import stable_marriage as sm, json


if __name__ == "__main__":    
    f = open('data.json')

    data = json.load(f)

    # main program
    print("Welcome to the School Allocation System\n")
    answer = 0
    while answer not in range(1, 3):
        try:
            print("Please select an option from the following:")
            print("1. Students serenade schools")
            print("2. Schools serenade students")
            answer = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a valid choice\n")
            continue
    
    if answer == 1:
        serenading = "students"
    elif answer == 2:
        serenading = "schools"

    stable_marriage = sm.StableMarriage(data, serenading=serenading)

    stable_marriage.run()

    schools = stable_marriage.get_schools()
    unmatched_students = stable_marriage.get_unmatched_students()
    rounds = stable_marriage.get_rounds()


    print(f"School Allocation completed in {rounds} rounds")
    print("The following students have been allocated to the following schools:\n")
    for school in schools:
        print(f"{school.name}: {school.students}\n")

    print("The following students could not be allocated to any school:\n")
    for student in unmatched_students:
        if student.school is None:
            print(student.name)

    f.close()