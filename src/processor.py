import csv
import numpy as np
import warnings
import matplotlib.pyplot as plt
from matplotlib2tikz import save as tikz_save


def process_csv(csv_path, image='image_id_', stage='image_stage_', fake='image_fake_', answer='image_answer_'):
    """
    Process a csv file to a list of Result objects
    :param csv_path:
    :param image:
    :param stage:
    :param fake:
    :param answer:
    :return:
    """
    results = []
    with open(csv_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            image_ids = {key for key in row.keys() if key.startswith(image)}
            answered_images = {key: value for key, value in row.items() if key in image_ids and value != ''}
            answered_ids = {key.replace(image, '') for key in answered_images.keys()}

            row_answers = []
            for answered_id in answered_ids:
                image_answer = {
                    'image': row[image + answered_id],
                    'stage': row[stage + answered_id],
                    'fake': True if row[fake + answered_id] == '1' else False,
                    'guess': True if row[answer + answered_id] == '1' else False,
                    'guessed_correctly': row[fake + answered_id] == row[answer + answered_id]
                }
                row_answers.append(image_answer)

            row_result = {
                'uuid': row['uuid'],
                'name': row['name'],
                'age': row['age'],
                'feedback': row['feedback'],
                'answers': row_answers,
            }
            results.append(row_result)

    return results


def get_by_uuid(uuid, dictionary):
    """
    Get a specific UUID from a dictionary
    :param uuid:
    :param dictionary:
    :return:
    """
    for response in dictionary:
        if response['uuid'] == uuid:
            return response
    return None


def count_by_guess(dictionary, correctly=False):
    """
    Count the number of correctly/incorrectly guessed images for a dataset

    :param dictionary:
    :param correctly:
    :return:
    """
    guessed = 0
    for response in dictionary:
        guessed = guessed + count_by_guess_user(response, correctly)

    return guessed


def count_by_guess_user(response, correctly=False):
    guessed = 0
    for answer in response['answers']:
        if answer['guessed_correctly'] == correctly:
            guessed = guessed + 1

    return guessed


def calculate_percentages(dictionary, name="Datapoint", should_print=True):
    """
    Calculate the percentages for a dictionary, and print the output if requested
    :param dictionary:
    :param name:
    :param should_print:
    :return:
    """
    incorrect = count_by_guess(dictionary, correctly=False)
    correct = count_by_guess(dictionary, correctly=True)
    percentage = np.around((incorrect / (correct + incorrect)) * 100, 2)
    if should_print:
        print('Results for {}'.format(name))
        print('Incorrectly guessed: {}'.format(incorrect))
        print('Correctly guessed: {}'.format(correct))
        print('Percentage incorrect: {}\n'.format(percentage))

    return {'percentage_incorrect': percentage, 'incorrect': incorrect, 'correct': correct}


def calculate_percentages_user(dictionary, name="Datapoint", should_print=True):
    """
    Create a dictionary with the percentages for every user.

    :param dictionary:
    :param name:
    :param should_print:
    :return:
    """
    lowest_percentage = 100
    highest_percentage = 0
    responses = []
    for response in dictionary:
        incorrect = count_by_guess_user(response, correctly=False)
        correct = count_by_guess_user(response, correctly=True)
        if correct + incorrect == 0:
            percentage = lowest_percentage
        else:
            percentage = np.around((incorrect / (correct + incorrect)) * 100, 2)

        if percentage < lowest_percentage:
            lowest_percentage = percentage

        if percentage > highest_percentage:
            highest_percentage = percentage

        if should_print:
            print('Results for {} for {}'.format(name, response['uuid']))
            print('Incorrectly guessed: {}'.format(incorrect))
            print('Correctly guessed: {}'.format(correct))
            print('Percentage incorrect: {}\n'.format(percentage))

        responses.append({
            'uuid': response['uuid'],
            'age': response['age'],
            'incorrect': incorrect,
            'correct': correct,
            'percentage': percentage,
        })

    if should_print:
        print('Highest percentage: {}'.format(highest_percentage))
        print('Lowest percentage: {}'.format(lowest_percentage))

    return {
        'highest_percentage': highest_percentage,
        'lowest_percentage': lowest_percentage,
        'responses': responses
    }


def boxplot(data_dict, metric, header, filename):
    """
    Generate a boxplot for the given data.

    :param data_dict:
    :param metric:
    :param header:
    :param filename:
    :return:
    """
    data = []
    for data_point in [data_points['dataset'] for data_points in data_dict]:
        data.append([guess_data[metric] for guess_data in data_point])

    fig, ax = plt.subplots()
    ax.boxplot(data, widths=0.75)
    ax.set_title(header)
    ax.set_ylabel(metric.capitalize())
    ax.set_xticklabels([data_points['label'] for data_points in data_dict])

    if filename.endswith('.tex'):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            tikz_save('../output/{}'.format(filename))
    else:
        plt.savefig('../output/{}'.format(filename))



