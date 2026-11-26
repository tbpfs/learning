# 從零開始寫程式，輕鬆搞懂資料結構，演算法

大家好:   
我是紫楓，之前曾經在職業版發表一個關於軟體工程師，問都給問的文   
其中有很多個問題是關於   

1. 我是學生，我該學什麼?   
2. 我想轉職，我該學什麼?   
3. 我想精益求精，我該學什麼?   

這類的問題，那歸根究柢，就是目前的軟體工程師中，很多人的基本功不足，所以對學習，對找工作會非常迷惘   
所以我打算開設這一個最基本功的鐵人賽主題，幫助基本功沒練好，或是想轉職當軟體工程師的人。   
而所謂的基本功，便是資料結構，演算法，物件導向   
當然，這一系列可能對已經身經百戰的強者們來說，實在太淺了。   
那也歡迎強者們對我的影片做個批評指教。   
如果你覺得我的影片做得不錯，也會非常感謝你給個讚或訂閱。   
這是對我而言最大的鼓勵   


完整播放清單:
https://www.youtube.com/playlist?list=PLhxdaTcUMi3nRM5mtOdQgO4VEtAEsTiYd

程式新手學習發問區，問都給問: https://www.facebook.com/groups/914880435669061

線上互動教學與程式碼預覽網站：https://learn.ai-purplemaple.com/

---

## 課程章節與互動教學導覽（Course Table of Contents）

| 章節 | 互動教學頁（含程式碼預覽與重點解說） | 核心學習重點 | 對應範例程式 |
| :---: | :--- | :--- | :--- |
| **Ch.01** | [**陣列與單向鏈結串列（Array & Singly Linked List）**](https://learn.ai-purplemaple.com/ch01.html) | 連續記憶體存取 $O(1)$ vs. 節點指標串接、插入、刪除與三指標原地反轉 | `examples/ch01_array_linked_list.py` |
| **Ch.02** | [**堆疊與佇列（Stack & Queue）**](https://learn.ai-purplemaple.com/ch02.html) | 後進先出（LIFO）括號匹配檢查 vs. 先進先出（FIFO）雙端佇列排隊模型 | `examples/ch02_stack_queue.py` |
| **Ch.03** | [**搜尋與排序演算法（Search & Sort）**](https://learn.ai-purplemaple.com/ch03.html) | 二分搜尋法 $O(\log n)$、合併排序法（Merge Sort）$O(n \log n)$ 分治實作 | `examples/ch03_search_sort.py` |
| **Ch.04** | [**雜湊表與二元搜尋樹（Hash Table & BST）**](https://learn.ai-purplemaple.com/ch04.html) | 鏈結法碰撞處理、Two Sum $O(n)$ 解法、二元搜尋樹中序遞增走訪 | `examples/ch04_hash_bst.py` |
| **Ch.05** | [**圖論走訪與物件導向設計（Graph BFS / DFS & OOP）**](https://learn.ai-purplemaple.com/ch05.html) | 泛型鄰接表封裝、廣度優先搜尋無權重最短路徑、深度優先搜尋走訪 | `examples/ch05_graph_oop.py` |
| **Ch.06** | [**動態規劃與記憶化搜尋（Dynamic Programming & Memoization）**](https://learn.ai-purplemaple.com/ch06.html) | 爬樓梯 $O(1)$ 空間狀態壓縮、0/1 背包一維滾動陣列、二分優化 LIS $O(n \log n)$ | `examples/ch06_dynamic_programming.py` |
| **Ch.07** | [**堆積、優先佇列與 Top-K 演算法（Heap, Priority Queue & Top-K）**](https://learn.ai-purplemaple.com/ch07.html) | 手寫泛型最小二元堆積 `MinHeap`、海量資料 Top-K 篩選、合併 $K$ 個排序序列 | `examples/ch07_heap_priority_queue.py` |

## 執行範例、單元測試與靜態網站建置

```bash
# 執行各章節教學範例
python3 examples/ch01_array_linked_list.py
python3 examples/ch02_stack_queue.py
python3 examples/ch03_search_sort.py
python3 examples/ch04_hash_bst.py
python3 examples/ch05_graph_oop.py
python3 examples/ch06_dynamic_programming.py
python3 examples/ch07_heap_priority_queue.py

# 執行完整單元測試套件
python3 -W error -m unittest discover -s tests -v

# 建置 GitHub Pages 靜態教學網站至 _site/index.html 與 _site/ch01.html..ch07.html
python3 build_site.py -o _site
```

---

## 紫楓（王紫楓 / Purple Maple）相關免費教學與開發作品

- **[紫楓（王紫楓）官方網站](https://ai-purplemaple.com/)**：AI 繪圖、Suno 原創音樂、原創看板娘白瀬アイリ與全系列軟體開發作品
- **[紫楓原創有聲小說庫](https://novel.ai-purplemaple.com/)**：多流派原創輕小說 × 不斷音原聲帶 × Podcast 有聲劇
- **[MapleQuant 紫楓量化實驗室](https://invest.ai-purplemaple.com/)**：繁日英三語投資風控、部位計算與台日美 ETF 參數對決沙盒
- **[時空守護者｜國小 108 課綱免費互動學習網](https://edu.ai-purplemaple.com/)**：近 900 篇段考攻略與低年級注音朗讀
- **[府城保衛戰｜台南古蹟 3D 網頁戰術射擊](https://fps.ai-purplemaple.com/)**（Three.js）｜ **[星界斷章｜原創機甲音遊](https://astral.ai-purplemaple.com/)**
- **X (Twitter)**：[@tbpfs1](https://x.com/tbpfs1) ｜ **AI 語料索引**：https://learn.ai-purplemaple.com/llms.txt

---

## 版權與雙重授權說明（Dual License & Copyright）

本倉庫採**程式碼與書籍內容分離之雙重授權**（詳見 [LICENSE](./LICENSE) 與 [全站版權與轉載聲明](https://ai-purplemaple.com/privacy.html#copyright)）：

- **範例程式碼（`examples/`、建置與測試程式）**：採 **MIT License**，歡迎自由執行、學習、修改與於專案中使用。
- **專書內文、章節講義、原創圖解與封面視覺**：**© 2026 紫楓（Purple Maple / 王紫楓）. All Rights Reserved.** 歡迎非商業學習筆記、書評與搜尋引用節錄少量內容（建議 200 字內）並附原作者名稱與原文連結；**禁止未經書面授權全文搬運、鏡像站複製或打包販售**。
