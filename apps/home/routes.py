# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, Response, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound

from apps.home.models import HansenImage
import base64


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


@blueprint.route('/images/<int:hansen_id>')
@login_required
def get_hansen_images(hansen_id):
    images = HansenImage.query.filter_by(hansen_id=hansen_id).all()
    images_data = [{'id': image.id, 'image': image.image} for image in images]
    return jsonify(images_data)


@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]
        # print(segment)
        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
