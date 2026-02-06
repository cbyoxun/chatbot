-- 初始化数据库表结构
-- 可以根据实际需求修改此文件

-- 示例：创建文档表
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(500) NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建问答记录表
CREATE TABLE IF NOT EXISTS qa_records (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建配置表
CREATE TABLE IF NOT EXISTS config (
    id SERIAL PRIMARY KEY,
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建AI服务商表
CREATE TABLE IF NOT EXISTS ai_providers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    provider_type VARCHAR(50) NOT NULL,
    host VARCHAR(500) NOT NULL,
    api_key TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建聊天会话表
CREATE TABLE IF NOT EXISTS chats (
    id VARCHAR(36) PRIMARY KEY,
    title TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建消息表
CREATE TABLE IF NOT EXISTS messages (
    id VARCHAR(36) PRIMARY KEY,
    chat_id VARCHAR(36) REFERENCES chats(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建文件表
CREATE TABLE IF NOT EXISTS files (
    id VARCHAR(36) PRIMARY KEY,
    message_id VARCHAR(36) REFERENCES messages(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(500) NOT NULL,
    media_type VARCHAR(100) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 插入默认配置
INSERT INTO config (config_key, config_value) VALUES 
('max_upload_size', '16777216'),
('allowed_file_types', 'pdf,doc,docx,txt,md')
ON CONFLICT (config_key) DO UPDATE SET config_value = EXCLUDED.config_value;

-- 插入默认AI服务商
INSERT INTO ai_providers (name, provider_type, host, api_key) VALUES 
('OpenAI', 'openai', 'https://api.openai.com/v1', '')
ON CONFLICT DO NOTHING;