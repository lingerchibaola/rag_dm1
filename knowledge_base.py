"""
知识库
"""
import os
import config_data as config
import hashlib
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
    def __init__(self):
        # 若文件不存在则创建
        os.makedirs(config.persist_directory, exist_ok=True)
        self.chroma = Chroma(
            collection_name=config.collection_name,   # 数据库表名
            embedding_function=DashScopeEmbeddings(
                model="text-embedding-v4",
                dashscope_api_key="sk-9ed94ef4e7e94168a812998aec056a99"
            ),
            persist_directory=config.persist_directory  # 数据库本地路径
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,   # 分块大小
            chunk_overlap=config.chunk_overlap,  # 允许的重叠数量
            separators=config.separators,  # 分割符
            length_function=len  # 使用python自带的len函数统计长度
        )

    def upload_by_str(self,data: str, file_name):
        """上传字符串,向量化，存入向量数据库中"""
        md5_str = get_string_md5(data)
        if check_md5(md5_str):
            print("文件已处理")
            return "文件已上传"
        if len(data) > config.max_number:
            text_splits = self.spliter.split_text(data)
        else:
            text_splits = [data]
        metadata = {
            "source": file_name, # 源文件名
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator":"绫儿",

        }
        self.chroma.add_texts(
            text_splits,
            metadata = [ metadata for _ in text_splits],
        )
        save_md5(md5_str)
        print("上传成功")
        return "上传成功"

# 测试
if __name__ == '__main__':
    kbs = KnowledgeBaseService()
    kbs.upload_by_str("今天天气不错", "test.txt")





