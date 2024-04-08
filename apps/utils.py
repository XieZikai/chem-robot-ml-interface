def image_serializer(image):
    return {
        'image_id': image.id,
        'father_id': image.father_id,
        'image': image.image,
        'image_time': image.time
    }


def history_serializer(data):
    return {
        'id': data.id,
        'time': data.time,
        'sample_number': data.sample_number,
        'ongoing': data.ongoing,
        'comments': data.comments
    }


def sample_serializer(sample):
    return {
        'sample_id': sample.id,
        'father_id': sample.father_id,
        'sample_name': sample.sample_name,
        'sample_pos': sample.sample_pos
    }


def rack_serializer(sample):
    return {
        'row': sample.row,
        'col': sample.col
    }
