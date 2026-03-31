"""
知识库
"""
import os
import config_data as config
import hashlib
import streamlit as st
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

def check_md5(md5_str):
    """
    检查传入的md5字符串是否被处理了
    """
    if not os.path.exists(config.md5_path):
        print("文件不存在")
        open(config.md5_path, "w", encoding="utf-8").close()
        return False
    else:
        with open(config.md5_path, "r", encoding="utf-8") as f:
            print("文件已存在")
            md5_list = f.readlines()  # 读取文件所有行
            for md5 in md5_list:
                if md5_str == md5.strip():
                    return True
            else:
                return False



def save_md5(md5_str):
    """保存到文件内"""
    with open(config.md5_path, "a", encoding="utf-8") as f:
        f.write(md5_str+'\n')


def get_string_md5(input_str):
    """将传入的字符串转为md5字符串"""
    str_bytes = input_str.encode(encoding="utf-8") # 将字符串转为bytes字节数组
    md5_obj = hashlib.md5()                       # 创建md5对象
    md5_obj.update(str_bytes)                     # 更新md5对象
    return md5_obj.hexdigest()


class KnowledgeBaseService(object):
    """知识库服务"""

    def __init__(self, user_id=None):
        # 若文件不存在则创建
        if user_id:
            self.user_id = user_id
            self.user_persist_dir = os.path.join(config.persist_directory, user_id)
            self.user_md5_path = config.md5_path.replace('.txt', f'_{user_id}.txt')
        else:
            self.user_id = "default"
            self.user_persist_dir = config.persist_directory
            self.user_md5_path = config.md5_path

        # 创建用户专属目录
        os.makedirs(self.user_persist_dir, exist_ok=True)

        # 修复：使用用户专属路径
        self.chroma = Chroma(
            collection_name=f"{config.collection_name}_{self.user_id}",  # 用户专属集合
            embedding_function=DashScopeEmbeddings(
                model="text-embedding-v4",
                dashscope_api_key=config.dashscope_api_key  # 从配置读取
            ),
            persist_directory=self.user_persist_dir  # 修复：使用用户路径
        )

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len
        )

    def check_md5(self, md5_str):
        """检查md5（使用用户专属文件）"""
        if not os.path.exists(self.user_md5_path):
            open(self.user_md5_path, "w", encoding="utf-8").close()
            return False
        else:
            with open(self.user_md5_path, "r", encoding="utf-8") as f:
                md5_list = f.readlines()
                for md5 in md5_list:
                    if md5_str == md5.strip():
                        return True
                return False

    def save_md5(self, md5_str):
        """保存md5（使用用户专属文件）"""
        with open(self.user_md5_path, "a", encoding="utf-8") as f:
            f.write(md5_str + '\n')

    def upload_by_str(self, data: str, file_name):
        """上传字符串,向量化，存入向量数据库中"""
        md5_str = get_string_md5(data)
        if self.check_md5(md5_str):
            print(f"开始上传文件: {file_name}")
            print(f"文件内容长度: {len(data)} 字符")
            return "文件已上传"

        if len(data) > config.max_number:
            text_splits = self.spliter.split_text(data)
        else:
            text_splits = [data]

        metadata = {
            "source": file_name,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": st.session_state.get("user_name", "匿名用户")  # 从 session 获取用户名
        }

        self.chroma.add_texts(
            text_splits,
            metadata=[metadata for _ in text_splits],
        )
        self.save_md5(md5_str)  # 修复：使用实例方法
        return "上传成功"

# 测试
if __name__ == '__main__':
    kbs = KnowledgeBaseService()
    kbs.upload_by_str("今天天气不错", "test.txt")

