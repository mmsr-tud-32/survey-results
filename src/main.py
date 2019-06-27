import argparse
from processor import process_csv, get_by_uuid


def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('short_csv', help='File containing all data for the longer choices')
    parser.add_argument('long_csv', help='File containing all data for the shorter choices')

    return parser.parse_args()


if __name__ == "__main__":
    args = vars(get_arguments())
    short_results = process_csv(args['short_csv'])
    long_results = process_csv(args['long_csv'])
    print(get_by_uuid('4265c253-a824-445d-a516-d0fd22e2090c', long_results))