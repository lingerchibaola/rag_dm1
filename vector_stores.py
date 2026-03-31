from langchain_chroma import Chroma
import config_data as config


class VectorStoreService(object):
    """向量数据库服务"""

    def __init__(self, embedding, user_id="default"):
        self.embedding = embedding
        self.user_id = user_id
        # 为每个用户创建独立的集合
        collection_name = f"{config.collection_name}_{user_id}"
        persist_directory = os.path.join(config.persist_directory, user_id)

        os.makedirs(persist_directory, exist_ok=True)

        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self.embedding,
            persist_directory=persist_directory,
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": config.similarity_threshold})

if __name__ == '__main__':
    from langchain_community.embeddings import DashScopeEmbeddings
    embedding = DashScopeEmbeddings(model="text-embedding-v4")
    vector_store = VectorStoreService(embedding).get_retriever()
    res = vector_store.invoke("张三多少岁")
    print(res)
