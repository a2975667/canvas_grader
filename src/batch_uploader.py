import readline
import os

ASSIGNMENT_ID = {}
FILE_PATHS = {}

def ask_batch_pairs():

    assignment_id = None
    grade_file = None

    # Ask for assignment ID
    flag = True
    while flag:
        readline.set_completer_delims('')
        readline.parse_and_bind("tab: complete")
        readline.set_completer(assignment_complete)

        line = input('Assignment Name>> ')
        try:
            assignment_id = ASSIGNMENT_ID[line]
            print("You are matching assignment ", line, " with an ID of ", ASSIGNMENT_ID[line], " to an existing file")
        except KeyError:
            if type(line) == int:
                print("You are matching assignment ID ", line, " to an existing file")
                assignment_id = line
            else:
                print("No assingment Name found. You can rerun the list function or key in the assignment ID directly.")
                line = input('Assignment ID>> ')
                assignment_id = line
        
        confirm = input("Is this correct? (y/n)")
        if confirm == 'y':
            flag = False
            assignment_id = assignment_id
        else:
            assignment_id = None
    
    # Ask for file path
    flag = True
    while flag:
        readline.set_completer_delims('')
        readline.parse_and_bind("tab: complete")
        readline.set_completer(file_autocomplete)

        line = input('Gradeing File>> ')
        try:
            grade_file = FILE_PATHS[line]
            print("You will import csv file from path: ", grade_file, "for this assignment")
        except KeyError:
            if type(line) == str:
                print("You will import csv file from path: ", line, "for this assignment")
                grade_file = line
            else:
                print("No assingment path found. You can rerun the program or paste in the path to the csv.")
                line = input('Gradeing File>> ')
                grade_file = line
    
        confirm = input("Is this correct? (y/n)")
        if confirm == 'y':
            flag = False
            grade_file = grade_file
        else:
            grade_file = None
    
    # add to batch
    return (assignment_id, grade_file)

def assignment_complete(text,state):
    data = open("metadata/canvas.assignment.csv").readlines()[1:]
    for entry in data:
        raw_assignment = entry.split("(")
        ASSIGNMENT_ID['('.join(raw_assignment[:-1]).strip()] = raw_assignment[-1].split(")")[0].strip()
    
    assignment_names = list(ASSIGNMENT_ID.keys())
    results = [x for x in assignment_names if x.lower().startswith(text.lower()) ] + [None]
    
    return results[state]

def file_autocomplete(text, state,):
    imported_files = os.listdir("import")
    script_files = os.listdir("scripts")

    for file in imported_files:
        FILE_PATHS[file] = "import/" + file
    
    for file in script_files:
        FILE_PATHS[file] = "scripts/" + file

    file_names = list(FILE_PATHS.keys())
    results = [x for x in file_names if (text.lower()) in x.lower()] + [None]

    return results[state]

    

def batch_create():
    print("Entering interactive tool to create batch grading.")
    print("When prompted, tab to search for the input. Hints are provided at program runtime.")
   

    batch = {}
    done = False
    while not done:
        status = input("Enter:\n >>'a' to add a new pair to the batch\n >>'c' to create a batch file\n >>'l' to list current construction\n >>'q' to quit or end batch creation\n")
        if (status == 'q'):
            done = True
            if len(batch) == 0:
                print("No batch file created.")
                print("Exiting batch creation tool.")
            else:
                # open a new csv file with current timestamp
                import datetime
                now = datetime.datetime.now()
                batch_file = open("batch/" + now.strftime("%Y-%m-%d-%H-%M-%S") + ".csv", "w")
                
                for pairs in batch:
                    batch_file.write(pairs + ',' + batch[pairs] + "\n")
                print("Batch file created.")
                print("Exiting batch creation tool.")
            exit(1)
        elif (status == 'l'):
            print("Listing current construction...")
            for pairs in batch:
                print(pairs, batch[pairs])
        elif (status == 'a'):
            a, f = ask_batch_pairs()
            print("Adding entry: ", a, f)
            batch[a] = f
        else:
            print("Invalid input. Please try again.")