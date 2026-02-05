from flask import Blueprint

bp = Blueprint('qa', __name__)

@bp.route('/')
def qa_index():
    return {'message': 'QA API'}