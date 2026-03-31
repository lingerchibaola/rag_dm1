# config_data.py
import os
from dotenv import load_dotenv

load_dotenv()

# API 配置（从环境变量读取）
dashscope_api_key = os.getenv("DASHSCOPE_API_KEY", "sk-9ed94ef4e7e94168a812998aec056a99")

# 向量数据库配置
persist_directory = "./chroma_db"
collection_name = "rag_collection"
md5_path = "./uploaded_md5.txt"

# 文本分割配置
chunk_size = 500
chunk_overlap = 50
max_number = 1000
separators = ["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]

# 模型配置
embedding_model = "text-embedding-v4"
chat_model = "qwen-turbo"

# RAG 配置
similarity_threshold = 3  # 检索文档数量
system_template = """你是一个友好的AI助手，名叫Rge小助手。请用温暖、可爱的语气回答问题。
如果用户的问题需要参考知识库，请基于提供的上下文信息回答。
如果不知道答案，请诚实地告诉用户，不要编造信息。"""

# Session 配置
session_config = {
    "configurable": {
        "session_id": "default"
    }
}
