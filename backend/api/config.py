from flask import Blueprint

bp = Blueprint('config', __name__)

@bp.route('/')
def config_index():
    return {'message': 'Config API'}