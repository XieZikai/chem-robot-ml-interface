import sys
import os
import time
import sqlite3
import datetime
from ml_models import HSPModelLoader, ParticleModelLoader, SolubilityModelLoader

current_dir = os.path.dirname(os.path.abspath(__file__))


def load_model(model_type: str):
    """
    Please implement this function to load your model.
    The output of this function should be a model object that can be used to evaluate sample images.
    """
    assert model_type in ['solubility', 'hsp', 'particle'], "Invalid model type!"
    if model_type == 'solubility':
        return SolubilityModelLoader()
    if model_type == 'hsp':
        return HSPModelLoader()
    if model_type == 'particle':
        return ParticleModelLoader()


def run_experiment(sample_row: int, sample_col: str, shake: bool):
    """
    Please implement this function to run your experiment on a sample.
    The procedure should include running the robot to collect the sample and take a picture.
    The output of this function should be an image.
    """
    raise NotImplementedError


def predict_on_base64_image(model, img, concentration=None):
    """
    Please implement this function to use your model to predict on a base64 image.
    The output of this function should be a prediction value.
    """
    raise NotImplementedError


def run_database_monitor():
    conn = sqlite3.connect(os.path.join(os.path.dirname(current_dir), 'history.db'))
    cursor = conn.cursor()

    models = [load_model('hsp'), load_model('particle'), load_model('solubility')]

    while True:
        for table in ['Hansen', 'Particle', 'Solubility']:  # Recursively check all tables
            try:
                cursor.execute("SELECT * FROM {}".format(table))
                data = cursor.fetchall()
                for row in data:
                    if row[3] == 0:  # ongoing = 0 -> task not running
                        # ongoing = 1 -> task running
                        cursor.execute("UPDATE {} SET ongoing = 1 WHERE id = {}".format(table, row[0]))
                        conn.commit()
                        # select data from sample table
                        cursor.execute("SELECT * from '{}' WHERE father_id = {}".format(table + '-samples', row[0]))
                        sample_data = cursor.fetchall()

                        for sample in sample_data:

                            if table == 'Hansen':  # HSP
                                # sample[3] = sample_row, sample[4] = sample_col, sample[5] = shake
                                img = run_experiment(sample[3], sample[4], sample[5])
                                prediction = models[0].predict(img)

                            elif table == 'Particle':  # Particle size
                                # sample[3] = sample_row, sample[4] = sample_col, sample[5] = concentration,
                                # sample[6] = shake
                                img = run_experiment(sample[3], sample[4], sample[6])
                                prediction = models[1].predict(img, sample[5])

                            else:  # Solubility
                                # sample[3] = sample_row, sample[4] = sample_col, sample[5] = shake
                                img = run_experiment(sample[3], sample[4], sample[5])
                                prediction = models[2].predict(img)

                            current_time = str(datetime.datetime.now())
                            cursor.execute(
                                "INSERT INTO '{}' (father_id, image, time, prediction) VALUES (?, ?, ?, ?)".format(
                                    table + '-image'), (row[0], img, current_time, int(prediction)))
                            conn.commit()
                        # ongoing = 2 -> task finished
                        cursor.execute("UPDATE {} SET ongoing = 2 WHERE id = {}".format(table, row[0]))
                        conn.commit()
            except Exception as e:
                print("Error:", e)
            time.sleep(5)  # wait for 5 seconds before checking again
