# Python 互動教學站（`learn.ai-purplemaple.com`）簡中與英文多語 SEO 擴張技術設計書

- **版本**：v1.1
- **狀態**：Goldfish-Resolved（已全數吸收 3 項 BLOCKER、6 項 MAJOR、4 項 MINOR 審查修訂）
- **所屬專案**：`tbpfs/learning`（GitHub Pages 靜態站 `https://learn.ai-purplemaple.com/`）
- **關聯文件**：`Python教學站SEO與內容深度升級設計書.md`、`章節微回饋與私密提問箱設計書.md`

---

## 0. EGM Goldfish 審查決議摘要（v1.0 → v1.1）
- **B1（範例程式碼完整在地化與 Fail-Fast 校驗）**：拆分為 `CODE_REPLACEMENTS`（涵蓋全部 docstring、5 處 `ValueError` 例外訊息與所有 `print`/f-string 標籤）與 `OUTPUT_REPLACEMENTS`，內建 fail-fast 命中檢查、`compile(..., "exec")` 語法驗證與英文零漢字／零全形標點斷言。
- **B2（全頁 `<head>`／JSON-LD／JS 零硬編碼繁中）**：`og:image:alt`、`twitter:image:alt`、JSON-LD 實體名稱與 `render_copy_script` 8 處 JS 訊息全部移入語系字典並以 `json.dumps` 安全序列化（英文版使用 `Shirase Airi (Aily)`，全檔零漢字）。
- **B3（章節延伸資源卡片在地化）**：`zh-TW` 保留博客來 AP 卡片；`/zh-cn/` 與 `/en/` 改為非贊助之官方文件／經典延伸閱讀卡片（無 `books.com.tw`、無 `rel="sponsored"`、不掛 `data-affiliate-partner` 以免汙染 GA4 聯盟事件）。
- **M4–M9 & Minor 10–13**：`Course.@id` 依語系隔離，`VideoObject.inLanguage` 固定 `"zh-Hant"` 忠實反映中文語音；`ChapterSpec` 增設可選 `short_title: str = ""`；全站子目錄採根絕對路徑（`/ads.txt`、`/zh-cn/`、`/en/`，嚴禁 `index.html`）；保留 `zh-TW` 標題頓號／H1 逗號精確契約；CI 與本機統一 `-W error`；英文單章正文門檻統一 `>= 600` words 且全檔掃描（僅剝除 `lang-switcher`）零漢字；簡中全檔掃描雙檢 19 個台灣 CS 禁詞與高頻純繁體字；`:root:lang(zh-Hans)` 同步覆寫 `--font-sans` 與 `--font-serif`；`pages.yml` IndexNow 擴充為 26 筆（24 頁 HTML + `llms.txt` + `llms-full.txt`）並補 JSON 解析測試；`fbKey = 'learnFb:' + chId` 跨語系共用以配合主站限流契約。

---

## 1. 背景、目標與邊界（Scope & Non-Goals）

### 1.1 業務與流量目標
`learn.ai-purplemaple.com` 目前僅有 8 頁繁體中文（`zh-Hant`）教材（`/` 首頁與 `ch01.html`～`ch07.html`）。為同時收割：
1. **全球英文高 RPM 開發者流量（Tier 1 美國／英國／加拿大／澳洲／新加坡／印度）**：透過 `/en/` 與 `/en/ch01.html`～`/en/ch07.html` 鎖定 `Python data structures and algorithms`、`LeetCode 206 reverse linked list Python`、`Python heapq Top-K`、`0/1 knapsack dynamic programming Python` 等高價值長尾查詢詞，提升 AdSense 單價與國際品牌能見度。
2. **中國大陸與海外簡體中文開發者流量**：透過 `/zh-cn/` 與 `/zh-cn/ch01.html`～`/zh-cn/ch07.html` 鎖定「Python 数据结构与算法」「数组与链表」「栈和队列」「哈希表与二叉搜索树」「动态规划 0/1 背包」「堆与优先队列 Top-K」等高搜尋量簡中技術詞。

本次擴充將站點由 **8 頁升級為 24 頁完全對稱三語靜態站**（`zh-Hant` 8 頁 ＋ `zh-Hans` 8 頁 ＋ `en` 8 頁），維持零外部依賴、GitHub Actions 自動建置與 GitHub Pages 純靜態託管。

### 1.2 嚴格範圍與非目標（Non-Goals）
- **繁中根站零回歸**：既有的 `zh-TW` 首頁與 `ch01.html`～`ch07.html` 之 URL、HTML 結構、雙軌品牌錨點（`王紫楓（紫楓 / Purple Maple）`）、`ch07.html` `twitter:description` 契約、純中文正文 `>= 1,200` 字與全部既有單元測試斷言必須 100% 不變。
- **不改動可執行範例原始碼**：`examples/ch01..ch07.py` 維持原貌不改，確保既有 Python 單元測試與教學範例 100% 穩定；簡中與英文頁面之程式碼註解／輸出標籤改由建置期在地化映射層安全轉換並驗證可通過 Python 語法編譯。
- **不新增外部依賴或變更後端 API**：微回饋與私密提問 API 繼續呼叫主站 `https://ai-purplemaple.com/api/v1/learn-feedback` 與 `/api/v1/learn-question`，`slug` 仍傳送 `ch01`～`ch07`（相容既有後端白名單），僅前端介面與狀態訊息依語系在地化。

---

## 2. 系統架構與設計決策

### 2.1 URL 拓樸、語系對應與全連接雙向 `hreflang`

| 語系代碼 | HTML `lang` | `hreflang` | `og:locale` | 輸出目錄（相對於 `_site/`） | 規範網址（Canonical） |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `zh-TW`（預設根站） | `zh-Hant` | `zh-Hant` | `zh_TW` | `index.html`, `ch01.html`..`ch07.html` | `https://learn.ai-purplemaple.com/` 與 `/{ch}.html` |
| `zh-CN`（大陸簡中） | `zh-Hans` | `zh-Hans` | `zh_CN` | `zh-cn/index.html`, `zh-cn/ch01.html`..`ch07.html` | `https://learn.ai-purplemaple.com/zh-cn/` 與 `/zh-cn/{ch}.html` |
| `en`（國際英文） | `en` | `en` | `en_US` | `en/index.html`, `en/ch01.html`..`ch07.html` | `https://learn.ai-purplemaple.com/en/` 與 `/en/{ch}.html` |

- **全連接雙向 `hreflang`（All-to-All）**：
  - 每一頁（3 個首頁、21 個章節頁）均輸出全部 4 條 `<link rel="alternate" hreflang="...">`：`zh-Hant`、`zh-Hans`、`en` 與 `x-default`（指向繁中根頁 `/` 或 `/{ch}.html`），搭配自指 `<link rel="canonical">` 與 `og:locale` + 兩條 `og:locale:alternate`。
- **子目錄相對／絕對路徑安全（零 404 鐵則）**：
  - 根站（`zh-TW`）：首頁連結為 `/`，章節互連為 `{ch}.html`，頁尾 `ads.txt` 為 `/ads.txt`。
  - `/zh-cn/` 子站：首頁連結為 `/zh-cn/`，章節互連為 `{ch}.html`（解析至 `/zh-cn/{ch}.html`），頁尾 `ads.txt` 必須為根絕對路徑 `/ads.txt`。
  - `/en/` 子站：首頁連結為 `/en/`，章節互連為 `{ch}.html`（解析至 `/en/{ch}.html`），頁尾 `ads.txt` 必須為根絕對路徑 `/ads.txt`。
- **語系切換導覽列（`<nav class="lang-switcher">`）**：
  - 置於 Hero 區塊頂部，提供三語切換連結（`繁體中文` / `简体中文` / `English`），每個連結均帶對應 `lang` 屬性（`zh-Hant` / `zh-Hans` / `en`），當前語系標記 `aria-current="true"`；於章節頁切換時直接跳轉至對應語系的同一章（例如 `/ch03.html` ⇄ `/zh-cn/ch03.html` ⇄ `/en/ch03.html`），不回跳首頁。
  - CSS 加上 `display: flex; flex-wrap: wrap; gap: 0.45rem;`，確保 320px 行動版零水平溢位。

### 2.2 模組化多語資料架構（避免 `build_site.py` 單檔膨脹）
新增 `i18n/` 模組套件（零外部依賴、純 Python 標準庫）：
1. `i18n/__init__.py`：定義語系規格 `LocaleConfig`（`code`、`html_lang`、`hreflang`、`og_locale`、`url_prefix`、`output_subdir`、`site_name` 等）與統一查詢函式 `get_locale_bundle(locale)`。
2. `i18n/zh_cn.py`：提供大陸簡中完整 `CHAPTERS_ZH_CN: tuple[ChapterSpec, ...]`（7 章全手寫／術語對齊，每章純中文正文維持 `>= 1,200` 字）、`UI_ZH_CN`、`YOUTUBE_ZH_CN`、`RESOURCES_ZH_CN`、`CODE_DOCSTRING_MAP_ZH_CN`。
3. `i18n/en.py`：提供自然流暢的國際英文 `CHAPTERS_EN: tuple[ChapterSpec, ...]`（7 章完整技術教材，每章純英文正文 `>= 600` words，含完整複雜度表、逐步追蹤、CPython 3.12 底層原理、LeetCode 模板與面試 FAQ）、`UI_EN`、`YOUTUBE_EN`、`RESOURCES_EN`、`CODE_DOCSTRING_MAP_EN`。

### 2.3 四大跨語系防坑與合規設計
1. **程式碼與實機輸出在地化（杜絕英文頁外洩漢字、簡中頁外洩繁詞）**：
   - `execute_all_examples` 仍只執行 `examples/ch01..ch07.py` 一次取得真實輸出；針對 `zh-CN` 與 `en` 頁面，透過 `localize_code_and_output(locale, ch_id, raw_src, raw_out)` 替換範例內的 docstring 與 stdout 標籤文字，同時保證替換後的 Python 原始碼 100% 通過 `compile(src, ..., "exec")` 語法檢查，且計算出的數值結果完全來自實機執行輸出。
2. **停用外語首頁的繁中 CMS 動態注入**：
   - `index.html`（`zh-TW`）維持 `include_cms_fetch=True` 載入主站動態補充講義；`/zh-cn/index.html` 與 `/en/index.html` 設為 `include_cms_fetch=False`，避免將繁體中文動態卡片注入簡中或英文頁面。
3. **聯盟書籍與 YouTube 區塊在地化**：
   - `zh-TW` 完整保留既有博客來策略聯盟（`books.com.tw`）與 Hahow 區塊（0 變更）。
   - `zh-CN` 改為簡體中文精選書單與免費學習資源表（《算法图解》《流畅的 Python》《算法导论》、Python 3.12 官方中文文档、LeetCode 力扣），無台灣限定物流／書城用語；YouTube 影片標題與說明全面轉寫為簡體中文並註明「普通话／中文讲解，附动态图解」。
   - `en` 改為純英文經典 CS 書單與資源表（*Grokking Algorithms*, *Fluent Python 2nd Ed.*, *CLRS*, Python 3.12 Official Docs），YouTube 區塊標題與 `VideoObject` JSON-LD 全面以英文撰寫並註明 `Mandarin Chinese audio with visual step-by-step diagrams`，**全頁零任何中文字元外洩**。
4. **字體防拖速與品牌雙軌一致性**：
   - `render_shared_styles()` 新增 `:root:lang(zh-Hans)` 系統簡中無襯線／襯線字體堆疊（`"PingFang SC", "Hiragino Sans GB", "Microsoft YaHei"`）與 `:root:lang(en)` 歐文字體堆疊，絕不載入 Google Fonts CJK 字體。
   - 英文頁創作者署名採用 `Purple Maple (Wang Tzu-Feng / @tbpfs1)`（對應 `https://ai-purplemaple.com/`），簡中頁採用 `紫枫（王紫枫 / Purple Maple）`，繁中頁維持既有 `王紫楓（紫楓 / Purple Maple）` 雙軌錨點契約。
   - `GTM-WNSFQT5V`、`G-B24GXZ32MW`、`ca-pub-6485917848711473` 嚴格置於全部 24 頁 `<head>` 正下方第一行。

### 2.4 `sitemap.xml`、`llms.txt`、`llms-full.txt` 與 CI/CD 升級
- `sitemap.xml` 收錄全部 **24 筆**規範 HTML URL（8 筆繁中 ＋ 8 筆簡中 ＋ 8 筆英文，不含 `llms*.txt`）。
- `llms.txt` 新增三語總覽索引（繁中／簡中／英文入口與 7 章對照），維持既有所有 `zh-TW` 斷言；`llms-full.txt` 保持繁中完整語料並於文首列出 `/zh-cn/` 與 `/en/` 入口連結。
- `.github/workflows/pages.yml`：
  - `py_compile` 補上 `i18n/*.py` 與 `chapter_content.py`、`affiliate_config.py`。
  - IndexNow `urlList` 補齊 `ch06.html`、`ch07.html`、`/zh-cn/`、`/zh-cn/ch01.html`..`ch07.html`、`/en/`、`/en/ch01.html`..`ch07.html`。

---

## 3. 替代方案比較（Alternatives Considered）

| 方案 | 優點 | 缺點與風險 | 決策 |
| :--- | :--- | :--- | :--- |
| **A. `i18n/zh_cn.py` + `i18n/en.py` 靜態多語資料模組＋統一參數化渲染器（採行）** | 零外部依賴、可被 `py_compile` 與 `unittest` 完整校驗、`build_site.py` 維持清晰不膨脹，24 頁共享一致的 SEO/GEO/AEO 契約。 | 需手寫精校兩套完整 7 章教材資料。 | **採行** |
| **B. 建置期以 OpenCC 自動繁轉簡、僅手寫英文** | 簡中建置速度快。 | OpenCC 無法處理台灣／大陸 CS 術語差異（陣列/数组、佇列/队列、雜湊表/哈希表、堆積/堆、物件導向/面向对象），且會破壞零外部依賴原則。 | 捨棄 |
| **C. 僅建置 `/en/` 不建 `/zh-cn/`** | 工作量減半。 | 錯失簡體中文極高搜尋量的 Python 演算法／刷題教學長尾詞與百度／Google 簡中索引紅利。 | 捨棄 |

---

## 4. 檔案級變更清單（File-Level Implementation Plan）

1. `i18n/__init__.py`（新增）：`LocaleConfig`、三語設定、`localize_code_and_output`、語系資料載入器。
2. `i18n/zh_cn.py`（新增）：大陸簡中完整 7 章 `ChapterSpec`、UI 字典、YouTube 簡中 metadata、簡中學習資源與範例 docstring/stdout 對照表。
3. `i18n/en.py`（新增）：國際英文完整 7 章 `ChapterSpec`、UI 字典、YouTube 英文 metadata、英文經典資源與範例 docstring/stdout 對照表。
4. `build_site.py`（修改）：將 `build_index_json_ld`、`build_chapter_json_ld`、各區塊渲染器、`render_index_page`、`render_chapter_page`、`render_footer`、`render_copy_script`、`render_shared_styles` 與 `build_site` 參數化支援三語，產出 24 頁 HTML + 24 筆 `sitemap.xml` + 更新 `llms.txt`/`llms-full.txt`。
5. `.github/workflows/pages.yml`（修改）：`py_compile` 納入 `i18n/*.py`，更新 IndexNow `urlList` 涵蓋全部核心三語頁面。
6. `tests/test_examples.py`（修改）：保留全部既有 `zh-TW` 斷言 100% 不變，新增三語測試：
   - 24 頁產出與 `sitemap.xml` 24 筆 URL 完整驗證。
   - 全連接雙向 `hreflang`（`zh-Hant` / `zh-Hans` / `en` / `x-default`）、自指 `canonical`、`og:locale` 與 DOM `< 1,500` 驗證。
   - **英文機械質檢閘門**：8 頁 `/en/` HTML（移除 `<nav class="lang-switcher">` 後）**零任何 CJK 中文字元**（`[\u4e00-\u9fff]` == 0）且單章正文 `>= 500` 英文單字。
   - **簡中機械質檢閘門**：8 頁 `/zh-cn/` HTML（移除 `<nav class="lang-switcher">` 後）單章純中文 `>= 1,200` 字，且**零任何台灣 CS 專屬禁詞**（`陣列`、`鏈結串列`、`堆疊`、`佇列`、`雜湊表`、`堆積`、`演算法`、`物件導向`、`遞迴`、`變數`、`迴圈`、`程式碼`、`連結`、`試算`、`視窗`、`資訊`、`記憶體`、`講義`、`預設`）。
   - 在地化程式碼均通過 Python `compile()` 語法檢查，且所有頁內連結無 404 死鏈（含 `/ads.txt`）。

---

## 5. 驗收條件（Verification Plan）

1. `python -m py_compile build_site.py chapter_content.py affiliate_config.py i18n/*.py examples/*.py tests/*.py` 全數通過。
2. `python -m unittest discover -s tests -v` 與 `python ~/.gemini/bin/pm.py verify learn` 三道閘門全數通過。
3. 透過 `python ~/.gemini/bin/pm.py ship learn` 推送至 `tbpfs/learning` 觸發 GitHub Actions 部署後，實機驗證 `https://learn.ai-purplemaple.com/zh-cn/` 與 `https://learn.ai-purplemaple.com/en/` 皆回傳 `HTTP 200`。
