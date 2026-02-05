from flask import Blueprint, jsonify
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

bp = Blueprint('config', __name__)

# 数据库连接函数
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'chat_db'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'password')
    )
    return conn

@bp.route('/models', methods=['GET'])
def get_models():
    """获取可用模型列表"""
    try:
        # 从环境变量或配置中获取模型列表
        # 这里返回一个示例列表
        models = [
            {
                "id": "gpt-3.5-turbo",
                "name": "GPT-3.5 Turbo",
                "description": "OpenAI的GPT-3.5 Turbo模型",
                "contextWindow": 16384,
                "default": True
            },
            {
                "id": "gpt-4",
                "name": "GPT-4",
                "description": "OpenAI的GPT-4模型",
                "contextWindow": 8192,
                "default": False
            },
            {
                "id": "gpt-4-turbo",
                "name": "GPT-4 Turbo",
                "description": "OpenAI的GPT-4 Turbo模型",
                "contextWindow": 128000,
                "default": False
            }
        ]
        
        return jsonify(models)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/', methods=['GET'])
def get_config():
    """获取配置信息"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("SELECT config_key, config_value FROM config")
        configs = cur.fetchall()
        
        cur.close()
        conn.close()
        
        # 构建配置字典
        config_dict = {}
        for config in configs:
            config_dict[config['config_key']] = config['config_value']
        
        return jsonify(config_dict)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/<key>', methods=['GET'])
def get_config_key(key):
    """获取指定配置项"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("SELECT config_value FROM config WHERE config_key = %s", (key,))
        config = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if not config:
            return jsonify({"error": "Config not found"}), 404
        
        return jsonify({"value": config['config_value']})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500