md5_path = "./md5.text"

# Chroma
collection_name = "Rag"
persist_directory = "./chroma_db"

# spliter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", " ", "","，", "。", "？", "！", "；", "：", "、", "（", "）", "《", "》", "、", "【", "】"]
max_number = 1000     # 超过才会分割

#
similarity_threshold = 1     # 返回匹配的文档数量
embedding_model = "text-embedding-v4"
chat_model = "tongyi-xiaomi-analysis-pro"

system_template = """
你是一个知识库问答助手，请根据用户输入的文本，从数据库中查询最相关的内容，并返回给用户。
参考资料：{context}
"""

session_config = {
        "configurable": {
            "session_id": "1"
        }
    }

# config_data.py
dashscope_api_key = "sk-9ed94ef4e7e94168a812998aec056a99"

