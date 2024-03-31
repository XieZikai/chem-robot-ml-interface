from apps.home import blueprint
from flask import jsonify
from flask_login import login_required

from apps.home.models import *
from apps.utils import image_serializer, history_serializer, sample_serializer


@blueprint.route('/image/<int:image_id>')
@login_required
def get_image(image_id):  # for test
    image = HansenImage.query.get(image_id)
    if image:
        # base64_image = base64.b64decode(image.image.encode('utf-8'))
        return jsonify({'image': image.image})
    return jsonify({'error': 'Image not found'}), 404


@blueprint.route('/hansen_history')
@login_required
def get_hansen_history():
    data = Hansen.query.all()
    data = [history_serializer(history_data) for history_data in data]
    return jsonify(data)


@blueprint.route('/hansen_image_id')
@login_required
def get_hansen_image_id():
    father_ids = HansenImage.query.with_entities(HansenImage.father_id).distinct().all()
    father_ids = [father_id[0] for father_id in father_ids]
    return jsonify(father_ids)


@blueprint.route('/hansen_images/<int:father_id>')
@login_required
def get_hansen_images(father_id):
    images = HansenImage.query.filter_by(father_id=father_id).all()
    images_data = [{'id': image.id, 'image': image.image} for image in images]
    return jsonify(images_data)


@blueprint.route('/particle_history')
@login_required
def get_particle_history():
    data = Particle.query.all()
    data = [history_serializer(history_data) for history_data in data]
    return jsonify(data)


@blueprint.route('/particle_image_id')
@login_required
def get_particle_image_id():
    father_ids = ParticleImage.query.with_entities(ParticleImage.father_id).distinct().all()
    father_ids = [father_id[0] for father_id in father_ids]
    return jsonify(father_ids)


@blueprint.route('/particle_images/<int:father_id>')
@login_required
def get_particle_images(father_id):
    images = ParticleImage.query.filter_by(father_id=father_id).all()
    images_data = [{'id': image.id, 'image': image.image} for image in images]
    return jsonify(images_data)


@blueprint.route('/solubility_history')
@login_required
def get_solubility_history():
    data = Solubility.query.all()
    data = [history_serializer(history_data) for history_data in data]
    return jsonify(data)


@blueprint.route('/solubility_image_id')
@login_required
def get_solubility_image_id():
    father_ids = SolubilityImage.query.with_entities(SolubilityImage.father_id).distinct().all()
    father_ids = [father_id[0] for father_id in father_ids]
    return jsonify(father_ids)


@blueprint.route('/solubility_images/<int:father_id>')
@login_required
def get_solubility_images(father_id):
    images = SolubilityImage.query.filter_by(father_id=father_id).all()
    images_data = [{'id': image.id, 'image': image.image} for image in images]
    return jsonify(images_data)
