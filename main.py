import json
import hashlib

def loadSetupData():
    with open('gc_setup.json') as data_file:
        course = json.load(data_file)

    return course["course_setup"]

def loadStudentGrades(st_id):
    try:
        new_file = open('gc_grades.json', 'r+')
        if new_file.readlines() == []:
           new_file.write("{}")
           new_file.close()
    except:
        new_file = open('gc_grades.json', "w")
        new_file.write("{}")
        new_file.close()

    with open('gc_grades.json') as data_file:
        student_grades = json.load(data_file)


    return student_grades

def UserInput():
    st_id = raw_input("Please enter your name. ").capitalize()
    ID = raw_input("Please enter you ID. ")
    password = raw_input("Please enter your password. ")
    return st_id, ID, password

def CheckPassword(st_id, ID, password, student_grades):
    p = hashlib.sha224(password).hexdigest()
    try:
        while True:
            if p == student_grades[ID]['password']:
                break
            else:
                password = raw_input("Wrong Password! Please try again! ")
                p = hashlib.sha224(password).hexdigest()
    except:
        pass

    return p

def askForAssignmentMarks(st_id, grades, ID, student_grades):
    current_grades = {ID: {"grades": {}, "name": st_id}}

    for key in grades:
        if ID in student_grades.keys():
            if student_grades[ID]["grades"][key] > -1:
                answer = raw_input("Your grade from " + key + " is " + str(student_grades[ID]["grades"][key]) + ". Do you want to change your grade for " + key + "?" + " Please write yes or no.")
                if answer == "yes":
                    student_answer = int(raw_input("What is your Current Grade for " + key + "? Please insert -1 if you don't have a grade yet."))
                    if (student_answer >= 0 and student_answer <= 100) or (student_answer == -1):
                        current_grades[ID]["grades"][key] = student_answer
                    else:
                        current_grades[ID]["grades"][key] = student_grades[ID]["grades"][key]
                        print "You should import a number between 0 and 100."
                else:
                    current_grades[ID]["grades"][key] = student_grades[ID]["grades"][key]
            else:
                student_answer = int(raw_input( "What is your Current Grade for " + key + "? Please insert -1 if you don't have a grade yet."))
                if (student_answer >= 0 and student_answer <= 100) or (student_answer == -1):
                    current_grades[ID]["grades"][key] = student_answer
                else:
                    current_grades[ID]["grades"][key] = student_grades[ID]["grades"][key]
                    print "You should import a number between 0 and 100."
        else:
            student_answer1 = int(raw_input("What is your Current Grade for " + key + "? Please insert -1 if you don't have a grade yet."))
            if (student_answer1 >= 0) and (student_answer1 <= 100) or (student_answer1 == -1):
                current_grades[ID]["grades"][key] = student_answer1


    return current_grades

def saveGrades(st_id, student_grades, current_grades, ID, p):
    student_grades[current_grades.keys()[0]] = current_grades[current_grades.keys()[0]]
    student_grades[ID]['name'] = st_id
    student_grades[ID]['password'] = p
    file = open("gc_grades.json", "w")
    file.write(json.dumps(student_grades))
    file.close()

def printCurrentGrade(st_id, grades, ID, current_grades):
    curr_grade = 0
    for key in current_grades[ID]["grades"]:
        if current_grades[ID]["grades"][key] != -1:
            calc_grade = float(current_grades[ID]["grades"][key]) * grades[key] / 100
            curr_grade = curr_grade + calc_grade

    print float(curr_grade)
    return curr_grade

def printLetterGrade(curr_grade, matrix):
    for i in range(len(matrix)):
        if matrix[i]["min"] < curr_grade and matrix[i]["max"] >= curr_grade:
            print matrix[i]["mark"]


def main():
    course = loadSetupData()
    grades = course["grade_breakdown"]
    conv_matrix = course["conv_matrix"]
    st_id, ID, password = UserInput()
    p = CheckPassword(ID, st_id, password, grades)
    student_grades = loadStudentGrades(st_id)
    current_grades = askForAssignmentMarks(st_id, grades, ID, student_grades)
    saveGrades(st_id, student_grades, current_grades, ID, p)
    curr_grade = printCurrentGrade(st_id, grades, ID, current_grades)
    printLetterGrade(curr_grade, conv_matrix)

main()