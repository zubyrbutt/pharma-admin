from flask import jsonify
from werkzeug.exceptions import HTTPException, NotFound
from sqlalchemy.exc import SQLAlchemyError


class APIError(Exception):
    """Base class for API errors."""
    
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status'] = 'error'
        return rv


class NotFoundError(APIError):
    """Resource not found error."""
    
    def __init__(self, message="Resource not found", payload=None):
        super().__init__(message, 404, payload)


class ValidationError(APIError):
    """Validation error."""
    
    def __init__(self, message="Validation error", payload=None):
        super().__init__(message, 400, payload)


class AuthError(APIError):
    """Authentication error."""
    
    def __init__(self, message="Authentication error", payload=None):
        super().__init__(message, 401, payload)


def register_error_handlers(app):
    """Register error handlers for the app."""
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(404)
    def handle_not_found_error(error):
        """Handle specific 404 errors with JSON response."""
        response = jsonify({
            'status': 'error',
            'message': 'The requested URL was not found on the server.'
        })
        response.status_code = 404
        return response
    
    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        response = jsonify({
            'status': 'error',
            'message': error.description,
        })
        response.status_code = error.code
        return response
    
    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error):
        response = jsonify({
            'status': 'error',
            'message': str(error),
        })
        response.status_code = 500
        return response
    
    @app.errorhandler(Exception)
    def handle_generic_error(error):
        response = jsonify({
            'status': 'error',
            'message': str(error),
        })
        response.status_code = 500
        return response
    
    return app 