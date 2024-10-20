from apps.home import blueprint
from apps.home.utils import monitor_directory, task_status
from flask import jsonify, request, render_template
from flask_login import login_required
import sqlite3
import datetime
from sqlalchemy import func
import threading

from apps.home.models import *
from apps.utils import rack_serializer, history_serializer
import pandas as pd

RACK_NUM = 6


@blueprint.route('/image/<int:image_id>')
@login_required
def get_image(image_id):  # for test
    image = HansenImage.query.get(image_id)
    if image:
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
    images_data = [{'id': image.id, 'image': image.image, 'prediction': image.prediction} for image in images]
    return jsonify(images_data)


@blueprint.route('/submit_hansen_task', methods=['POST'])
@login_required
def submit_hansen():
    data = request.json
    conn = sqlite3.connect('./apps/history.db')
    cursor = conn.cursor()
    time = str(datetime.datetime.now())
    cursor.execute("INSERT INTO Hansen (time, sample_number, ongoing) VALUES (?, ?, ?)",
                   (time, data['sampleNum'], 0))
    cursor.execute("INSERT INTO AllTasks (time, sample_number, ongoing) VALUES (?, ?, ?)",
                   (time, data['sampleNum'], 0))
    conn.commit()
    cursor.close()
    conn.close()

    id = Hansen.query.with_entities(func.max(Hansen.id)).scalar()

    conn = sqlite3.connect('./apps/history.db')
    cursor = conn.cursor()

    for rack in range(RACK_NUM):
        click_count = data['globalClickCount'][rack]
        for i in range(click_count):
            cursor.execute("INSERT INTO 'Hansen-samples' (father_id, sample_name, sample_row, sample_col, shake, rack, solvent_name) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (id, data['sampleName'][rack][i], data['selectedRows'][rack][i], data['selectedCols'][rack][i], data['shakeList'][rack][i], rack, data['selectedOptions'][rack][i]))
            cursor.execute("UPDATE 'Rack-availability' SET available = 1 WHERE row = ? AND col = ? AND rack = ?",
                           (data['selectedRows'][rack][i], data['selectedCols'][rack][i], rack))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Complete!'})


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
    images_data = [{'id': image.id, 'image': image.image, 'prediction': image.prediction} for image in images]
    return jsonify(images_data)


@blueprint.route('/submit_particle_task', methods=['POST'])
@login_required
def submit_particle():

    data = request.json
    conn = sqlite3.connect('./apps/history.db')
    cursor = conn.cursor()
    time = str(datetime.datetime.now())
    cursor.execute("INSERT INTO Particle (time, sample_number, ongoing) VALUES (?, ?, ?)",
                   (time, data['sampleNum'], 0))
    cursor.execute("INSERT INTO AllTasks (time, sample_number, ongoing) VALUES (?, ?, ?)",
                   (time, data['sampleNum'], 0))
    conn.commit()
    cursor.close()
    conn.close()

    id = Particle.query.with_entities(func.max(Particle.id)).scalar()

    conn = sqlite3.connect('./apps/history.db')
    cursor = conn.cursor()

    for rack in range(RACK_NUM):
        click_count = data['globalClickCount'][rack]
        for i in range(click_count):
            cursor.execute(
                "INSERT INTO 'Particle-samples' (father_id, sample_name, sample_row, sample_col, concentration, shake, rack) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (id, data['sampleName'][rack][i], data['selectedRows'][rack][i], data['selectedCols'][rack][i],
                 data['concentration'][rack][i], data['shakeList'][rack][i], rack))
            cursor.execute("UPDATE 'Rack-availability' SET available = 1 WHERE row = ? AND col = ? AND rack = ?",
                           (data['selectedRows'][rack][i], data['selectedCols'][rack][i], rack))

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Complete!'})


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
    images_data = [{'id': image.id, 'image': image.image, 'prediction': image.prediction} for image in images]
    return jsonify(images_data)


@blueprint.route('/submit_solubility_task', methods=['POST'])
@login_required
def submit_solubility():
    data = request.json
    conn = sqlite3.connect('./apps/history.db')
    cursor = conn.cursor()
    time = str(datetime.datetime.now())
    cursor.execute("INSERT INTO Solubility (time, sample_number, ongoing, model_class) VALUES (?, ?, ?, ?)",
                   (time, data['sampleNum'], 0, data['numClass']))
    cursor.execute("INSERT INTO AllTasks (time, sample_number, ongoing) VALUES (?, ?, ?)",
                   (time, data['sampleNum'], 0))
    conn.commit()
    cursor.close()
    conn.close()

    id = Solubility.query.with_entities(func.max(Solubility.id)).scalar()

    conn = sqlite3.connect('./apps/history.db')
    cursor = conn.cursor()

    for rack in range(RACK_NUM):
        click_count = data['globalClickCount'][rack]
        for i in range(click_count):
            cursor.execute(
                "INSERT INTO 'Solubility-samples' (father_id, sample_name, sample_row, sample_col, shake, rack) VALUES (?, ?, ?, ?, ?, ?)",
                (id, data['sampleName'][rack][i], data['selectedRows'][rack][i], data['selectedCols'][rack][i],
                 data['shakeList'][rack][i], rack))
            cursor.execute("UPDATE 'Rack-availability' SET available = 1 WHERE row = ? AND col = ? AND rack = ?",
                           (data['selectedRows'][rack][i], data['selectedCols'][rack][i], rack))

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Complete!'})


@blueprint.route('/rack_avail/<int:rack_id>')
@login_required
def rack_avail(rack_id):
    data = RackAvailability.query.filter_by(available=1, rack=rack_id).all()
    data = [rack_serializer(rack_data) for rack_data in data]
    return jsonify(data)


@blueprint.route('/get_solvent_info')
@login_required
def get_solvent_info():
    df = pd.read_csv('./apps/yesblend_nowater_solventlist_HSP.csv')
    solvent_list = df['name'].to_list()
    return jsonify(solvent_list)


@blueprint.route('/optimize/<int:task_id>')
@login_required
def optimize(task_id):
    return render_template('home/optimize.html', task_id=task_id)


@blueprint.route('/task_status')
def get_task_status():
    return jsonify(task_status)


@blueprint.route('/start_optimize')
def start_task():
    thread = threading.Thread(target=monitor_directory)
    thread.start()
    return jsonify({'message': 'Task started!'})
