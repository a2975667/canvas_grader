import logging
from datetime import datetime

from canvasapi import Canvas

from src.canvas_wrapper import get_all_assignments
from src.grading import grade_upload, grader_initialization
from src.utils import parse_config, parse_input, setup_logger

if __name__ == '__main__':
    # define mode
    parsed_data = parse_input()
    if parsed_data.list:
        log_name = datetime.now()
    elif parsed_data.grade:
        parsed_data.assignment_id = parsed_data.grade[0]
        parsed_data.filepath = parsed_data.grade[1]
        log_name = parsed_data.assignment_id
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
