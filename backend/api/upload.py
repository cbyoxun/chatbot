from flask import Blueprint, request, jsonify, send_from_directory
import uuid
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

bp = Blueprint('upload', __name__)

# 数据库连接函数
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'chat_db'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'password')
    )
    return conn

@bp.route('/<chat_id>', methods=['POST'])
def upload_file(chat_id):
    """上传文件"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        # 生成唯一文件名
        unique_filename = str(uuid.uuid4()) + '_' + file.filename
        filepath = os.path.join('uploads', unique_filename)
        
        # 确保上传目录存在
        os.makedirs('uploads', exist_ok=True)
        
        # 保存文件
        file.save(filepath)
        
        # 构建响应
        response = {
            "id": str(uuid.uuid4()),
            "name": file.filename,
            "url": f"/uploads/{unique_filename}",
            "type": file.content_type or "application/octet-stream",
            "size": os.path.getsize(filepath)
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/<filename>', methods=['GET'])
def serve_file(filename):
    """提供上传文件的访问"""
    try:
        return send_from_directory('uploads', filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 404
