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
            input_grade[students[entry[0]]] = {
                "netid": entry[0],
                "grade": float(entry[1].strip()),
                "comments": entry[2].strip()
            }
        except:
            logging.critical('Something critical happened for ' +
                entry[0] + ': the entry is: ' + str(entry))

    # writing to canvas
    logging.warning('Pushing updates to canvas...')
    for _, submission in tqdm(submissions.items()):
        canvas_id = str(submission.user_id)
        if canvas_id in input_grade:
            record = input_grade[canvas_id]
            upload_grade_with_comment(
                submission, record['grade'], record['comments'])
        else:
            logging.warning('Cannot find grade for: ' +
                            reversed_student[canvas_id])
            upload_grade_with_comment(
                submission, 0, ' cannot find submission.')

    logging.warning('Done.')
