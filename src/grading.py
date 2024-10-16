# The MIT License (MIT)
# Copyright (c) 2020 Mehdi Ataei
# Modified by Ti-Chung Cheng

import csv
import logging
from os.path import exists

from tqdm import tqdm

from src.canvas_wrapper import (fetch_student_id_mapping, get_all_submissions,
                            get_student_mapping, upload_grade_with_comment)


def grader_initialization(course, assignment_id):

    logging.warning('Retrieving user information...')
    users = course.get_users(enrollment_type=['student'])

    logging.warning('Checking student metadata...')
    if not exists('metadata/canvas.student.csv'):
        logging.warning('No metadata found, creating one...')
        fetch_student_id_mapping(users)

    logging.warning('Retrieving all submissions...')
    assignment = course.get_assignment(assignment_id)
    submissions = get_all_submissions(users, course, assignment)

    return submissions


def grade_upload(submissions, gradebook):

    # create student - canvas ID mapping
    logging.warning('Building student index...')
    students, reversed_student = get_student_mapping(
        filename='metadata/canvas.student.csv')

    # read in grading data
    logging.warning('Reading grade information...')
    input_grade = {}
    gb = csv.reader(open(gradebook))
    next(gb, None)
    for entry in gb:
        if entry[0] not in students:
            logging.warning(entry[0] + ' is not on canvas.')
            continue
        if entry[1].strip() == "":
            logging.warning(entry[0] + ' does not have a (valid) score. Assuming 0.')
            entry[1] = '0'
        
        try:
            # Attempt to parse as a float, which is valid for numeric grades
            input_grade[students[entry[0]]] = {
                "netid": entry[0],
                "grade": float(entry[1].strip()),
                "comments": entry[2].strip().replace('$$$', ',')
            }
        except ValueError:
            non_numeric_grades = [
                'A+', 'A', 'A-', 
                'B+', 'B', 'B-', 
                'C+', 'C', 'C-', 
                'D+', 'D', 'D-', 
                'F', 'Ex', 'EX'
            ]
            # Handle non-numeric grades
            grade = entry[1].strip().upper()  # Convert grade to uppercase for uniformity
            if grade in non_numeric_grades:
                input_grade[students[entry[0]]] = {
                    "netid": entry[0],
                    "grade": grade,
                    "comments": entry[2].strip().replace('$$$', ',')
                }
            else:
                logging.critical('Something critical happened for ' +
                                entry[0] + ': the entry is: ' + str(entry) +
                                '. It might be uploading grades that are non-values that are not predefined in the system.')
    # writing to canvas
    logging.warning('Pushing updates to canvas...')
    for _, submission in tqdm(submissions.items()):
        canvas_id = str(submission.user_id)
        try:
            if canvas_id in input_grade:
                record = input_grade[canvas_id]
                upload_grade_with_comment(
                    submission, record['grade'], record['comments'])
            else:
                logging.warning('Cannot find grade for: ' +
                                reversed_student[canvas_id])
                upload_grade_with_comment(
                    submission, 0, ' cannot find submission.')
        except Exception as e:
            logging.error('Error with the following submission: ')
            logging.error(submission)
            logging.error('You might want to recreate the student metadata file.')

    logging.warning('Done.')
