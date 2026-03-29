"""
基于Streamlit完成web网页上传服务
"""
import streamlit as st
from knowledge_base import KnowledgeBaseService

# 添加网页标题
st.title("文件上传服务")

uploader_file = st.file_uploader(
    "请上传txt文件",
    type=["txt"],                  # 支持的文件类型
    accept_multiple_files=False,   # 是否允许上传多个文件
)


if "service" is not st.session_state:
    st.session_state["service"] = KnowledgeBaseService()


if uploader_file is not None:
    # 获取上传文件的名称
    file_name = uploader_file.name
    # 类型
    file_type = uploader_file.type
    # 大小
    file_size = uploader_file.size/1024  # 单位KB
    # 获取上传文件的内容
    file_content = uploader_file.read()
    st.subheader(f"文件名称: {file_name}")
    st.write(f"文件类型: {file_type} | 文件大小: {file_size:.2f}KB")
    text = uploader_file.getvalue().decode("utf-8")
    res = st.session_state["service"].upload_by_str(text, file_name)
    st.write(res)
