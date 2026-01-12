"""
SmartHR RAG System - Phase 2: Retrieval & Generation
Streamlit 應用程式，提供企業規章問答介面。
"""
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import time
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


def stream_text(text, delay=0.02):
    """將文字轉換為生成器，用於打字機效果"""
    words = text.split()
    for i, word in enumerate(words):
        if i == 0:
            yield word
        else:
            yield " " + word
        time.sleep(delay)


def main():
    """主程式：Streamlit 應用介面"""
    st.set_page_config(page_title="SmartHR 企業規章助手", page_icon="🤖", layout="wide")
    
    # 全域 Custom CSS - 修正 Streamlit 預設樣式問題
    st.markdown("""
    <style>
        /* 移除 Streamlit 預設的頂部 padding */
        .main > div {
            padding-top: 2rem;
        }
        
        /* 移除預設的 block-container padding */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }
        
        /* 調整文字段落間距 */
        p {
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
            line-height: 1.6;
        }
        
        /* 調整標題間距 */
        h1 {
            margin-top: 0.5rem;
            margin-bottom: 0.75rem;
        }
        
        h2 {
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
        }
        
        h3 {
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
        }
        
        /* 調整容器間距 */
        .stContainer {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }
        
        /* 調整對話訊息間距 */
        .stChatMessage {
            padding-top: 0.75rem;
            padding-bottom: 0.75rem;
        }
        
        /* 調整按鈕間距 */
        .stButton > button {
            margin-top: 0.25rem;
            margin-bottom: 0.25rem;
        }
        
        /* 調整側邊欄間距 */
        .css-1d391kg {
            padding-top: 1rem;
        }
        
        /* 防止文字跑版 */
        .stMarkdown {
            word-wrap: break-word;
            overflow-wrap: break-word;
        }
        
        /* 調整 expander 間距 */
        .streamlit-expanderHeader {
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
        }
        
        /* 移除多餘的垂直間距 */
        div[data-testid="stVerticalBlock"] > div {
            gap: 0.5rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # 初始化對話歷史和快速查詢狀態
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "quick_query" not in st.session_state:
        st.session_state.quick_query = None
    
    # 側邊欄
    with st.sidebar:
        st.markdown("## 🤖 SmartHR")
        st.divider()
        
        # 對話歷史標題
        st.markdown("### 💬 對話歷史")
        
        # 顯示簡短的對話歷史（僅顯示最近的幾條）
        if st.session_state.messages:
            recent_messages = st.session_state.messages[-5:]  # 只顯示最近5條
            for msg in recent_messages:
                role_icon = "👤" if msg["role"] == "user" else "🤖"
                role_text = "您" if msg["role"] == "user" else "助理"
                content_preview = msg["content"][:50] + "..." if len(msg["content"]) > 50 else msg["content"]
                st.markdown(f"{role_icon} **{role_text}**: {content_preview}")
                st.markdown("---")
        else:
            st.markdown("*尚無對話記錄*")
        
        st.divider()
        
        if st.button("🗑️ 清除對話", type="secondary", use_container_width=True):
            st.session_state.messages = []
            st.session_state.quick_query = None
            st.rerun()
    
    # 初始化元件
    try:
        embeddings = init_embeddings()
        vectorstore = init_vectorstore(embeddings)
        llm = init_llm()
        qa_chain = create_qa_chain(llm, vectorstore)
        system_ready = True
    except Exception as e:
        st.error(f"系統初始化失敗：{str(e)}")
        st.info("請確認已執行 ingest.py 建立向量資料庫，並設定 ANTHROPIC_API_KEY 環境變數。")
        system_ready = False
    
    # 主內容區域
    main_container = st.container()
    
    with main_container:
        # Hero Section - 僅在沒有對話時顯示
        if not st.session_state.messages:
            hero_container = st.container()
            with hero_container:
                # 置中佈局
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col2:
                    # 狀態徽章
                    st.markdown("""
                    <div style="text-align: center; margin-bottom: 1rem;">
                        <span style="display: inline-flex; align-items: center; gap: 0.5rem; 
                                     padding: 0.5rem 1rem; background-color: #E3F2FD; 
                                     color: #1976D2; border-radius: 999px; font-size: 0.875rem; 
                                     font-weight: 500;">
                            <span style="display: inline-block; width: 8px; height: 8px; 
                                         background-color: #1976D2; border-radius: 50%; 
                                         animation: pulse 2s infinite;"></span>
                            AI 助理已就緒
                        </span>
                    </div>
                    <style>
                        @keyframes pulse {
                            0%, 100% { opacity: 1; }
                            50% { opacity: 0.5; }
                        }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    # 主標題
                    st.markdown("""
                    <h1 style="text-align: center; font-size: 3rem; font-weight: bold; 
                               margin-bottom: 1rem; line-height: 1.2;">
                        Hello, Alex!<br>
                        <span style="color: #1976D2;">有什麼我可以幫你的嗎？</span>
                    </h1>
                    """, unsafe_allow_html=True)
                    
                    # 副標題
                    st.markdown("""
                    <p style="text-align: center; font-size: 1.125rem; color: #666; 
                              margin-bottom: 2rem; max-width: 600px; margin-left: auto; 
                              margin-right: auto;">
                        我是您的智慧人資助理，可以回答任何關於公司規章制度的問題
                    </p>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
        
        # 對話區域
        chat_container = st.container()
        with chat_container:
            # 如果有對話歷史，顯示對話
            if st.session_state.messages:
                st.markdown("### 💬 對話")
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.write(message["content"])
                        # 如果有參考來源，顯示在 expander 中
                        if message["role"] == "assistant" and "sources" in message:
                            with st.expander("📚 查看參考來源"):
                                for i, doc in enumerate(message["sources"], 1):
                                    st.markdown(f"**來源 {i}:**")
                                    st.text(doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content)
                                    st.divider()
        
        # 處理快速查詢（在搜尋輸入之前）
        if st.session_state.quick_query and system_ready:
            prompt = st.session_state.quick_query
            st.session_state.quick_query = None
            
            # 顯示使用者訊息
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            # 生成 AI 回答
            with st.chat_message("assistant"):
                with st.spinner("正在查詢中..."):
                    try:
                        result = qa_chain.invoke({"query": prompt})
                        answer = result["result"]
                        sources = result.get("source_documents", [])

                        # 使用打字機效果顯示回答
                        response_placeholder = st.empty()
                        full_response = ""
                        for chunk in stream_text(answer):
                            full_response += chunk
                            response_placeholder.write(full_response + "▌")
                        
                        # 移除游標並顯示完整回答
                        response_placeholder.write(full_response)

                        # 顯示參考來源
                        if sources:
                            with st.expander("📚 查看參考來源"):
                                for i, doc in enumerate(sources, 1):
                                    st.markdown(f"**來源 {i}:**")
                                    st.text(doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content)
                                    st.divider()

                        # 保存到對話歷史
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": full_response,
                            "sources": sources
                        })
                        st.rerun()

                    except Exception as e:
                        error_msg = f"查詢失敗：{str(e)}"
                        st.error(error_msg)
                        st.info("請確認 ANTHROPIC_API_KEY 環境變數已正確設定。")
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": error_msg
                        })
        
        # 搜尋欄位區域
        search_container = st.container()
        with search_container:
            if not st.session_state.messages:
                st.markdown("<br>", unsafe_allow_html=True)
            
            # 搜尋輸入框
            if prompt := st.chat_input("請輸入您的問題，例如：請假需要什麼證明？"):
                # 顯示使用者訊息
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.write(prompt)

                # 生成 AI 回答
                if system_ready:
                    with st.chat_message("assistant"):
                        with st.spinner("正在查詢中..."):
                            try:
                                result = qa_chain.invoke({"query": prompt})
                                answer = result["result"]
                                sources = result.get("source_documents", [])

                                # 使用打字機效果顯示回答
                                response_placeholder = st.empty()
                                full_response = ""
                                for chunk in stream_text(answer):
                                    full_response += chunk
                                    response_placeholder.write(full_response + "▌")
                                
                                # 移除游標並顯示完整回答
                                response_placeholder.write(full_response)

                                # 顯示參考來源
                                if sources:
                                    with st.expander("📚 查看參考來源"):
                                        for i, doc in enumerate(sources, 1):
                                            st.markdown(f"**來源 {i}:**")
                                            st.text(doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content)
                                            st.divider()

                                # 保存到對話歷史
                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": full_response,
                                    "sources": sources
                                })
                                st.rerun()

                            except Exception as e:
                                error_msg = f"查詢失敗：{str(e)}"
                                st.error(error_msg)
                                st.info("請確認 ANTHROPIC_API_KEY 環境變數已正確設定。")
                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": error_msg
                                })
        
        # 快速存取區域 - 僅在沒有對話時顯示
        if not st.session_state.messages:
            st.markdown("<br><br>", unsafe_allow_html=True)
            quick_access_container = st.container()
            with quick_access_container:
                st.markdown("""
                <div style="text-align: center; margin-bottom: 1.5rem;">
                    <h2 style="font-size: 0.875rem; font-weight: 600; color: #666; 
                               text-transform: uppercase; letter-spacing: 0.05em;">
                        快速存取 Quick Access
                    </h2>
                </div>
                """, unsafe_allow_html=True)
                
                # 快速查詢卡片
                col1, col2, col3, col4 = st.columns(4)
                
                quick_queries = [
                    ("📅 請假規定", "請假需要什麼證明？請假的流程是什麼？"),
                    ("💰 報帳流程", "報帳需要哪些文件？報帳的流程是什麼？"),
                    ("🎁 員工福利", "公司提供哪些員工福利？"),
                    ("📋 規章制度", "公司的規章制度有哪些？")
                ]
                
                for i, (icon_title, query) in enumerate(quick_queries):
                    with [col1, col2, col3, col4][i]:
                        if st.button(
                            icon_title,
                            key=f"quick_{i}",
                            use_container_width=True,
                            type="secondary"
                        ):
                            st.session_state.quick_query = query
                            st.rerun()
        
        # Footer
        st.markdown("<br><br>", unsafe_allow_html=True)
        footer_container = st.container()
        with footer_container:
            st.markdown("""
            <div style="text-align: center; padding: 1rem; border-top: 1px solid #e0e0e0; 
                       margin-top: 2rem;">
                <p style="font-size: 0.875rem; color: #666;">
                    © 2026 SmartHR. 由 AI 驅動的企業人資系統。
                </p>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
