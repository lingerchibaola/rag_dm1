from langchain_chroma import Chroma
import config_data as config


class VectorStoreService(object):
    """向量数据库服务"""
    def __init__(self,embedding):
        """

        :param embedding: 嵌入模型的传入
        """
        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name=config.collection_name,   # 集合名称
            embedding_function=self.embedding,   # 嵌入模型
            persist_directory=config.persist_directory,   # 数据库路径
        )

    def get_retriever(self):
        """获取向量数据库的检索器"""
        return self.vector_store.as_retriever(search_kwargs={"k": config.similarity_threshold})

if __name__ == '__main__':
    from langchain_community.embeddings import DashScopeEmbeddings
    embedding = DashScopeEmbeddings(model="text-embedding-v4")
    vector_store = VectorStoreService(embedding).get_retriever()
    res = vector_store.invoke("张三多少岁")
    print(res)