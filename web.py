import time
from rag import RAGService
from knowledge_base import KnowledgeBaseService
import config_data as config
import streamlit as st
import base64
from pathlib import Path
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title=" 清梦的Rge小助手",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)


def set_custom_background():
    """设置自定义背景"""

    # 默认背景图片路径
    default_bg = "bjt.jpg"  # 放在项目根目录

    # 检查背景设置（使用session_state存储用户偏好）
    if "bg_mode" not in st.session_state:
        st.session_state.bg_mode = "default"

    # 侧边栏背景设置
    with st.sidebar:
        with st.expander("🎨 界面美化设置", expanded=False):
            st.markdown("#### 背景设置")

            bg_choice = st.radio(
                "选择背景",
                ["默认图片", "默认渐变", "自定义图片", "纯色背景"],
                index=0,  # 改为默认图片
                horizontal=True
            )

            # 默认图片背景
            if bg_choice == "默认图片":
                # 检查默认图片是否存在
                if Path(default_bg).exists():
                    # 读取并编码默认图片
                    with open(default_bg, "rb") as f:
                        img_data = base64.b64encode(f.read()).decode()

                    # 获取图片格式
                    img_ext = Path(default_bg).suffix.lower()
                    if img_ext in ['.jpg', '.jpeg']:
                        img_type = "jpeg"
                    elif img_ext == '.png':
                        img_type = "png"
                    else:
                        img_type = "jpeg"

                    # 透明度调节
                    opacity = st.slider("遮罩透明度", 0.2, 1.0, 0.2, 0.05, key="default_opacity")
                    blur = st.slider("背景模糊度", 0, 20, 0, key="default_blur")

                    # 应用背景
                    st.markdown(
                        f"""
                        <style>
                        .stApp {{
                            background-image: url(data:image/{img_type};base64,{img_data});
                            background-size: cover;
                            background-position: center;
                            background-attachment: fixed;
                            background-repeat: no-repeat;
                        }}

                        .stApp::before {{
                            content: "";
                            position: fixed;
                            top: 0;
                            left: 0;
                            width: 100%;
                            height: 100%;
                            background-color: rgba(255, 255, 255, {opacity});
                            backdrop-filter: blur({blur}px);
                            z-index: 0;
                        }}

                        .main > div {{
                            position: relative;
                            z-index: 1;
                        }}

                        .stChatMessage {{
                            background-color: rgba(255, 255, 255, 0.92) !important;
                            backdrop-filter: blur(5px);
                        }}

                        [data-testid="stSidebar"] {{
                            background-color: rgba(255, 255, 255, 0.88) !important;
                            backdrop-filter: blur(10px);
                        }}
                        </style>
                        """,
                        unsafe_allow_html=True
                    )
                    st.success("✨ 默认背景已应用！")
                else:
                    st.warning(f"默认图片 '{default_bg}' 不存在，请检查文件路径")
                    # 降级到渐变背景
                    st.markdown(
                        """
                        <style>
                        .stApp {
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        }

                        .stChatMessage {
                            background-color: rgba(255, 255, 255, 0.95) !important;
                        }

                        [data-testid="stSidebar"] {
                            background-color: rgba(255, 255, 255, 0.9) !important;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )
                return

            # 自定义图片背景
            elif bg_choice == "自定义图片":
                uploaded_bg = st.file_uploader(
                    "上传背景图片 (JPG/PNG)",
                    type=["jpg", "jpeg", "png"],
                    key="bg_upload"
                )

                if uploaded_bg:
                    # 临时保存
                    img_data = base64.b64encode(uploaded_bg.read()).decode()
                    img_type = uploaded_bg.type.split('/')[-1]

                    # 透明度调节
                    opacity = st.slider("遮罩透明度", 0.2, 1.0, 0.2, 0.05, key="custom_opacity")
                    blur = st.slider("背景模糊度", 0, 20, 0, key="custom_blur")

                    # 应用背景
                    st.markdown(
                        f"""
                        <style>
                        .stApp {{
                            background-image: url(data:image/{img_type};base64,{img_data});
                            background-size: cover;
                            background-position: center;
                            background-attachment: fixed;
                            background-repeat: no-repeat;
                        }}

                        .stApp::before {{
                            content: "";
                            position: fixed;
                            top: 0;
                            left: 0;
                            width: 100%;
                            height: 100%;
                            background-color: rgba(255, 255, 255, {opacity});
                            backdrop-filter: blur({blur}px);
                            z-index: 0;
                        }}

                        .main > div {{
                            position: relative;
                            z-index: 1;
                        }}

                        .stChatMessage {{
                            background-color: rgba(255, 255, 255, 0.92) !important;
                            backdrop-filter: blur(5px);
                        }}

                        [data-testid="stSidebar"] {{
                            background-color: rgba(255, 255, 255, 0.88) !important;
                            backdrop-filter: blur(10px);
                        }}
                        </style>
                        """,
                        unsafe_allow_html=True
                    )
                    st.success("✨ 背景已更新！")
                    return
                else:
                    # 如果没有上传图片，保持当前设置
                    st.info("请上传图片文件")

            # 纯色背景
            elif bg_choice == "纯色背景":
                bg_color = st.color_picker("选择背景颜色", "#f8f9fa", key="bg_color")
                st.markdown(
                    f"""
                    <style>
                    .stApp {{
                        background-color: {bg_color};
                    }}

                    .stApp::before {{
                        display: none;
                    }}

                    .stChatMessage {{
                        background-color: rgba(255, 255, 255, 0.95) !important;
                    }}

                    [data-testid="stSidebar"] {{
                        background-color: rgba(255, 255, 255, 0.9) !important;
                    }}
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                return

            # 默认渐变背景
            elif bg_choice == "默认渐变":
                st.markdown(
                    """
                    <style>
                    .stApp {
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    }

                    .stApp::before {
                        display: none;
                    }

                    .stChatMessage {
                        background-color: rgba(255, 255, 255, 0.95) !important;
                    }

                    [data-testid="stSidebar"] {
                        background-color: rgba(255, 255, 255, 0.9) !important;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                return


# 在页面加载时自动应用默认背景
def init_default_background():
    """初始化默认背景（在页面加载时调用）"""
    default_bg = "bjt.jpg"

    if Path(default_bg).exists():
        with open(default_bg, "rb") as f:
            img_data = base64.b64encode(f.read()).decode()

        img_ext = Path(default_bg).suffix.lower()
        if img_ext in ['.jpg', '.jpeg']:
            img_type = "jpeg"
        elif img_ext == '.png':
            img_type = "png"
        else:
            img_type = "jpeg"

        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/{img_type};base64,{img_data});
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                background-repeat: no-repeat;
            }}

            .stApp::before {{
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(255, 255, 255, 0.7);
                backdrop-filter: blur(10px);
                z-index: 0;
            }}

            .main > div {{
                position: relative;
                z-index: 1;
            }}

            .stChatMessage {{
                background-color: rgba(255, 255, 255, 0.92) !important;
                backdrop-filter: blur(5px);
            }}

            [data-testid="stSidebar"] {{
                background-color: rgba(255, 255, 255, 0.88) !important;
                backdrop-filter: blur(10px);
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        # 如果默认图片不存在，使用渐变背景
        st.markdown(
            """
            <style>
            .stApp {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }

            .stChatMessage {
                background-color: rgba(255, 255, 255, 0.95) !important;
            }

            [data-testid="stSidebar"] {
                background-color: rgba(255, 255, 255, 0.9) !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )



# 在你的主程序中调用
set_custom_background()

# 自定义CSS - 添加可爱样式
st.markdown("""
<style>
    /* 可爱字体和颜色 */
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Quicksand', sans-serif;
    }

    /* 标题样式 */
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        animation: fadeIn 1s ease-in;
    }

    /* 动画效果 */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    /* 聊天消息气泡样式 */
    .stChatMessage {
        border-radius: 20px !important;
        animation: fadeIn 0.5s ease-in;
    }

    /* 用户消息样式 */
    [data-testid="stChatMessage"]:has(.user) {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }

    /* 助手消息样式 */
    [data-testid="stChatMessage"]:has(.assistant) {
        background: #f0f0f0 !important;
        border: 2px solid #e0e0e0 !important;
    }

    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fff5f5 0%, #ffe8e8 100%);
        border-radius: 20px 0 0 20px;
    }

    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: bold;
        transition: transform 0.3s, box-shadow 0.3s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }

    /* 文件上传区域样式 */
    [data-testid="stFileUploader"] {
        background: white;
        border-radius: 15px;
        padding: 20px;
        border: 2px dashed #667eea;
    }

    /* 成功消息样式 */
    .stAlert {
        border-radius: 15px;
        animation: bounce 0.5s ease;
    }

    /* 自定义滚动条 */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 10px;
    }

    /* 可爱的小装饰 */
    .cute-decoration {
        text-align: center;
        font-size: 0.8em;
        color: #999;
        margin-top: 20px;
    }

    /* 加载动画 */
    .custom-spinner {
        text-align: center;
        padding: 20px;
    }

    /* 聊天输入框样式 */
    [data-testid="stChatInput"] textarea {
        border-radius: 25px !important;
        border: 2px solid #667eea !important;
        padding: 10px 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# 可爱的标题区域
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div class="main-title">
         Rge小助手 
    </div>
    """, unsafe_allow_html=True)
    st.caption("✨ 你的专属AI小伙伴，随时为你解答问题 ✨")

st.divider()

# 初始化 session state
if "rag" not in st.session_state:
    with st.spinner(" 正在唤醒小助手..."):
        st.session_state["rag"] = RAGService()
if "message" not in st.session_state:
    st.session_state["message"] = [
        {"role": "assistant",
         "content": " 欢迎来到Rge小助手！\n\n我是你的专属AI小伙伴，可以帮你：\n 回答各种问题\n 提供创意建议\n 分析上传的文件\n\n有什么我可以帮你的吗？上传文件请点击左上角“>>”符号"}
    ]
if "kb_service" not in st.session_state:
    st.session_state["kb_service"] = KnowledgeBaseService()

# 侧边栏 - 可爱风格
with st.sidebar:
    # 可爱的头像区域
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <div style="font-size: 4em;"></div>
        <h3 style="color: #667eea;">Rge小助手</h3>
        <p style="color: #999;"> 你的贴心小伙伴</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # 文件上传区域
    st.markdown("### 📁 知识库管理")
    st.markdown("💡 **小贴士：** 上传文件后，我能更好地帮你解答相关问题哦~")

    uploader_file = st.file_uploader(
        "📄 点击或拖拽上传TXT文件",
        type=["txt"],
        accept_multiple_files=False,
        help="支持TXT格式文件，文件大小不限"
    )

    if uploader_file is not None:
        file_name = uploader_file.name
        file_type = uploader_file.type
        file_size = uploader_file.size / 1024  # 单位KB

        # 可爱文件卡片
        st.markdown(f"""
        <div style="background: white; border-radius: 15px; padding: 15px; margin: 10px 0;">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 2em;">📄</span>
                <div style="margin-left: 10px;">
                    <strong>{file_name}</strong><br>
                    <small>📏 大小: {file_size:.2f} KB | 📝 类型: {file_type}</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 添加上传按钮
        if st.button("✨ 确认上传", type="primary", use_container_width=True):
            with st.spinner(f"📤 正在上传 {file_name}..."):
                try:
                    text = uploader_file.getvalue().decode("utf-8")
                    res = st.session_state["kb_service"].upload_by_str(text, file_name)
                    st.success(f"🎉 {res}")
                    st.balloons()  # 添加庆祝动画
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"😢 上传失败: {str(e)}")

    st.divider()

    # 统计信息
    st.markdown("### 📊 今日统计")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💬 对话次数", len(st.session_state["message"]) // 2)
    with col2:
        st.metric("📚 知识库", "待统计")

    st.divider()

    # 功能按钮区域
    st.markdown("### 🎮 快捷操作")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ 清空对话", use_container_width=True):
            st.session_state["message"] = [
                {"role": "assistant", "content": "✨ 对话已清空！有什么新问题想问我的吗？😊"}
            ]
            st.success("对话已清空~")
            st.rerun()

    with col2:
        if st.button("💡 随机提示", use_container_width=True):
            tips = [
                "💡 你可以上传TXT文件让我学习！",
                "💡 试试问我一些有趣的问题~",
                "💡 我能帮你做很多事情哦！",
                "💡 记得多和我聊天，我会越来越懂你~"
            ]
            import random

            st.info(random.choice(tips))

    st.divider()
    st.caption(" 由 Rge小助手 提供支持 | 随时为你服务")

# 主聊天界面 - 美化消息显示
for idx, message in enumerate(st.session_state["message"]):
    with st.chat_message(message["role"]):
        # 添加可爱的emoji到消息开头
        if message["role"] == "assistant":
            st.markdown(f" {message['content']}")
        else:
            st.markdown(f" {message['content']}")

# 聊天输入区域
prompt = st.chat_input("💭 在这里输入你的问题...")

# 处理用户输入
if prompt:
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(f"👤 {prompt}")
    st.session_state["message"].append({"role": "user", "content": prompt})

    # 显示助手消息（带动画效果）
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        # 显示思考动画
        with st.spinner("🤔 小助手正在思考中..."):
            try:
                # 获取流式生成器
                res = st.session_state["rag"].chain.stream(
                    {"input": prompt},
                    config=config.session_config
                )

                # 流式输出
                response_content = ""
                for chunk in res:
                    response_content += chunk
                    # 实时显示带光标的文本
                    message_placeholder.markdown(f"🤗 {response_content}▌")

                # 最终显示
                message_placeholder.markdown(f"🤗 {response_content}")

                # 存入历史记录
                st.session_state["message"].append(
                    {"role": "assistant", "content": response_content}
                )

            except Exception as e:
                error_msg = f" 哎呀，出了点小问题：{str(e)}\n\n请稍后再试吧~"
                message_placeholder.markdown(f" {error_msg}")
                st.session_state["message"].append(
                    {"role": "assistant", "content": error_msg}
                )

# 底部可爱装饰
st.markdown("""
<div class="cute-decoration">
    <p> 用心回答每一个问题 |  你的专属AI小伙伴</p>
    <p style="font-size: 0.7em;"> 小助手会努力给你最好的答案 </p>
</div>
""", unsafe_allow_html=True)

# 添加自动滚动到底部的JavaScript
st.markdown("""
<script>
    // 自动滚动到底部
    function scrollToBottom() {
        const elements = document.querySelectorAll('.stChatMessage');
        if (elements.length > 0) {
            elements[elements.length - 1].scrollIntoView({ behavior: 'smooth' });
        }
    }

    // 监听DOM变化
    const observer = new MutationObserver(scrollToBottom);
    observer.observe(document.body, { childList: true, subtree: true });
</script>
""", unsafe_allow_html=True)
