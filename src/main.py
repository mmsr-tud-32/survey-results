import argparse
from processor import process_csv, calculate_percentages, calculate_percentages_user, boxplot


def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('short_csv', help='File containing all data for the longer choices')
    parser.add_argument('long_csv', help='File containing all data for the shorter choices')

    return parser.parse_args()


if __name__ == "__main__":
    args = vars(get_arguments())
    short_results = process_csv(args['short_csv'])
    long_results = process_csv(args['long_csv'])
    percentage_long = calculate_percentages(long_results, 'Long', False)
    percentage_short = calculate_percentages(short_results, 'Short', False)
    data_long = calculate_percentages_user(long_results, 'Long', False)
    data_short = calculate_percentages_user(short_results, 'short', False)
    boxplot(
        [
            {
                'dataset': data_short['responses'],
                'label': '1 second',
            },
            {
                'dataset': data_long['responses'],
                'label': '10 seconds',
            }
        ],
        'percentage',
        'Percentages guessed incorrectly',
        'percentage_boxplot.tex'
    )
