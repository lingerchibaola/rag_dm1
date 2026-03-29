import time
from rag import RAGService
import config_data as config
import streamlit as st


st.title("Rge助手")
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
        time.sleep(2)
        res = st.session_state["rag"].chain.stream({"input": prompt}, config=config.session_config)
        st.chat_message("assistant").write_stream(res)
        st.session_state["message"].append({"role": "assistant", "content": res})