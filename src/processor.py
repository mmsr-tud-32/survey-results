import csv


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
                    'fake': True if row[fake + answered_id] == 1 else False,
                    'guess': True if row[answer + answered_id] == 1 else False,
                    'guessed_correctly': row[fake + answered_id] == row[answer + answered_id]
                }
                row_answers.append(image_answer)

            row_result = {
                'name': row['name'],
                'uuid': row['uuid'],
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
        if response['uuid'] == uuid:c
            return response
    return None
