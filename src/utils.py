import argparse
import configparser
import logging
import tqdm
import time
class TqdmLoggingHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super().__init__(level)

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.tqdm.write(msg)
            time.sleep(0.05)
            self.flush()
        except Exception:
            self.handleError(record)  

def parse_input():
    parser = argparse.ArgumentParser(
        prog ='Canvas grader',
        description='A script for batch grade and comment upload to Canvas LMS.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--list", "-l", help='list all assignments', action="store_true")
    group.add_argument("--grade", "-g", nargs=2,
                       metavar=('assignment_id', 'filepath'), help='grading mode')
    group.add_argument("--batch_upload", "-u", help='upload batch file', nargs=1)
    group.add_argument("--create_batch", "-b", help='create batch file', action="store_const", const=True)
    
    # parser.add_argument("assignment_id", help='assignment ID')
    # parser.add_argument('filename', help='grade filename')
    return parser.parse_args()


def parse_config():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    return config['Settings']


def setup_logger(assignment_id):
    logging.getLogger(__name__)
    logging.basicConfig(filename='logs/' + str(assignment_id) + '.log',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.WARNING)
    # adding tqdm logger to preserve pg bar at the bottom
    logging.getLogger('').addHandler(TqdmLoggingHandler())
