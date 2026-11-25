# 紫楓出版社（Purple Maple Press）書本架構、AI 工程專書與地端產文流水線技術設計書

- **版本**：v1.1
- **狀態**：Goldfish-Resolved（已全數吸收 4 項 BLOCKER、6 項 MAJOR、7 項 MINOR 審查修訂）
- **所屬專案**：`tbpfs/learning`（`https://learn.ai-purplemaple.com/`，GitHub Pages 靜態託管）
- **關聯文件**：`Python教學站簡中與英文多語SEO擴張技術設計書.md`（v1.1）、`章節微回饋與私密提問箱設計書.md`

---

## 0. EGM Goldfish 審查決議摘要（v1.0 → v1.1）
- **B1（單一 SSOT ＋ 三語原子出版閘門）**：移除 `book.json` 內重複的 `published_locales` 欄位，以 `chapters/<locale>/chXX.json` 的 `status == "published"` 為唯一 SSOT；單章必須同時滿足 `zh-TW`、`zh-CN`、`en` 三語皆為 `"published"` 才共同輸出公開 HTML、`sitemap.xml`、`hreflang` 與 `llms*.txt`（單語先驗收完先標 `"reviewed"`），徹底杜絕單語先發產生 404 `hreflang` 與死連切換鈕。
- **B2（既有測試與三語隱私聲明完整對齊）**：同步更新三語 `privacy_body_html` 改述僅傳送匿名幫助度評分（`#fbBox`），移除過時「私密提問」字樣與死 JS（`/api/v1/learn-question`、`#askForm`、`.fb-ask`）；鎖定總館首頁既有 `Course` JSON-LD、`twitter:image` 與禁用 `.chapter-badge` 契約；更新 `test_examples.py` 驗證 30 頁 `sitemap.xml`、32 筆 `pages.yml` IndexNow，並新增 `set(sitemap_locs) | {llms.txt, llms-full.txt} == set(pages_yml_urlList)` 一致性不變量。
- **B3（`#fbBox` 命名空間防碰撞）**：Book 1 章節之 `localStorage` 鍵與 `data-chapter` 使用獨立命名空間前綴（如 `ai-engineering-ch01`），並依主站 `/api/v1/learn-feedback` 實際白名單規則決定是否送出或於主站白名單外採本機即時感謝回饋（避免 HTTP 400 錯誤）。
- **B4（共用 QA 規則與中文 FB 社團雙語覆蓋）**：統一常數 `FB_GROUP_URL = "https://www.facebook.com/share/g/19jsJ8crsC/"`，`zh-TW` 與 `zh-CN` 首頁 Hero 與章末提問卡皆導向該社團（`UI_ZH_CN` 補齊 `cta_fb_group` 與純簡中模板文案）；將擴充含 AI 工程與社團詞彙之 `ZH_CN_BANNED_TERMS`、`ZH_CN_BANNED_TRAD_CHARS`、`validate_svg_safe()`、`count_prose()` 抽至 `book_models.py` 由 `book_forge.py` 與 `test_examples.py` 單一共享。
- **M1–M6 & Minor 1–7**：目錄頁強制帶尾斜線且使用根絕對內部連結、`og:image`/`twitter:image`/JSON-LD `image` 使用完整 `https://learn.ai-purplemaple.com/assets/...`、`build_site(out_dir)` 複製 `assets/`；側欄 TOC 與上下章 Pager 對未出版章節嚴禁輸出 `<a>` 並採三語在地化（`撰寫中` / `撰写中` / `Coming Soon`）；SVG 封鎖 `<script`/`<foreignObject`/`on*=`/`javascript:`/`<image`/`<use`/`<!ENTITY` 並限 `< 80` 節點；互動測驗採預渲染 `<fieldset>`＋零 `innerHTML`；`ai_ch08_local_llm_client.py` 內建離線模擬傳輸不打網路；`book_forge.py` 鎖定 `http/https`、逾時、原子寫入且無 `--force` 不覆寫已出版檔；書封固定 `width="640" height="857"` 對應實際 WebP 尺寸，側欄共用單一 DOM 防膨脹。

---

## 1. 背景、定位與範圍（Scope & Non-Goals）

### 1.1 產品願景（紫楓版歐萊禮）
將 `learn.ai-purplemaple.com` 從單一系列的 7 章演算法入門講義，升級為具備出版級書本結構的 **「紫楓出版社（Purple Maple Press）」技術專書平台**：
- **Book 1（創刊旗艦專書，Phase 1 上架 Ch.01 黃金示範章，Ch.02–Ch.10 備妥真代碼、大綱與地端產文管線）**：**《AI 工程師實戰聖經：從 LLM 底層、生產級 RAG、MCP 智能體到地端部署與規格驅動開發》**（4 篇 10 章，對標 2025–2026 YouTube 最爆款 AI 課程與 iThome 鐵人賽冠軍主題）。
- **Book 2（既有經典，URL 100% 零搬家零掉權）**：**《Python 3.12 資料結構與演算法精解》**（完整保留既有的 `/ch01.html`..`/ch07.html`、`/zh-cn/ch01..07.html`、`/en/ch01..07.html` 全部 21 頁章節 URL）。
- **白瀬アイリ（艾莉）學者／工程師典藏書封**：兩本專書各配一張 AI 繪製並壓縮至 `< 100 KB` 的 WebP 典藏書封（嚴守異色瞳鐵則：觀看者畫面左側＝緋紅 `#fb7185`、右側＝蒼藍 `#38bdf8`）。
- **中文語系集中 FB 社團導流**：依用戶決策，繁體中文（`zh-TW`）與簡體中文（`zh-CN`）章節頁全面以 **FB 社團集中提問卡片（`https://www.facebook.com/share/g/19jsJ8crsC/`）取代原私密提問箱（`#askForm`）**，保留極簡 👍/👎 幫助度評分（`#fbBox`），並附「一鍵複製帶書名／章號之發問模板」按鈕，將中文讀者發問集中導向 FB 社團雙向聚流；英文版（`en`）則導向 GitHub Discussions／Issues（零漢字）。
- **地端 LM Studio × Antigravity 三段式出版流水線**：建置 `scripts/book_forge.py` 對接本機 LM Studio（`127.0.0.1:1234`），先產出繁中初稿 ➔ Antigravity 總編驗收並標記 `status: "published"` ➔ 地端兩段式翻譯簡中／英文＋機械質檢過關才公開輸出，徹底杜絕未審核草稿或低質 AI 內容混入 `sitemap.xml` 與 `hreflang`。

### 1.2 非目標（Non-Goals）
- **不搬移任何既有 Book 2 網址**：既有 `/ch01.html`..`/ch07.html`（及 `/zh-cn/`、`/en/` 對應頁）路徑 100% 不變。
- **不導入外部第三方 Python 套件或前端框架**：SSG、Book 1 全部 10 支 Python 範例與 `scripts/book_forge.py` 全數以 **Python 3.12 標準庫**撰寫（含 `urllib.request` 呼叫本機 LM Studio），CI 零 `pip install`。
- **不上線空章節或未驗收草稿頁**：`status != "published"` 之章節（例如 Book 1 Ch.02–Ch.10 在尚未完成地端產稿與總編驗收前）**不得產生公開 HTML、不得進入 `sitemap.xml`、不得出現在 `hreflang`**，在書本目錄中標示「撰寫／校審中（Coming Soon）」，嚴防 Thin Content 拖累全站 SEO。

---

## 2. 系統架構與資料模型設計

### 2.1 URL 拓樸與多語全連接 `hreflang`

| 頁面類型 | `zh-TW`（根站 `zh-Hant`） | `zh-CN`（`zh-Hans`） | `en`（`en`） |
| :--- | :--- | :--- | :--- |
| 出版社總館首頁（Bookshelf） | `/` | `/zh-cn/` | `/en/` |
| Book 2 既有 7 章（零變動） | `/ch01.html`..`/ch07.html` | `/zh-cn/ch01.html`..`ch07.html` | `/en/ch01.html`..`ch07.html` |
| Book 1 專書封面總覽頁 | `/books/ai-engineering/` | `/zh-cn/books/ai-engineering/` | `/en/books/ai-engineering/` |
| Book 1 已出版章節頁 | `/books/ai-engineering/ch01.html`.. | `/zh-cn/books/ai-engineering/ch01.html`.. | `/en/books/ai-engineering/ch01.html`.. |
| 靜態書封資產 | `/assets/cover-ai-engineering.webp`、`/assets/cover-python-dsa.webp`（全語系共用根絕對路徑 `/assets/...`） | 同左 | 同左 |

- **Phase 1 上線總頁數（已驗收可索引頁）**：
  - 原有 24 頁（3 總館首頁 ＋ Book 2 三語 21 章）
  - 新增 Book 1 專書封面頁 3 頁（`/books/ai-engineering/`、`/zh-cn/books/ai-engineering/`、`/en/books/ai-engineering/`）
  - 新增 Book 1 Ch.01 黃金示範章 3 頁（`/books/ai-engineering/ch01.html`、`/zh-cn/books/ai-engineering/ch01.html`、`/en/books/ai-engineering/ch01.html`）
  - **Phase 1 共 30 頁可索引 HTML（均為三語對稱 All-to-All `hreflang` + 自指 `canonical` + `x-default` 指回繁中根頁）**；後續每驗收出版一章 Book 1（Ch.02–Ch.10），自動擴增 3 頁（全書完稿後達 57 頁）。

### 2.2 分片式書本資料結構（`books/ai-engineering/`）
為避免重蹈單檔破萬行難以維護的覆轍，所有新專書採目錄分片儲存：
- `books/ai-engineering/book.json`：定義全書中繼資料（三語書名、副標、封面圖路徑、4 大 `parts` 篇目、10 章目錄骨架、各章範例檔路徑與 `published_locales` 狀態）。
- `books/ai-engineering/outlines.json`：10 章詳細課綱規格書（每章 3–4 節深度小節題綱、核心公式／類比、必檢技術點、翻車場景清單與專屬範例檔對應），供 `scripts/book_forge.py` 與地端模型精準依規起草。
- `books/ai-engineering/glossary.json`：AI 工程領域三語術語鎖定表（`zh-TW` / `zh-CN` / `en`，例如 `詞元/词元/Token`、`檢索增強生成/检索增强生成/RAG`、`微調/微调/Fine-tuning`、`上下文視窗/上下文窗口/Context Window`、`推論/推理/Inference`、`雜湊/哈希/Hash`），同時服務繁中寫作與地端兩段式翻譯。
- `books/ai-engineering/chapters/<locale>/chXX.json`：每章各語系獨立 JSON 檔案（`<locale>` 為 `zh-TW`、`zh-CN`、`en`），包含：
  - `status`（`"draft"` / `"reviewed"` / `"published"`）
  - `id`, `part_id`, `badge`, `title`, `short_title`, `reading_minutes`, `prerequisites`, `lastmod`, `keywords`, `summary`, `aeo_capsule`
  - `svg_diagram`（專屬原生輕量內嵌 `<svg>` 圖解與 `caption`）
  - `sections`（3–4 個深度正文小節，每節含 `heading`, `paragraphs`, `callout`）
  - `comparison_table`（結構化對照表）
  - `code_file`（對應 `examples/ai_chXX_*.py`）與 `code_replacements` / `output_replacements`（延續既有 fail-fast 語法驗證與英文零漢字機制）
  - `pitfalls`（3 個實戰翻車現場）
  - `quiz`（3 題互動隨堂測驗：`question`, `options`, `answer_index`, `explanation`）
  - `interview_faqs`（`>= 3` 題深度 FAQ，自動輸出 `FAQPage` JSON-LD）
  - `further_reading`（非贊助官方技術文件／論文參考）

### 2.3 紫楓版歐萊禮單章 UX 與視覺規格
1. **出版社總館首頁（`/`、`/zh-cn/`、`/en/`）**：
   - 保留既有 O'Reilly × MIT Press 典雅書紙配色與字體系統，於 Hero 下方新增**「精選出版專書書架（Featured Bookshelf）」雙欄典藏卡**（左側顯示 AI 繪製白瀬艾莉書封 `width="320" height="420" loading="eager"` 防 CLS，右側顯示書名、篇目亮點、章節進度與「進入全書閱讀」CTA）。
   - 下方保留既有 Book 2 Ch.01–Ch.07 互動檢索與快速預覽卡片（確保現有繁中首頁測試與使用者習慣零斷層）。
2. **專書封面頁（`/books/ai-engineering/` 等）**：
   - 完整呈現白瀬艾莉書封、全書定位（為何寫這本書）、Part I–IV 階層章節目錄（已出版章節為可點擊卡片，撰寫中章節標記 `In Progress` 灰階徽章且無空連結）、環境與開源說明、`Book` + `Course` JSON-LD。
3. **書本章節頁（`/books/ai-engineering/chXX.html`）**：
   - 雙欄書本排版（桌面端左側 `260px` 黏性全書目錄側欄 `Book Sidebar TOC`＋頂部閱讀進度條；行動端自動收合為頂部 `<details>` 抽屜，確保行動版零水平溢位且全頁 DOM `< 1,500`）。
   - **原生互動隨堂測驗元件（`.quiz-card`）**：純前端無依賴 JS，點選選項即時顯示正確／錯誤與原理詳解，不發送任何網路請求、零外部套件。
   - **中／英文社群提問機制（符合決策 A2）**：
     - **`zh-TW` 與 `zh-CN`（Book 1 與 Book 2 全數章節頁）**：保留極簡 👍/👎 幫助度按鈕（`#fbBox`）與選填原因列；**移除原 `#askForm` 私密提問表單，改為醒目的「紫楓程式＆AI 學習 FB 社團提問區」**，提供：
       1. 「一鍵複製發問模板」按鈕（自動帶入 `[書名 Ch.XX] 我的卡關點：...`）。
       2. 主按鈕直連 [`https://www.facebook.com/share/g/19jsJ8crsC/`](https://www.facebook.com/share/g/19jsJ8crsC/)（`target="_blank" rel="noopener noreferrer"`），並於 Hero 區亦同步更新為該新社團連結。
     - **`en`（Book 1 與 Book 2 英文章節頁）**：保留 👍/👎 幫助度按鈕，提問區導向 GitHub Discussions／Issues（`https://github.com/tbpfs/learning/issues`），嚴格維持全檔零漢字。
   - **JSON-LD 結構化資料**：每章輸出 `@graph`（`TechArticle`、`Chapter` / `isPartOf: Book`、`FAQPage`、`BreadcrumbList`），`inLanguage` 與 `@id` 嚴格依語系隔離。

### 2.4 Book 1 全部 10 支真實可執行 Python 3.12 範例（Phase 1 一次寫齊並納入 CI）
全部存放於 `examples/` 下，嚴守**零外部依賴（純 Python 3.12 標準庫）**，並在 `tests/test_ai_examples.py` 中逐一單元測試其演算法正確性：
1. `examples/ai_ch01_tokenizer_embedding.py`：手刻簡易 BPE Tokenizer（詞表訓練、編碼、解碼）＋ 餘弦相似度（Cosine Similarity）與詞義聚類計算。
2. `examples/ai_ch02_context_schema.py`：Context Budget 裁切器 ＋ 嚴格 JSON Schema 校驗與自動錯誤回饋重試（Retry-with-Feedback）管線。
3. `examples/ai_ch03_hybrid_rag.py`：純標準庫手刻智慧切塊（Overlap Chunker）、BM25 關鍵字檢索、TF-IDF 向量檢索與 Reciprocal Rank Fusion（RRF）混合排序。
4. `examples/ai_ch04_rag_eval.py`：RAG 評測套件（Recall@K、MRR、引用句忠實度 Faithfulness 檢查與簡易 Query Rewriter）。
5. `examples/ai_ch05_agent_fsm.py`：有限狀態機（FSM）ReAct Tool-Calling Agent 引擎（含工具註冊表、步數上限防無限迴圈、對話摘要壓縮記憶）。
6. `examples/ai_ch06_mini_mcp_server.py`：純標準庫 **JSON-RPC 2.0 迷你 MCP Server**（完整實作 `initialize`、`tools/list`、`tools/call`、`resources/list` 協定訊息處理）。
7. `examples/ai_ch07_multi_agent_guard.py`：Supervisor/Worker 多代理人任務派發器 ＋ Prompt Injection 規則偵測 ＋ 危險工具 Human-in-the-Loop 審批閘門。
8. `examples/ai_ch08_local_llm_client.py`：OpenAI-Compatible 本機 LM Studio 客戶端封裝（零依賴 `urllib`、剝離 `<think>`、強制 `reasoning_effort="none"`、SHA-256 斷點快取、VRAM 粗估計算器）。
9. `examples/ai_ch09_spec_driven_gate.py`：規格驅動開發（SDD）自動化契約驗證閘門示範（以宣告式規格自動驗證模組介面、不變量與回歸案例）。
10. `examples/ai_ch10_llmops_router.py`：雙層模型智慧路由器（依複雜度分流輕量／旗艦模型）＋ 精確 Token 成本帳本 ＋ Token Bucket 限流與超時降級（Fallback）。

### 2.5 標準化地端產文與翻譯 CLI（`scripts/book_forge.py`）
- **零外部依賴**（純標準庫 `urllib.request` + `argparse` + `hashlib` + `json`），支援以下子命令：
  1. `status --book ai-engineering`：列出全書 10 章各語系之 `status`（`missing` / `draft` / `reviewed` / `published`）與字數統計。
  2. `check-lm`：探測本機 LM Studio（預設 `http://127.0.0.1:1234/v1/models`，支援 `--base-url`）並回報已載入模型。
  3. `draft --book ai-engineering --chapter ch02 [--model ...]`：讀取 `outlines.json`、`glossary.json` 與已驗證的 `examples/ai_ch02_*.py` 原始碼＋實測輸出，呼叫本機 LM Studio（`"reasoning_effort": "none"`，自動剝離 `<think>` 與多餘圍欄，支援 SHA-256 快取），產出繁中草稿寫入 `chapters/zh-TW/ch02.json`（強制標記 `status: "draft"`，絕不自動公開！）。
  4. `translate --book ai-engineering --chapter ch01 --lang zh-CN|en`：沿用 `local-llm-i18n-translator` 兩段式（鎖詞直譯 → 母語潤飾）與術語表注入，內建確定性機械質檢（英文零漢字、簡中零台灣詞與純繁體字、段落守恆、JSON 結構完整），失敗自動帶錯誤回饋重試最多 3 次；通過後寫入 `chapters/<lang>/chXX.json`（標記 `status: "draft"` 待總編驗收）。
  5. `audit --book ai-engineering`：對所有 `status == "published"` 章節執行全量品質閘門（繁中／簡中純正文 `≥ 2,500` 字、英文純正文 `≥ 1,200` words、原生 SVG 存在且無 `<script>`、3 題測驗格式正確、程式碼替換 100% 命中並通過 `compile()`、簡中零台灣詞、英文零漢字）。

---

## 3. 替代方案比較（Alternatives Considered）

| 方案 | 優點 | 缺點與風險 | 決策 |
| :--- | :--- | :--- | :--- |
| **A. JSON 分片書本資料層 ＋ 既有 SSG 擴充 ＋ `book_forge.py` 驗收閘門（採行）** | 零外部依賴、GitHub Pages 原生相容、既有 24 頁 URL 0 變動、地端草稿與已出版頁完全隔離不汙染 SEO。 | 需重構 `build_site.py` 新增書本渲染器與雙欄 CSS。 | **採行** |
| **B. 改用 Docusaurus / MkDocs / Astro 重寫整站** | 內建文件側欄 UI。 | 破壞現有 0 依賴 Python 建置與 `pm.py verify learn` 全部測試契約，且需大改 URL 與 SEO/JSON-LD 結構，風險過高。 | 捨棄 |
| **C. 一次用本機 LLM 全自動生成 10 章並直接全部公開** | 速度最快。 | 未經總編驗收容易混入幻覺、AI 腔、錯誤程式碼或重複套話，踩中 Google Scaled Content Abuse 雷區。 | 捨棄 |

---

## 4. 檔案級變更清單（File-Level Implementation Plan）

1. `assets/cover-ai-engineering.webp` & `assets/cover-python-dsa.webp`（新增）：AI 繪製白瀬アイリ（左緋紅 `#fb7185`、右蒼藍 `#38bdf8`）學者／工程師風格典藏書封，壓縮至 `< 100 KB`。
2. `book_models.py`（新增）：定義 `BookMeta`, `BookPart`, `BookChapterEntry`, `BookSection`, `QuizQuestion`, `BookChapterData` dataclasses 與載入／驗證函式。
3. `books/ai-engineering/book.json`、`outlines.json`、`glossary.json`（新增）：Book 1 完整 4 篇 10 章出版規格、大綱與三語術語表。
4. `books/ai-engineering/chapters/{zh-TW,zh-CN,en}/ch01.json`（新增）：Book 1 Ch.01 黃金示範章（`status: "published"`，繁中 `≥ 2,500` 字、簡中 `≥ 2,500` 字、英文 `≥ 1,200` words，含專屬原生 SVG 圖解、3 題隨堂測驗與 CI 驗證範例）。
5. `examples/ai_ch01_tokenizer_embedding.py` .. `examples/ai_ch10_llmops_router.py`（新增 10 支）：Book 1 全書 10 支零外部依賴可執行 Python 3.12 範例。
6. `scripts/book_forge.py`（新增）：地端 LM Studio 產草稿、兩段式多語翻譯與全量品質審查 CLI。
7. `build_site.py`（修改）：
   - 複製 `assets/*.webp` 至 `_site/assets/`。
   - 總館首頁新增「紫楓出版社專書書架」雙欄書封卡。
   - 新增專書封面頁渲染器 `render_book_index_page` 與書本章節頁渲染器 `render_book_chapter_page`（含書本側欄 TOC、閱讀進度條、SVG 圖解框、互動隨堂測驗 JS）。
   - 中文語系（`zh-TW`、`zh-CN`）全面以新 FB 社團提問卡（`https://www.facebook.com/share/g/19jsJ8crsC/`，附一鍵複製發問模板）取代原 `#askForm` 私密提問箱，英文版導向 GitHub Issues；更新 Hero 社團連結。
   - 更新 `sitemap.xml`（動態納入所有已出版書頁與章節頁，Phase 1 共 30 頁）、`llms.txt` 與 `llms-full.txt`。
8. `.github/workflows/pages.yml`（修改）：`py_compile` 補上 `book_models.py` 與 `scripts/book_forge.py`，IndexNow `urlList` 納入 `/books/ai-engineering/` 與 `ch01.html`（三語共 32 筆）。
9. `tests/test_ai_examples.py`（新增）& `tests/test_examples.py`（修改）：
   - 測試 Book 1 全部 10 支 Python 範例演算法正確性與 `book_forge.py` 機械質檢／JSON 清理邏輯。
   - 更新 `test_examples.py` 中文版 FB 社團導流契約（驗證新社團 URL、一鍵複製提問模板按鈕、確認原 `#askForm` 已於中文頁移除、👍/👎 `#fbBox` 保留）。
   - 驗證全部 30 頁 HTML（DOM `< 1,500`、全連接雙向 `hreflang`、書封資產存在、原生 SVG 無 `<script>`、互動測驗結構、Book 1 Ch.01 繁／簡 `≥ 2,500` 字與英文 `≥ 1,200` words 且全檔零漢字、簡中零台灣詞與純繁體字）。

---

## 5. 驗收條件（Verification Plan）

1. 兩張書封經視覺檢查確認白瀬アイリ異色瞳方向 100% 正確（觀看者左側緋紅 `#fb7185`、右側蒼藍 `#38bdf8`）且每張 `< 100 KB`。
2. `python -m py_compile build_site.py book_models.py chapter_content.py affiliate_config.py i18n/*.py scripts/*.py examples/*.py tests/*.py` 全數通過。
3. `python -W error -m unittest discover -s tests -v` 與 `python ~/.gemini/bin/pm.py verify learn` 三道閘門全數通過。
4. `python ~/.gemini/bin/pm.py ship learn` 上架後，實機驗證 `/books/ai-engineering/`、`/books/ai-engineering/ch01.html`、`/zh-cn/books/ai-engineering/ch01.html`、`/en/books/ai-engineering/ch01.html` 與既有 Book 2 頁面全數 `HTTP 200`。
