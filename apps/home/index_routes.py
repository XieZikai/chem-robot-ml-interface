from apps.home import blueprint
from flask import jsonify, request
from flask_login import login_required
import sqlite3
import datetime
from sqlalchemy import func

from apps.home.models import *


@blueprint.route('/index_get_task_num')
@login_required
def index_get_task_num():
    ongoing = 0
    finished = 0
    awaiting = 0

    for database in [Hansen, Particle, Solubility]:
        ongoing += len(database.query.filter_by(ongoing=1).all())
        finished += len(database.query.filter_by(ongoing=2).all())
        awaiting += len(database.query.filter_by(ongoing=0).all())

    return jsonify({
        'ongoing': ongoing,
        'finished': finished,
        'awaiting': awaiting
    })


@blueprint.route('/index_get_task_info')
@login_required
def index_get_task_info():
    def to_dict(self):
        return {
            'id': self.id,
            'time': self.time,
            'ongoing': self.ongoing,
            'sample_number': self.sample_number,
            'comments': self.comments
        }
    data = AllTasks.query.all()
    data = [to_dict(task) for task in data]

    print(jsonify(data))

    return jsonify(data)
