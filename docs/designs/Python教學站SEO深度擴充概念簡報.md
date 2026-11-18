# Python 教學站（`learn.ai-purplemaple.com`）SEO 與內容深度升級概念簡報（EGM Concept Brief）

## 1. 問題假設與量化現況診斷（Problem Hypothesis & Baseline Metrics）

### 1.1 現況痛點（Observed Symptoms）
`learn.ai-purplemaple.com`（GitHub 儲存庫 `tbpfs/learning`，由 [`build_site.py`](../../build_site.py) 靜態生成並部署於 GitHub Pages）目前已具備完整的技術 SEO 外殼（GTM/GA4 置頂、Canonical 對齊、X Card、AdSense 內嵌廣告位 `1673180799`、`llms.txt` / `llms-full.txt` 與 IndexNow），但在 Google Search Console（`sc-domain:ai-purplemaple.com`）中，`ch04.html` 與 `ch05.html` 長期處於「已檢索／已探索－目前未建立索引（Crawled / Discovered - currently not indexed）」狀態，且自然搜尋長尾關鍵字曝光量偏低。

### 1.2 根本原因剖析（Root-Cause Analysis）
經審計 [`build_site.py`](../../build_site.py) 與 [`tests/test_examples.py`](../../tests/test_examples.py)，定位出三大結構性問題：

1. **單章節自然語言教學正文（Prose）嚴重不足（Thin Content）**：
   - 在 [`build_site.py` 的 `CHAPTERS` 資料結構（第 22–83 行）](../../build_site.py#L22-L83) 中，每個章節僅包含 1 句 `summary`（約 55–70 字）與 2 條 `concepts` 項目（合計約 180–240 字）。
   - 扣除 Python 原始碼與 stdout 輸出後，單章自然語言解說僅約 **250–300 個中文字**，遠低於技術教學文章在 Google 搜尋與 Google AdSense 內容品質評估中的建議門檻（每篇獨立教學頁至少 1,000–1,500+ 字結構化正文）。
2. **首頁（`index.html`）與獨立章節頁（`ch01.html`～`ch05.html`）自我重複競爭（Self-Cannibalization & Boilerplate Duplication）**：
   - 在 [`build_site.py` 第 797–846 行](../../build_site.py#L797-L846) 中，`ch01.html`～`ch05.html` 是透過對 `index.html` 的 `page_html` 執行字串替換（`.replace()`）生成。
   - **內容重疊率高達 95%**：`index.html` 已經完整渲染了全部章節的觀念、完整原始碼與執行結果；而 `ch01.html`～`ch05.html` 僅是把 `all_cards` 替換成單一 `ch_card`，**沒有任何單章獨有的深度教學內容**。
   - **樣板與結構化資料重複**：單章頁保留了與首頁完全相同的 `#study-guide` 區塊、全站 TOC 錨點（在單章頁點擊 `#ch02` 甚至無法跳轉，因為單章頁 DOM 中只有單一章節！），且單章頁 `<head>` 中的 JSON-LD 仍為指向首頁 `@id: "https://learn.ai-purplemaple.com/#course"` 的 `Course` 結構，缺少單章專屬的 `TechArticle`、`LearningResource`、`FAQPage` 與 `BreadcrumbList`。
3. **缺少演算法搜尋意圖必備的「結構化比較表」與「白板題 FAQ」**：
   - 搜尋「Python 鏈結串列 vs 陣列」、「Python Stack Queue 複雜度」、「Binary Search 邊界條件」、「Two Sum 雜湊表」、「BFS vs DFS 差異」的工程師與學生，最依賴 **時間／空間複雜度對照表（HTML `<table>`）**、**逐步執行狀態拆解（Step-by-Step Walkthrough）**、**Python 底層實作陷阱（Pitfalls）** 以及 **LeetCode 對應題號與常見面試問答（FAQ）**。
   - 此外，作為「從零開始寫程式，輕鬆搞懂資料結構、演算法」鐵人賽核心教材，目前僅涵蓋 `Ch.01`～`Ch.05`，尚未收錄軟體工程師面試必考的兩大壓軸主題：**`Ch.06 動態規劃（Dynamic Programming：記憶化搜尋與自底向上狀態轉移）`** 與 **`Ch.07 堆積與優先佇列（Heap / Priority Queue & Top-K 問題）`**。

---

## 2. 企劃目標與非目標（Goals & Non-Goals）

### 2.1 核心目標（Goals）
1. **解除首頁與單章頁自我競爭（Information Architecture De-duplication）**：
   - **首頁（`index.html`）**：維持「全課程總覽與實機程式碼快速預覽中心」定位（保留現有測試斷言所需的各章摘要、核心重點、完整可複製程式碼與 CI 實測輸出），並在每章卡片底部新增醒目的「📖 進入 `Ch.0X` 獨立深度講義（含複雜度對照表、逐步圖解、Python 3.12 底層陷阱與 LeetCode 面試 FAQ）→」導流按鈕。
   - **獨立章節頁（`ch01.html`～`ch07.html`）**：不再使用脆弱的 `page_html.replace()` 字串替換，改由專屬渲染器生成具備 **1,200～1,800+ 字深度教學正文** 的獨立講義頁，移除單章頁內失效的 `#ch0X` 頁內錨點與重複的 `#study-guide` 樣板，並加上跨章節導覽列（上一章／返回總目錄／下一章）。
2. **每章新增四大結構化深度教學模組（4 Deep-Dive Modules per Chapter）**：
   - **模組 A — 結構化複雜度與特性對照表（`comparison_table`）**：渲染語意化 HTML `<table>`（含 `<thead>`、`<tbody>`、`<caption>`），直接搶攻 Google 表格精選摘要（Featured Snippets）。
   - **模組 B — 演算法逐步執行與記憶體狀態拆解（`walkthrough`）**：以具體輸入資料逐步追蹤指標／索引／佇列／遞迴樹在每個 Step 的狀態變化。
   - **模組 C — Python 3.12 底層原理與實戰常見陷阱（`pitfalls`）**：剖析 CPython 實作細節（如 `list` 連續指標陣列 over-allocation、`deque` 雙向區塊鏈結、`mid = left + (right - left) // 2` 邊界與 `bisect`、CPython `dict` 緊湊開放定址法、遞迴深度限制 `sys.getrecursionlimit()` 等）。
   - **模組 D — 技術面試必考 FAQ 與 LeetCode 對照表（`interview_faqs` & `leetcode_problems`）**：每章收錄 3 題深度面試問答與對應 LeetCode 經典題號、難度與破題關鍵。
3. **擴充壓軸章節 `Ch.06` 與 `Ch.07`（7 章完整鐵人賽體系）**：
   - 新增 **`Ch.06 動態規劃與記憶化搜尋（Dynamic Programming & Memoization）`**（`examples/ch06_dynamic_programming.py`：實作爬樓梯／費氏數列狀態壓縮 `O(1)` 空間、0/1 背包問題 `knapsack_01` 與最長遞增子序列 `length_of_lis`）。
   - 新增 **`Ch.07 堆積、優先佇列與 Top-K 演算法（Heap, Priority Queue & Top-K Elements）`**（`examples/ch07_heap_priority_queue.py`：實作最小堆積 `MinHeap` 上浮/下沉封裝、`heapq` Top-K 最大元素 `top_k_frequent_or_largest` 與 K 個已排序串列合併 `merge_k_sorted_lists`）。
4. **單章專屬 Schema.org JSON-LD 與 Sitemap 強化**：
   - 首頁（`index.html`）輸出包含 `hasCourseInstance` 與 7 章 `Syllabus` / `hasPart` 的 `Course` + `ItemList` JSON-LD。
   - 每個單章頁（`ch01.html`～`ch07.html`）輸出專屬 `@graph` JSON-LD：包含 `TechArticle`（含 `proficiencyLevel`、`dependencies: "Python 3.12"`、`isPartOf: {"@id": "https://learn.ai-purplemaple.com/#course"}`）、`FAQPage`（直接映射該章 3 題面試 FAQ）與 `BreadcrumbList`（首頁 → `Ch.0X`）。
   - `sitemap.xml` 移除純文字語料檔（`llms.txt`、`llms-full.txt` 改由 `robots.txt` 與首頁 `<link rel="alternate" type="text/markdown">` 暴露），確保 `sitemap.xml` 100% 為具備對應 `<link rel="canonical">` 的 HTML 教學頁面（或保留既有測試相容性同時補齊 `<lastmod>`，見下方替代方案權衡）。

### 2.2 非目標（Non-Goals）
- 不引入任何第三方 Python 套件（如 Jinja2、Markdown、MkDocs）或前端打包工具（Webpack/Vite），維持 **100% Python 3.12 標準庫零依賴建置**。
- 不引入外部字型檔、外部 CSS 框架或高耗能前端執行環境（如 Pyodide WebAssembly），確保頁面維持極速載入（LCP < 1.0s，CLS = 0）。
- 不破壞 [`tests/test_examples.py`](../../tests/test_examples.py) 現有的向後相容性斷言，僅在此基礎上擴充新章節與深度內容斷言。

---

## 3. 候選方案與拒絕理由（Alternatives Considered）

### 方案 A：維持現有單檔 `build_site.py` 並在其中硬塞上萬字字典字串（Rejected）
- **作法**：直接把 7 個章節的比較表、逐步拆解、陷阱分析與面試 FAQ 全部寫進 `build_site.py` 頂部的 `CHAPTERS` 字典。
- **拒絕技術理由**：會導致 `build_site.py` 暴增至 2,000+ 行，使「教材內容資料（Content Data）」與「HTML 模板渲染邏輯（Rendering Logic）」嚴重耦合，違反關注點分離（Separation of Concerns），不利後續維護與單元測試。

### 方案 B：引入 MkDocs / Sphinx / Hugo 等外部靜態站框架（Rejected）
- **作法**：改用第三方 SSG 框架將 Markdown 轉為 HTML。
- **拒絕技術理由**：
  1. 違反本專案「零外部依賴（Zero external dependencies）」與「建置時自動執行 `examples/ch0X_*.py` 擷取真實 stdout 輸出」的核心架構。
  2. 現有 GitHub Actions 工作流與 `tests/test_examples.py` 皆直接呼叫 `build_site(Path(tmpdir))`，更換框架會破壞所有既有 CI 測試、AdSense 內嵌廣告位精準控制與 CMS API（`https://ai-purplemaple.com/api/v1/content`）動態掛載邏輯。

### 方案 C（選定方案）：零依賴資料與渲染分離架構（`chapter_content.py` + 雙模式渲染器 `build_site.py`）
- **作法**：
  1. 將結構化深度教材抽離為純 Python 標準庫資料模組 `chapter_content.py`（使用 `@dataclass(frozen=True)` 嚴格定義 `ChapterSpec`、`ComparisonTable`、`WalkthroughStep`、`PitfallItem`、`LeetCodeRef`、`FAQItem` 型別結構）。
  2. `build_site.py` 匯入 `CHAPTERS`，並提供獨立的 `render_index_page()` 與 `render_chapter_page(ch_idx)` 函式，徹底淘汰脆弱的 `page_html.replace()` 字串替換。
  3. 同步將深度教學內容匯出至 `llms-full.txt`，讓 AI 搜尋引擎（ChatGPT、Perplexity、Claude、Grok）也能索引完整的複雜度表格、逐步解析與面試 FAQ。
