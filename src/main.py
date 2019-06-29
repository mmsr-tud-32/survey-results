import argparse
from processor import process_csv, calculate_percentages, calculate_percentages_user, boxplot


def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('short_csv', help='File containing all data for the longer choices')
    parser.add_argument('long_csv', help='File containing all data for the shorter choices')

    return parser.parse_args()


def filter_fake(results, fake=True):
    fake_results = []
    for result in results:
        result2 = dict(result)

        result2['answers'] = [answer for answer in result['answers'] if answer['fake'] == fake]

        fake_results.append(result2)

    return fake_results


if __name__ == "__main__":
    args = vars(get_arguments())
    short_results = process_csv(args['short_csv'])
    long_results = process_csv(args['long_csv'])

    short_results_fake = filter_fake(short_results)
    long_results_fake = filter_fake(long_results)
    short_results_real = filter_fake(short_results, False)
    long_results_real = filter_fake(long_results, False)

    percentage_long = calculate_percentages(long_results, 'Long', False)
    percentage_long_fake = calculate_percentages(long_results_fake, 'Long', False)
    percentage_long_real = calculate_percentages(long_results_real, 'Long', False)

    percentage_short = calculate_percentages(short_results, 'Short', False)
    percentage_short_fake = calculate_percentages(short_results_fake, 'Short', False)
    percentage_short_real = calculate_percentages(short_results_real, 'Short', False)

    data_long = calculate_percentages_user(long_results, 'Long', False)
    data_long_fake = calculate_percentages_user(long_results_fake, 'Long', False)
    data_long_real = calculate_percentages_user(long_results_real, 'Long', False)

    data_short = calculate_percentages_user(short_results, 'short', False)
    data_short_fake = calculate_percentages_user(short_results_fake, 'Short', False)
    data_short_real = calculate_percentages_user(short_results_real, 'Short', False)

    boxplot(
        [
            {'dataset': data_short['responses'], 'label': '1 second', },
            {'dataset': data_long['responses'], 'label': '10 seconds', }
        ],
        'percentage',
        'Percentages guessed incorrectly',
        'percentage_boxplot.tex'
    )
    boxplot(
        [
            {'dataset': data_short_fake['responses'], 'label': '1 second', },
            {'dataset': data_long_fake['responses'], 'label': '10 seconds', }
        ],
        'percentage',
        'Percentages guessed incorrectly ',
        'percentage_boxplot_fake.tex'
    )
    boxplot(
        [
            {'dataset': data_short_real['responses'], 'label': '1 second', },
            {'dataset': data_long_real['responses'], 'label': '10 seconds', }
        ],
        'percentage',
        'Percentages guessed incorrectly ',
        'percentage_boxplot_real.tex'
    )
