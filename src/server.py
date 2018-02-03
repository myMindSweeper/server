from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

from os import environ
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(environ.get('SERVER_PORT')))
