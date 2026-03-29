from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda

from file_history import get_history
from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models import ChatTongyi
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


class RAGService(object):
    """RAG服务"""

    def __init__(self):
        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(
                model=config.embedding_model,
                dashscope_api_key=config.dashscope_api_key
            )
        )
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", config.system_template),
            ("system", "历史记录如下"),
            MessagesPlaceholder(variable_name="history"),
            ("user", "请回答用户提问:{input}")
        ])
        # 改用千问 API
        self.chat_model = ChatTongyi(
            model=config.chat_model,
            dashscope_api_key=config.dashscope_api_key,
        )
        self.chain = self.__get_chain()

    def __get_chain(self):
        """获取最终的执行链"""
        retriever = self.vector_service.get_retriever()

        def format_document(docs):
            if not docs:
                return "没有相关参考资料"
            result_str = ""
            for doc in docs:
                result_str += f"文档片段:\n{doc.page_content}\n文档来源:{doc.metadata}\n"
            return result_str

        def temp1(value):
            return value["input"]

        def temp2(value):
            ...

        chain = (
                {
                    "input": RunnablePassthrough(),
                    "context": RunnableLambda(temp1) | retriever | format_document,
                    "history": lambda x: x.get("history", []),
                } | self.prompt_template | self.chat_model | StrOutputParser()
        )
        # 增加历史记忆
        chain_2 = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )
        return chain_2


if __name__ == "__main__":
    session_config = {
        "configurable": {
            "session_id": "1"
        }
    }
    rag = RAGService()
    res = rag.chain.invoke({"input": "小王多少岁"}, config=session_config)
    print(res)