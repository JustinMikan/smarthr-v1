# SmartHR Project - 開發進度存檔

## 📅 最後更新時間：Phase 4 完成 (Ready for Phase 5)

## 🎯 專案目標
建立「SmartHR 企業規章智慧問答助手」，使用 RAG 技術回答員工關於請假、報帳等問題。

## 🛠 技術堆疊 (Current Stack)
- **Language**: Python 3.10+
- **Frontend**: Streamlit
- **Orchestration**: LangChain
- **Database**: ChromaDB (Vector Store)
- **Embedding**: sentence-transformers (all-MiniLM-L6-v2)
- **LLM**: Anthropic API (目前降級使用 `claude-3-haiku` 以節省成本並解決權限問題)

## 📂 目前檔案結構與功能
1. **data/**: 存放 `employees_handbook.txt` (測試用規章)。
2. **.claude/project_instructions.md**: 定義 AI 為「資深後端工程師」的角色設定檔。
3. **requirements.txt**: 專案相依套件清單。
4. **ingest.py**: 資料消化腳本 (ETL)。負責讀取 txt -> 切分 (Chunk 500) -> 向量化 -> 存入 ChromaDB。
5. **app.py**: 應用程式主檔。Streamlit 介面，負責接收問題 -> 檢索 ChromaDB -> 呼叫 LLM -> 回答。

## ✅ 已完成項目
- [x] 環境建置 (Git, venv, requirements)
- [x] 技術規格書制定 (`tech_spec.md`)
- [x] AI 角色設定 (Context Setting)
- [x] 資料消化流程 (Ingestion Pipeline) 測試成功
- [x] 應用程式 (Streamlit App) 測試成功 (已驗證可回答問題並附上來源)

## 🚀 下一步 (Next Step)
**Phase 5: Cursor 精修與前端整合**
- 使用 Cursor 編輯器進行 UI 美化 (仿 ChatGPT 風格)。
- 優化 System Prompt，讓回答更具 HR 專業溫暖感。
- 增加「查看原始文件」的側邊欄功能。
