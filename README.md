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

線上教學與程式碼預覽網站: https://learn.ai-purplemaple.com/ （備用鏡像：https://tbpfs.github.io/learning/）

---

## 課程章節與基礎範例導覽（Course Table of Contents）

| 章節 | 主題名稱 | 核心學習重點 | 對應範例程式 |
| :---: | :--- | :--- | :--- |
| **Ch.01** | **陣列與單向鏈結串列（Array & Singly Linked List）** | 連續記憶體存取 $O(1)$ vs. 節點指標串接、插入與刪除、原地反轉 | `examples/ch01_array_linked_list.py` |
| **Ch.02** | **堆疊與佇列（Stack & Queue）** | 後進先出（LIFO）括號匹配檢查 vs. 先進先出（FIFO）雙端佇列模型 | `examples/ch02_stack_queue.py` |
| **Ch.03** | **搜尋與排序演算法（Search & Sort）** | 二分搜尋法 $O(\log n)$、合併排序法（Merge Sort）$O(n \log n)$ | `examples/ch03_search_sort.py` |
| **Ch.04** | **雜湊表與二元搜尋樹（Hash Table & BST）** | 鏈結法碰撞處理、Two Sum $O(n)$ 解法、二元搜尋樹中序走訪 | `examples/ch04_hash_bst.py` |
| **Ch.05** | **圖論走訪與物件導向設計（Graph BFS / DFS & OOP）** | 泛型鄰接表封裝、廣度優先搜尋最短路徑、深度優先搜尋走訪 | `examples/ch05_graph_oop.py` |
| **Ch.06** | **動態規劃與記憶化搜尋（Dynamic Programming & Memoization）** | 爬樓梯狀態壓縮 $O(1)$ 空間、0/1 背包一維逆序更新、最長遞增子序列 LIS $O(n \log n)$ | `examples/ch06_dynamic_programming.py` |
| **Ch.07** | **堆積、優先佇列與 Top-K 演算法（Heap, Priority Queue & Top-K）** | 完全二元樹陣列映射 `MinHeap` 上浮/下沉、Top-K 篩選 $O(n \log k)$、合併 K 個排序串列 | `examples/ch07_heap_priority_queue.py` |

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

# 建置 GitHub Pages 靜態教學網站至 _site/
python3 build_site.py -o _site
```
