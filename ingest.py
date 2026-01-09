"""
SmartHR RAG System - Phase 1: Data Ingestion
從 data/ 資料夾讀取文件，切分文字，生成向量，存入 ChromaDB。
"""

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma


def load_documents(data_dir: str = "./data"):
    """載入 data/ 資料夾中的所有 .txt 檔案"""
    loader = DirectoryLoader(
        data_dir,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    documents = loader.load()

    if not documents:
        raise FileNotFoundError(f"在 {data_dir} 資料夾中找不到任何 .txt 檔案")

    return documents


def split_documents(documents, chunk_size: int = 500, chunk_overlap: int = 50):
    """將文件切分成較小的文字區塊"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    return chunks


def create_vector_store(chunks, persist_directory: str = "./chroma_db"):
    """建立向量資料庫並儲存"""
    embeddings = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )

    return vectorstore


def main():
    """主程式：執行完整的資料消化流程"""
    print("開始資料消化流程...")

    # Step 1: 載入文件
    print("步驟 1: 載入文件...")
    documents = load_documents()
    print(f"  - 載入了 {len(documents)} 個文件")

    # Step 2: 切分文字
    print("步驟 2: 切分文字...")
    chunks = split_documents(documents)
    print(f"  - 切分成 {len(chunks)} 個區塊")

    # Step 3 & 4: 向量化並存入 ChromaDB
    print("步驟 3: 向量化並存入 ChromaDB...")
    vectorstore = create_vector_store(chunks)

    print(f"\n成功存入 {len(chunks)} 筆資料")
    print("向量資料庫已儲存至 ./chroma_db")


if __name__ == "__main__":
    main()
