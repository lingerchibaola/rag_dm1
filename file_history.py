from langchain_core.messages import message_to_dict, messages_from_dict
from langchain_core.chat_history import BaseChatMessageHistory
import os, json
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser



class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, filename="chat_history.json"):
        self.session_id = session_id
        self.filename = filename
        self.file_path = os.path.join("chat_histories", session_id, filename)
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_messages(self, messages) -> None:
        all_message = list(self.messages)
        if isinstance(messages, list):
            all_message.extend(messages)
        else:
            all_message.append(messages)

        new_message = [message_to_dict(msg) for msg in all_message]

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_message, f, ensure_ascii=False)

    @property
    def messages(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages = json.load(f)
                return messages_from_dict(messages)
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        if os.path.exists(self.file_path):
            os.remove(self.file_path)


model = ChatOllama(
    model="qwen3:1.7b",
    base_url="http://localhost:11434",  # Ollama 默认地址
)

prompt_1 = PromptTemplate.from_template(
    "根据对话历史回答。\n对话历史：{chat_history}\n用户问题：{input}\n请回答："
)

str_parser = StrOutputParser()

chain_1 = prompt_1 | model | str_parser


def get_history(session_id):
    return FileChatMessageHistory(session_id)


chain_2 = RunnableWithMessageHistory(
    chain_1,
    get_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)
