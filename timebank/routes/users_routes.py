# Import funkcii a modulov
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, \
    jwt_required, get_jwt_identity, unset_jwt_cookies
from sqlalchemy.exc import IntegrityError, NoResultFound
from werkzeug.security import generate_password_hash, check_password_hash

from timebank.models.serviceregister_model import Serviceregister
from timebank.models.services_model import Service
from timebank.models.users_model import User
from timebank import app, db
from timebank.libs.response_helpers import record_sort_params_handler, get_all_db_objects, is_number, ValidationError, \
    phone_number_match


# Funckia na vytiahnutie vsetkych pouzivatelov z databazi
@app.route('/api/v1/users', methods=['GET'])
def api_users():
    sort_field, sort_dir, valid = record_sort_params_handler(request.args, User)
    if not valid:
        app.logger.error(f"{request.remote_addr}, Request in get all users failed, check your request and try again")
        return '', 400
    db_objs = get_all_db_objects(sort_field, sort_dir, db.session.query(User)).all()
    # Pokial je aspon jeden objekt v db_objs prejdeme podmienkou
    if len(db_objs):
        response_obj = []
        for obj in db_objs:
            # Do prazdneho listu response_obj pridavame vsetky dictionaries ktore mame v db_objs
            response_obj.append(dict(
                id=obj.id,
                phone=obj.phone,
                user_name=obj.user_name,
                time_account=obj.time_account,
            ))
        app.logger.info(f"{request.remote_addr}, All users have been loaded successfully.")
        return jsonify(response_obj), 200
    else:
        app.logger.warning(f"{request.remote_addr}, No user has been found.")
        return '{"Message": "No user to be found."}', 404


# Funkcia na vytiahnutie jedneho pouzivatela z databazky podla user_id
@app.route('/api/v1/user/<user_id>', methods=['GET'])
def api_single_user_get(user_id):

    # Vytiahnem z databazy model User
    db_query = db.session.query(User)
    # do premennej obj si ulozim konkretneho pouzivatela podla user_id
    obj = db_query.get(user_id)

    if not obj:
        app.logger.warning(f"{request.remote_addr}, Selected user: {user_id} doesn't exist.")
        return jsonify({"Message": "No user to be found."}), 404

    response_obj = [dict(
        id=obj.id,
        phone=obj.phone,
        user_name=obj.user_name,
        time_account=obj.time_account,
    )]

    response = jsonify(response_obj)
    app.logger.info(f"{request.remote_addr}, Selected user: {user_id} has been loaded successfully.")
    return response, 200


# Funkcia na updatovanie pouzivatela z databazi
@app.route('/api/v1/user/<user_id>', methods=['PUT'])
@jwt_required(optional=True)
def api_single_user_put(user_id):
    if get_jwt_identity() is None:
        app.logger.warning(f"{request.remote_addr}, User is not logged in.")
        return jsonify({'error': 'User is not logged in.'}), 401
    db_query = db.session.query(User)
    db_obj = db_query.get(user_id)
    if not db_obj:
        app.logger.warning(f"{request.remote_addr}, Selected user: {user_id} does not exist.")
        return '{"message": "No user to be found."}', 404
    old_obj = [db_obj.phone, db_obj.user_name, db_obj.time_account]
    req_data = None
    # Skontroluje ci je telo poziadavky vo formate application/json a ak je tak z neho vytiahne data
    if request.content_type == 'application/json':
        req_data = request.json
    # Skontroluje ci je telo poziadavky vo formate application/x-www-form-urlencoded a ak je tak z neho vytiahne data
    elif request.content_type == 'application/x-www-form-urlencoded':
        req_data = request.form

    if 'phone' in req_data:
        try:
            # Kontrola telefonneho cisla ci je v spravnom tvare podla funckie phone_number_match
            phone_number_match(req_data['phone'])
            db_obj.phone = req_data['phone']
        except ValidationError as e:
            app.logger.error(f"{request.remote_addr}, Validation error: "
                             f"Updating user failed, phone number is not valid format.")
            return jsonify({'error': str(e)}), 400

    if 'user_name' in req_data:
        if len(req_data['user_name']) > 30:
            app.logger.warning(f"{request.remote_addr}, Username too long while editing user.")
            return jsonify({'error': 'User name too long.'}), 400
        db_obj.user_name = req_data['user_name']

    # Podmienka ktora skontroluje ci je v requeste cislo. Pokial nie tak vyhodi error
    if 'time_account' in req_data:
        try:
            is_number(req_data['time_account'])
        except ValidationError as e:
            app.logger.error(f"{request.remote_addr}, Validation error: "
                             f"Updating user failed, time account is not a number.")
            return jsonify({'error': str(e)}), 400

        db_obj.time_account = int(req_data['time_account'])

    try:
        # Potvrdi zmenu v databaze
        db.session.commit()
        db.session.refresh(db_obj)
    except IntegrityError as e:
        app.logger.error(f"{request.remote_addr}, Integrity error: There has been problem "
                         f"with updating user in the database. Recheck your request and try again.")
        return jsonify({'error': str(e.orig)}), 405

    app.logger.info(f"{request.remote_addr}, User: {user_id} has been updated by requestor: {get_jwt_identity()}\n"
                    f"  Phone has been changed from {old_obj[0]} to {db_obj.phone},\n"
                    f"  Username has been changed from \"{old_obj[1]}\" to \"{db_obj.user_name}\",\n"
                    f"  Time account has been changed from {old_obj[2]} to {db_obj.time_account}.")
    return jsonify({"Message": "user successfully updated."}), 204


# Funkcia na zmazanie pouzivatela z databazi
@app.route('/api/v1/user/<user_id>', methods=['DELETE'])
@jwt_required(optional=True)
def api_single_user_delete(user_id):
    if get_jwt_identity() is None:
        app.logger.warning(f"{request.remote_addr}, User is not logged in.")
        return jsonify({'error': 'User is not logged in.'}), 401
    db_query = db.session.query(User)
    db_test = db_query.get(user_id)
    db_obj = db_query.filter_by(id=user_id)

    if not db_test:
        app.logger.warning(f"{request.remote_addr}, Selected user: {user_id} does not exist.")
        return '{"Message": "No user to be found."}', 404

    try:
        db_obj.delete()
        db.session.commit()
    except IntegrityError as e:
        app.logger.error(f"{request.remote_addr}, Integrity error: "
                         f"There has been problem with deleting user from the database. "
                         f"Recheck your request and try again.")
        return jsonify({'error': str(e.orig)}), 405
    else:
        app.logger.info(f"{request.remote_addr}, Selected user: {user_id} "
                        f"has been deleted successfully by requestor: {get_jwt_identity()}.")
        return jsonify({'Message': 'Logout successfully'}), 204


# Funckia na vytvorenie uzivatela a pridania ho do databazi
@app.route('/api/v1/user-create', methods=['POST'])
def api_single_user_create():
    db_obj = User()

    req_data = None
    if request.content_type == 'application/json':
        req_data = request.json
    elif request.content_type == 'application/x-www-form-urlencoded':
        req_data = request.form

    if 'user_name' not in req_data or 'phone' not in req_data \
            or 'password' not in req_data or 'password_val' not in req_data:
        return jsonify({'error': 'request not valid'}), 400

    if len(req_data['user_name']) > 30:
        app.logger.warning(f"{request.remote_addr}, Username too long while creting user.")
        return jsonify({'error': 'Username too long.'}), 400

    try:
        phone_number_match(req_data['phone'])
    except ValidationError as e:
        app.logger.error(f"{request.remote_addr}, Validation error: "
                         f"Creating user failed, check your request and try again.")
        return jsonify({'error': str(e)}), 400

    # Z tela poziadavky vytiahneme cislo a vlozime ho do databazy
    db_obj.phone = req_data['phone']
    # Z tela poziadavky vytiahneme heslo, zahashujeme ho a vlozime ho do databazy
    if req_data['password'] == req_data['password_val']:
        db_obj.password = generate_password_hash(req_data['password'])
    else:
        app.logger.warning(f"{request.remote_addr}, Passwords are not equal while creating user, try again.")
        return jsonify({'error': 'Passwords are not equal'}), 400
    # Z tela poziadavky vytiahneme meno a vlozime ho do databazy
    db_obj.user_name = req_data['user_name']
    db_obj.time_account = 0
    try:
        # Pridame zmeny do databazy
        db.session.add(db_obj)
        # Ulozime zmeny v databaze
        db.session.commit()
        db.session.refresh(db_obj)

    except IntegrityError as e:
        app.logger.error(f"{request.remote_addr}, Integrity error: "
                         f"There has been problem with creating new user into database. "
                         f"Recheck your request and try again.")
        return jsonify({'error': str(e.orig)}), 405
    app.logger.info(f"{request.remote_addr}, User has been created successfully, New user has following parameters:\n"
                    f"  Id: {db_obj.id},\n"
                    f"  Phone: {db_obj.phone},\n"
                    f"  Username: {db_obj.user_name},\n"
                    f"  Time account: {db_obj.time_account}.")

    return api_single_user_get(db_obj.id)


# Funckia ktora zmeni zadanemu pouzivatelovy heslo
@app.route('/api/v1/user/<user_id>/set-password', methods=['PUT'])
def api_single_user_set_password(user_id):

    db_query = db.session.query(User)
    db_obj = db_query.get(user_id)
    if not db_obj:
        app.logger.warning(f"{request.remote_addr}, Selected user: {user_id} does not exist.")
        return jsonify({"Message": "No user to be found."}) , 404

    req_data = None
    if request.content_type == 'application/json':
        req_data = request.json
    elif request.content_type == 'application/x-www-form-urlencoded':
        req_data = request.form

    if 'password' not in req_data or 'password_val' not in req_data:
        app.logger.warning(f"{request.remote_addr}, Passwords are missing while setting password.")
        return jsonify({'error': 'Missing passwords'}), 400

    if req_data['password'] == req_data['password_val']:
        db_obj.password = generate_password_hash(req_data['password'])
    else:
        app.logger.warning(f"{request.remote_addr}, Passwords are not equal while setting password, try again.")
        return jsonify({"Message": "Passwords are not equal."}), 400

    try:
        db.session.commit()
    except IntegrityError as e:
        app.logger.error(f"{request.remote_addr}, Integrity error: "
                         f"There has been problem with setting password for user: {user_id}. "
                         f"Recheck your request and try again.")
        return jsonify({'error': str(e.orig)}), 405
    app.logger.info(f"{request.remote_addr}, Selected user: {user_id} password has been changed.")
    return jsonify({"Message": "User password succesfully changed."}), 204


# Funkcia na prihlasenie uzivatela
@app.route('/api/v1/user/login', methods=['POST'])
def api_single_user_login():
    req_data = None
    if request.content_type == 'application/json':
        req_data = request.json
    elif request.content_type == 'application/x-www-form-urlencoded':
        req_data = request.form
    # Podmienka ktora kontroluje ci mame v tele poziadavky telefonne cislo a heslo
    if 'phone' not in req_data or 'password'not in req_data:
        app.logger.warning(f"{request.remote_addr}, Login failed, check your request and try again")
        return '{"Message": "Phone number and password not defined"}', 400
    phone = req_data['phone']
    password = req_data['password']

    db_query = db.session.query(User)
    try:
        db_obj = db_query.filter_by(phone=phone).one()
    except NoResultFound:
        app.logger.warning(f"{request.remote_addr}, Phone number has been not found in database, cannot login")
        return jsonify({'Message': 'Number doesn\'t exist'}), 404

    if not check_password_hash(db_obj.password, password):
        app.logger.warning(f"{request.remote_addr}, Password is not correct, cannot login")
        return jsonify({'Message': 'Password not correct'}), 401

    identity = phone
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)

    response = jsonify({'login': True, 'phone': phone, 'id': db_obj.id,
                        'user_name': db_obj.user_name, 'access_token': access_token})
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    app.logger.info(f"{request.remote_addr}, Selected user: {identity} has logged in successfully.")
    return response, 201


# Funkcia na odhlasenie pouzivatela
@app.route('/api/v1/user/logout', methods=['POST'])
# Metoda vyzauje JWT-token
@jwt_required(optional=True)
def api_single_user_logout():
    if get_jwt_identity() is None:
        app.logger.warning(f"{request.remote_addr}, User is not logged in.")
        return jsonify({'error': 'User is not logged in.'}), 401
    # get_jwt_identity je funckia ktora zo zadaneho tokenu vytiahne identitu
    identity = get_jwt_identity()
    db_query = db.session.query(User)
    try:
        db_obj = db_query.filter_by(phone=identity).one()
    except NoResultFound:
        app.logger.error(f"{request.remote_addr}, User with this token does not exist, log out failed.")
        return '{"Message": "No result found."}', 401

    response = jsonify({'logout': True, "msg": "see ya again"})
    unset_jwt_cookies(response)
    app.logger.info(f"{request.remote_addr}, Selected user: {get_jwt_identity()} has logged out successfully.")
    return response, 201


# Funkcia na vypisanie profilu uzivatela
@app.route('/api/v1/user/profile', methods=['GET'])
@jwt_required(optional=True)
def api_single_user_profile():
    if get_jwt_identity() is None:
        app.logger.warning(f"{request.remote_addr}, User is not logged in.")
        return jsonify({'error': 'User is not logged in.'}), 401
    phone = get_jwt_identity()
    db_query = db.session.query(User)
    try:
        obj = db_query.filter_by(phone=phone).one()
    except NoResultFound:
        app.logger.error(f"{request.remote_addr}, User with this token does not exist, can not show user profile.")
        return '{"Message": "No result found."}', 404
    db_query2 = db.session.query(Serviceregister)
    obj2 = db_query2.filter_by(service_id=Service.id).all()

    services = []
    for ser in obj.Service:
        serviceregister = []
        for serreg in obj2:
            if serreg.service_id == ser.id:
                serviceregister.append(dict(
                    id=serreg.id,
                    consumer_id=serreg.consumer_id,
                    hours=serreg.hours,
                    service_status=serreg.service_status.name,
                    end_time=serreg.end_time,
                    rating=serreg.rating,
                ))
        services.append(dict(
            id=ser.id,
            title=ser.title,
            estimate=ser.estimate,
            avg_rating=ser.avg_rating,
            serviceregister=serviceregister,
        ))
    response_obj = [dict(
        id=obj.id,
        phone=obj.phone,
        user_name=obj.user_name,
        time_account=obj.time_account,
        services=services,
    )]

    response = jsonify(response_obj)
    app.logger.info(f"{request.remote_addr}, Selected user: {get_jwt_identity()} has loaded his profile successfully.")
    return response, 200


@app.route('/api/v1/user/services', methods=['GET'])
@jwt_required(optional=True)
def api_single_user_services():
    if get_jwt_identity() is None:
        app.logger.warning(f"{request.remote_addr}, User is not logged in.")
        return jsonify({'error': 'User is not logged in.'}), 401

    phone = get_jwt_identity()
    user_query = db.session.query(User)
    user_obj = user_query.filter_by(phone=phone).one()

    ser_query = db.session.query(Service)
    ser_obj = ser_query.filter_by(user_id=user_obj.id).all()

    services = []
    for s in ser_obj:
        services.append(dict(
            id=s.id,
            title=s.title,
            estimate=s.estimate,
            avg_rating=s.avg_rating,
        ))

    response = jsonify(services)
    return response, 200


@app.route('/api/v1/user/history-log', methods=['GET'])
@jwt_required(optional=True)
def api_single_user_history():
    if get_jwt_identity() is None:
        app.logger.warning(f"{request.remote_addr}, User is not logged in.")
        return jsonify({'error': 'User not logged in'}), 401

    phone = get_jwt_identity()
    user_query = db.session.query(User)
    user_obj = user_query.filter_by(phone=phone).one()

    reg_query = db.session.query(Serviceregister).join(Service)
    reg_obj = reg_query.filter(Service.user_id == user_obj.id,
                                  Serviceregister.service_status == 'ended')

    history = []
    for r in reg_obj:
        history.append(dict(
            title=r.Service.title,
            hours=r.hours,
            end_time=r.end_time,
            rating=r.rating,
            consumer_id=r.consumer_id,
        ))

    response = jsonify(history)
    app.logger.info(f"{request.remote_addr}, User history log successsfully loaded by requestor: {get_jwt_identity()}")
    return response, 200


# Funckia na refresnutie tokenu
@app.route('/token/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    # Get_jwt_identity je funckia ktora vrati identitu JWT-tokenu. Ak nenajde ziadnu vrati None.
    current_user = get_jwt_identity()
    # Create_access_token je funkcia ktora vytvara JWT-token. V nasom pripade len aktualizuje konkretnemu pouzivatelovy
    # jeho aktualny token. Da sa tam nastavit aj expiracia.
    access_token = create_access_token(identity=current_user)

    resp = jsonify({'refresh': True})
    set_access_cookies(resp, access_token)
    app.logger.info(f"Token has been successfully refreshed for selected user: {get_jwt_identity()}")
    return resp, 200


# Funkcia na kontrolu ci je telefonne cislo v databaze
@app.route('/api/v1/user/phone', methods=['POST'])
def get_number():
    db_obj = db.session.query(User)

    req_data = None
    if request.content_type == 'application/json':
        req_data = request.json
    elif request.content_type == 'application/x-www-form-urlencoded':
        req_data = request.form

    number = req_data['phone']

    for num in db_obj:
        if num.phone == number:
            app.logger.warning(f"{request.remote_addr}, Phone is already in the database. Try again")
            return jsonify(result=False), 200

    app.logger.info(f"{request.remote_addr}, Phone does not exist in database.")
    return jsonify(result=True), 200
