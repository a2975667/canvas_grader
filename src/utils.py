import argparse
import configparser
import logging


def parse_input():
    parser = argparse.ArgumentParser(description='Canvas grader')
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--list", "-l", help='list all assignments', action="store_true")
    group.add_argument("--grade", "-g", nargs=2,
                       metavar=('assignment_id', 'filepath'), help='grading mode')
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
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
