from flask import Blueprint

bp = Blueprint('docs', __name__)

@bp.route('/')
def docs_index():
    return {'message': 'Docs API'}