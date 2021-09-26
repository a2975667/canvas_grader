# The MIT License (MIT)
# Copyright (c) 2020 Mehdi Ataei

import logging
from canvasapi import Canvas
from canvasapi.user import User
from pprint import pprint
from parser import parse_input, parse_config, setup_logger
import csv
from os.path import exists
from tqdm import tqdm

def get_all_submissions(users, course, assignment):
    submissions = {}
    for user in tqdm(users):
        submissions[user.id] = assignment.get_submission(
            user.id, include=['submission_comments'])
    return submissions

def get_student_mapping(filename='metadata/canvas.student.csv'):
    file_name = open(filename)
    students = csv.reader(file_name)
    student_dict = {}
    reversed_student_dict = {}
    for row in students:
        student_dict[row[1]] = row[0]
        reversed_student_dict[row[0]] = row[1]
    return student_dict, reversed_student_dict

def fetch_student_id_mapping(users):
    info_writer = csv.writer(open('metadata/canvas.student.csv', 'w+'))
    info_writer.writerow(['canvas_id', 'netid', 'name', 'email'])
    for user in users:
        profile = User.get_profile(user)
        info = [profile['id'], profile['login_id'], profile['name'], profile['primary_email']]
        info_writer.writerow(info)

def upload_grade_with_comment(submission, grade, ta_comment):
    comment = submission.submission_comments
    submission.edit(comment={'text_comment': ta_comment },
                    submission={'posted_grade': grade})

## Main Script
# Initialization
parsed_data = parse_input()
parsed_config = parse_config()
assignment_id = parsed_data.assignment_id
gradebook = parsed_data.filename
API_URL = parsed_config['base_url']
API_KEY = parsed_config['API_token']
setup_logger(assignment_id)
logging.warning('Canvas Grader Initializing...')

canvas = Canvas(API_URL, API_KEY)

course = canvas.get_course(parsed_config['course_id'])
users = course.get_users(enrollment_type=['student'])
assignment = course.get_assignment(assignment_id)
logging.warning('Retrieving all submissions...')
submissions = get_all_submissions(users, course, assignment)

logging.warning('Checking student metadata...')
if not exists('metadata/canvas.student.csv'): 
    logging.warning('No metadata found, creating one...')
    fetch_student_id_mapping(users)
students, reversed_student = get_student_mapping(filename='metadata/canvas.student.csv')

# read in grading data
logging.warning('Reading grade information...')
input_grade = {}
gb = csv.reader(open(gradebook))
next(gb, None)
for entry in gb:
    if entry[0] not in students:
        logging.warning(entry[0] + ' is not on canvas.')
        continue
    input_grade[students[entry[0]]] = {
        "netid": entry[0],
        "grade": float(entry[1].strip()),
        "comments": entry[2].strip()
    }

# writing to canvas
logging.warning('Pushing updates to canvas...')
for _, submission in tqdm(submissions.items()):
    canvas_id = str(submission.user_id)
    if canvas_id in input_grade:
        record = input_grade[canvas_id]
        upload_grade_with_comment(submission, record['grade'], record['comments'])
    else:
        logging.warning('Cannot find grade for: ' + reversed_student[canvas_id])
        upload_grade_with_comment(submission, 0, ' cannot find submission.')

logging.warning('Done.')