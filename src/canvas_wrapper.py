from tqdm import tqdm
import logging
import csv
from canvasapi.user import User

def get_all_submissions(users, course, assignment):
    submissions = {}
    for user in tqdm(users):
        submissions[user.id] = assignment.get_submission(
            user.id, include=['submission_comments'])
    return submissions

def get_all_assignments(course):
    logging.warning('Fetching all assignments...')
    assignments = course.get_assignments()
    output_file = open('metadata/canvas.assignment.csv', 'w+')
    writer = csv.writer(output_file)
    writer.writerow(['info'])
    for assignment in tqdm(assignments):
        writer.writerow([str(assignment)])
    logging.warning('Done.')

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
        info = [profile['id'], profile['login_id'],
                profile['name'], profile['primary_email']]
        info_writer.writerow(info)


def upload_grade_with_comment(submission, grade, ta_comment):
    comment = submission.submission_comments
    submission.edit(comment={'text_comment': ta_comment},
                    submission={'posted_grade': grade})