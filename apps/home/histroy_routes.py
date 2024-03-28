from apps.home import blueprint
from flask import jsonify
from flask_login import login_required

from apps.home.models import HansenImage, ParticleImage, SolubilityImage


@blueprint.route('/image/<int:image_id>')
@login_required
def get_image(image_id):
    image = HansenImage.query.get(image_id)
    if image:
        # base64_image = base64.b64decode(image.image.encode('utf-8'))
        return jsonify({'image': image.image})
    return jsonify({'error': 'Image not found'}), 404


@blueprint.route('/hansen_image_id')
@login_required
def get_hansen_image_id():
    hansen_ids = HansenImage.query.with_entities(HansenImage.hansen_id).distinct().all()
    hansen_ids = [hansen_id[0] for hansen_id in hansen_ids]
    return jsonify(hansen_ids)


@blueprint.route('/hansen_images/<int:hansen_id>')
@login_required
def get_hansen_images(hansen_id):
    images = HansenImage.query.filter_by(hansen_id=hansen_id).all()
    images_data = [{'id': image.id, 'image': image.image} for image in images]
    return jsonify(images_data)


@blueprint.route('/particle_image_id')
@login_required
def get_particle_image_id():
    particle_ids = ParticleImage.query.with_entities(ParticleImage.particle_id).distinct().all()
    particle_ids = [particle_id[0] for particle_id in particle_ids]
    return jsonify(particle_ids)


@blueprint.route('/particle_images/<int:particle_id>')
@login_required
def get_hansen_images(particle_id):
    images = ParticleImage.query.filter_by(particle_id=particle_id).all()
    images_data = [{'id': image.id, 'image': image.image} for image in images]
    return jsonify(images_data)


@blueprint.route('/solubility_image_id')
@login_required
def get_solubility_image_id():
    solubility_ids = SolubilityImage.query.with_entities(SolubilityImage.solubility_id).distinct().all()
    solubility_ids = [solubility_id[0] for solubility_id in solubility_ids]
    return jsonify(solubility_ids)


@blueprint.route('/solubility_images/<int:solubility_id>')
@login_required
def get_hansen_images(solubility_id):
    images = SolubilityImage.query.filter_by(solubility_id=solubility_id).all()
    images_data = [{'id': image.id, 'image': image.image} for image in images]
    return jsonify(images_data)
