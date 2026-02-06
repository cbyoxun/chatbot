from flask import Blueprint, jsonify, request
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

# AI服务商管理API
@bp.route('/ai-providers', methods=['GET'])
def get_ai_providers():
    """获取所有AI服务商"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("SELECT id, name, provider_type, host FROM ai_providers")
        providers = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return jsonify(providers)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/ai-providers/<int:id>', methods=['GET'])
def get_ai_provider(id):
    """获取指定AI服务商详情"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("SELECT * FROM ai_providers WHERE id = %s", (id,))
        provider = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if not provider:
            return jsonify({"error": "Provider not found"}), 404
        
        return jsonify(provider)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/ai-providers', methods=['POST'])
def add_ai_provider():
    """添加新AI服务商"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        required_fields = ['name', 'provider_type', 'host', 'api_key']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            "INSERT INTO ai_providers (name, provider_type, host, api_key) "
            "VALUES (%s, %s, %s, %s) RETURNING id",
            (data['name'], data['provider_type'], data['host'], data['api_key'])
        )
        provider_id = cur.fetchone()[0]
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"id": provider_id, "message": "Provider added successfully"}), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/ai-providers/<int:id>', methods=['PUT'])
def update_ai_provider(id):
    """更新AI服务商"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 构建更新语句
        update_fields = []
        values = []
        
        if 'name' in data:
            update_fields.append("name = %s")
            values.append(data['name'])
        if 'provider_type' in data:
            update_fields.append("provider_type = %s")
            values.append(data['provider_type'])
        if 'host' in data:
            update_fields.append("host = %s")
            values.append(data['host'])
        if 'api_key' in data:
            update_fields.append("api_key = %s")
            values.append(data['api_key'])
        
        if not update_fields:
            return jsonify({"error": "No fields to update"}), 400
        
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        values.append(id)
        
        cur.execute(
            f"UPDATE ai_providers SET {', '.join(update_fields)} WHERE id = %s",
            values
        )
        
        if cur.rowcount == 0:
            cur.close()
            conn.close()
            return jsonify({"error": "Provider not found"}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"message": "Provider updated successfully"})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/ai-providers/<int:id>', methods=['DELETE'])
def delete_ai_provider(id):
    """删除AI服务商"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("DELETE FROM ai_providers WHERE id = %s", (id,))
        
        if cur.rowcount == 0:
            cur.close()
            conn.close()
            return jsonify({"error": "Provider not found"}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"message": "Provider deleted successfully"})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500