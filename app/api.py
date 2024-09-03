from flask import Blueprint, jsonify, request
from sqlalchemy import and_, or_
from .models import PPD
from . import db

api = Blueprint('api',__name__)

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

