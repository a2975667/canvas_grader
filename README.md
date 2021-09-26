# Canvas Grader
This script is a grade uploader for canvas. It supports uploading grades and comments.

## Getting started
You need to have a `settings.ini` file to get started. Start by copying the `settings_template.ini` file and rename the file as `settings.ini`. The api token is generated on canvas.

You should also install all required modules (and setup virtual enviornment) by using:
```bash
venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage
```bash
python grading.py <assignment_id> <filename>
```
You can find the assignment_id on canvas. This is currently the most tedious part of this script.

The filename is the gradebook for that specific assignment. It is important that you follow the required format as described in the import folder. Since this is a csv file, **YOU MUST NOT USE COMMA IN THE COMMENTS SECTION**.

```
netid,grade,comments
student01,99,nicely done
student02,99,good job
```
