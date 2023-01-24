import logging
import os
from datetime import datetime, timezone, timedelta
from flask import Flask, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, set_access_cookies, get_jwt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # Inicializacia Flask aplikacie
if app.config["ENV"] == "production":
    app.config.from_object("timebank.utils.config.ProductionConfig")
elif app.config["ENV"] == "testing":
    app.config.from_object("timebank.utils.config.TestingConfig")
else:
    app.config.from_object("timebank.utils.config.DevelopmentConfig")

# Nacitanie a nastavenie db, cors a jwt pre aplikaciu
db = SQLAlchemy(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
jwt = JWTManager(app)


# Nastavenie loggingu
@app.before_first_request
def before_first_request():
    log_level = logging.DEBUG  # Nastavenie Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    # Vymazanie preddefinovanych handlerov
    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)

    # Nastavenie ukladacieho priecinka (/logs/year/month/day)
    logdir = os.path.join('logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    os.chdir(logdir)
    year_dir = os.path.join(datetime.now().strftime('%Y'))
    if not os.path.exists(datetime.now().strftime('%Y')):
        os.mkdir(datetime.now().strftime('%Y'))
    os.chdir(year_dir)
    month_dir = os.path.join(datetime.now().strftime('%m'))
    if not os.path.exists(datetime.now().strftime('%m')):
        os.mkdir(datetime.now().strftime('%m'))
    os.chdir(month_dir)
    day_dir = os.path.join(datetime.now().strftime('%d'))
    if not os.path.exists(datetime.now().strftime('%d')):
        os.mkdir(datetime.now().strftime('%d'))
    os.chdir(day_dir)

    # Nastavenie nazvu logu a aj handlera prenho
    log = datetime.now().strftime('%Y-%m-%d - %H-%M-%S.log')
    log_file = os.path.join(log)
    handler = logging.FileHandler(log_file)
    handler.setLevel(log_level)
    app.logger.addHandler(handler)

    # Nastavenie levelu, obsahu logu a jeho naformatovanie
    app.logger.setLevel(log_level)
    default_formatter = logging.Formatter("[%(asctime)s] %(levelname)s %(message)s", datefmt='%y %b %d - %H:%M:%S')
    handler.setFormatter(default_formatter)


# Nastavenie CORS policy
@app.after_request
def add_header(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    response.headers.add('X-Content-Type-Options', 'nosniff')

    if response.content_type == '':
        response.content_type = 'application/json'  # Nastavanie response v json

    # Nastavenie refresh tokenu aby sa access token obnovil po 30 minutach
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


@app.errorhandler(404)
def error404(error):
    return render_template('404.html'), 404

import timebank.models
import timebank.routes
import timebank.utils
