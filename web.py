import time
from rag import RAGService
import config_data as config
import streamlit as st


st.title("清梦的Rge助手")
st.divider()  # 分割线

if "rag" not in st.session_state:
    st.session_state["rag"] = RAGService()
if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "assistant", "content": "欢迎来到Rge助手"}]

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])


prompt = st.chat_input("请输入问题")
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    with st.spinner("思考中..."):
        # 1. 获取流式生成器
        res = st.session_state["rag"].chain.stream({"input": prompt}, config=config.session_config)
        
        # 2. 显示流式输出，并拼接完整内容
        # 创建一个空的容器来显示文字
        full_response = st.chat_message("assistant").empty()
        response_content = ""
        
        # 遍历生成器，一边显示一边拼接
        for chunk in res:
            response_content += chunk
            full_response.markdown(response_content + "▌") # 加个光标效果
            
        # 循环结束后，去掉光标，显示最终结果
        full_response.markdown(response_content)
        
        # 3. 存入历史记录（现在存的是字符串，不是生成器了）
        st.session_state["message"].append({"role": "assistant", "content": response_content})
