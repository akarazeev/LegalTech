from flask import Flask, request
import pandas as pd
import requests
import difflib
import logging
import typing
import json

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/project_id/<project_id>', methods=['get'])
def translate_phrase(project_id):
    return project_id + 'test'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
