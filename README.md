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

## Functionalities

This script supports:

1. retrieve assignments on canvas for assignment id lookup
2. push student grades and comments to canvas

## Usage

```bash
$ python main.py --help
usage: main.py [-h] [--list | --grade assignment_id filepath]

Canvas grader

optional arguments:
  -h, --help            show this help message and exit
  --list, -l            list all assignments
  --grade assignment_id filepath, -g assignment_id filepath
                        grading mode
```

To use this script, you should run the following to retrieve all the assignment ids.

```bash
python main.py --list
```

Then use the following to upload the grades.

```bash
python main.py <assignment_id> <filename>
```

The filename is the gradebook for that specific assignment. It is important that you follow the required format as described in the import folder. Since this is a csv file, **YOU MUST NOT USE COMMA IN THE COMMENTS SECTION**.

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

## Contributions

Feel free to contribute to this repository. The core of this script was inspired by [quercus-bots](https://github.com/mehdiataei/quercus-bots) developed by Mehdi Ataei acknowledged in the MIT Licence.
