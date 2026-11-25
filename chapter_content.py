#!/usr/bin/env python3
"""
chapter_content.py - 紫楓 (Purple Maple) Python 3.12 教學站深度教材資料模型與結構化課綱。
採用零外部依賴標準庫 dataclasses 定義 Ch.01 ~ Ch.07 四大深度教學模組：
1. ComparisonTable（時間／空間複雜度與底層特性對照表）
2. WalkthroughStep（演算法逐步執行與記憶體指標狀態追蹤）
3. PitfallItem（CPython 3.12 底層實作原理與常見效能陷阱）
4. LeetCodeProblem & InterviewFAQ（白板題題號對應與技術面試深度問答）
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ComparisonTable:
    caption: str
    headers: tuple[str, ...]
    rows: tuple[tuple[str, ...], ...]


@dataclass(frozen=True)
class WalkthroughStep:
    step_label: str
    state_snapshot: str
    explanation: str


@dataclass(frozen=True)
class PitfallItem:
    title: str
    symptom: str
    root_cause_and_fix: str


@dataclass(frozen=True)
class LeetCodeProblem:
    number: int
    title: str
    difficulty: str
    pattern: str


@dataclass(frozen=True)
class InterviewFAQ:
    question: str
    answer: str


@dataclass(frozen=True)
class ChapterSpec:
    id: str
    badge: str
    title: str
    complexity: str
    summary: str
    concepts: tuple[str, ...]
    file: str
    lastmod: str
    keywords: tuple[str, ...]
    deep_intro: str
    comparison_table: ComparisonTable
    walkthrough_title: str
    walkthrough_steps: tuple[WalkthroughStep, ...]
    pitfalls: tuple[PitfallItem, ...]
    leetcode_problems: tuple[LeetCodeProblem, ...]
    interview_faqs: tuple[InterviewFAQ, ...]
    short_title: str = ""

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


CHAPTERS: tuple[ChapterSpec, ...] = (
    ChapterSpec(
        id="ch01",
        badge="Ch.01",
        title="Python 陣列（list）與單向鏈結串列（Array & Singly Linked List）",
        complexity="頭部插入 O(1) ・ 尾部附加 / 搜尋 / 刪除 / 原地反轉 O(n)",
        summary="完整解析 Python 陣列（list 動態陣列）與單向鏈結串列（Linked List）的連續記憶體配置、索引 O(1) 存取與指標串接差異，附 Python 3.12 Generic 實作與 O(1) 空間原地反轉。",
        concepts=(
            "連續記憶體 vs. 指標串接：陣列（Array / Python list）透過連續記憶體區塊支援 O(1) 隨機索引存取，但在頭部或中間插入元素需搬移後續元素（O(n)）；單向鏈結串列（Singly Linked List）則以 Node 節點與 next 指標動態串接，在已知頭節點時可於 O(1) 時間完成頭部插入（prepend）。",
            "白板題必考「原地反轉（In-place Reverse）」：透過 prev、curr、nxt 三個指標迭代翻轉 next 指向，不需額外建立新串列，空間複雜度嚴格控制在 O(1)，是軟體工程師面試最常出現的基礎題型。",
            "硬體快取親和性（CPU Cache Locality）：現代 CPU 讀取記憶體時會一次載入整條 Cache Line（通常 64 Bytes）。連續配置的陣列能充分受惠於空間局部性預先載入；而鏈結串列的節點散落於堆積（Heap）各處，頻繁追蹤指標容易觸發 Cache Miss。",
        ),
        file="examples/ch01_array_linked_list.py",
        lastmod="2026-11-24",
        keywords=(
            "Python 陣列",
            "Python list",
            "Python 鏈結串列",
            "Singly Linked List",
            "反轉鏈結串列",
            "Reverse Linked List",
            "Python list 底層原理",
            "陣列與鏈結串列比較",
            "LeetCode 206",
            "雙指標演算法",
        ),
        deep_intro=(
            "在學習所有進階演算法之前，軟體工程師必須先建立清晰的「記憶體物理模型」。"
            "電腦記憶體可視為一排編號連續的儲物櫃：陣列（Array）要求一次租下連續 N 個櫃位，"
            "因此只要知道起始位址（Base Address）與元素大小，CPU 就能用簡單的乘法與加法在 O(1) 常數時間內直接跳到第 i 個元素；"
            "然而一旦要在陣列最前面插入新資料，就必須把後面所有元素往後挪動一格，造成 O(n) 的搬移成本。"
            "相對地，單向鏈結串列（Singly Linked List）不要求連續空間，每個節點（ListNode）除了存放資料值 val 外，"
            "還存放指向下一個節點記憶體位址的參照指標 next。這種設計讓「在頭部插入或刪除節點」只需修改指標指向即可在 O(1) 完成，"
            "也是後續實作雜湊表鏈結桶位（Chaining Bucket）、LRU 快取（搭配雙向鏈結串列）與圖論鄰接串列的基石。"
        ),
        comparison_table=ComparisonTable(
            caption="陣列（Python list 動態陣列）、單向鏈結串列與雙向鏈結串列操作複雜度對照表",
            headers=("操作項目 ／ 結構特性", "Python list（動態陣列）", "單向鏈結串列（Singly Linked List）", "雙向鏈結串列（Doubly Linked List）"),
            rows=(
                ("依索引隨機讀取 (Index Access)", "O(1) — 基址加偏移量直接定位", "O(n) — 需從 head 依序走訪", "O(n) — 需從頭或尾依序走訪"),
                ("頭部插入 ／ 刪除 (Prepend / Pop Head)", "O(n) — 需搬移後續所有元素指標", "O(1) — 僅更新 head 指標指向", "O(1) — 更新 head 與 prev 指標"),
                ("尾部附加 (Append at Tail)", "均攤 O(1) — 滿載擴容時為 O(n)", "無 tail 指標 O(n) ／ 有 tail 指標 O(1)", "O(1) — 直接透過 tail 指標串接"),
                ("指定值搜尋 (Search by Value)", "O(n) — 線性掃描（已排序可二分 O(log n)）", "O(n) — 僅能單向線性巡覽", "O(n) — 線性巡覽"),
                ("已知節點下刪除自身 (Delete Given Node)", "O(n) — 需搬移後續元素填補空缺", "O(n) — 需先從頭尋找前驅節點 prev", "O(1) — 直接串接 prev 與 next"),
                ("CPU 快取親和性與額外記憶體", "高（連續指標陣列，Cache Locality 佳）", "低（每節點含 next 參照與物件標頭）", "低（每節點含 prev 與 next 雙參照）"),
            ),
        ),
        walkthrough_title="原地反轉單向鏈結串列（In-place Reverse）三指標逐步狀態追蹤",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1：初始狀態與指標設定（串列 5 -> 10 -> 30 -> None）",
                state_snapshot="prev = None | curr = Node(5) | head = Node(5)",
                explanation="在進入 while curr is not None 迴圈前，將前驅指標 prev 初始化為 None（因為原本的頭節點 Node(5) 在反轉後會變成新的尾節點，其 next 必須指向 None），當前指標 curr 則指向 head。",
            ),
            WalkthroughStep(
                step_label="Step 2：第一輪迭代 — 暫存下一個節點並翻轉 Node(5) 指標",
                state_snapshot="nxt = Node(10) | Node(5).next = None | prev = Node(5) | curr = Node(10)",
                explanation="關鍵第一步是先用 nxt = curr.next 備份 Node(10) 的位址，否則一旦執行 curr.next = prev 將 Node(5) 指向 None，後續串列就會永遠斷鏈遺失。接著將 prev 與 curr 同步往後推進一格。",
            ),
            WalkthroughStep(
                step_label="Step 3：第二輪迭代 — 翻轉中間節點 Node(10) 指向 Node(5)",
                state_snapshot="nxt = Node(30) | Node(10).next = Node(5) | prev = Node(10) | curr = Node(30)",
                explanation="先記錄 nxt = Node(30)，再將 Node(10).next 改指回 prev（即 Node(5)），形成局部反轉鏈 10 -> 5 -> None。隨後 prev 推進至 Node(10)，curr 推進至最後一個節點 Node(30)。",
            ),
            WalkthroughStep(
                step_label="Step 4：第三輪迭代與收尾 — 完成反轉並更新 self.head",
                state_snapshot="nxt = None | Node(30).next = Node(10) | prev = Node(30) | curr = None => self.head = prev",
                explanation="將 Node(30).next 指向 Node(10)，此時 curr 推進至 nxt（即 None）觸發迴圈結束。最後別忘了執行 self.head = prev，將串列頭指標正式指向 Node(30)，完成 30 -> 10 -> 5 -> None 的 O(1) 額外空間反轉。",
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="陷阱一：反轉或刪除節點時未先備份 curr.next 導致「斷鏈（Lost Reference）」",
                symptom="在撰寫 reverse() 時若先寫 curr.next = prev 再寫 curr = curr.next，迴圈跑完只剩一個節點，其餘節點全部消失。",
                root_cause_and_fix="一旦覆寫 curr.next，原本指向下一個節點的唯一參照就被洗掉了。正確順序永遠是：1. 先備份 nxt = curr.next → 2. 修改指標 curr.next = prev → 3. 推進 prev = curr → 4. 推進 curr = nxt。",
            ),
            PitfallItem(
                title="陷阱二：忽略刪除頭節點（head）或空串列的邊界條件（Edge Cases）",
                symptom="在實作 remove(target) 時直接存取 prev.next = curr.next，當待刪除目標剛好位於第一個節點（head）時拋出 AttributeError: 'NoneType' object has no attribute 'next'。",
                root_cause_and_fix="當目標位於頭節點時 prev 為 None，必須特判將 self.head = curr.next；實務白板題也常引入「虛擬頭節點（Dummy Head Node, dummy = ListNode(0, head)）」，讓包含頭節點在內的所有節點都擁有前驅節點，統一刪除邏輯。",
            ),
            PitfallItem(
                title="陷阱三：誤以為在 Python 中自訂 SinglyLinkedList 一定比內建 list 更省記憶體",
                symptom="為了節省記憶體而將數十萬筆整數改存在自訂的 Python ListNode 類別中，結果記憶體佔用反而暴增數倍且走訪速度變慢。",
                root_cause_and_fix="CPython 3.12 的內建 list 底層是 C 語言的 PyObject* 連續指標陣列（每個元素僅需 8 Bytes 指標空間加上預分配緩衝）；而每個自訂 Python ListNode 實例都帶有完整的 PyObject 標頭與屬性結構（即便加上 slots 也遠大於 8 Bytes）。在工程實務中，除非需要高頻率的雙端操作（此時應選用 collections.deque）或教學演練，否則隨機存取一律優先使用內建 list。",
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(206, "Reverse Linked List（反轉單向鏈結串列）", "Easy", "三指標原地迭代反轉 ／ 遞迴反轉 ・ 時間 O(n) / 空間 O(1)"),
            LeetCodeProblem(21, "Merge Two Sorted Lists（合併兩個已排序鏈結串列）", "Easy", "虛擬頭節點（Dummy Node）＋雙指標拉鍊合併 ・ 時間 O(n + m) / 空間 O(1)"),
            LeetCodeProblem(141, "Linked List Cycle（環路檢測）", "Easy", "Floyd 龜兔賽跑演算法（快慢雙指標 Fast & Slow Pointers） ・ 時間 O(n) / 空間 O(1)"),
            LeetCodeProblem(19, "Remove Nth Node From End of List（刪除倒數第 N 個節點）", "Medium", "快指標先走 N 步＋虛擬頭節點單次掃描 ・ 時間 O(n) / 空間 O(1)"),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="為什麼 Python 的 list.append() 時間複雜度是「均攤 O(1)（Amortized O(1)）」，但 list.insert(0, val) 卻是 O(n)？",
                answer="CPython 的 list 採用動態陣列（Dynamic Array）實作，底層配置空間時會進行「超額配置（Over-allocation）」，預留額外空位。因此絕大多數 append() 只需在尾端空位寫入指標，耗時 O(1)；僅在容量滿載時才重新申請約 1.125 倍的新陣列並複製舊指標，將該次 O(n) 成本平攤到每次插入後即為均攤 O(1)。相反地，list.insert(0, val) 必須將索引 0 之後的所有元素指標全部往右搬移一格以騰出首格空間，每次呼叫都必然消耗 O(n) 時間。",
            ),
            InterviewFAQ(
                question="面試官要求在 O(1) 額外空間內判斷單向鏈結串列是否有環（Cycle），且不能修改節點結構，該如何實作？",
                answer="標準解法為「Floyd 龜兔賽跑演算法（快慢雙指標）」。設定慢指標 slow = head（每次走 1 步：slow = slow.next）與快指標 fast = head（每次走 2 步：fast = fast.next.next）。若串列不存在環，fast 會率先抵達 None；若串列存在環，進入環後快指標每輪與慢指標的距離會縮短 1 步，最終必定在環內某個節點相遇（slow is fast），時間複雜度 O(n)，且只使用兩個指標變數，空間複雜度為嚴格的 O(1)。",
            ),
            InterviewFAQ(
                question="在什麼情況下，我們需要在鏈結串列題目中使用「虛擬頭節點（Dummy Node）」？",
                answer="當題目的操作可能會「改變、刪除或替換原本的頭節點（head）」時（例如：合併兩個排序串列 LeetCode #21、刪除特定值的所有節點 #203、刪除倒數第 N 個節點 #19、區間反轉 #92），若不使用 Dummy Node，就必須寫大量 if prev is None 的分支來特別處理頭節點。先建立 dummy = ListNode(0, head) 並讓 prev = dummy，所有真實節點（包含原 head）就都成為某個節點的 next，處理完畢後直接 return dummy.next 即可，程式碼簡潔且不易出錯。",
            ),
            InterviewFAQ(
                question="Python 陣列（array）跟 list（串列）有什麼差別？寫程式該用 list、array.array 還是 NumPy 陣列？",
                answer="Python 內建的 list 本質上是「動態指標陣列」，可混裝任意型態元素，隨機存取 O(1)、尾端 append 均攤 O(1)，是日常開發與演算法刷題的首選。標準庫 array.array 則只存放單一 C 原始型態（如 int32 / float64），記憶體更緊湊，適合需要節省 RAM 或對接二進位串流的場景。若涉及大量數值運算與矩陣操作，則應改用 NumPy ndarray，透過連續記憶體與底層 C/SIMD 向量化加速達到數十倍效能提升。",
            ),
        ),
    ),
    ChapterSpec(
        id="ch02",
        badge="Ch.02",
        title="堆疊與佇列（Stack & Queue）",
        complexity="Push / Pop / Enqueue / Dequeue 均為 O(1)",
        summary="掌握後進先出（LIFO）與先進先出（FIFO）兩大抽象資料型態（ADT），並透過 Stack 實作經典的面試常考題：多層括號平衡檢查器。",
        concepts=(
            "堆疊（Stack，後進先出 LIFO）：如同疊盤子，最後放入的元素最先取出。常用於函式呼叫堆疊（Call Stack）、瀏覽器上一頁紀錄、語法括號匹配檢查與深度優先搜尋（DFS）。",
            "佇列（Queue，先進先出 FIFO）：如同排隊買票，最先進入的元素最先處理。在 Python 中切勿使用 list.pop(0)（會導致 O(n) 記憶體搬移），應採用 collections.deque 雙端佇列達成真正的 O(1) 雙端操作，廣泛應用於廣度優先搜尋（BFS）與非同步任務佇列。",
            "單調堆疊（Monotonic Stack）進階模式：在維護堆疊 LIFO 特性的同時，強制保持堆疊內元素呈遞增或遞減順序，能在 O(n) 線性時間內解決「下一個更大元素（Next Greater Element）」與「直方圖最大矩形面積」等中高階面試題。",
        ),
        file="examples/ch02_stack_queue.py",
        lastmod="2026-11-17",
        keywords=(
            "Python 堆疊",
            "Python 佇列",
            "Stack and Queue",
            "collections.deque",
            "括號平衡檢查",
            "Valid Parentheses",
            "LIFO FIFO",
            "LeetCode 20",
        ),
        deep_intro=(
            "堆疊（Stack）與佇列（Queue）並非特定的硬體記憶體排列方式，而是定義了「資料進出順序契約」的抽象資料型態（Abstract Data Type, ADT）。"
            "透過限制資料只能在特定端點進行讀寫，我們能讓複雜的程式狀態變得高度可預測。"
            "堆疊遵循「後進先出（Last-In, First-Out, LIFO）」原則：作業系統管理每個執行緒的函式呼叫堆疊（Call Stack）、"
            "編譯器解析巢狀算式與括號匹配、文字編輯器的 Undo 復原功能，背後全都是 Stack 在運作。"
            "佇列則遵循「先進先出（First-In, First-Out, FIFO）」原則：從作業系統的 CPU 排程器、網路封包緩衝區（Buffer）、"
            "微服務架構中的訊息佇列（Message Queue），到圖論演算法中尋找最短路徑的廣度優先搜尋（BFS），都仰賴 Queue 確保公平與逐層處理順序。"
        ),
        comparison_table=ComparisonTable(
            caption="堆疊（Stack）、雙端佇列（collections.deque）與錯誤佇列寫法（list.pop(0)）效能對照表",
            headers=("資料結構 ／ 實作方式", "核心順序模型", "寫入操作（Push / Enqueue）", "取出操作（Pop / Dequeue）", "工程實戰建議與適用場景"),
            rows=(
                ("Stack（底層封裝 Python list）", "後進先出 (LIFO)", "list.append(x) — 均攤 O(1)", "list.pop() — O(1)", "推薦！記憶體緊湊且尾端操作極速，適用括號匹配、DFS、復原紀錄"),
                ("Queue（底層封裝 collections.deque）", "先進先出 (FIFO)", "deque.append(x) — O(1)", "deque.popleft() — O(1)", "推薦！底層為雙向區塊鏈結串列，雙端讀寫皆為嚴格 O(1)，適用 BFS 與任務排程"),
                ("錯誤 Queue（使用 list.pop(0)）", "先進先出 (FIFO)", "list.append(x) — 均攤 O(1)", "list.pop(0) — O(n) 災難", "嚴禁在刷題或大型佇列中使用！每次 pop(0) 都會搬移整排陣列導致 TLE"),
                ("執行緒安全佇列（queue.Queue）", "先進先出 (FIFO)", "put(x) — O(1) 含鎖定開銷", "get() — O(1) 含鎖定開銷", "內建 Mutex 鎖，專供多執行緒（Multi-threading）生產者／消費者模型使用"),
                ("單調堆疊（Monotonic Stack）", "具單調性之 LIFO", "每個元素最多入堆疊 1 次 — 均攤 O(1)", "違反單調性即彈出 — 均攤 O(1)", "搜尋陣列中每個元素「左側／右側第一個更大或更小值」的 O(n) 利器"),
            ),
        ),
        walkthrough_title="多層括號平衡檢查（is_balanced_brackets('{[()]}')）堆疊狀態逐步追蹤",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1：依序讀取左括號 '{'、'['、'(' — 全數推入堆疊",
                state_snapshot="輸入字元: '{' -> '[' -> '(' | Stack 內部狀態（底 -> 頂）: ['{', '[', '(']",
                explanation="當掃描到任何開括號（屬於 opening 集合 {'(', '[', '{'}）時，表示開啟了一個尚未閉合的語法範疇，直接呼叫 stack.push(ch) 將其壓入堆疊頂端等待後續配對。",
            ),
            WalkthroughStep(
                step_label="Step 2：讀取第一個右括號 ')' — 檢查堆疊頂端是否為對應的 '('",
                state_snapshot="輸入字元: ')' | 查表 pairs[')'] == '(' | stack.pop() -> '('（配對成功）| Stack 剩餘: ['{', '[']",
                explanation="遇到閉括號 ')' 時，根據 LIFO 原則，它必須與「最近一次出現且尚未閉合的左括號」配對。此時檢查堆疊非空，且彈出的頂端元素正好是 '('，該層小括號成功抵銷。",
            ),
            WalkthroughStep(
                step_label="Step 3：依序讀取 ']' 與 '}' — 逐層往外彈出配對",
                state_snapshot="讀取 ']': pop() 得 '[' ✓ | 讀取 '}': pop() 得 '{' ✓ | Stack 剩餘: []",
                explanation="接著遇到 ']' 與 '}'，分別與堆疊頂端的 '[' 及 '{' 完美匹配並彈出。若途中遇到如 '([)]' 的交錯情況，stack.pop() 彈出的會是 '(' 而非 '['，函式便會立即回傳 False。",
            ),
            WalkthroughStep(
                step_label="Step 4：字串掃描完畢 — 檢查 stack.is_empty() 確認無殘留左括號",
                state_snapshot="迴圈結束 | stack.is_empty() == True => 最終回傳 True",
                explanation="走訪完所有字元後，不能直接回傳 True，必須檢查 stack.is_empty()！因為若輸入為 '((('，迴圈中不會觸發任何錯誤，唯有確認堆疊已完全清空，才能保證所有左括號都找到對應的右括號。",
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="陷阱一：在 BFS 或佇列題目中寫出 queue.pop(0) 造成隱藏版 O(n²) 超時（TLE）",
                symptom="演算法邏輯完全正確，小測資秒過，但在 LeetCode 遇到 N = 10^5 節點的圖或樹時直接 Time Limit Exceeded。",
                root_cause_and_fix="Python 的 list 是連續記憶體陣列，呼叫 list.pop(0) 刪除首元素後，CPython 必須呼叫 memmove 將後面 N-1 個指標全部往前搬移一格，單次耗時 O(n)，N 次出佇列總耗時變成 O(n²)。請務必養成習慣：只要需要 FIFO 佇列，第一行先寫 from collections import deque，並以 popleft() 取代 pop(0)。",
            ),
            PitfallItem(
                title="陷阱二：對空堆疊執行 pop() 或 peek() 前忘記檢查 is_empty()",
                symptom="在括號匹配中遇到以右括號開頭的字串（例如 ')()' 或 ']'），程式直接崩潰拋出 IndexError: pop from empty list。",
                root_cause_and_fix="任何會從 Stack 或 Queue 取出或查看頂端元素的邏輯（包含括號匹配、單調堆疊 while stack and stack[-1] < cur），都必須將 not stack.is_empty()（或布林判斷 if stack:）放在條件判斷的最左側，利用短路求值（Short-circuit evaluation）保護後續的 pop/peek 操作。",
            ),
            PitfallItem(
                title="陷阱三：括號檢查結束時直接 return True，漏判「只有左括號」的輸入",
                symptom="測試輸入 '(((' 或 '{[' 時，函式錯誤回傳 True。",
                root_cause_and_fix="迴圈內的檢查只負責抓出「右括號多餘」或「括號種類不匹配」；若輸入字串全都是左括號，迴圈只會一直 push 而不會進入 elif 分支。因此函式最後一行必須寫 return stack.is_empty()，確保所有開啟的括號皆已閉合。",
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(20, "Valid Parentheses（有效的括號）", "Easy", "Stack 堆疊配對與空堆疊邊界檢查 ・ 時間 O(n) / 空間 O(n)"),
            LeetCodeProblem(232, "Implement Queue using Stacks（用兩個堆疊實作佇列）", "Easy", "輸入堆疊 in_stack ＋ 輸出堆疊 out_stack 惰性倒轉 ・ 均攤時間 O(1)"),
            LeetCodeProblem(155, "Min Stack（最小堆疊）", "Medium", "主堆疊搭配輔助最小值堆疊（或差值壓縮） ・ getMin 時間 O(1)"),
            LeetCodeProblem(739, "Daily Temperatures（每日溫度）", "Medium", "單調遞減堆疊（Monotonic Decreasing Stack 存索引） ・ 時間 O(n) / 空間 O(n)"),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="Python 的 collections.deque 底層是如何實作的？為什麼它能同時支援頭尾 O(1) 插入與刪除，卻不適合用來隨機讀取中間元素？",
                answer="CPython 的 deque（Double-Ended Queue）底層並非單一連續陣列，而是由多個固定長度（通常為 64 個元素指標）的區塊（Block）所組成的「雙向鏈結串列（Doubly Linked List of Blocks）」。因為維護了指向頭尾區塊的指標與偏移量，在頭尾兩端執行 append()、appendleft()、pop()、popleft() 都只需在當前區塊增減或分配新區塊，時間複雜度為嚴格的 O(1)；但若執行 d[i] 存取中間索引，則必須跨越區塊鏈結逐一走訪，時間複雜度會退化為 O(n)。",
            ),
            InterviewFAQ(
                question="如何只用兩個 Stack（LIFO）實作出一個支援均攤 O(1) 操作的 Queue（FIFO，LeetCode #232）？",
                answer="準備兩個堆疊：in_stack（專門負責接收 enqueue 新元素）與 out_stack（專門負責提供 dequeue 與 peek）。當呼叫 enqueue(x) 時，直接將 x 壓入 in_stack（O(1)）。當呼叫 dequeue() 或 peek() 時，若 out_stack 不為空，直接從 out_stack 彈出頂端元素（O(1)）；若 out_stack 為空，才將 in_stack 中的所有元素逐一彈出並壓入 out_stack（經歷兩次 LIFO 翻轉後，最先進入的元素就會浮到 out_stack 最頂端）。由於每個元素一輩子只會進 in_stack 一次、轉移到 out_stack 一次、出 out_stack 一次，因此均攤時間複雜度為 O(1)。",
            ),
            InterviewFAQ(
                question="什麼是「單調堆疊（Monotonic Stack）」？遇到什麼特徵的題目應該立刻聯想到它？",
                answer="單調堆疊是指堆疊內的元素由底到頂始終維持單調遞增或單調遞減的順序。當新元素準備入堆疊前，會透過 while 迴圈將堆疊頂端所有破壞單調性的元素彈出。只要題目要求在陣列中尋找每個元素「左邊或右邊第一個比它大（或比它小）的元素位置」（例如 LeetCode #739 每日溫度、#496 下一個更大元素、#84 柱狀圖中最大的矩形），使用暴力雙層迴圈需 O(n²)，改用單調堆疊存放索引，每個元素最多入堆疊一次、出堆疊一次，即可在 O(n) 時間內完美解決。",
            ),
        ),
    ),
    ChapterSpec(
        id="ch03",
        badge="Ch.03",
        title="搜尋與排序演算法（Search & Sort Algorithms）",
        complexity="二分搜尋法 O(log n) ・ 合併排序法（Merge Sort）O(n log n)",
        summary="比較線性搜尋與二分搜尋的效率跨越，並以分治法（Divide & Conquer）實作穩定排序演算法 Merge Sort。",
        concepts=(
            "二分搜尋法（Binary Search）：在「已排序」的序列中，每次比對中間元素即可排除一半搜尋範圍，將搜尋複雜度由線性 O(n) 大幅降至對數級 O(log n)（100 萬筆資料最多只需比對約 20 次）。",
            "合併排序法（Merge Sort）：經典的「分治法（Divide and Conquer）」演算法，先遞迴將陣列對半拆解至單一元素，再以雙指標（Two Pointers）線性合併兩個已排序子陣列。無論最佳、平均或最壞情況，時間複雜度皆穩定維持 O(n log n)，且具備穩定排序（Stable Sort）特性。",
            "穩定排序（Stability）與 Timsort：當兩個元素鍵值相等時，若排序後仍能保證它們原本的先後相對順序不變，即稱為穩定排序。Python 內建的 sorted() 與 list.sort() 採用結合了 Merge Sort 與 Insertion Sort 優點的 Timsort，正是穩定且實務極速的排序演算法。",
        ),
        file="examples/ch03_search_sort.py",
        lastmod="2026-11-17",
        keywords=(
            "二分搜尋法",
            "Binary Search",
            "合併排序法",
            "Merge Sort",
            "分治法 Divide and Conquer",
            "Python 排序演算法",
            "Timsort",
            "時間複雜度 O(n log n)",
        ),
        deep_intro=(
            "搜尋（Searching）與排序（Sorting）是電腦科學中最核心的演算法基石。"
            "當資料雜亂無章時，要在 N 筆資料中尋找特定目標，唯一的辦法是從頭到尾逐一比對（線性搜尋 Linear Search，時間複雜度 O(n)）。"
            "然而一旦資料經過「排序」整理為單調遞增序列，我們就能施展「二分搜尋法（Binary Search）」——每次直接檢查區間正中央的元素，"
            "若目標較大就捨棄左半部、若目標較小就捨棄右半部。每比對一次，問題規模就瞬間減半："
            "面對 10 億（10^9）筆已排序資料，線性搜尋最差要跑 10 億次，二分搜尋卻只需要最多 30 次比對（log2(10^9) ≈ 29.89）！"
            "為了將無序資料高效轉化為有序序列，本章透過「分治法（Divide and Conquer）」實作合併排序法（Merge Sort），"
            "將 O(n²) 的基礎排序瓶頸一舉突破至理論下限 O(n log n)。"
        ),
        comparison_table=ComparisonTable(
            caption="主流搜尋與排序演算法之時間複雜度、空間複雜度與穩定性完整對照表",
            headers=("演算法名稱", "最佳時間", "平均時間", "最差時間", "額外空間複雜度與穩定性（Stability）"),
            rows=(
                ("線性搜尋 (Linear Search)", "O(1)", "O(n)", "O(n)", "空間 O(1) ・ 不需事先排序"),
                ("二分搜尋 (Binary Search)", "O(1)", "O(log n)", "O(log n)", "迭代版空間 O(1) ・ 前提：序列必須已排序（或具單調性）"),
                ("插入排序 (Insertion Sort)", "O(n)", "O(n²)", "O(n²)", "空間 O(1) ・ 穩定排序（小規模或近乎有序資料極快）"),
                ("合併排序 (Merge Sort)", "O(n log n)", "O(n log n)", "O(n log n)", "空間 O(n) ・ 穩定排序（保證無 O(n²) 最壞退化）"),
                ("快速排序 (Quick Sort)", "O(n log n)", "O(n log n)", "O(n²)", "空間 O(log n) 遞迴堆疊 ・ 不穩定排序（Pivot 選取不當時退化）"),
                ("堆積排序 (Heap Sort)", "O(n log n)", "O(n log n)", "O(n log n)", "空間 O(1) 原地排序 ・ 不穩定排序"),
                ("Python Timsort (sorted / .sort)", "O(n)", "O(n log n)", "O(n log n)", "空間 O(n) ・ 穩定排序（結合自然連續區段 Run 與二分插入）"),
            ),
        ),
        walkthrough_title="合併排序法（Merge Sort）分治拆解與雙指標合併逐步追蹤",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1：遞迴拆分階段（Divide）— 對半切分直到子陣列長度 <= 1",
                state_snapshot="[38, 27, 43, 3] => 左半 [38, 27] 與 右半 [43, 3] => 基底 [38], [27], [43], [3]",
                explanation="merge_sort() 利用 mid = len(arr) // 2 持續遞迴切分左右半部。當子陣列只剩 1 個元素（len(arr) <= 1）時，單一元素本身即為已排序狀態，直接回傳作為遞迴基底（Base Case）。",
            ),
            WalkthroughStep(
                step_label="Step 2：底層雙指標合併（Conquer Level 1）— 兩兩合併為長度 2 的有序子陣列",
                state_snapshot="合併 [38] 與 [27] -> [27, 38] | 合併 [43] 與 [3] -> [3, 43]",
                explanation="在每一層遞迴返回時，利用雙指標 i=0, j=0 比較左右兩個已排序子陣列的最前端元素，將較小者優先放入 merged 陣列，形成局部有序的 [27, 38] 與 [3, 43]。",
            ),
            WalkthroughStep(
                step_label="Step 3：頂層雙指標拉鍊式合併（Conquer Level 2）— 比較 [27, 38] 與 [3, 43]",
                state_snapshot="比對 27 vs 3 (取 3) -> 比對 27 vs 43 (取 27) -> 比對 38 vs 43 (取 38) -> 尾端補齊 43",
                explanation="i 指向 [27, 38] 開頭、j 指向 [3, 43] 開頭：1. 3 < 27 取 3（j=1）；2. 27 <= 43 取 27（i=1）；3. 38 <= 43 取 38（i=2 抵達左半尾端）；4. 將右半剩餘的 [43] 直接 extend 附加至結果尾端。",
            ),
            WalkthroughStep(
                step_label="Step 4：在排序結果上執行二分搜尋（binary_search([3, 9, 10, 27, 38, 43, 82], 27)）",
                state_snapshot="left = 0, right = 6 => mid = 3 => sorted_nums[3] == 27（一擊命中索引 3！）",
                explanation="完整 7 個元素排序後為 [3, 9, 10, 27, 38, 43, 82]。二分搜尋計算 mid = 0 + (6 - 0) // 2 = 3，讀取索引 3 的值恰好就是 27，僅比對 1 次即回傳索引 3。",
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="陷阱一：二分搜尋邊界更新寫成 left = mid 或 right = mid 導致無窮迴圈",
                symptom="在閉區間 [left, right]（迴圈條件 while left <= right）搜尋不存在的元素時，程式卡死在 left == right 的無窮迴圈。",
                root_cause_and_fix="當搜尋區間定義為閉區間 [left, right] 時，一旦確認 sorted_nums[mid] != target，索引 mid 本身已經被排除！因此下一輪搜尋範圍必須嚴格縮小為 left = mid + 1 或 right = mid - 1，確保每次迭代區間長度至少減少 1。",
            ),
            PitfallItem(
                title="陷阱二：合併排序比較條件誤寫成 < 而非 <=，破壞穩定排序（Stability）特性",
                symptom="在合併左右子陣列時寫 if left_half[i] < right_half[j]:，導致相同鍵值的元素在排序後順序被顛倒。",
                root_cause_and_fix="當左半部元素與右半部元素相等（left_half[i] == right_half[j]）時，因為左半部元素在原始陣列中排在前面，必須優先選取左半部元素（使用 left_half[i] <= right_half[j]），才能保證相等元素的相對先後順序維持不變。",
            ),
            PitfallItem(
                title="陷阱三：其他語言轉來的整數溢位（Integer Overflow）與 Python 實戰標準庫 bisect",
                symptom="在 C++/Java 寫 mid = (left + right) / 2 當 left + right > 2^31 - 1 時會發生正整數溢位變負數。",
                root_cause_and_fix="雖然 Python 3 的 int 支援任意精度大整數不會溢位，但在跨語言面試中寫 mid = left + (right - left) // 2 能展現優秀的工程防禦習慣。此外在 Python 實務開發與競賽中，可直接呼叫標準庫 bisect.bisect_left(arr, target)（C 語言底層實作）進行極速二分查找。",
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(704, "Binary Search（標準二分搜尋）", "Easy", "閉區間 [left, right] 模板 ・ 時間 O(log n) / 空間 O(1)"),
            LeetCodeProblem(33, "Search in Rotated Sorted Array（搜尋旋轉排序陣列）", "Medium", "利用 mid 判斷哪一半部維持單調遞增再縮小區間 ・ 時間 O(log n)"),
            LeetCodeProblem(34, "Find First and Last Position of Element in Sorted Array", "Medium", "左右邊界二分搜尋（bisect_left / bisect_right） ・ 時間 O(log n)"),
            LeetCodeProblem(912, "Sort an Array（排序陣列）", "Medium", "手寫 Merge Sort 分治排序避免 Quick Sort 最差 O(n²) 退化 ・ 時間 O(n log n)"),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="為什麼合併排序法（Merge Sort）的時間複雜度是 O(n log n)？能用直觀的方式推導嗎？",
                answer="將長度為 n 的陣列不斷對半切分，直到長度為 1，總共需要切分 log2(n) 層（即遞迴樹的高度為 log n + 1）。而在遞迴樹的「每一層」中，無論子陣列被切成幾份，將該層所有子陣列透過雙指標線性掃描合併起來的總元素個數剛好都是 n，因此每一層的合併工作量固定為 O(n)。將「每層工作量 O(n)」乘以「總層數 O(log n)」，即得出無論資料原本順序為何，總時間複雜度恆為 O(n log n)。",
            ),
            InterviewFAQ(
                question="既然 Quick Sort 平均也很快且是原地排序，為什麼 Python 內建的 sorted() 與 list.sort() 選擇以 Merge Sort 為基礎的 Timsort？",
                answer="主要有兩大原因：第一是「穩定性（Stability）」，Python 保證多重條件排序時相等元素的原始相對順序不變（例如先按分數排序再按部門排序），而原地 Quick Sort 是不穩定排序；第二是「真實世界資料局部有序性」，真實應用中的陣列往往包含許多已經排好序的連續區段（稱為 Natural Runs），Timsort 會自動偵測這些有序區段並用二分插入排序擴展，再用聰明的 Galloping 模式合併，使已排序或近乎有序的陣列能在 O(n) 最佳時間內瞬間完成排序。",
            ),
            InterviewFAQ(
                question="二分搜尋法只能用在「找某個數字是否存在於排序陣列」嗎？還有什麼進階應用？",
                answer="二分搜尋的本質並非「搜尋陣列元素」，而是「在具有單調性（Monotonicity）的解空間上尋找轉折邊界」。只要問題滿足「若答案 X 可行，則所有大於 X 的值也都可行；若 X 不可行，則所有小於 X 的值也都不可行」，就能直接「對答案本身進行二分搜尋（Binary Search on Answer）」！常見題型包含：愛吃香蕉的珂珂（LeetCode #875 求最小吃蕉速度）、在 D 天內送達包裹的最低運載能力（#1011）與分割陣列的最大值（#410）。",
            ),
        ),
    ),
    ChapterSpec(
        id="ch04",
        badge="Ch.04",
        title="雜湊表與二元搜尋樹（Hash Table & Binary Search Tree）",
        complexity="雜湊表平均讀寫 O(1) ・ 二元搜尋樹平衡搜尋/插入 O(log n) ・ 中序走訪 O(n)",
        summary="掌握面試出場率最高的雜湊碰撞處理（Separate Chaining）與 Two Sum O(n) 秒殺技巧，並實作二元搜尋樹（BST）與中序遞增走訪。",
        concepts=(
            "雜湊表（Hash Table / Python dict）：透過雜湊函式（Hash Function）將鍵值映射至桶位索引，達成平均 O(1) 的極速查找；當不同鍵值落入同一桶位產生碰撞（Collision）時，常以鏈結法（Separate Chaining）或開放定址法（Open Addressing）化解。經典白板題 Two Sum 即是利用 Hash Table 以空間換取時間，將雙層迴圈 O(n²) 降至單次掃描 O(n)。",
            "二元搜尋樹（Binary Search Tree, BST）：滿足「左子樹所有節點 < 根節點 < 右子樹所有節點」不變量（Invariant）的樹狀結構。在樹高平衡時搜尋與插入皆為 O(log n)，且對 BST 執行「左 -> 根 -> 右」中序走訪（In-order Traversal）即可在 O(n) 時間內直接輸出由小到大的排序結果。",
            "負載因子（Load Factor）與動態擴容（Rehashing）：當雜湊表內的元素數量 N 與桶位總數 M 的比值（α = N / M）過高時，碰撞機率會急劇上升；現代雜湊表會在 α 超過門檻（如 CPython dict 為 2/3）時自動擴增桶位並重新計算雜湊位置。",
        ),
        file="examples/ch04_hash_bst.py",
        lastmod="2026-11-17",
        keywords=(
            "Python 雜湊表",
            "Hash Table",
            "Two Sum 解法",
            "二元搜尋樹",
            "Binary Search Tree BST",
            "雜湊碰撞 Separate Chaining",
            "中序走訪 Inorder Traversal",
            "LeetCode 1",
        ),
        deep_intro=(
            "在軟體工程技術面試中，如果有一句話能幫你解開一半以上的演算法題，那就是：「當遇到 O(n²) 的重複查找瓶頸時，先想能不能用雜湊表（Hash Table）以空間換取時間！」"
            "雜湊表透過雜湊函式 `hash(key) % bucket_count` 將任意可雜湊鍵值直接轉換為陣列索引，實現平均 O(1) 的增刪查改。"
            "然而雜湊表是「無序」的（雖然 Python 3.7+ 的 dict 保留了插入順序，但並非依鍵值大小排序），無法高效回答「大於 X 且小於 Y 的所有元素」或「排名第 K 小的元素」。"
            "這正是二元搜尋樹（Binary Search Tree, BST）登場的時刻：BST 嚴格遵守「左子樹所有值 < 根節點 < 右子樹所有值」的結構不變量，"
            "不僅支援平均 O(log n) 的動態插入與搜尋，還能透過中序走訪（In-order Traversal）天然產生遞增有序序列。"
        ),
        comparison_table=ComparisonTable(
            caption="雜湊表（Hash Table）、平衡二元搜尋樹与退化斜樹之複雜度與功能特性對照表",
            headers=("操作項目 ／ 結構特性", "雜湊表（Hash Table / dict）", "平衡二元搜尋樹（Balanced BST）", "退化二元搜尋樹（Skewed BST 最差情況）"),
            rows=(
                ("單一鍵值查找 (Search / Get)", "平均 O(1) ／ 碰撞最差 O(n)", "O(log n) — 每次比較排除半棵子樹", "O(n) — 退化為單向鏈結串列"),
                ("插入與更新 (Insert / Put)", "均攤 O(1) ／ 擴容時 O(n)", "O(log n) — 含旋轉平衡維護", "O(n) — 依序走訪至最深葉節點"),
                ("刪除鍵值 (Remove / Delete)", "平均 O(1)", "O(log n) — 尋找中序後繼替換", "O(n) — 線性搜尋後刪除"),
                ("依鍵值大小順序輸出全部元素", "O(n log n) — 需額外呼叫 sorted()", "O(n) — 直接執行中序走訪 (In-order)", "O(n) — 中序走訪"),
                ("區間範圍查詢 (Range Query [L, R])", "O(n) — 必須全表掃描過濾", "O(log n + k) — 剪枝跳過無關子樹", "O(n) — 無法有效剪枝"),
                ("鍵值型別限制 (Key Constraint)", "必須可雜湊且不可變 (Hashable)", "必須支援大小比較運算 (<, >)", "必須支援大小比較運算 (<, >)"),
            ),
        ),
        walkthrough_title="Two Sum O(n) 單次雜湊掃描與 BST 中序走訪（In-order）逐步狀態追蹤",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1：Two Sum 掃描索引 0（nums = [2, 7, 11, 15], target = 9）",
                state_snapshot="idx = 0, num = 2 | complement = 9 - 2 = 7 | 7 not in seen | 寫入 seen = {2: 0}",
                explanation="讀取第一個數字 2，計算它需要的互補數 complement = 9 - 2 = 7。查詢雜湊表 seen 發現 7 尚未出現，因此將當前數值與索引 {2: 0} 存入 seen 字典中。",
            ),
            WalkthroughStep(
                step_label="Step 2：Two Sum 掃描索引 1 — O(1) 瞬間命中互補數並回傳",
                state_snapshot="idx = 1, num = 7 | complement = 9 - 7 = 2 | 2 in seen (索引 0) => 回傳 (0, 1)",
                explanation="讀取第二個數字 7，計算 complement = 9 - 7 = 2。查詢 seen 字典在 O(1) 時間內發現鍵值 2 已存在且對應索引為 0，立即回傳 (0, 1)，省去雙層迴圈的重複配對。",
            ),
            WalkthroughStep(
                step_label="Step 3：建立二元搜尋樹（依序插入 [50, 30, 70, 20, 40, 60, 80]）",
                state_snapshot="Root = 50 | 左子樹: 30 (左 20, 右 40) | 右子樹: 70 (左 60, 右 80)",
                explanation="第一個元素 50 成為根節點；30 < 50 進入左子樹、70 > 50 進入右子樹；接著 20 < 30 掛在 30 左側、40 > 30 掛在 30 右側，形成高度平衡的三層完美二元搜尋樹。",
            ),
            WalkthroughStep(
                step_label="Step 4：執行中序走訪（左子樹 -> 根節點 -> 右子樹）輸出排序序列",
                state_snapshot="走訪順序: (20 -> 30 -> 40) -> 50 -> (60 -> 70 -> 80) => [20, 30, 40, 50, 60, 70, 80]",
                explanation="遞迴函式 _traverse 先一路往左深入到最左葉節點 20 印出，回到父節點 30 印出，再訪問右子節點 40；完成左半部後印出根節點 50，最後以相同邏輯走訪右子樹，不需任何額外排序即得遞增陣列。",
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="陷阱一：將可變容器（如 list、dict、set）當作雜湊表的 Key 觸發 TypeError",
                symptom="在分組題（如 Group Anagrams）中嘗試寫 seen[[1, 2, 3]] = val，執行時直接拋出 TypeError: unhashable type: 'list'。",
                root_cause_and_fix="雜湊表要求 Key 的雜湊值在生命週期內永遠不可改變（否則修改內容後雜湊值改變，就再也找不到原本的桶位）。在 Python 中，若需以序列作為字典的 Key，必須先轉為不可變的 tuple(my_list)；若需以集合為 Key，則應轉為 frozenset(my_set)。",
            ),
            PitfallItem(
                title="陷阱二：將「已排序陣列」直接依序插入普通 BST，導致樹高退化為 O(n) 斜樹",
                symptom="若依序將 [10, 20, 30, 40, 50] 插入未自平衡的 BinarySearchTree，搜尋時間從 O(log n) 退化成 O(n)。",
                root_cause_and_fix="因為每個新數字都比前一個大，所有節點都會一路掛在右側（right child），使二元搜尋樹徹底退化為一條單向鏈結串列。若已知輸入為已排序陣列，應每次取正中央元素 arr[mid] 作為根節點並遞迴建構左右子樹（LeetCode #108）；在工程系統中則會採用紅黑樹（Red-Black Tree）或 AVL 樹透過旋轉維持平衡。",
            ),
            PitfallItem(
                title="陷阱三：驗證二元搜尋樹（Validate BST）時只檢查「左子節點 < 父節點 < 右子節點」",
                symptom="面對根節點為 50、左子節點為 30，但 30 的右子節點為 60 的樹時，錯誤判定為合法 BST（實際上 60 > 50 不應出現在 50 的左子樹中）。",
                root_cause_and_fix="BST 的不變量要求「左子樹的所有後代節點」都必須嚴格小於根節點。正確驗證方式有兩種：1. 在遞迴時傳遞開區間上下界 validate(node, low, high)，確保 low < node.val < high；2. 執行中序走訪，檢查輸出的序列是否嚴格單調遞增。",
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(1, "Two Sum（兩數之和）", "Easy", "Hash Table 記錄已訪問數值與索引單次掃描 ・ 時間 O(n) / 空間 O(n)"),
            LeetCodeProblem(49, "Group Anagrams（字母異位詞分組）", "Medium", "將排序後字元 tuple 或 26 字母計數 tuple 作為 dict Key ・ 時間 O(n * k)"),
            LeetCodeProblem(98, "Validate Binary Search Tree（驗證二元搜尋樹）", "Medium", "遞迴傳遞 (low, high) 上下界或中序嚴格遞增檢查 ・ 時間 O(n)"),
            LeetCodeProblem(230, "Kth Smallest Element in a BST（BST 中第 K 小的元素）", "Medium", "中序走訪第 K 個訪問到的節點即為所求 ・ 時間 O(H + k)"),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="本講義實作了「鏈結法（Separate Chaining）」處理雜湊碰撞，那 Python 內建的 dict 底層也是用鏈結法嗎？",
                answer="教學上常以鏈結法（每個桶位存放一個串列）展示碰撞處理，因為邏輯最直觀；但 CPython 3.6+ 的內建 dict 採用的是高度優化的「緊湊型開放定址法（Compact Open Addressing）」。它將稀疏的雜湊索引表（Indices Array）與緊湊存放實際 (hash, key, value) 的項目陣列（Entries Table）拆開，當發生碰撞時使用偽隨機探測（Perturb Probing）尋找下一個空槽。這項設計不僅省下 20%～25% 的記憶體，更同時保留了元素的插入順序並大幅提升 CPU Cache 命中率。",
            ),
            InterviewFAQ(
                question="二元樹的前序（Pre-order）、中序（In-order）、後序（Post-order）走訪分別代表什麼？各自有什麼實際用途？",
                answer="三者的差異在於「根節點（Root）在何時被處理」：1. 前序（根 -> 左 -> 右）：一見到節點就處理，適合用來複製整棵樹或將樹結構序列化（Serialization）；2. 中序（左 -> 根 -> 右）：先處理完左子樹、再處理根節點、最後處理右子樹，對二元搜尋樹（BST）執行中序走訪會直接產生由小到大的排序序列；3. 後序（左 -> 右 -> 根）：必須等左右子樹都算完才能計算當前節點，廣泛用於計算樹高、子樹節點總和、釋放記憶體與底層樹狀 DP。",
            ),
            InterviewFAQ(
                question="在 Two Sum 題目中，為什麼「邊走訪邊寫入字典（One-pass Hash Table）」比「先把全部數字塞進字典再查表（Two-pass）」更好？",
                answer="除了少跑一趟迴圈外，One-pass 最大的優勢在於能自然優雅地處理「兩個相同數字加總等於 target」的重複元素情況（例如 nums = [3, 3], target = 6）。在 One-pass 中，當掃描到索引 1 的第二個 3 時，先檢查 complement = 3 是否在字典 seen 中，此時 seen[3] 正好記錄著索引 0，立刻就能配對回傳 (0, 1)，不會被第二個 3 覆蓋掉索引 0 的紀錄，也完全不必擔心同一個元素自己跟自己配對。",
            ),
        ),
    ),
    ChapterSpec(
        id="ch05",
        badge="Ch.05",
        title="圖論走訪與物件導向設計（Graph BFS / DFS & OOP）",
        complexity="BFS / DFS 走訪與無權重最短路徑均為 O(V + E)",
        summary="以物件導向封裝鄰接串列（Adjacency List），實作廣度優先搜尋（BFS）、深度優先搜尋（DFS）與無權重圖最短路徑回溯。",
        concepts=(
            "廣度優先搜尋（BFS）vs. 深度優先搜尋（DFS）：BFS 搭配佇列（Queue / deque）由起點呈同心圓逐層向外擴散，因此第一次抵達終點時必為「最少步數最短路徑」；DFS 則利用遞迴（Call Stack）或顯式堆疊一條路走到底再回溯（Backtracking），常用於連通分量、拓樸排序與環路檢測。",
            "物件導向封裝（OOP Encapsulation）：將內部鄰接串列 `_adj` 與訪問狀態隱藏於 `Graph[T]` 類別方法內，對外提供乾淨的 `add_edge`、`bfs`、`dfs` 與 `shortest_path_bfs` 介面，兼具型別安全與高維護性。",
            "稀疏圖與稠密圖表示法：真實世界的網路（如社群好友圖、道路網、網頁連結）絕大多數屬於「稀疏圖（Sparse Graph，邊數 E 遠小於 V²）」，使用鄰接串列（Adjacency List）僅需 O(V + E) 空間，遠優於鄰接矩陣的 O(V²) 空間。",
        ),
        file="examples/ch05_graph_oop.py",
        lastmod="2026-11-17",
        keywords=(
            "圖論演算法",
            "廣度優先搜尋 BFS",
            "深度優先搜尋 DFS",
            "Python 物件導向 OOP",
            "鄰接串列 Adjacency List",
            "無權重圖最短路徑",
            "LeetCode 200 島嶼數量",
            "Graph Traversal",
        ),
        deep_intro=(
            "當資料之間的關係不再是單純的「一對一（線性串列）」或「一對多（階層式樹狀結構）」，"
            "而是任意兩個實體之間都可能存在關聯的「多對多網路」時，我們就進入了圖論（Graph Theory）的世界。"
            "從 Google Maps 的道路導航網、社交網路的好友推薦、套件管理器的相依性解析，到迷宮尋路與遊戲 AI 決策，"
            "背後全都是由頂點（Vertex, V）與邊（Edge, E）所構成的圖。"
            "本章同時展示了中型軟體工程極為重要的「物件導向設計（Object-Oriented Programming, OOP）」精神："
            "我們透過 Python Generic 泛型將底層鄰接串列 `_adj: dict[T, list[T]]` 封裝於 `Graph[T]` 類別內，"
            "讓呼叫端無須關心內部字典如何初始化或如何防止重複邊，只需呼叫高階語意方法即可安全完成 BFS、DFS 與最短路徑回溯。"
        ),
        comparison_table=ComparisonTable(
            caption="圖論表示法（鄰接串列 vs. 鄰接矩陣）與走訪演算法（BFS vs. DFS）完整對照表",
            headers=("比較維度 ／ 演算法", "空間複雜度", "走訪／查詢時間複雜度", "核心資料結構", "最佳工程與面試應用場景"),
            rows=(
                ("鄰接串列 (Adjacency List)", "O(V + E)", "巡覽所有鄰居 O(deg(v))", "dict[T, list[T]]", "稀疏圖首選（95% 實務與 LeetCode 圖論題標準表示法）"),
                ("鄰接矩陣 (Adjacency Matrix)", "O(V²)", "判斷兩點是否相連 O(1)", "二維陣列 matrix[V][V]", "頂點數 V 極小（如 V <= 500）且邊極為稠密的完全圖"),
                ("廣度優先搜尋 (BFS)", "O(V) 佇列與 visited", "O(V + E)", "FIFO 佇列 (collections.deque)", "無權重圖最短路徑、最少步數轉換、多源點同時擴散問題"),
                ("深度優先搜尋 (DFS)", "O(V) 遞迴堆疊深度", "O(V + E)", "LIFO 堆疊 ／ 遞迴 Call Stack", "連通分量計數、迷宮所有可能路徑枚舉、回溯法、環路檢測"),
                ("BFS 最短路徑回溯 (Parent Map)", "O(V) 儲存前驅節點", "O(V + E)", "deque + parent: dict[T, T|None]", "不但求出最短距離，還能完整還原起點到終點的頂點序列"),
            ),
        ),
        walkthrough_title="無權重圖 BFS 最短路徑與 Parent 回溯（shortest_path_bfs('A', 'F')）逐步追蹤",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1：初始化起點 'A'（距離 0 層）",
                state_snapshot="queue = deque(['A']) | parent = {'A': None}",
                explanation="從起點 'A' 出發，將 'A' 放入雙端佇列 queue，並在前驅字典 parent 記錄 {'A': None}。此 parent 字典同時身兼兩職：1. 取代 visited 集合防止重複訪問；2. 記錄每個節點是由哪個父節點首次擴散而來。",
            ),
            WalkthroughStep(
                step_label="Step 2：擴散第 1 層 — 彈出 'A' 並將鄰居 'B'、'C' 入佇列",
                state_snapshot="popleft() -> 'A' | 探索鄰居 'B', 'C' | queue = deque(['B', 'C']) | parent = {'A': None, 'B': 'A', 'C': 'A'}",
                explanation="從佇列左端彈出 'A'，檢查其鄰居 'B' 與 'C' 均尚未在 parent 中，立即將 parent['B'] = 'A'、parent['C'] = 'A' 寫入並推入佇列尾端，完成距離為 1 的第一層同心圓搜尋。",
            ),
            WalkthroughStep(
                step_label="Step 3：擴散第 2 層 — 依序彈出 'B' 與 'C'，探索 'D' 與 'E'",
                state_snapshot="彈出 'B' -> 入佇列 'D' (parent['D']='B') | 彈出 'C' -> 入佇列 'E' (parent['E']='C') | queue = deque(['D', 'E'])",
                explanation="彈出 'B' 時，鄰居 'A' 已在 parent 中跳過，新鄰居 'D' 記錄 parent['D'] = 'B'；接著彈出 'C'，新鄰居 'E' 記錄 parent['E'] = 'C'。此時佇列中為距離起點 2 步的節點 ['D', 'E']。",
            ),
            WalkthroughStep(
                step_label="Step 4：擴散第 3 層命中終點 'F' — 順著 parent 指標反向回溯還原最短路徑",
                state_snapshot="彈出 'D' -> 鄰居 'F' == goal | parent['F'] = 'D' | 回溯: F -> D -> B -> A => reverse() 得 ['A', 'B', 'D', 'F']",
                explanation="彈出 'D' 時發現鄰居 'F' 正好等於目標 goal！記錄 parent['F'] = 'D' 後，從 'F' 開始順著 parent 字典一路往回找（F -> D -> B -> A -> None），最後將串列反轉即得到最少步數最短路徑 ['A', 'B', 'D', 'F']。",
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="陷阱一：在 BFS 中等到「從佇列彈出（popleft）時」才標記 visited，導致重複入佇列爆記憶體",
                symptom="在網格圖（Grid）或稠密圖執行 BFS 時，同一個節點被周圍多個鄰居重複 append 進 queue 數十次，造成 Memory Limit Exceeded 或 TLE。",
                root_cause_and_fix="BFS 黃金鐵律：必須在「決定將鄰居節點 nb 推入 queue 的那一瞬間（queue.append(nb) 之前）」就立刻執行 visited.add(nb)（或寫入 parent[nb] = curr）！這樣同層的其他節點再看到 nb 時，就能立刻知道它已經在佇列裡排隊了，確保每個頂點嚴格只入佇列一次。",
            ),
            PitfallItem(
                title="陷阱二：在「邊帶有不同正權重（Weighted Graph）」的圖上誤用普通 BFS 求最短路徑",
                symptom="地圖上 A 直接到 C 距離為 100 公里（1 步），而 A 經 B 到 C 距離為 10 + 10 = 20 公里（2 步），普通 BFS 卻錯誤回傳 A -> C。",
                root_cause_and_fix="普通 BFS（使用 FIFO deque）求的是「最少邊數（Hops）」。當每條邊的權重完全相等（或無權重）時，最少邊數才等於最短距離；若邊具有不同非負權重，必須將普通佇列替換為「優先佇列（Min-Heap）」，改用 Dijkstra 演算法（複雜度 O((V + E) log V)）。",
            ),
            PitfallItem(
                title="陷阱三：在深度極深的圖上使用遞迴 DFS，觸發 Python 預設遞迴上限 RecursionError",
                symptom="當圖退化為長度超過 1,000 個節點的長鏈時，呼叫遞迴版 dfs() 拋出 RecursionError: maximum recursion depth exceeded。",
                root_cause_and_fix="CPython 預設的呼叫堆疊深度限制約為 1,000（可由 sys.getrecursionlimit() 查看）。面對節點數 V > 1,000 的大型圖論問題，建議改用「顯式堆疊（Explicit Stack，使用 Python list 迭代 pop/append）」實作非遞迴版 DFS，或改用迭代式 BFS，即可完全避開呼叫堆疊溢位風險。",
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(200, "Number of Islands（島嶼數量）", "Medium", "二維網格連通分量 BFS / DFS 走訪標記 ・ 時間 O(M * N)"),
            LeetCodeProblem(994, "Rotting Oranges（腐爛的橘子）", "Medium", "多源點廣度優先搜尋（Multi-source BFS）求最少分鐘數 ・ 時間 O(M * N)"),
            LeetCodeProblem(207, "Course Schedule（課程表相依性檢查）", "Medium", "有向圖環路檢測（Kahn 演算法入度 BFS 拓樸排序 ／ 三色標記 DFS） ・ 時間 O(V + E)"),
            LeetCodeProblem(133, "Clone Graph（複製無向圖）", "Medium", "Hash Table (舊節點 -> 新節點映射) 搭配 BFS / DFS 深拷貝 ・ 時間 O(V + E)"),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="為什麼廣度優先搜尋（BFS）的時間複雜度寫作 O(V + E)，而不是 O(V * E)？",
                answer="因為透過 visited 集合（或 parent 字典）的保護，圖中的每一個頂點（Vertex）最多只會進入佇列一次、並從佇列彈出一次，這部分共耗時 O(V)。而當某個頂點 u 從佇列彈出時，我們只會巡覽它自己的鄰接串列 `_adj[u]`（長度為該點的度數 deg(u)）。將所有頂點的鄰接串列長度加總起來，在有向圖中正好等於總邊數 E（無向圖則為 2E），因此檢查所有邊的總次數為 O(E)。兩階段相加即為線性的 O(V + E)。",
            ),
            InterviewFAQ(
                question="在工程程式碼中，為什麼要把鄰接串列 `_adj` 封裝在 `Graph[T]` 類別內，而不是直接把 `dict[str, list[str]]` 裸露在外面操作？",
                answer="這體現了物件導向設計（OOP）的「封裝（Encapsulation）」與「單一職責原則（SRP）」。若將裸字典暴露在外，每個呼叫處都必須自己處理「頂點尚未存在於字典時的 KeyError」、「無向邊忘記同時寫入雙向 u->v 與 v->u」以及「重複加入相同邊」等瑣碎細節；封裝於 Graph[T] 類別後，資料不變量由 add_vertex 與 add_edge 統一把關，且 neighbors() 回傳淺拷貝 list(self._adj.get(vertex, []))，防止外部程式意外竄改圖的內部結構。",
            ),
            InterviewFAQ(
                question="什麼是「多源點 BFS（Multi-source BFS）」？它跟跑好幾次單源 BFS 有什麼差別？",
                answer="當題目有多個起點同時向外擴散（例如 LeetCode #994 多顆腐爛橘子同時傳染新鮮橘子，或 #542 01 矩陣求每個 1 到最近 0 的距離）時，若對每個起點各跑一次 BFS，時間複雜度會高達 O(K * V * E) 而超時。正確做法是在 BFS 初始化時，直接把「所有起點」一起放進同一個 deque 佇列中作為第 0 層，然後啟動唯一一次 BFS 同心圓擴散，就能在 O(V + E) 時間內算出所有節點到最近起點的最短距離。",
            ),
        ),
    ),
    ChapterSpec(
        id="ch06",
        badge="Ch.06",
        title="動態規劃與記憶化搜尋（Dynamic Programming & Memoization）",
        complexity="爬樓梯狀態壓縮 O(n) 時間 / O(1) 空間 ・ 0/1 背包 O(N×W) ・ LIS 最長遞增子序列 O(n log n)",
        summary="破除暴力遞迴 O(2^n) 指數級爆炸瓶頸，掌握重疊子問題、最優子結構、一維滾動陣列狀態壓縮與二分優化 LIS。",
        concepts=(
            "動態規劃兩大核心條件：「重疊子問題（Overlapping Subproblems）」與「最優子結構（Optimal Substructure）」。透過記錄已算過的子問題答案，避免像暴力遞迴一樣重複計算成千上萬次相同的分支。",
            "Top-Down 記憶化搜尋 vs. Bottom-Up 狀態轉移表：由上而下（Top-Down）直接在遞迴函式加上快取（如 Python `@functools.cache`）；由下而上（Bottom-Up）則從基底狀態 `dp[0]` 依序往後填表，且常能進一步利用「滾動變數／一維陣列」將空間複雜度壓縮至 O(1) 或 O(W)。",
            "0/1 背包一維逆序更新關鍵：當將二維 `dp[i][w]` 壓縮為一維 `dp[w]` 時，內層容量迴圈必須「由大到小（capacity -> weight）逆序走訪」，才能確保每件物品在讀取 `dp[cap - w]` 時拿到的是「上一輪尚未放入當前物品」的舊狀態。",
        ),
        file="examples/ch06_dynamic_programming.py",
        lastmod="2026-11-17",
        keywords=(
            "動態規劃",
            "Dynamic Programming DP",
            "記憶化搜尋 Memoization",
            "0/1 背包問題 Knapsack",
            "最長遞增子序列 LIS",
            "爬樓梯 Climbing Stairs",
            "狀態轉移方程式",
            "LeetCode 70 300 322",
        ),
        deep_intro=(
            "許多初學者與轉職工程師聽到「動態規劃（Dynamic Programming, 簡稱 DP）」就心生畏懼，"
            "但其實 DP 的本質非常單純：**「記住算過的答案，用空間換取時間，並按照依賴順序由小到大推導出最終解答」**。"
            "以經典的爬樓梯（Climbing Stairs）為例：要爬到第 n 階，最後一步一定是從第 n-1 階跨 1 步、或是從第 n-2 階跨 2 步上來，"
            "因此方法數滿足狀態轉移方程式 `f(n) = f(n-1) + f(n-2)`。若直接寫純遞迴，`f(40)` 會重複計算 `f(20)` 上萬次，時間複雜度為恐怖的指數級 O(2^n)；"
            "但只要我們由下而上從第 0 階、第 1 階開始往後累加，而且只保留前兩階的數值（`prev2`, `prev1`），"
            "就能在 O(n) 時間、O(1) 額外空間內瞬間算出答案！"
            "本章進一步帶你掌握面試最常考的兩大進階模型：**0/1 背包一維滾動陣列**與 **O(n log n) 二分搜尋優化之最長嚴格遞增子序列（LIS）**。"
        ),
        comparison_table=ComparisonTable(
            caption="動態規劃實作策略（暴力遞迴、記憶化搜尋、二維/一維 DP 與滾動變數壓縮）完整對照表",
            headers=("實作策略 ／ 演算法模型", "時間複雜度", "空間複雜度", "核心實作機制", "工程與白板題適用場景"),
            rows=(
                ("暴力遞迴 (Naive Recursion)", "O(2^n) 指數級爆炸", "O(n) 呼叫堆疊", "直接遞迴展開所有分支，無快取", "僅適合 n <= 20 的極小規模枚舉，大測資必 TLE"),
                ("Top-Down 記憶化搜尋 (Memoization)", "O(狀態總數 × 轉移成本)", "O(狀態總數 + 遞迴深度)", "遞迴搭配 dict 或 @functools.cache", "狀態轉移方向複雜、不需算滿所有狀態的子樹型／區間型 DP"),
                ("Bottom-Up 標準填表法 (Tabulation)", "O(狀態總數 × 轉移成本)", "O(狀態總數)", "建立一維或二維 dp 陣列由基底迭代填表", "零遞迴呼叫開銷，無 RecursionError 風險，邏輯最直觀"),
                ("Bottom-Up 空間狀態壓縮 (Space-Optimized)", "O(狀態總數 × 轉移成本)", "O(1) 或降一維 O(W)", "僅保留上一輪計算所需的少數變數或單列陣列", "爬樓梯 O(1) 空間、0/1 背包一維 O(W) 空間面試加分寫法"),
                ("LIS 二分貪婪優化 (Patience Sorting)", "O(n log n)", "O(n) 維護 tails 陣列", "以 bisect_left 維護各長度遞增子序列之最小結尾", "當 n 高達 10^5 時取代傳統 O(n²) DP 的唯一正解"),
            ),
        ),
        walkthrough_title="0/1 背包問題一維滾動陣列逆序更新（knapsack_01）逐步狀態追蹤",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1：初始化一維 DP 陣列（背包容量 capacity = 50）",
                state_snapshot="dp = [0, 0, ..., 0]（長度 51，代表容量 0 ~ 50 在尚未放入任何物品時最大價值皆為 0）",
                explanation="建立長度為 capacity + 1 的一維陣列 dp，其中 dp[cap] 代表「在背包容量上限為 cap 時所能獲得的最大總價值」。初始狀態全部填 0。",
            ),
            WalkthroughStep(
                step_label="Step 2：處理第 1 件物品（重量 w=10, 價值 v=60）— 由 cap=50 逆序更新至 10",
                state_snapshot="cap = 50..10: dp[cap] = max(dp[cap], dp[cap - 10] + 60) => dp[10..50] 全數更新為 60",
                explanation="內層迴圈從 cap = 50 往回走到 10。因為讀取的 dp[cap - 10] 都是尚未被本輪修改過的 0，所以容量 10 以上的格子都放入一件物品 1，價值變為 60（不會發生同一件物品被放兩次變成 120 的錯誤）。",
            ),
            WalkthroughStep(
                step_label="Step 3：處理第 2 件物品（重量 w=20, 價值 v=100）— 逆序決策選或不選",
                state_snapshot="dp[50..30] = dp[20..0] + 100 = 160（同時裝入物品 1 與 2）| dp[20..29] = 100 | dp[10..19] = 60",
                explanation="當 cap >= 30 時，比較「不放物品 2（維持 60）」與「空出 20 容量放物品 2（dp[cap-20] + 100 = 60 + 100 = 160）」，更新為 160；當 20 <= cap < 30 時，則更新為單獨放物品 2 的價值 100。",
            ),
            WalkthroughStep(
                step_label="Step 4：處理第 3 件物品（重量 w=30, 價值 v=120）— 得出最終最大價值 dp[50] = 220",
                state_snapshot="cap = 50: max(原 dp[50]=160, dp[50-30] + 120 = 100 + 120 = 220) => dp[50] = 220",
                explanation="最後處理重量 30、價值 120 的物品 3。在 cap = 50 時，讀取上一輪的 dp[20]（價值 100，代表只放物品 2）加上物品 3 的 120，得到 220 > 160，成功找出最佳組合（選取物品 2 與物品 3，總重 50、總價值 220）。",
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="陷阱一：0/1 背包一維陣列將內層容量迴圈寫成「由小到大（正序）」，意外變成無限背包",
                symptom="在每件物品只能選一次的 0/1 背包題中，內層寫 for cap in range(w, capacity + 1):，算出來的最大價值遠超過正確答案。",
                root_cause_and_fix="若由小到大正序更新，當計算 dp[10] 時放入了物品 1（重量 10），接著計算 dp[20] 時讀取 dp[20 - 10] 就會讀到「剛剛已經放入過物品 1 的 dp[10]」，導致同一件物品被無限次重複放入！口訣請記牢：0/1 背包一維陣列內層容量必「逆序（由大到小）」；完全背包（每件物品可無限選取）內層容量才用「正序（由小到大）」。",
            ),
            PitfallItem(
                title="陷阱二：定義了狀態轉移方程式，卻漏掉或設錯基底狀態（Base Cases）與非法狀態初始化",
                symptom="在湊零錢（Coin Change）求最少硬幣數時，將 dp 陣列全部初始化為 0，結果所有 min() 計算出來永遠是 0。",
                root_cause_and_fix="初始化的值必須根據目標是求 max 還是 min 來決定：求最大價值（如背包問題）時，可初始化為 0；但求最小成本／最少步數（如 Coin Change LeetCode #322）時，除基底 dp[0] = 0 外，其餘位置必須初始化為正無限大 float('inf')（或 capacity + 1），否則 min(dp[i], ...) 永遠會被 0 吃掉。",
            ),
            PitfallItem(
                title="陷阱三：在最長遞增子序列（LIS）中誤以為 tails 陣列本身的內容就是最終的子序列",
                symptom="執行 length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]) 時直接把 tails 陣列當成答案印出，發現元素出現順序與原陣列不符。",
                root_cause_and_fix="在 O(n log n) 的二分貪婪 LIS 演算法中，tails[k] 的嚴格定義是「所有長度為 k+1 的遞增子序列中，結尾最小的那個數值」。用較小的新數值覆蓋 tails 中間元素是為了讓未來更容易接上新數字，這不會改變 tails 的總長度，因此 len(tails) 100% 保證等於 LIS 長度；若題目要求輸出實際子序列本身，則需額外搭配 prev_idx 陣列記錄每個元素的前驅索引再回溯。",
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(70, "Climbing Stairs（爬樓梯）", "Easy", "一維線性 DP 與滾動變數 O(1) 空間狀態壓縮 ・ 時間 O(n) / 空間 O(1)"),
            LeetCodeProblem(198, "House Robber（打家劫捨）", "Medium", "選與不選的狀態轉移 dp[i] = max(dp[i-1], dp[i-2] + nums[i]) ・ 時間 O(n) / 空間 O(1)"),
            LeetCodeProblem(322, "Coin Change（零錢兌換）", "Medium", "完全背包模型求最少硬幣數 ・ 時間 O(amount * len(coins)) / 空間 O(amount)"),
            LeetCodeProblem(300, "Longest Increasing Subsequence（最長嚴格遞增子序列）", "Medium", "贪婪維護最小結尾 tails ＋ 二分搜尋 bisect_left ・ 時間 O(n log n)"),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="在白板面試時，面對一道沒見過的動態規劃（DP）題目，標準的「破題四部曲」是什麼？",
                answer="建議嚴格按照以下四個步驟向面試官闡述思路：1. 定義狀態（State Definition）：明確說出 dp[i]（或 dp[i][j]）代表什麼物理意義（例如「考慮前 i 件物品、容量上限為 j 時的最大價值」）；2. 推導狀態轉移方程式（State Transition）：找出當前狀態如何由規模更小的子問題決策而來（例如「選第 i 件」vs「不選第 i 件」取 max）；3. 確定基底與初始化（Base Cases）：設定 dp[0] 等最小邊界值；4. 決定計算順序與空間壓縮（Iteration Order & Space Optimization）：確認填表方向能保證用到的子問題皆已算出，並評估能否用滾動變數降維。",
            ),
            InterviewFAQ(
                question="Top-Down 記憶化搜尋（Memoization）跟 Bottom-Up 填表法（Tabulation）在實戰中該如何選擇？",
                answer="若在時間緊迫的線上測驗（OA）或狀態轉移依賴關係較不規則（例如樹形 DP、博弈型區間 DP）時，使用 Python 3.9+ 內建的 `@functools.cache` 裝飾器搭配 Top-Down 遞迴最快且不會算到無效狀態；但在正式技術面試中，將解法改寫為 Bottom-Up 填表法並進一步展示「空間複雜度從 O(n) 壓縮至 O(1)（或從二維 O(N*W) 壓縮至一維 O(W)）」是極具說服力的 Senior 加分亮點，且能徹底免除遞迴呼叫堆疊溢位（RecursionError）的風險。",
            ),
            InterviewFAQ(
                question="為什麼求「最長嚴格遞增子序列（LIS）」能從傳統 DP 的 O(n²) 加速到 O(n log n)？關鍵直覺是什麼？",
                answer="關鍵直覺來自「貪婪（Greedy）思維」：假設目前有兩個長度同為 3 的遞增子序列 `[2, 5, 100]` 與 `[2, 5, 7]`，為了讓後面出現的數字（例如 `8`）更容易接上去變成長度 4，我們永遠只關心「相同長度下，結尾數字越小越好」的那個代表！當我們維護一個記錄各長度最小結尾的陣列 `tails` 時，可以證明 `tails` 必然保持嚴格單調遞增，因此每讀入一個新數字 `x`，就不必像傳統 DP 往回線性掃描 O(n) 個元素，而是直接對 `tails` 執行 O(log n) 的二分搜尋（`bisect_left`）找到替換或擴展位置。",
            ),
        ),
    ),
    ChapterSpec(
        id="ch07",
        badge="Ch.07",
        title="堆積、優先佇列與 Top-K 演算法（Heap, Priority Queue & Top-K Elements）",
        complexity="堆積 Push / Pop O(log n) ・ Top-K 篩選 O(n log k) ・ 合併 K 個排序序列 O(N log K)",
        summary="深入理解完全二元樹陣列映射與 Sift-Up / Sift-Down 機制，手寫泛型 MinHeap 並實作海量資料 Top-K 與多路合併演算法。",
        concepts=(
            "二元堆積（Binary Heap）與陣列索引映射：堆積是一棵「完全二元樹（Complete Binary Tree）」，不需使用指標節點，直接用單一陣列即可零浪費儲存：索引 `i` 的父節點為 `(i - 1) // 2`，左子節點為 `2 * i + 1`，右子節點為 `2 * i + 2`。",
            "海量資料 Top-K 問題的最佳解：若要在 1 億筆資料中找出最大的前 K 筆（例如 K = 10），不需將全部資料排序（耗時 O(n log n) 且塞爆記憶體），只需維護一個容量固定為 K 的「最小堆積（Min-Heap）」，當新元素大於堆頂最小值時即替換下沉，時間複雜度僅 O(n log k)、空間僅 O(k)。",
            "多路合併（K-Way Merge）：當需要將 K 個已排序的資料流或鏈結串列合併為單一有序序列時，利用最小堆積存放每個序列當前的最小代表元素，每次彈出全局最小值後推入該序列的下一個元素，即可在 O(N log K) 時間內完成。",
        ),
        file="examples/ch07_heap_priority_queue.py",
        lastmod="2026-11-17",
        keywords=(
            "二元堆積 Binary Heap",
            "優先佇列 Priority Queue",
            "Python heapq 教學",
            "Top-K 問題演算法",
            "MinHeap 實作",
            "合併 K 個排序串列",
            "LeetCode 215 23 347",
            "Sift-Up Sift-Down",
        ),
        deep_intro=(
            "在作業系統排程、急診室檢傷分類、遊戲尋路演算法（A* / Dijkstra）與即時排行榜系統中，"
            "我們需要的不是先進先出的普通佇列，而是**「誰的優先順序最高（或數值最小／最大），誰就優先出列」的優先佇列（Priority Queue）**。"
            "若使用未排序陣列實作，每次插入雖為 O(1)，但每次找最小值卻要花 O(n)；若每次插入都重新完整排序，單次維護又高達 O(n)。"
            "「二元堆積（Binary Heap）」完美折衷了這兩者：它規定我們不需要讓整棵樹完全排序，只需要維持「每個父節點的值都小於等於（最小堆 Min-Heap）或大於等於（最大堆 Max-Heap）其左右子節點」的堆積序性質（Heap Order Property）。"
            "如此一來，全局最小（或最大）值永遠穩坐陣列索引 `0` 的堆頂位置（讀取 O(1)），而插入新元素的上浮（Sift-Up）與彈出堆頂後的下沉（Sift-Down）都只需沿著樹高走訪，時間複雜度嚴格控制在對數級 O(log n)！"
        ),
        comparison_table=ComparisonTable(
            caption="優先佇列底層實作方案（二元堆積、未排序陣列、有序陣列與完整排序）效能對照表",
            headers=("操作項目 ／ 應用場景", "二元堆積（MinHeap / heapq）", "未排序陣列（Unsorted list）", "維持排序陣列（Sorted list）", "一次性完整排序（sorted()）"),
            rows=(
                ("查看極值 (Peek Min / Max)", "O(1) — 直接讀取 _data[0]", "O(n) — 需全陣列線性掃描", "O(1) — 讀取首或尾元素", "排序後 O(1)"),
                ("插入新元素 (Push / Insert)", "O(log n) — 尾端附加並 _sift_up", "均攤 O(1) — 直接 append", "O(n) — 二分搜尋 O(log n) + 搬移 O(n)", "不支援動態串流插入"),
                ("彈出極值 (Pop Min / Max)", "O(log n) — 尾端補頂並 _sift_down", "O(n) — 搜尋極值並搬移刪除", "移除尾端 O(1) ／ 移除首端 O(n)", "不支援動態高效重排"),
                ("將 N 筆現有資料建構為結構", "O(n) — Floyd 自底向上 heapify", "O(n) — 直接複製", "O(n log n)", "O(n log n)"),
                ("N 筆海量資料求前 K 大 (Top-K)", "時間 O(n log k) ・ 空間 O(k)", "不適用", "時間 O(n * k) ・ 空間 O(k)", "時間 O(n log n) ・ 空間 O(n)"),
                ("合併 K 個已排序串列（總長 N）", "時間 O(N log K) ・ 空間 O(K)", "時間 O(N * K)", "時間 O(N * K)", "時間 O(N log N) ・ 空間 O(N)"),
            ),
        ),
        walkthrough_title="MinHeap 上浮／下沉維護與固定大小 K 最小堆積篩選 Top-K 逐步追蹤",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1：MinHeap 依序插入 [5, 1, 8, 3] — 觀察上浮（_sift_up）過程",
                state_snapshot="push(5) -> [5] | push(1): 1 < 5 上浮交換 -> [1, 5] | push(8) -> [1, 5, 8] | push(3): 3 < 5 上浮 -> [1, 3, 8, 5]",
                explanation="當 push(3) 附加至索引 3 時，計算其父節點索引 parent = (3 - 1) // 2 = 1（值為 5）。因為 3 < 5 違反最小堆性質，將 3 與 5 交換；接著比較索引 1 與根節點索引 0（值為 1），1 <= 3 滿足性質，停止上浮。",
            ),
            WalkthroughStep(
                step_label="Step 2：呼叫 MinHeap.pop() 彈出堆頂 1 — 尾端元素補位並下沉（_sift_down）",
                state_snapshot="取出堆頂 1 | 尾端 5 移至索引 0 -> [5, 3, 8] | 5 與較小子節點 3 交換 -> [3, 5, 8]",
                explanation="彈出最小值 1 後，為了不破壞完全二元樹結構，將陣列最後一個元素 5 移到索引 0。接著執行 _sift_down(0)：比較左子節點 3（索引 1）與右子節點 8（索引 2），選出較小的 3 與 5 交換，堆頂更新為次小值 3。",
            ),
            WalkthroughStep(
                step_label="Step 3：Top-3 最大元素篩選（nums = [64, 34, 25, 12, 22, 11, 90]）— 建立容量 3 守門員",
                state_snapshot="前 3 個元素直接入堆: min_heap = [25, 64, 34]（堆頂 min_heap[0] == 25 為目前第 3 大守門員）",
                explanation="要找「前 K 大」，我們反而要使用「最小堆積（Min-Heap）」！因為最小堆的堆頂 min_heap[0] 正好是「目前暫居前 K 名當中最弱的守門員（第 K 大）」。後續遇到的 12、22、11 皆小於守門員 25，直接淘汰不入堆。",
            ),
            WalkthroughStep(
                step_label="Step 4：遇到強者 90 > 守門員 25 — 執行 heapreplace 替換並輸出結果",
                state_snapshot="90 > 25 => heapreplace(min_heap, 90) => min_heap = [34, 64, 90] => 降序輸出 [90, 64, 34]",
                explanation="掃描到最後一個數字 90 時，90 > min_heap[0] (25)，呼叫 heapq.heapreplace 將 25 踢出並放入 90 下沉調整，最終堆積內留下的 [34, 64, 90] 即為全陣列最大的前 3 名。",
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="陷阱一：要找「前 K 大（Top-K Largest）」卻誤用最大堆積，或搞混最小堆／最大堆方向",
                symptom="把全部 N 個元素都丟進最大堆積再 pop K 次，在串流資料（Data Stream）情境下把記憶體塞爆。",
                root_cause_and_fix="請記住反向口訣：「求前 K 大，用大小為 K 的最小堆積（Min-Heap 淘汰太小的數）；求前 K 小，用大小為 K 的最大堆積（Max-Heap 淘汰太大的數）」。這樣堆積中永遠只需要保留 K 個元素，空間複雜度嚴格控制在 O(k)。",
            ),
            PitfallItem(
                title="陷阱二：Python 標準庫 heapq 只有最小堆積（Min-Heap），需要最大堆積時不知所措",
                symptom="在實作雙堆積求資料流中位數（LeetCode #295）或最大優先佇列時，找不到 MaxHeap 類別可用。",
                root_cause_and_fix="Python 的 heapq 模組僅實作了最小堆積。若需要數值型別的最大堆積，最簡潔的工程慣用法是「存入時將數值取負號 `heapq.heappush(max_heap, -val)`，取出時再加負號還原 `-heapq.heappop(max_heap)`」；因為數值越大，加上負號後越小，就會自動浮到最小堆的堆頂！",
            ),
            PitfallItem(
                title="陷阱三：將 `(priority, obj)` 放入 heapq 時，當 priority 相同卻因 obj 無法比較大小而拋出 TypeError",
                symptom="在合併 K 個鏈結串列（LeetCode #23）或自訂任務排程時寫 `heappush(heap, (node.val, node))`，當兩個節點的 val 相等時拋出 `TypeError: '<' not supported between instances of 'ListNode' and 'ListNode'`。",
                root_cause_and_fix="Python 比較 Tuple 時是逐欄由左往右比對：當第 0 欄的數值相等（Tie）時，會自動比較第 1 欄！若第 1 欄是不支援 `<` 運算子的自訂物件就會崩潰。標準解法是在中間插入一個永不重複的遞增序號或列表索引 `(val, list_idx, node)`（正如本章 `merge_k_sorted_lists` 的實作），讓平手時在第 2 欄就分出勝負。",
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(215, "Kth Largest Element in an Array（陣列中的第 K 個最大元素）", "Medium", "維護大小為 K 的最小堆積（Min-Heap） ・ 時間 O(n log k) / 空間 O(k)"),
            LeetCodeProblem(347, "Top K Frequent Elements（前 K 個高頻元素）", "Medium", "Counter 雜湊計數 ＋ 大小為 K 的最小堆積篩選頻率 ・ 時間 O(n log k)"),
            LeetCodeProblem(23, "Merge k Sorted Lists（合併 K 個升序鏈結串列）", "Hard", "Min-Heap 存放 (val, list_idx, elem_idx) 多路合併 ・ 時間 O(N log K)"),
            LeetCodeProblem(295, "Find Median from Data Stream（資料流的中位數）", "Hard", "對頂雙堆積（左半最大堆 + 右半最小堆平衡大小） ・ 插入 O(log n) / 查詢 O(1)"),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="為什麼完全二元樹（Complete Binary Tree）可以直接用一維陣列儲存，而一般的二元搜尋樹（BST）卻必須用指標節點（Node.left / Node.right）？",
                answer="因為二元堆積嚴格規定樹的結構必須是「完全二元樹」——除了最後一層外每一層都完全填滿，且最後一層的節點全部緊靠左側排列，中間絕不會出現任何空洞。在沒有空洞的前提下，若按廣度優先（由上到下、由左到右）為節點編號 0, 1, 2...，就能用純數學公式 `left = 2*i + 1`、`right = 2*i + 2` 與 `parent = (i - 1) // 2` 精確算出父子關係，完全省去指標記憶體開銷；相反地，一般 BST 可能呈現任意歪斜形狀，若硬用陣列存會產生大量空白浪費。",
            ),
            InterviewFAQ(
                question="將 N 個無序元素逐一呼叫 push() 塞進空堆積需要 O(n log n)，為什麼呼叫 `heapq.heapify(arr)` 原地建堆只需要線性的 O(n) 時間？",
                answer="因為 `heapify()` 採用的是「Floyd 自底向上下沉法（Bottom-Up Sift-Down）」：陣列後半部（約 N/2 個元素）全都是沒有子節點的葉節點，根本不需要調整（耗時 0）；倒數第二層（約 N/4 個節點）最多只需下沉 1 層；倒數第三層（約 N/8 個節點）最多只需下沉 2 層……只有唯一的根節點最多需要下沉 log2(N) 層。根據級數求和 `Σ (N / 2^(h+1)) * h`，當 h 從 1 加到 log N 時，級數收斂上界為 2N，因此總時間複雜度是嚴格的線性 O(n)！",
            ),
            InterviewFAQ(
                question="在 `top_k_largest` 中，為什麼當 `num > min_heap[0]` 時呼叫 `heapq.heapreplace(min_heap, num)` 比先 `heappop` 再 `heappush` 更快？",
                answer="若先呼叫 `heappop()` 再呼叫 `heappush()`，會先經歷一次完整的下沉（Sift-Down），再經歷一次從底部的上浮（Sift-Up），共兩趟樹高調整。而當我們已經確定新元素 `num` 比堆頂 `min_heap[0]` 更大時，直接呼叫 `heapq.heapreplace(min_heap, num)` 會一步到位把堆頂替換成 `num` 並只執行唯一一次下沉（Sift-Down），常數時間開銷直接減半。",
            ),
        ),
    ),
)
