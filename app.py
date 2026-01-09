"""
SmartHR RAG System - Phase 2: Retrieval & Generation
Streamlit 應用程式，提供企業規章問答介面。
"""

import streamlit as st
from langchain_anthropic import ChatAnthropic
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.chains import RetrievalQA


@st.cache_resource
def init_embeddings():
    """初始化 Embedding 模型"""
    return SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")


@st.cache_resource
def init_vectorstore(_embeddings):
    """初始化向量資料庫"""
    return Chroma(
        persist_directory="./chroma_db",
        embedding_function=_embeddings
    )


@st.cache_resource
def init_llm():
    """初始化 Claude LLM"""
    return ChatAnthropic(
        model="claude-3-haiku-20240307",
        temperature=0
    )


def create_qa_chain(llm, vectorstore):
    """建立 RetrievalQA 鏈"""
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

    return qa_chain


def main():
    """主程式：Streamlit 應用介面"""
    st.set_page_config(page_title="SmartHR 企業規章助手", page_icon="📋")
    st.title("📋 SmartHR 企業規章助手")
    st.markdown("歡迎使用企業規章問答系統，請在下方輸入您的問題。")

    # 初始化元件
    try:
        embeddings = init_embeddings()
        vectorstore = init_vectorstore(embeddings)
        llm = init_llm()
        qa_chain = create_qa_chain(llm, vectorstore)
    except Exception as e:
        st.error(f"系統初始化失敗：{str(e)}")
        st.info("請確認已執行 ingest.py 建立向量資料庫，並設定 ANTHROPIC_API_KEY 環境變數。")
        return

    # 使用者輸入
    question = st.text_input("請輸入您的問題：", placeholder="例如：請假需要什麼證明？")

    if question:
        with st.spinner("正在查詢中..."):
            try:
                result = qa_chain.invoke({"query": question})

                # 顯示回答
                st.subheader("回答")
                st.write(result["result"])

                # 顯示參考來源
                with st.expander("查看參考來源"):
                    for i, doc in enumerate(result["source_documents"], 1):
                        st.markdown(f"**來源 {i}:**")
                        st.text(doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content)
                        st.divider()

            except Exception as e:
                st.error(f"查詢失敗：{str(e)}")
                st.info("請確認 ANTHROPIC_API_KEY 環境變數已正確設定。")


if __name__ == "__main__":
    main()
