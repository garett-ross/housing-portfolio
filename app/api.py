from flask import Blueprint, jsonify, request
from sqlalchemy import and_, or_, select
from .models import PPD
from . import db

api = Blueprint('api',__name__)

#endpoint to fetch all data
@api.route("/all", methods=["POST", "GET"])
def all_data():
    if request.method == 'GET':
        results = db.session.execute(select(PPD)).scalars().all()
        data = [item.to_dict() for item in results]
        return jsonify(data)

@api.route("/api", methods=["POST", "GET"])
def handle_request():
    if request.method == 'POST':
        # Handle POST requests for filtered queries
        filters = request.get_json()
        query = db.session.query(PPD.price, PPD.date)  # Fetch only price and date

        if filters:
            filter_conditions = []
            for key, value in filters.items():
                if isinstance(value, dict):
                    field = key
                    operator = value.get('operator')
                    field_value = value.get('value')

                    if hasattr(PPD, field):
                        column = getattr(PPD, field)
                        if operator == 'eq':
                            filter_conditions.append(column == field_value)
                        elif operator == 'ne':
                            filter_conditions.append(column != field_value)
                        elif operator == 'gt':
                            filter_conditions.append(column > field_value)
                        elif operator == 'lt':
                            filter_conditions.append(column < field_value)
                        elif operator == 'ge':
                            filter_conditions.append(column >= field_value)
                        elif operator == 'le':
                            filter_conditions.append(column <= field_value)

            if filter_conditions:
                query = query.filter(and_(*filter_conditions))

        results = query.all()
        data = [{'price': r[0], 'date': r[1]} for r in results]
        return jsonify(data)
    
    elif request.method == 'GET':
        # Handle GET requests for total data
        results = db.session.query(PPD.price, PPD.date).all()
        data = [{'price': r[0], 'date': r[1]} for r in results]
        return jsonify(data)

# endpoint to return unique values, used by front end to populate options
@api.route("/unique", methods=["POST"])
def unique_values():
    if request.method == "POST":
        request_data = request.get_json()
        filters = request_data.get('filters', {})  # Current filter selections
        col = request_data.get('db_header')       # Column for which unique values are requested

        # Start a base query
        query = db.session.query(getattr(PPD, col)).distinct()

        # Apply the existing filters to limit results
        if filters:
            filter_conditions = []
            for key, value in filters.items():
                if hasattr(PPD, key):
                    column = getattr(PPD, key)
                    filter_conditions.append(column == value)
            query = query.filter(and_(*filter_conditions))
        query = query.order_by(getattr(PPD, col).asc())
        # Fetch distinct values
        unique_values = query.all()
        values_list = [value[0] for value in unique_values]
        return jsonify(values_list)
