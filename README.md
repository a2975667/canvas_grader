# Canvas Grader

This script is a grade uploader for canvas. It supports uploading grades and comments.

## Getting started

You need to have a `settings.ini` file to get started. Start by copying the `settings_template.ini` file and rename the file as `settings.ini`. The API token is generated on canvas.

You should also install all required modules (and set up the virtual environment) by using:

```bash
venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Functionalities

This script supports:

1. retrieve assignments on canvas for assignment id lookup
2. push student grades and comments to canvas
3. (beta) batch push grades and comments to canvas

## Usage

```bash
$ python main.py --help
usage: Canvas grader [-h] [--list | --grade assignment_id filepath | --batch_upload BATCH_UPLOAD | --create_batch]

A script for batch grade and comment upload to Canvas LMS.

optional arguments:
  -h, --help            show this help message and exit
  --list, -l            list all assignments
  --grade assignment_id filepath, -g assignment_id filepath
                        grading mode
  --batch_upload BATCH_UPLOAD, -u BATCH_UPLOAD
                        upload batch file
  --create_batch, -b    create batch file
```

To use this script, you should run the following to retrieve all the assignment ids.

```bash
python main.py --list
```

Then use the following to upload the grades.

```bash
python main.py <assignment_id> <filename>
```

The filename is the gradebook for that specific assignment. You must follow the required format as described in the import folder. Since this is a csv file, **YOU MUST NOT USE COMMA IN THE COMMENTS SECTION**.

```
netid,grade,comments
student01,99,nicely done
student02,99,good job
```

Successfully running the script would show the following (you can adjust the logging level in the utils file):

```bash
$ python main.py -g 28***1 import/filename.csv
 476it [01:25,  5.57it/s]
 12%|███████████▍                                                   | 57/476 [00:21<02:13,  3.14it/s]
```

## (Beta) Batch upload grades
This is a beta feature and part of this feature will be ported to single assignment upload. The batch upload feature allows you to upload multiple assignment grades to assignment canvas assignments at once. To batch upload grades, you need to create a batch file. The batch file is a csv file that contains the assignment id and the gradebook file path. Use the following command to create a batch file.

```bash
python main.py --create_batch
Entering interactive tool to create batch grading.
When prompted, tab to search for the input. Hints are provided at program runtime.
Enter:
 >>'a' to add a new pair to the batch
 >>'c' to create a batch file
 >>'l' to list current construction
 >>'q' to quit or end batch creation
```

The tool will walk you through matching assignment IDs and the csv files. When you add an entry (by keying in `a`), the system will first ask you the assignment you want to upload grades for. You can search for the assignment by typing the assignment name you can use tabs to autocomplete it. Same with the grade book.

All batch files will be stored in the batch folder. Once a batch file is generated, you can then use the following command to upload the grades.

```bash
python main.py -u batch/<batch_file_name.csv>
```
Upon confirmation, the script will upload all the grades instructed in the batch file.

```

## Contributions

Feel free to contribute to this repository. The core of this script was inspired by [quercus-bots](https://github.com/mehdiataei/quercus-bots) developed by Mehdi Ataei acknowledged in the MIT Licence.
