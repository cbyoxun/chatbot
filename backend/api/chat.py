from flask import Blueprint, request, jsonify
import uuid
import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

bp = Blueprint('chat', __name__)

# 数据库连接函数
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'chat_db'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'password')
    )
    return conn

@bp.route('/<chat_id>', methods=['GET'])
def get_chat(chat_id):
    """获取聊天历史"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # 获取聊天信息
        cur.execute("SELECT * FROM chats WHERE id = %s", (chat_id,))
        chat = cur.fetchone()
        
        if not chat:
            return jsonify({"error": "Chat not found"}), 404
        
        # 获取消息列表
        cur.execute("SELECT * FROM messages WHERE chat_id = %s ORDER BY created_at", (chat_id,))
        messages = cur.fetchall()
        
        # 获取每个消息的文件
        message_with_files = []
        for msg in messages:
            cur.execute("SELECT * FROM files WHERE message_id = %s", (msg['id'],))
            files = cur.fetchall()
            
            # 构建消息格式
            message_data = {
                "id": msg['id'],
                "role": msg['role'],
                "parts": []
            }
            
            # 添加文本内容
            if msg['content']:
                message_data['parts'].append({
                    "type": "text",
                    "text": msg['content']
                })
            
            # 添加文件
            for file in files:
                message_data['parts'].append({
                    "type": "file",
                    "url": f"/uploads/{file['filename']}",
                    "mediaType": file['media_type']
                })
            
            message_with_files.append(message_data)
        
        cur.close()
        conn.close()
        
        return jsonify({
            "id": chat['id'],
            "title": chat['title'] or "New Chat",
            "messages": message_with_files
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/<chat_id>', methods=['POST'])
def send_message(chat_id):
    """发送消息"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 获取请求数据
        data = request.json
        model = data.get('model', 'gpt-3.5-turbo')
        
        # 处理流式请求
        if 'stream' in data and data['stream']:
            return handle_streaming_request(chat_id, data, model)
        
        # 处理非流式请求
        messages = data.get('messages', [])
        
        # 保存用户消息
        user_message_id = str(uuid.uuid4())
        user_content = ''
        for part in messages[0].get('parts', []):
            if part['type'] == 'text':
                user_content = part['text']
        
        cur.execute(
            "INSERT INTO messages (id, chat_id, role, content) VALUES (%s, %s, %s, %s)",
            (user_message_id, chat_id, 'user', user_content)
        )
        
        # 生成AI回复
        ai_message_id = str(uuid.uuid4())
        ai_response = "这是一个AI回复示例。在实际应用中，这里会调用真实的AI模型来生成回复。"
        
        cur.execute(
            "INSERT INTO messages (id, chat_id, role, content) VALUES (%s, %s, %s, %s)",
            (ai_message_id, chat_id, 'assistant', ai_response)
        )
        
        # 更新聊天标题（如果是第一条消息）
        cur.execute("SELECT COUNT(*) FROM messages WHERE chat_id = %s", (chat_id,))
        message_count = cur.fetchone()[0]
        
        if message_count == 2:  # 第一条用户消息和第一条AI回复
            # 用用户消息的前50个字符作为标题
            title = user_content[:50] + ('...' if len(user_content) > 50 else '')
            cur.execute(
                "UPDATE chats SET title = %s, updated_at = NOW() WHERE id = %s",
                (title, chat_id)
            )
        else:
            cur.execute("UPDATE chats SET updated_at = NOW() WHERE id = %s", (chat_id,))
        
        conn.commit()
        cur.close()
        conn.close()
        
        # 构建响应
        response = {
            "id": ai_message_id,
            "role": "assistant",
            "parts": [
                {
                    "type": "text",
                    "text": ai_response
                }
            ]
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def handle_streaming_request(chat_id, data, model):
    """处理流式请求"""
    # 这里应该实现流式响应逻辑
    # 由于是示例，返回一个简单的非流式响应
    return jsonify({"error": "Streaming not implemented yet"}), 501

@bp.route('/', methods=['POST'])
def create_chat():
    """创建新聊天"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        chat_id = str(uuid.uuid4())
        
        cur.execute(
            "INSERT INTO chats (id, title) VALUES (%s, %s)",
            (chat_id, "New Chat")
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"id": chat_id, "title": "New Chat"}), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/', methods=['GET'])
def list_chats():
    """获取聊天列表"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("SELECT id, title, created_at FROM chats ORDER BY updated_at DESC")
        chats = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return jsonify(chats)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
