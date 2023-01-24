import datetime
import re
from sqlalchemy import inspect, text
from timebank import db
from timebank.models.services_model import Service


# Validacia sortovacich parametrov z requestu
def record_sort_params_handler(args, modeldb):
    valid = True
    if args.get('field'):
        sort_field = args.get('field')
    else:
        sort_field = 'id'

    if args.get('sort'):
        sort_dir = args.get('sort')
    else:
        sort_dir = 'asc'

    if not (sort_dir == 'asc' or sort_dir == 'desc'):
        valid = False

    if sort_field:
        col_exist = False
        for col in [column.name for column in inspect(modeldb).columns]:
            if col == sort_field:
                col_exist = True
        if not col_exist:
            valid = False

    return sort_field, sort_dir, valid


# Sorovanie DB query
def get_all_db_objects(sort_field, sort_dir, base_query):
    sort_query = base_query.order_by(text(sort_field + ' ' + sort_dir))
    return sort_query


# Reforatovanie datetime objektu na isoformat
def format_date(date):
    if date is None:
        return date
    else:
        date = date.isoformat()
        return date

# Custom error na handlovanie validacii
class ValidationError(Exception):
    def __init__(self, value, message):
        self.value = str(value)
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.value} -> {self.message}'


# Validacia datoveho typu
def is_number(field):
    try:
        int(field)
    except ValueError:
        raise ValidationError(field, f"Number is not valid.")


# Validacia formatu hodnotenia sluzby
def is_rating(field):
    if -1 < int(field) < 6:
        return field
    else:
        raise ValidationError(field, f"Number is not in 5* rating from 0 to 5.")


# Validacia formatu odhadovaneho casu sluzby
def is_estimate(field):
    if 31 > int(field) > 0:
        return field
    else:
        raise ValidationError(field, f"Estimate must be positive.")


# Kontrola existencie sluzby pri vytvarani serviceRegister
def service_exists(field):
    if not db.session.query(Service).get(field):
        raise ValidationError(field, f"Service id does not exist.")


# Validacia formatu datumu
def is_date(field, date_format='%Y-%m-%d'):
    if field:
        try:
            date = datetime.datetime.strptime(str(field), date_format).date()
        except ValueError:
            raise ValidationError(field, f"Incorrect data format, should be {date_format}")


# Validacia formatu tel. cisla
def phone_number_match(number):
    if not re.match(r"\A[+]\d{3} \d{3} \d{6}\Z", number):
        raise ValidationError(number, f"Incorrect number format")


# Validacia vstupu pri zadavani hodin za sluzbu
def is_hours(field):
    if 31 > int(field) > 0:
        return field
    else:
        raise ValidationError(field, f"Hours are not valid.")
