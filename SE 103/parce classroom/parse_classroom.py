'''This file has to be in your environment folder
Otherwise you need to use directory of file where it has saved
'''

SIMPLE_CLASSROOM_PATH = "classroom_simple.txt"


def read_file(filename):
    '''Reading a file lines and return in a str form'''
    with open(filename, 'r', encoding='utf-8') as fileobj:
        data = fileobj.read().rstrip()
    return data


def separated_lines(text):
    '''Split Lines with argument "#"
    Check if there is "\n" char in replace it with " "
    Then Replace singe '\n' with (" ") '''
    alist = text.split('#')
    clean_list = []
    for line in alist:
        if line != '':
            line = line.replace('\n', ' ')
            line = line.strip()
            clean_list.append(line)
    return clean_list


def single_space_index(text):
    '''Return index of space'''
    return text.find(' ')


def find_number_index(text):
    '''Return first number occurence as index'''
    for char in text:
        if char.isnumeric():
            return text.find(char)
    return None


def convert_int(text):
    '''Using strip() method to clean whitespace
    Then return converted value'''
    text = text.strip()
    return int(text)


def create_rows(alist):
    '''Using string slicing to extract:
    name: str
    country: str
    grades: list of integer'''
    students = []
    for line in alist:
        student = {}
        first_space = single_space_index(line)
        name = line[:first_space].strip()
        student['name'] = name
        # Slicing country part till numeric faction
        partician = line[first_space+1:]
        numeric_index = find_number_index(partician)
        country_part = partician[:numeric_index].strip()
        student['country'] = country_part
        # Slicing numeric part according first index of number
        numeric_part = partician[numeric_index:]
        grades = numeric_part.split()
        grades = list(map(convert_int, grades))
        student['grades'] = grades
        students.append(student)
    return students


def parse_simple_classroom(file_path):
    """ Parse classroom file that is given in `file_path` parameter.
    Returns a list of dictionaries describing the students in the classroom,
    each student is describe with the dictionary: {
      'name': ...,
      'country': ...,
      'grades': [...]
    }"""
    student_list = read_file(file_path)
    list_students = separated_lines(student_list)
    students = create_rows(list_students)
    return students


def student_avg(students, student_name):
    '''Calculate average grade of given student name'''
    for student in students:
        # print(student['name'])
        if student['name'] == student_name:
            # print(student['name'])
            grades = student['grades']
            # print(grades)
            average = sum(grades) / len(grades)
            # print(average)
            return round(average, 2)
    return None


def main():
    """Function Flow"""
    student_name = input('Enter the Student Name: ')
    students_list = parse_simple_classroom(SIMPLE_CLASSROOM_PATH)
    avg = student_avg(students_list, student_name)
    if not avg is None:
        print(f'{student_name} avereage is {avg}')
    else:
        print(f'No record found for {student_name}')


def main_2():
    """Function Flow"""
    student_name = input('Enter the Student Name: ')
    students_list = parse_simple_classroom('classroom_complex.txt')
    avg = student_avg(students_list, student_name)
    if not avg is None:
        print(f'{student_name} avereage is {avg}')
    else:
        print(f'No record found for {student_name}')


if __name__ == '__main__':
    main()
    main_2()
