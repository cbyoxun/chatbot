from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建 Flask 应用
app = Flask(__name__)
CORS(app)  # 启用 CORS 支持

# 配置
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB 限制

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 导入路由
from api import docs, qa, config

# 注册蓝图
app.register_blueprint(docs.bp, url_prefix='/api/docs')
app.register_blueprint(qa.bp, url_prefix='/api/qa')
app.register_blueprint(config.bp, url_prefix='/api/config')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)