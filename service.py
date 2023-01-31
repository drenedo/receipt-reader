from flask import Flask, request
from werkzeug import exceptions
from werkzeug.utils import secure_filename
import click
import os
import tempfile
from flask import jsonify
from ocr import scan

app = Flask(__name__)


@app.route("/ocr", methods=['POST'])
def post_image_to_ocr():
    if request.method == 'POST':
        file = get_file()
        filename = secure_filename(file.filename)
        path = os.path.join(tempfile.gettempdir(), filename)
        file.save(path)
        result = jsonify(scan(path).to_json())
        os.remove(path)
        return result


def get_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        click.echo(f"File is not in request.files: ${request.files}")
        raise exceptions.NotAcceptable
    file = request.files['file']
    # check if filename is empty
    if file.filename == '':
        raise exceptions.NotAcceptable
    return file
