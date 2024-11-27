from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.document_loaders.word_document import Docx2txtLoader
from langchain_community.embeddings import OpenAIEmbeddings
import os
import logging
#
# import os
#
# class KnowledgeBase:
#     def __init__(self, embedding_model="sentence-transformers/all-mpnet-base-v2"):
#         self.embeddings = OpenAIEmbeddings(model_name=embedding_model)
#         self.vectorstore = None
#
#     def load_documents(self, folder_path):
#         documents = []
#         for file_name in os.listdir(folder_path):
#             file_path = os.path.join(folder_path, file_name)
#             if file_name.endswith(".txt"):
#                 loader = TextLoader(file_path)
#             elif file_name.endswith(".pdf"):
#                 loader = PyPDFLoader(file_path)
#             elif file_name.endswith(".docx"):
#                 loader = Docx2txtLoader(file_path)
#             else:
#                 continue
#             documents.extend(loader.load())
#         return documents
#
#     def build_index(self, folder_path):
#         documents = self.load_documents(folder_path)
#         self.vectorstore = FAISS.from_documents(documents, self.embeddings)



# Установить ключ OpenAI
os.environ["OPENAI_API_KEY"] = "token"

class KnowledgeBase:
    def __init__(self, embedding_model="text-embedding-ada-002"):
        """
        Инициализация базы знаний.
        """
        try:
            self.embeddings = OpenAIEmbeddings(model=embedding_model)
            self.vectorstore = None
        except Exception as e:
            logging.error(f"Ошибка инициализации OpenAIEmbeddings: {e}")
            raise

    def load_documents(self, folder_path):
        """
        Загрузка документов из указанной папки.
        :param folder_path: Путь к папке с файлами.
        :return: Список документов.
        """
        documents = []
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if file_name.endswith(".txt"):
                loader = TextLoader(file_path)
            elif file_name.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
            elif file_name.endswith(".docx"):
                loader = Docx2txtLoader(file_path)
            else:
                continue
            documents.extend(loader.load())
        return documents

    def build_index(self, folder_path):
        """
        Построение индекса из документов.
        :param folder_path: Путь к папке с файлами.
        """
        documents = self.load_documents(folder_path)
        try:
            self.vectorstore = FAISS.from_documents(documents, self.embeddings)
        except Exception as e:
            logging.error(f"Ошибка построения индекса: {e}")
            raise

    def query(self, query_text, top_k=5):
        """
        Поиск по базе знаний.
        :param query_text: Текст запроса.
        :param top_k: Количество возвращаемых результатов.
        :return: Список найденных документов.
        """
        if not self.vectorstore:
            raise ValueError("Индекс не создан. Сначала вызовите build_index().")
        try:
            return self.vectorstore.similarity_search(query_text, top_k)
        except Exception as e:
            logging.error(f"Ошибка выполнения запроса: {e}")
            return []

    def query(self, query_text, top_k=5):
        return self.vectorstore.similarity_search(query_text, top_k)
