"""
Oliver Wilkins
08/10/2018
"""

# Imports

import csv
from tkinter import *
from tkinter import filedialog


def get_file_location():
    root = Tk()
    root.filename = filedialog.askopenfilename()
    root.withdraw()
    return root.filename


with open(get_file_location(), encoding='utf-8') as csvfile:
    # Opens the gmclrmp.full csv file
    # Please note that il you don't pick the correct file, the script will crash!
    reader = csv.DictReader(csvfile)
    with open('output.csv', 'w', encoding='utf-8', newline='') as writefile:
        # Opens/makes the new file we want to write to
        fieldnames = [
            "id",
            "gmc_number",
            "last_name",
            "first_name",
            "graduation_dt",
            "medical_school_id",
            "#medical_school",
            "degree_type_id",
            "programme_id",
            "hospital_id",
            "subspecialty_id",
            "grade_id",
            "subgrade_id",
            "programme_start_dt",
            "programme_end_dt",
            "gender"
        ]

        # Setting up the heading names/columns

        school_rows = []
        degree_rows = []
        training_rows = []
        subspecial_rows = []
        grade_rows = []
        # These arrays will hold the needed data from the lookup tables

        writer = csv.DictWriter(writefile, fieldnames=fieldnames)

        writer.writeheader()  # Writes the headers to the output file

        with open('lookup/table_1.csv', encoding='utf-8') as school_file:
            school_reader = csv.DictReader(school_file)
            for school_file_row in school_reader:
                school_rows.append([
                    school_file_row['gmc.`Place Of Qualification'],
                    school_file_row['db.medical_school_id']
                ])

        with open('lookup/table_2.csv', encoding='utf-8') as degree_file:
            degree_reader = csv.DictReader(degree_file)
            for degree_file_row in degree_reader:
                degree_rows.append([
                    degree_file_row['gmc.`Qualification`'],
                    degree_file_row['db.degree_type_id']
                ])

        with open('lookup/table_6.csv', encoding='utf-8') as training_file:
            training_reader = csv.DictReader(training_file)
            for training_file_row in training_reader:
                training_rows.append([
                    training_file_row['gmc.`Training Deanery/LETB`'],
                    training_file_row['Training Programme Specialty'],
                    training_file_row['db.programme_id'],
                    training_file_row['duration'],
                    training_file_row['db.programme_level']
                ])

        with open('lookup/table_7.csv', encoding='utf-8') as subspecial_file:
            subspecial_reader = csv.DictReader(subspecial_file)
            for subspecial_file_row in subspecial_reader:
                subspecial_rows.append([
                    subspecial_file_row['GMC.`Training Programme Specialty`'],
                    subspecial_file_row['db.subspecialty_id']
                ])

        with open('lookup/table_9.csv', encoding='utf-8') as grade_file:
            grade_reader = csv.DictReader(grade_file)
            for grade_file_row in grade_reader:
                grade_rows.append([
                    grade_file_row['db.subgrade_id'],
                    grade_file_row['db.grade_id']
                ])

        # Opens the lookup tables needed and appends the needed info to arrays

        for row in reader:
            # Iterates through every row in the gmclrmp.full file
            # Note: In each case, row will be a dictionary!
            qual_year = int(row['Year Of Qualification'])

            gmc_number = row['GMC Ref No']
            last_name = row['Surname']
            first_name = row['Given Name']
            graduation_dt = row['Year Of Qualification'] + '-07-01'

            medical_school_id = ''
            for school_row in school_rows:
                if row['Place of Qualification'] == school_row[0]:
                    medical_school_id = school_row[1]

            degree_type_id = ''
            for degree_row in degree_rows:
                if row['Qualification'] == degree_row[0]:
                    degree_type_id = degree_row[1]

            programme_id = ''
            duration = ''
            programme_level = ''
            for training_row in training_rows:
                if(
                    row['Training Deanery/LETB'] == training_row[0] and
                    row['Training Programme Specialty'] == training_row[1]
                ):
                    programme_id = training_row[2]
                    duration = training_row[3]
                    programme_level = training_row[4]

            if qual_year == 2018 or qual_year == 2017:
                programme_level = '1'
                duration = '2'

            subspecialty_id = ''
            for subspecial_row in subspecial_rows:
                if row['Training Programme Specialty'] == subspecial_row[0]:
                    subspecialty_id = subspecial_row[1]

            if(
                row['Registration Status'] == 'Registered with Licence' or
                row['Registration Status'] == 'Provisionally registered with Licence'
            ):
                if row['Specialist Register Date'] != '':
                    subgrade_id = '1'
                elif qual_year == 2018:
                    subgrade_id = '16'
                elif qual_year == 2017:
                    subgrade_id = '15'
                elif(qual_year == 2016):
                    subgrade_id = '12'
                elif qual_year == 2015:
                    subgrade_id = '11'
                elif qual_year == 2014:
                    subgrade_id = '9'
                elif qual_year == 2013:
                    subgrade_id = '8'
                elif qual_year == 2012:
                    subgrade_id = '7'
                elif qual_year == 2011:
                    subgrade_id = '6'
                elif qual_year <= 2010:
                    subgrade_id = '5'
            else:
                subgrade_id = ''

            grade_id = ''
            for grade_row in grade_rows:
                if subgrade_id == grade_row[0]:
                    grade_id = grade_row[1]

            programme_start_dt = ''
            programme_end_dt = ''

            for year in range(1900, 2020):
                if(
                    qual_year == year and
                    programme_level == '1' and
                    duration == '2'
                ):
                    programme_start_dt = f'{year}-08-01'
                    programme_end_dt = f'{year + int(duration)}-08-01'
                elif(
                    qual_year == year and
                    programme_level == '4' and
                    duration == '5'
                ):
                    programme_start_dt = f'{year + 4}-08-01'
                    programme_end_dt = f'{year + 4 + int(duration)}-08-01'
                elif(
                    qual_year == year and
                    programme_level == '2' and
                    duration == '2'
                ):
                    programme_start_dt = f'{year + 2}-08-01'
                    programme_end_dt = f'{year + 2 + int(duration)}-08-01'
                elif(
                    qual_year == year and
                    programme_level == '3' and
                    duration == '3'
                ):
                    programme_start_dt = f'{year + 2}-08-01'
                    programme_end_dt = f'{year + 2 + int(duration)}-08-01'
                elif(
                    qual_year == year and
                    programme_level == '3' and
                    duration == '7'
                ):
                    programme_start_dt = f'{year + 2}-08-01'
                    programme_end_dt = f'{year + 2 + int(duration)}-08-01'

            gender = row['Gender']

            writer.writerow({
                'id': '',
                'gmc_number': gmc_number,
                'last_name': last_name,
                'first_name': first_name,
                'graduation_dt': graduation_dt,
                'medical_school_id': medical_school_id,
                '#medical_school': '',
                'degree_type_id': degree_type_id,
                'programme_id': programme_id,
                'hospital_id': '',
                'subspecialty_id': subspecialty_id,
                'grade_id': grade_id,
                'subgrade_id': subgrade_id,
                'programme_start_dt': programme_start_dt,
                'programme_end_dt': programme_end_dt,
                'gender': gender
            })
            # Each iteration, the row is written to the new file

            # print(f'Person: {first_name} {last_name} written!')
