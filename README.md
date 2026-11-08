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

---

## 課程章節與基礎範例導覽（Course Table of Contents）

| 章節 | 主題名稱 | 核心學習重點 | 對應範例程式 |
| :---: | :--- | :--- | :--- |
| **Ch.01** | **陣列與單向鏈結串列（Array & Singly Linked List）** | 連續記憶體存取 $O(1)$ vs. 節點指標串接、插入與刪除操作 | `examples/ch01_array_linked_list.py` |
| **Ch.02** | **堆疊與佇列（Stack & Queue）** | 後進先出（LIFO）括號匹配檢查 vs. 先進先出（FIFO）排隊模型 | `examples/ch02_stack_queue.py` |
| **Ch.03** | **搜尋與排序演算法（Search & Sort）** | 二分搜尋法 $O(\log n)$、合併排序法（Merge Sort）$O(n \log n)$ | `examples/ch03_search_sort.py` |

## 執行範例與單元測試

```bash
# 執行各章節教學範例
python3 examples/ch01_array_linked_list.py
python3 examples/ch02_stack_queue.py
python3 examples/ch03_search_sort.py

# 執行完整單元測試套件
python3 -m unittest discover -s tests -v
```
