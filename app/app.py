#!/usr/bin/env python3
# coding: utf-8

import flask
from flask import request, jsonify
from container import run as docker_run
from two1.wallet import Wallet
from two1.bitserv.flask import Payment
import yaml
import json
import os

app = flask.Flask(__name__)
payment = Payment(app, Wallet())

app.config['DEBUG'] = os.getenv('DEBUG', False)

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/docker/run/', methods=['GET', 'POST'])
@payment.required(5000)
def run():
    run_params = request.get_json(silent=False)

    if 'image' in run_params:
        # check for image format being name:tag or docker-py pull will download all tags !
        if str(run_params['image']).endswith(":"):
            raise InvalidUsage('You must specify an image name AND tag.', status_code=422)
        if ":" not in run_params['image']:
            raise InvalidUsage('You must specify an image name AND tag.', status_code=422)
        try:
            container = docker_run(run_params)
            return jsonify(container)
        except(Exception) as error:
            # print(str(error))
            raise InvalidUsage(str(error), status_code=500)
    else:
        raise InvalidUsage('You must specify at the very least an image name AND tag.', status_code=422)

@app.route('/manifest')
def manifest():
    """Provide the app manifest to the 21 crawler.
    """
    with open('./manifest.yaml', 'r') as f:
        manifest = yaml.load(f)
    return json.dumps(manifest)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)