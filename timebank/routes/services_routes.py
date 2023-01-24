# Import funkcii a modulov
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from timebank.models.services_model import Service
from timebank.models.users_model import User
from timebank import app, db
from timebank.libs.response_helpers import record_sort_params_handler,\
    get_all_db_objects, is_number, ValidationError, is_estimate


# Funckia na vytiahnutie vsetkych servisov z databazi
@app.route('/api/v1/services', methods=['GET'])
def api_services():

    # Z requestu overujeme sortovacie parametre
    sort_field, sort_dir, valid = record_sort_params_handler(request.args, Service)
    if not valid:
        app.logger.error(f"{request.remote_addr}, Request in get all services failed, check your request and try again")
        return {'Bad Request': 'services not found'}, 400

    # Do premennej db_objs pridelime vsetky servisy podla zadanych sortovacich parametrov
    db_objs = get_all_db_objects(sort_field, sort_dir, db.session.query(Service)).all()
    if len(db_objs):
        response_obj = []
        # Iterujeme cez vsetky servisy
        for obj in db_objs:
            response_obj.append(dict(
                id=obj.id,
                title=obj.title,
                User=dict(
                    id=obj.User.id,
                    phone=obj.User.phone,
                    user_name=obj.User.user_name,
                    time_account=obj.User.time_account,
                ),
                avg_rating=obj.avg_rating,
                estimate=obj.estimate,
            ))
        app.logger.info(f"{request.remote_addr}, All services have been loaded successfully.")
        return jsonify(response_obj), 200
    else:
        app.logger.warning(f"{request.remote_addr}, No service has been found.")
        return '', 404


# Funckia na vytiahnutie konkretneho servisu podla jeho id z databazi
@app.route('/api/v1/service/<services_id>', methods=['GET'])
def api_single_service_get(services_id):

    # Vytiahnem z databazy model Service
    db_query = db.session.query(Service)
    # Do premennej obj si ulozim konkretny servis podla servis_id
    obj = db_query.get(services_id)

    if not obj:
        app.logger.warning(f"{request.remote_addr}, Selected service: {services_id} doesn't exist.")
        return {'Bad Request': f'Service {services_id} not found'}, 404

    response_obj = [dict(
        id=obj.id,
        title=obj.title,
        User=dict(
            id=obj.User.id,
            phone=obj.User.phone,
            user_name=obj.User.user_name,
            time_account=obj.User.time_account,
        ),
        avg_rating=obj.avg_rating,
        estimate=obj.estimate,
    )]

    response = jsonify(response_obj)
    app.logger.info(f"{request.remote_addr}, Selected service: {services_id} has been loaded successfully.")
    return response, 200


# Funkcia na updatovanie servisu z databazi
@app.route('/api/v1/service/<services_id>', methods=['PUT'])
@jwt_required(optional=True)
def api_single_service_put(services_id):
    if get_jwt_identity() is None:
        app.logger.warning(f"{request.remote_addr}, User is not logged in.")
        return jsonify({'error': 'User is not logged in.'}), 401

    db_query = db.session.query(Service)
    db_obj = db_query.get(services_id)

    if not db_obj:
        app.logger.warning(f"{request.remote_addr}, Selected service: {services_id} does not exist.")
        return {'Bad Request': f'Service {services_id} not found'}, 400
    old_obj = [db_obj.title, db_obj.user_id, db_obj.estimate]
    req_data = None
    if request.content_type == 'application/json':
        req_data = request.json
    elif request.content_type == 'application/x-www-form-urlencoded':
        req_data = request.form

    if 'title' in req_data:
        # Osetrenie velkosti titlu.. max 1000 znakov.
        if len(req_data['title']) > 1000:
            app.logger.warning(f"{request.remote_addr}, Title too long.")
            return jsonify({'error': 'Title too long.'}), 400
        db_obj.title = req_data['title']

    # V podmienke validujeme estimate ci je cislo a ci je vacsie ako 0
    if 'estimate' in req_data:
        if req_data['estimate'] is None:
            db_obj.estimate = None
        else:
            try:
                is_number(req_data['estimate'])
                is_estimate(req_data['estimate'])
            except ValidationError as e:
                app.logger.error(f"{request.remote_addr}, Validation error: "
                                 f"Updating services failed, estimate is not a number or not in range.")
                return jsonify({'error': str(e)}), 400
            db_obj.estimate = req_data['estimate']

    try:
        # Prida zmenu do databazy
        db.session.commit()
        db.session.refresh(db_obj)
    except IntegrityError as e:
        app.logger.error(f"{request.remote_addr}, Integrity error: There has been problem "
                         f"with updating service in the database. Recheck your request and try again.")
        return jsonify({'error': str(e.orig)}), 405
    app.logger.info(f"{request.remote_addr}, User: {services_id} has been updated by requestor: {get_jwt_identity()}\n"
                    f"  Title has been changed from \"{old_obj[0]}\" to \"{db_obj.title}\",\n"
                    f"  User ID has been changed from {old_obj[1]} to {db_obj.user_id},\n"
                    f"  Estimate has been changed from {old_obj[2]} to {db_obj.estimate}.")
    return jsonify({'Message': 'Service successfully edited'}), 204


# Funkcia na zmazanie servisu z databazi
@app.route('/api/v1/service/<services_id>', methods=['DELETE'])
@jwt_required(optional=True)
def api_single_service_delete(services_id):
    if get_jwt_identity() is None:
        app.logger.warning(f"{request.remote_addr}, User is not logged in.")
        return jsonify({'error': 'User is not logged in.'}), 401
    db_query = db.session.query(Service)

    # Do premennej db_test ulozime konkretny servis podla jeho ID
    db_test = db_query.get(services_id)
    db_obj = db_query.filter_by(id=services_id)

    # Pokial taky servis neexistuje vyhodi nam error a funckia skonci
    if not db_test:
        app.logger.warning(f"{request.remote_addr}, Selected service: {services_id} does not exist.")
        return {'Bad Request': f'Service {services_id} not found'}, 400

    try:
        db_obj.delete()
        db.session.commit()
    except IntegrityError as e:
        app.logger.error(f"{request.remote_addr}, Integrity error: "
                         f"There has been problem with deleting service from the database. "
                         f"Recheck your request and try again.")
        return jsonify({'error': str(e.orig)}), 405
    else:
        app.logger.info(f"{request.remote_addr}, Selected service: {services_id} "
                        f"has been deleted successfully by requestor: {get_jwt_identity()}.")
        return jsonify({'Message': 'Service successfully deleted'}), 204


# Funckia na vytvorenie servisu a pridania ho do databazi
@app.route('/api/v1/service-create', methods=['POST'])
@jwt_required(optional=True)
def api_single_service_create():
    # Kontrola ci je uzivatel prihlaseny. Ak nie vrati error + koment "uzivatel nieje prihlaseny"
    if get_jwt_identity() is None:
        app.logger.warning(f"{request.remote_addr}, User is not logged in.")
        return jsonify({'error': 'User is not logged in.'}), 401
    db_obj = Service()

    req_data = None
    if request.content_type == 'application/json':
        req_data = request.json
    elif request.content_type == 'application/x-www-form-urlencoded':
        req_data = request.form

    db_query2 = db.session.query(User)
    # Overujeme ci uzivatel moze vytvorit servis tym ze kontrolujeme ci je cislo z jeho tokenu v databaze
    obj2 = db_query2.filter_by(phone=get_jwt_identity()).one()

    # Overujeme ci je title v tele requestu. Ak nie vrati nam error.
    if 'title' not in req_data:
        app.logger.warning(f"{request.remote_addr}, Title is missing. Check your request and try again.")
        return jsonify({'error': 'Title is missing.'}), 400
    # Overujeme dlhziu titlu. Ak ma viac ako 1000 znakov tak nam vrati error.
    if len(req_data['title']) > 1000:
        app.logger.warning(f"{request.remote_addr}, Title too long.")
        return jsonify({'error': 'Title too long.'}), 400

    if 'estimate' in req_data:
        try:
            is_number(req_data['estimate'])
            is_estimate(req_data['estimate'])
            db_obj.estimate = int(req_data['estimate'])
        except ValidationError as e:
            app.logger.error(f"{request.remote_addr}, Validation error: "
                             f"Creating service failed, check estimate in your request and try again.")
            return jsonify({'error': str(e)}), 400

    db_obj.user_id = obj2.id
    db_obj.title = req_data['title']

    try:
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)
    except IntegrityError as e:
        app.logger.error(f"{request.remote_addr}, Integrity error: "
                         f"There has been problem with creating new service into database. "
                         f"Recheck your request and try again.")
        return jsonify({'error': str(e.orig)}), 405
    app.logger.info(f"{request.remote_addr}, Service has been created successfully, "
                    f"New service has following parameters:\n"
                    f"  Id: {db_obj.id},\n"
                    f"  Title: {db_obj.title},\n"
                    f"  User ID: {db_obj.user_id},\n"
                    f"  Estimate: {db_obj.estimate}.")
    return api_single_service_get(db_obj.id)


# metoda pro autocomplete - /api/v1/service-search?ord=asc&field=title&s=tit
@app.route('/api/v1/service-search', methods=['GET'])
def api_service_search():
    field, sort_dir, valid = record_sort_params_handler(request.args, Service)
    if not valid:
        app.logger.warning(f"{request.remote_addr}, Search of services failed, check your request and try again.")
        return jsonify({'error': 'Search of services failed'}), 400

    # Z URL hladame kluc[key] "s" a pridame mu jeho hodnotu["value"] ktoru vycitame z URL
    if request.args.get('s'):
        search_string = request.args.get('s')
    else:
        app.logger.warning(f"{request.remote_addr}, Search of services failed, check your request and try again.")
        return jsonify({'error': 'Search of services failed'}), 400

    response_obj = []
    # Dlzka hladanej hodnoty musi mat minimalne 3 znaky a viac
    if len(search_string) > 2:
        db_query = db.session.query(Service)
        # Zo servis titles filtrujeme vsetky titles ktore maju v sebe hladany string. To je hodnotu pri kluci "s" z URL
        db_filter = db_query.filter(Service.title.like('%' + search_string + '%'))

        # Pokial sme zadali sortovacie parametre tak ich podla nich zoradime
        if field and sort_dir:
            db_objs = db_filter.order_by(text(field + ' ' + sort_dir)).all()
        # Pokial sme nezadali sortovacie parametre tak ich zoradime zaradom ako idu.
        else:
            db_objs = db.filter.all()

        if len(db_objs):

            for obj in db_objs:
                response_obj.append(dict(
                    id=obj.id,
                    title=obj.title,
                    User=dict(
                        id=obj.User.id,
                        phone=obj.User.phone,
                        user_name=obj.User.user_name,
                        time_account=obj.User.time_account,
                    ),
                    avg_rating=obj.avg_rating,
                    estimate=obj.estimate,
                ))
    app.logger.info(f"{request.remote_addr}, Search of services has been completed successfully.")
    return jsonify(response_obj), 200


# Vytvor zoznam sluzieb ktory odfiltruje zoznam sluzieb podla konkretneho poskytovatela:
@app.route('/api/v1/services-user/<user_id>', methods=['GET'])
def api_service_user_id(user_id):
    sort_field, sort_dir, valid = record_sort_params_handler(request.args, Service)

    if not valid:
        app.logger.warning(f"{request.remote_addr}, Search of services by user failed. "
                           f"Check your request and try again.")
        return '', 400

    db_objs = get_all_db_objects(sort_field, sort_dir, db.session.query(Service)).all()

    db_query = db.session.query(User)
    obj = db_query.get(user_id)

    if not obj:
        app.logger.warning(f"{request.remote_addr}, Search of services failed. Selected user with id: {user_id}"
                           f" does not exist.")
        return '{"Message": "No user with that ID!"}', 404

    if len(db_objs):
        response_obj = []
        for service in db_objs:
            if service.user_id == obj.id:
                response_obj.append(dict(
                    title=service.title,
                    phone=obj.phone,
                    user_name=obj.user_name,
                    estimate=service.estimate,
                    rating=service.avg_rating,
                    user_id=obj.id,
                    service_id=service.id
                ))
        app.logger.info(f"{request.remote_addr}, Service search has been completed successfully.")
        return jsonify(response_obj), 200
    else:
        app.logger.warning(f"{request.remote_addr}, Service search failed, "
                           f"no service has been found for user with selected id: {user_id}.")
        return '', 404


# Vyhladaj z databazy serviceregister podla ratingu ktore sme zadali!!!
@app.route('/api/v1/find_service_rating', methods=['GET'])
def find_service_rating():

    search = request.args.get('s')
    serviceregister_model = db.session.query(Service)

    try:
        is_number(search)
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400

    sort_field, sort_dir, valid = record_sort_params_handler(request.args, Service)
    if not valid:
        return '', 400
    db_objs = get_all_db_objects(sort_field, sort_dir, db.session.query(Service)).all()

    result = []

    for x in db_objs:
        if x.avg_rating:
            if x.avg_rating >= int(search):
                result.append(dict(
                    id=x.id,
                    title=x.title,
                    user_id=x.user_id,
                    estiamte=x.estimate,
                    avg_rating=x.avg_rating,
                ))

    if result:
        return jsonify(result), 200

    return jsonify({"message": f"No services with {search} and higher rating!"}), 404
