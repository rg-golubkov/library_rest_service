"""Basic functionality for rest-service
"""
from typing import Optional

from flask import abort, jsonify
from flask.views import MethodView

from ..database import db_session
from . import bp


def register_api(view: MethodView, endpoint: str, url: str,
                 pk: str = 'id', pk_type: str = 'int'):
    """Add url rules for rest-api endpoint

    Args:
        view: view with get/post/put/delete methods
        endpoint: name of view
        url: endpoint url
        pk: primary key name
        pk_type: primary key type
    """
    view_func = view.as_view(endpoint)
    bp.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET',])
    bp.add_url_rule(url, view_func=view_func, methods=['POST',])
    bp.add_url_rule(f'{url}<{pk_type}:{pk}>', view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])


def get_record_or_404(model, pk):
    """Get row from database by primary key

    Args:
        model: database model (table)
        pk: primary key value

    Returns:
        instance of model

    Raises:
        HTTPError(404) if row is not found in table
    """
    record = model.query.get(pk)
    if record is None:
        abort(404)
    return record


class BaseAPI(MethodView):
    """Common class for description rest api

    Attributes:
        mode: base database model for enpoint
        namespace: name of endpoint
    """
    model = None
    namespace = None

    def get(self, pk: Optional[int] = None):
        """GET /<namespace>/<Optional: pk>

        Returns:
            200, object or list of objects
        """
        if pk is None:
            return self.get_list()

        return jsonify(get_record_or_404(self.model, pk).to_dict())

    def get_list(self):
        """GET /<namespace>/

        Returns:
            200, list of objects
        """
        recordset = [
            record.to_dict()
            for record in self.model.query.all()
        ]

        return jsonify({self.namespace: recordset})

    def post(self):
        """POST /<namespace>/

        Returns:
            201, Created object
        """
        record = self.create_record()

        db_session.add(record)
        db_session.commit()

        return (jsonify(record.to_dict()), 201)

    def put(self, pk: int):
        """PUT /<namespace>/<pk>

        Returns:
            200, changed object
        """
        record = get_record_or_404(self.model, pk)
        record = self.update_record(record)

        db_session.commit()
        return jsonify(record.to_dict())

    def delete(self, pk: int):
        """DELETE /<namespace>/<pk>

        Returns:
            204
        """
        record = get_record_or_404(self.model, pk)
        db_session.delete(record)
        db_session.commit()

        return ('', 204)

    def create_record(self):
        """Create record (POST-method)
        """
        raise NotImplementedError

    def update_record(self, record):
        """Update record (PUT-method)

        Args:
            record: source object
        """
        raise NotImplementedError
