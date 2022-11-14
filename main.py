#!/usr/bin/env python3
import logging
from datetime import datetime

from canvasapi import Canvas

from src.canvas_wrapper import get_all_assignments
from src.grading import grade_upload, grader_initialization
from src.utils import parse_config, parse_input, setup_logger
from src.batch_uploader import batch_create

if __name__ == '__main__':
    # define mode
    parsed_data = parse_input()
    if parsed_data.list:
        log_name = datetime.now()
    elif parsed_data.grade:
        parsed_data.assignment_id = parsed_data.grade[0]
        parsed_data.filepath = parsed_data.grade[1]
        log_name = parsed_data.assignment_id
    elif parsed_data.create_batch:
        batch_create()
    elif parsed_data.batch_upload:
        batch_filename = parsed_data.batch_upload[0]
        print(batch_filename)
        log_name = batch_filename.split('/')[-1] + " processed at " + str(datetime.now())
        print(log_name)
    else:
        print('No mode selected. Use -h for help.\nExiting...')
        exit(1)
    setup_logger(log_name)

    # initialization
    logging.warning('Canvas Grader Initializing...')
    parsed_config = parse_config()
    API_URL = parsed_config['base_url']
    API_KEY = parsed_config['API_token']
    canvas = Canvas(API_URL, API_KEY)

    # heavy duty
    logging.warning('Fetching course information...')
    course = canvas.get_course(parsed_config['course_id'])

    if parsed_data.list:
        get_all_assignments(course)
    elif parsed_data.grade:
        assignment_id = parsed_data.assignment_id
        filepath = parsed_data.filepath
        submissions = grader_initialization(course, assignment_id)
        grade_upload(submissions, filepath)
    elif parsed_data.batch_upload:
        logging.warning('Reading from batch file...')
        # read form file
        raw_pairs = open(batch_filename, 'r').readlines()
        print("\nYou are uploading the following grades\n")
        for pair in raw_pairs:
            p = pair.split(',')
            print(p[0]," from ",p[1].strip())
        confirm = input("\nAre you sure? (y/n): ")

        if confirm.lower() == 'y' or confirm.lower() == 'yes':
            for pair in raw_pairs:
                assignment_id, filepath = pair.split(',')
                filepath = filepath.strip()
                submissions = grader_initialization(course, assignment_id)
                grade_upload(submissions, filepath)
        else:
            print("Exiting...")
            exit(1)
