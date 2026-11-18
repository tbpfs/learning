#!/usr/bin/env python3
"""
chapter_content.py - 紫楓 (Purple Maple) Python 3.12 資料結構、演算法與物件導向深度教材資料模組。
採用 Python 標準庫 frozen dataclass 封裝 Ch.01 ~ Ch.07 四大獨家深度教學模組：
  - 模組 A：結構化複雜度與底層特性對照表 (ComparisonTable)
  - 模組 B：演算法逐步執行與記憶體狀態拆解 (WalkthroughStep)
  - 模組 C：Python 3.12 (CPython) 底層原理與常見實作陷阱 (PitfallItem)
  - 模組 D：LeetCode 經典題號對照與技術面試必考問答 (LeetCodeProblem & InterviewFAQ)
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

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


CHAPTERS: tuple[ChapterSpec, ...] = (
    # =========================================================================
    # Ch.01 陣列與單向鏈結串列
    # =========================================================================
    ChapterSpec(
        id="ch01",
        badge="Ch.01",
        title="陣列與單向鏈結串列（Array & Singly Linked List）",
        complexity="頭部插入 O(1) ・ 尾部附加 / 搜尋 / 刪除 / 原地反轉 O(n)",
        summary="理解連續記憶體配置（Array）與指標節點串接（Linked List）的本質差異，並以 Python Generic 型別實作單向鏈結串列的增刪查與 O(1) 額外空間原地反轉。",
        concepts=(
            "連續記憶體 vs. 指標串接：陣列（Array / Python list）透過連續記憶體區塊支援 O(1) 隨機索引存取，但在頭部或中間插入元素需搬移後續元素（O(n)）；單向鏈結串列（Singly Linked List）則以 Node 節點與 next 指標動態串接，在已知頭節點時可於 O(1) 時間完成頭部插入（prepend）。",
            "白板題必考「原地反轉（In-place Reverse）」：透過 prev、curr、nxt 三個指標迭代翻轉 next 指向，不需額外建立新串列，空間複雜度嚴格控制在 O(1)，是軟體工程師面試最常出現的基礎題型。",
            "CPU 快取友善度（Cache Locality）：陣列因連續存放於實體或虛擬記憶體頁中，能充分利用現代處理器 L1/L2 Cache Line 預取機制；鏈結串列的節點則分散於堆積（Heap）各處，頻繁追蹤指標容易觸發 Cache Miss。",
        ),
        file="examples/ch01_array_linked_list.py",
        lastmod="2026-11-17",
        keywords=(
            "Python 鏈結串列",
            "Singly Linked List",
            "反轉鏈結串列",
            "Reverse Linked List",
            "陣列與鏈結串列比較",
            "LeetCode 206",
            "指標操作",
            "時間複雜度",
        ),
        deep_intro=(
            "在學習所有進階演算法之前，「陣列（Array）」與「鏈結串列（Linked List）」是建構電腦科學記憶體世界觀的兩塊基石。"
            "許多初學者在寫 Python 時習慣所有場景都用內建的 list 解決，卻在面對技術面試或百萬級資料處理時，因為不理解底層記憶體布局而寫出效能瓶頸。"
            "在 CPython 3.12 底層中，Python 的 list 並非鏈結串列，而是以 C 語言結構 PyListObject 實作的「動態指標陣列（Dynamic Array of Pointers）」。"
            "當你對 list[i] 進行讀取時，直譯器只需計算 base_address + i * sizeof(PyObject*) 即可在 O(1) 常數時間內直接命中目標位址；"
            "但當你呼叫 list.insert(0, val) 在頭部插入元素時，底層必須將索引 0 到 n-1 的所有指標全數向後搬移一格，時間複雜度高達 O(n)。"
            "相對地，單向鏈結串列（Singly Linked List）將每個元素封裝在獨立的 ListNode 節點物件中，節點之間僅靠 next 參照（Reference）彼此串聯。"
            "這種設計放棄了 O(1) 隨機索引存取的能力，卻換來了在已知節點位置時 O(1) 修改指標即可完成插入或刪除的結構彈性，更是後續實作雜湊表碰撞鏈（Chaining）、"
            "雙端佇列（Deque）、圖論鄰接串列（Adjacency List）與 LRU Cache 的核心基礎。"
        ),
        comparison_table=ComparisonTable(
            caption="表 1-1：Python 動態陣列（list）與單向／雙向鏈結串列之操作複雜度與硬體特性對照表",
            headers=(
                "操作項目 / 結構特性",
                "動態陣列（Python list）",
                "單向鏈結串列（Singly Linked List）",
                "雙向鏈結串列（Doubly Linked List）",
                "底層關鍵原因剖析",
            ),
            rows=(
                (
                    "依索引隨機讀取（get by index）",
                    "O(1)",
                    "O(n)",
                    "O(n)",
                    "陣列支援基址加偏移量直接定址；鏈結串列必須從 head 沿 next 逐節點巡覽。",
                ),
                (
                    "頭部插入 / 刪除（prepend / pop first）",
                    "O(n)",
                    "O(1)",
                    "O(1)",
                    "陣列需將後續 n 個元素整體搬移；鏈結串列僅需重新指向 head 指標。",
                ),
                (
                    "尾部附加（append at tail）",
                    "攤銷 O(1)（Amortized）",
                    "無 tail 指標 O(n) / 有 tail O(1)",
                    "O(1)（維護 tail 指標）",
                    "Python list 採超額配置（Over-allocation），僅在容量滿時觸發 O(n) 擴容複製。",
                ),
                (
                    "已知目標節點下刪除該節點",
                    "O(n)",
                    "O(n)（需找前驅節點 prev）",
                    "O(1)（直接存取 node.prev）",
                    "單向串列無法逆向得知前驅節點，除非使用雙向串列或改寫下一個節點的值。",
                ),
                (
                    "按值線性搜尋（find target）",
                    "O(n)",
                    "O(n)",
                    "O(n)",
                    "未排序情況下皆須從頭逐一比對元素值。",
                ),
                (
                    "CPU 快取命中率與額外空間開銷",
                    "極高（連續記憶體） / 低額外空間",
                    "偏低（分散配置） / 每節點多 1 個指標",
                    "偏低（分散配置） / 每節點多 2 個指標",
                    "陣列具空間局部性（Spatial Locality）；Python 每個 Node 物件另有 GC 與型別標頭開銷。",
                ),
            ),
        ),
        walkthrough_title="逐步拆解：單向鏈結串列原地反轉（In-place Reverse, O(1) 空間）四步驟狀態追蹤",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1：初始化三指標（prev = None, curr = head）",
                state_snapshot="prev = None | curr -> [10] -> [20] -> [30] -> None",
                explanation=(
                    "假設原始串列為 10 -> 20 -> 30 -> None。我們宣告 prev 初始化為 None（代表反轉後的新尾部將指向 None），"
                    "curr 初始化為 self.head（指向第一個節點 10）。此時尚未修改任何指標，準備進入 while curr is not None 迴圈。"
                ),
            ),
            WalkthroughStep(
                step_label="Step 2：第一輪迭代 — 暫存 nxt 並翻轉首節點指標",
                state_snapshot="prev -> [10] -> None | curr = nxt -> [20] -> [30] -> None",
                explanation=(
                    "在修改 curr.next 之前，必須先執行 nxt = curr.next 將節點 [20] 的位址保存下來，否則一旦改變指向就會徹底遺失後續串列（斷鏈）。"
                    "接著執行 curr.next = prev（使 [10].next 指向 None），再將 prev 推進至 [10]、curr 推進至 nxt（[20]）。"
                ),
            ),
            WalkthroughStep(
                step_label="Step 3：第二與第三輪迭代 — 依序翻轉後續節點",
                state_snapshot="第二輪後：prev -> [20] -> [10] -> None | 第三輪後：prev -> [30] -> [20] -> [10] -> None, curr = None",
                explanation=(
                    "第二輪先暫存 nxt = [30]，將 [20].next 反指回 prev（[10]），推進後 prev = [20]、curr = [30]。"
                    "第三輪暫存 nxt = None，將 [30].next 反指回 prev（[20]），推進後 prev = [30]，而 curr 變為 None，正式結束 while 迴圈。"
                ),
            ),
            WalkthroughStep(
                step_label="Step 4：重新綁定串列頭指標（self.head = prev）",
                state_snapshot="self.head -> [30] -> [20] -> [10] -> None（完成 O(n) 時間、O(1) 空間原地反轉）",
                explanation=(
                    "當 curr 為 None 時，prev 恰好停在原串列的最後一個節點 [30]，也就是反轉後的新頭節點。"
                    "最後執行 self.head = prev，整條鏈結串列即完成原地反轉，全程僅使用三個區域變數指標，額外空間複雜度嚴格為 O(1)。"
                ),
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="陷阱一：反轉或插入節點時未先暫存 curr.next 導致「斷鏈（Lost Reference）」",
                symptom="在撰寫 reverse() 或中間插入邏輯時，直接寫出 curr.next = prev，下一行再寫 curr = curr.next，結果串列只剩下第一個節點或變成無窮迴圈。",
                root_cause_and_fix=(
                    "根因分析：指標賦值具有破壞性覆寫特性，一旦 curr.next 被改寫為 prev，原本指向下一個節點的唯一參照便立即消失，甚至會被 Python 垃圾回收器（Garbage Collector）回收。"
                    "正確對策：在任何修改 .next 指標的迴圈中，第一行永遠先寫 nxt = curr.next 保存下一個節點參照，最後再執行 curr = nxt。"
                ),
            ),
            PitfallItem(
                title="陷阱二：忽略刪除頭節點（head）或空串列的邊界條件（Boundary Conditions）",
                symptom="在 remove(target) 時若目標值剛好位於第一個節點（prev is None），直接執行 prev.next = curr.next 會立即拋出 AttributeError: 'NoneType' object has no attribute 'next'。",
                root_cause_and_fix=(
                    "根因分析：頭節點沒有前驅節點（prev 為 None），其刪除動作本質上是「更新 self.head = curr.next」而非修改前驅節點。"
                    "正確對策：務必像本章範例第 67 行顯式判斷 if prev is None: self.head = curr.next，或在白板題中使用「虛擬頭節點（Dummy Node / Sentinel Node）」讓所有節點都擁有前驅節點，統一刪除邏輯。"
                ),
            ),
            PitfallItem(
                title="陷阱三：在生產環境誤用自訂 Python 鏈結串列取代內建 list 或 deque",
                symptom="以為需要頻繁在頭尾增刪時，自己用純 Python class ListNode 寫鏈結串列會比內建容器快，實測卻發現記憶體暴增 4 倍且速度更慢。",
                root_cause_and_fix=(
                    "根因分析：CPython 中每個自訂 Python 物件（即使加了 @dataclass 或 __slots__）都有可觀的 PyObject 標頭與配置開銷；"
                    "而標準庫 collections.deque 在底層是以 C 語言實作的「定長 64 元素區塊雙向鏈結串列（Doubly Linked List of Blocks）」，兼具 O(1) 雙端操作與極佳的 CPU 快取局部性。"
                    "正確對策：手寫 ListNode 用於教學理解指標與通過 LeetCode 白板題；工程實務上需要 O(1) 頭尾操作時，應優先選用 collections.deque。"
                ),
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(
                number=206,
                title="Reverse Linked List（反轉單向鏈結串列）",
                difficulty="Easy",
                pattern="三指標迭代原地反轉（prev, curr, nxt） ・ 時間 O(n) / 空間 O(1)",
            ),
            LeetCodeProblem(
                number=21,
                title="Merge Two Sorted Lists（合併兩個已排序鏈結串列）",
                difficulty="Easy",
                pattern="虛擬頭節點（Dummy Head）+ 雙指標同步推進 ・ 時間 O(n + m) / 空間 O(1)",
            ),
            LeetCodeProblem(
                number=141,
                title="Linked List Cycle（鏈結串列環路檢測）",
                difficulty="Easy",
                pattern="Floyd 龜兔賽跑演算法（快慢雙指標 Fast & Slow Pointers） ・ 時間 O(n) / 空間 O(1)",
            ),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="Q1：Python 的內建 list 在執行 append() 時為什麼能達到攤銷 O(1) 時間複雜度？何時會退化為 O(n)？",
                answer=(
                    "CPython 的 list 底層為動態指標陣列（PyListObject），為了避免每次 append() 都重新向作業系統申請記憶體，它採用「超額配置（Over-allocation）」策略"
                    "（容量成長曲線約為 new_allocated = newsize + (newsize >> 3) + 6，即每次擴充約 12.5% 額外空間）。"
                    "大多數時候 append() 只是直接寫入已預留的空槽位，耗時嚴格為 O(1)；只有當預留容量完全填滿時，才會觸發一次 realloc 並複製既有 n 個指標（耗時 O(n)）。"
                    "將這一次 O(n) 成本平攤到前 n 次插入操作上，每次操作的攤銷時間複雜度（Amortized Time Complexity）即為 O(1)。"
                ),
            ),
            InterviewFAQ(
                question="Q2：面試白板題反轉鏈結串列（LeetCode #206）時，「三指標迭代法」與「遞迴法」該選哪一種？為什麼？",
                answer=(
                    "在生產環境與面試首選中，強烈建議優先寫出「三指標迭代法（Iterative）」，並主動向面試官補充說明兩者的空間複雜度差異。"
                    "雖然迭代法與遞迴法的時間複雜度同為 O(n)，但遞迴法需要依賴系統呼叫堆疊（Call Stack）保存每一層尚未返回的函式狀態，空間複雜度為 O(n)；"
                    "且 CPython 預設最大遞迴深度限制為 1000（sys.getrecursionlimit()），當鏈結串列長度超過 1000 個節點時，遞迴解法會直接拋出 RecursionError，而迭代法僅需 O(1) 額外空間且絕不會爆堆疊。"
                ),
            ),
            InterviewFAQ(
                question="Q3：如何在不額外使用 Hash Set（O(1) 空間限制）的前提下，判斷一條單向鏈結串列是否有環（Cycle）或找出中點？",
                answer=(
                    "標準解法是使用「快慢雙指標（Floyd's Tortoise and Hare Algorithm）」。設定慢指標 slow = head（每次走 1 步：slow = slow.next）"
                    "與快指標 fast = head（每次走 2 步：fast = fast.next.next）。"
                    "若要找無環串列的中點，當 fast 抵達尾部（fast is None or fast.next is None）時，slow 恰好位於正中央；"
                    "若要檢測是否有環，只要串列存在環路，快指標必定會在環內追上慢指標（slow is fast），時間複雜度 O(n)，額外空間複雜度嚴格為 O(1)。"
                ),
            ),
        ),
    ),
    # =========================================================================
    # Ch.02 堆疊與佇列
    # =========================================================================
    ChapterSpec(
        id="ch02",
        badge="Ch.02",
        title="堆疊與佇列（Stack & Queue）",
        complexity="Push / Pop / Enqueue / Dequeue 均為 O(1)",
        summary="掌握後進先出（LIFO）與先進先出（FIFO）兩大抽象資料型態（ADT），並透過 Stack 實作經典的面試常考題：多層括號平衡檢查器。",
        concepts=(
            "堆疊（Stack，後進先出 LIFO）：如同疊盤子，最後放入的元素最先取出。常用於函式呼叫堆疊（Call Stack）、瀏覽器上一頁紀錄、語法括號匹配檢查與深度優先搜尋（DFS）。",
            "佇列（Queue，先進先出 FIFO）：如同排隊買票，最先進入的元素最先處理。在 Python 中切勿使用 list.pop(0)（會導致 O(n) 記憶體搬移），應採用 collections.deque 雙端佇列達成真正的 O(1) 雙端操作，廣泛應用於廣度優先搜尋（BFS）與非同步任務佇列。",
            "抽象資料型態（Abstract Data Type, ADT）封裝精神：透過受限介面（Stack 僅開放頂端 push/pop/peek；Queue 僅開放尾進頭出 enqueue/dequeue），防止外部程式碼隨意修改中間元素而破壞演算法不變量。",
        ),
        file="examples/ch02_stack_queue.py",
        lastmod="2026-11-17",
        keywords=(
            "Python Stack",
            "Python Queue",
            "堆疊與佇列",
            "collections.deque",
            "括號匹配檢查",
            "Valid Parentheses",
            "LIFO FIFO",
            "LeetCode 20",
        ),
        deep_intro=(
            "堆疊（Stack）與佇列（Queue）雖然底層同樣儲存線性序列，但它們透過「限制元素的進出端口」建立了截然不同的時間順序契約。"
            "堆疊遵循「後進先出（Last-In, First-Out, LIFO）」原則：所有新增（Push）與取出（Pop）都只能在同一個端點（Top 堆頂）進行。"
            "當你在程式中呼叫函式 A、A 再呼叫函式 B 時，作業系統與 Python 虛擬機正是使用「呼叫堆疊（Call Stack）」將區域變數與返回位址一層層壓入，等最內層的 B 執行完畢彈出後，才回到外層的 A。"
            "這也是為什麼任何具有「巢狀對稱結構（如 HTML 標籤、JSON 括號、算術表達式）」或「回溯（Backtracking）」特性的問題，只要套上 Stack 就能迎刃而解。"
            "相對地，佇列遵循「先進先出（First-In, First-Out, FIFO）」原則：元素一律從隊尾進入（Enqueue），並從隊首離開（Dequeue）。"
            "這種公平排隊的機制，是作業系統 CPU 排程、訊息佇列（Message Queue）、Web 伺服器請求緩衝區，以及圖論「廣度優先搜尋（BFS）逐層擴散」不可或缺的核心引擎。"
        ),
        comparison_table=ComparisonTable(
            caption="表 2-1：Python 實作 Stack 與 Queue 各容器方案之時間複雜度與適用場景對照表",
            headers=(
                "容器方案 / 抽象結構",
                "尾端推入 append()",
                "尾端彈出 pop()",
                "首端彈出 popleft() / pop(0)",
                "工程實戰適用定位",
            ),
            rows=(
                (
                    "Stack（以 Python list 封裝）",
                    "攤銷 O(1)",
                    "O(1)",
                    "不適用（LIFO 僅操作尾端）",
                    "單執行緒 LIFO 堆疊首選，記憶體連續且存取速度最快。",
                ),
                (
                    "Queue（以 collections.deque 封裝）",
                    "O(1)",
                    "O(1)",
                    "O(1)（popleft）",
                    "FIFO 佇列與滑動視窗（Sliding Window）唯一標準正解。",
                ),
                (
                    "錯誤 Queue（誤用 list.pop(0)）",
                    "攤銷 O(1)",
                    "O(1)",
                    "O(n)（全體元素向前搬移）",
                    "嚴禁於大資料量使用！n 次出佇列總時間將退化為 O(n²)。",
                ),
                (
                    "queue.Queue / queue.LifoQueue",
                    "O(1)（含 Mutex 鎖開銷）",
                    "O(1)（含鎖開銷）",
                    "O(1)（含鎖開銷）",
                    "專供多執行緒（Multi-threading）生產者／消費者模型同步使用；演算法刷題勿用（無謂鎖開銷）。",
                ),
                (
                    "單調堆疊（Monotonic Stack）",
                    "每個元素最多入堆 1 次 O(1)",
                    "每個元素最多出堆 1 次 O(1)",
                    "不適用",
                    "在 O(n) 線性時間內解決「下一個更大／更小元素（Next Greater Element）」問題。",
                ),
            ),
        ),
        walkthrough_title="逐步拆解：括號平衡檢查器 is_balanced_brackets(\"{[()]}\") 四步驟堆疊追蹤",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1：依序讀取左括號 '{'、'['、'(' 並壓入堆疊",
                state_snapshot="輸入字元：'{' -> '[' -> '(' | Stack 狀態（底 -> 頂）：['{', '[', '(']",
                explanation=(
                    "迴圈巡覽字串前三個字元，由於 '{'、'['、'(' 皆屬於左括號集合 opening，因此依序呼叫 stack.push(ch)。"
                    "根據 LIFO 原則，越晚出現的左括號（越內層的括號 '('）會位在堆疊最頂端，等待最先被閉合。"
                ),
            ),
            WalkthroughStep(
                step_label="Step 2：讀取第一個右括號 ')' 並與堆頂比對彈出",
                state_snapshot="當前字元：')' | 查表 pairs[')'] == '(' | stack.pop() 彈出 '(' -> 配對成功！剩餘 Stack：['{', '[']",
                explanation=(
                    "遇到右括號 ')' 時，先確認 stack.is_empty() 為 False（代表有尚未配對的左括號），接著呼叫 stack.pop() 取出堆頂的 '('。"
                    "比對發現彈出的 '(' 完全等於 pairs[')']，證明最內層的小括號合法閉合，此時堆頂自然顯露出次內層的 '['。"
                ),
            ),
            WalkthroughStep(
                step_label="Step 3：依序讀取右括號 ']' 與 '}' 完成外層消除",
                state_snapshot="讀取 ']' 彈出 '[' -> 讀取 '}' 彈出 '{' | 剩餘 Stack：[]（空堆疊）",
                explanation=(
                    "繼續讀取 ']'，與堆頂彈出的 '[' 配對成功；再讀取 '}'，與堆頂彈出的 '{' 配對成功。"
                    "若中途遇到像 \"([)]\" 這種交錯順序，在讀取 ')' 時堆頂彈出的是 '[' != '('，函式便會在第一時間提早回傳 False。"
                ),
            ),
            WalkthroughStep(
                step_label="Step 4：迴圈結束後檢查 stack.is_empty() 防止多餘左括號",
                state_snapshot="return stack.is_empty() -> True（若輸入為 \"(((\" 則剩餘 3 個元素回傳 False）",
                explanation=(
                    "這是初學者最常漏寫的一步！迴圈平安跑完不代表一定合法（例如輸入 \"(((\" 從頭到尾都沒有觸發右括號失敗，但堆疊內還殘留 3 個未閉合的左括號）。"
                    "因此最後一行必須回傳 stack.is_empty()，唯有堆疊完全清空才代表 100% 成對平衡。"
                ),
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="陷阱一：在 BFS 或佇列模擬中寫出 queue.pop(0) 導致 O(n²) 超時（TLE）",
                symptom="在 LeetCode 執行廣度優先搜尋（BFS）或佇列題目時，小測資完全正確，一旦遇到 10 萬筆資料的隱藏測資立刻 Time Limit Exceeded。",
                root_cause_and_fix=(
                    "根因分析：Python 的 list.pop(0) 移除第一個元素後，必須在 C 底層呼叫 memmove 將後面 n-1 個指標全部往前挪一格，單次耗時 O(n)，"
                    "在迴圈中執行 n 次就會累積成 O(n²) 的效能災難。"
                    "正確對策：只要需要從左側（頭部）移除元素，一律執行 from collections import deque，並使用 queue.popleft()，確保單次操作嚴格為 O(1)。"
                ),
            ),
            PitfallItem(
                title="陷阱二：對空堆疊或空佇列直接呼叫 pop() / [-1] 觸發 IndexError",
                symptom="在括號檢查輸入為 \")\"（開頭就是右括號）時，未先檢查堆疊是否為空就直接執行 stack.pop()，導致程式崩潰。",
                root_cause_and_fix=(
                    "根因分析：當右括號數量多於左括號時，堆疊會在字串巡覽結束前提前變空。"
                    "正確對策：在呼叫 pop() 或存取堆頂元素前，必須以短路邏輯 if stack.is_empty() or stack.pop() != expected: 先行防護；"
                    "或者在自訂 Queue.peek() 中優雅回傳 None（如本章範例第 54 行）。"
                ),
            ),
            PitfallItem(
                title="陷阱三：不了解「單調堆疊（Monotonic Stack）」而用雙層迴圈硬解區間極值問題",
                symptom="面對「找出陣列中每個元素右邊第一個比它大的數（如每日溫度問題）」時，直覺寫出雙層 for 迴圈 O(n²)。",
                root_cause_and_fix=(
                    "根因分析：雙層迴圈重複比較了大量已經確定不可能成為答案的元素。"
                    "正確對策：維護一個「堆底到堆頂保持單調遞減（存索引）」的 Stack。當新元素大於堆頂索引對應的值時，不斷 pop() 堆頂並記錄答案，再將新索引 push() 入堆。"
                    "因為每個元素最多進堆一次、出堆一次，整體時間複雜度可直接從 O(n²) 降至線性 O(n)。"
                ),
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(
                number=20,
                title="Valid Parentheses（有效的括號）",
                difficulty="Easy",
                pattern="雜湊表配對字典 + LIFO 堆疊消除 ・ 時間 O(n) / 空間 O(n)",
            ),
            LeetCodeProblem(
                number=232,
                title="Implement Queue using Stacks（用兩個堆疊實作佇列）",
                difficulty="Easy",
                pattern="雙堆疊（in_stack 與 out_stack）懶惰倒換 ・ 攤銷時間 O(1) / 空間 O(n)",
            ),
            LeetCodeProblem(
                number=739,
                title="Daily Temperatures（每日溫度）",
                difficulty="Medium",
                pattern="單調遞減堆疊（Monotonic Decreasing Stack） ・ 時間 O(n) / 空間 O(n)",
            ),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="Q1：為什麼 CPython 的 collections.deque 可以同時做到雙端 O(1) 插入與刪除？它的底層結構是什麼？",
                answer=(
                    "collections.deque 在 CPython 底層（Modules/_collectionsmodule.c）並非使用單一連續陣列，而是實作為「由定長陣列區塊（Block，每個區塊可存放 64 個 PyObject* 指標）組成的雙向鏈結串列」，"
                    "並維護 leftblock/leftindex 與 rightblock/rightindex 兩組游標。"
                    "當執行 append() 或 popleft() 時，只需移動對應區塊內的游標（O(1)）；唯有當單一 64 元素區塊填滿或清空時，才配置或釋放一個區塊節點（同樣是 O(1)）。"
                    "這種區塊鏈結設計同時兼顧了雙端 O(1) 時間複雜度與優於傳統單節點鏈結串列的 CPU 快取局部性。"
                ),
            ),
            InterviewFAQ(
                question="Q2：面試常考「如何只用兩個 Stack（LIFO）實作出一個 Queue（FIFO）（LeetCode #232）」？為什麼時間複雜度是攤銷 O(1)？",
                answer=(
                    "準備兩個堆疊：in_stack（專門負責接收 enqueue 新元素）與 out_stack（專門負責提供 dequeue / peek 輸出）。"
                    "當呼叫 enqueue(x) 時，直接壓入 in_stack（O(1)）。當呼叫 dequeue() 或 peek() 時，若 out_stack 不為空，直接從 out_stack 彈出（O(1)）；"
                    "只有當 out_stack 完全為空時，才將 in_stack 中的所有元素逐一彈出並壓入 out_stack（經過兩次 LIFO 負負得正，順序剛好翻轉為 FIFO），再從 out_stack 頂端彈出。"
                    "因為每個元素一生只會經歷「進 in_stack 一次、出 in_stack 一次、進 out_stack 一次、出 out_stack 一次」共 4 次基本操作，所以攤銷時間複雜度嚴格為 O(1)。"
                ),
            ),
            InterviewFAQ(
                question="Q3：既然 collections.deque 雙端操作都是 O(1)，為什麼平常我們還是常拿 Python list 來當一般陣列，而不全部改用 deque？",
                answer=(
                    "關鍵在於「隨機索引讀取（Random Access, d[i]）」的複雜度差異！Python list 是連續記憶體區塊，讀取 list[50000] 是嚴格的 O(1)；"
                    "但 collections.deque 是由多個 64 元素區塊串接而成的鏈結結構，當你存取中間元素 deque[50000] 時，它必須沿著區塊鏈結逐塊跳轉，隨機存取時間複雜度退化為 O(n)。"
                    "因此：需要隨機索引、二分搜尋或排序時用 list；需要 FIFO 佇列、BFS 或雙端滑動視窗時用 collections.deque。"
                ),
            ),
        ),
    ),
    # =========================================================================
    # Ch.03 搜尋與排序演算法
    # =========================================================================
    ChapterSpec(
        id="ch03",
        badge="Ch.03",
        title="搜尋與排序演算法（Search & Sort Algorithms）",
        complexity="二分搜尋法 O(log n) ・ 合併排序法（Merge Sort）O(n log n)",
        summary="比較線性搜尋與二分搜尋的效率跨越，並以分治法（Divide & Conquer）實作穩定排序演算法 Merge Sort。",
        concepts=(
            "二分搜尋法（Binary Search）：在「已排序」的序列中，每次比對中間元素即可排除一半搜尋範圍，將搜尋複雜度由線性 O(n) 大幅降至對數級 O(log n)（100 萬筆資料最多只需比對約 20 次）。",
            "合併排序法（Merge Sort）：經典的「分治法（Divide and Conquer）」演算法，先遞迴將陣列對半拆解至單一元素，再以雙指標（Two Pointers）線性合併兩個已排序子陣列。無論最佳、平均或最壞情況，時間複雜度皆穩定維持 O(n log n)，且具備穩定排序（Stable Sort）特性。",
            "比較排序下界定理（Comparison Sort Lower Bound）：任何僅透過元素兩兩比較決定順序的排序演算法，其決策樹葉節點數至少為 n!，高度至少為 log₂(n!) = Ω(n log n)，因此 Merge Sort 在漸近時間複雜度上已達理論最優。",
        ),
        file="examples/ch03_search_sort.py",
        lastmod="2026-11-17",
        keywords=(
            "Python 二分搜尋法",
            "Binary Search",
            "合併排序法",
            "Merge Sort",
            "分治法 Divide and Conquer",
            "Timsort",
            "穩定排序 Stable Sort",
            "LeetCode 704",
        ),
        deep_intro=(
            "當資料規模從數百筆成長到數百萬筆時，O(n) 與 O(log n)、O(n²) 與 O(n log n) 之間的差距，就是系統「毫秒級回應」與「伺服器卡死超時」的分水嶺。"
            "以 1,000,000（一百萬）筆已排序資料為例，線性搜尋（Linear Search）在最壞情況下需要比對 1,000,000 次；"
            "而二分搜尋法（Binary Search）利用資料的單調性（Monotonicity），每次鎖定閉區間 [left, right] 的中點 mid，比對後直接捨棄不可能包含目標的一半區間，"
            "由於 2²⁰ = 1,048,576，最多只需比對 20 次即可斷定目標是否存在！"
            "然而，二分搜尋的前提是「資料必須預先排序」。傳統的氣泡排序（Bubble Sort）與插入排序（Insertion Sort）平均時間複雜度高達 O(n²)，"
            "面對百萬筆資料需執行 10¹² 次比較；而馮・諾伊曼（John von Neumann）提出的合併排序法（Merge Sort）則運用「分治法（Divide and Conquer）」："
            "將長為 n 的陣列遞迴對半切分為 log₂(n) 層，每一層再透過雙指標在 O(n) 時間內完成有序合併，總時間複雜度嚴格鎖定在 O(n log n)，更是 Python 內建 Timsort 的核心基石之一。"
        ),
        comparison_table=ComparisonTable(
            caption="表 3-1：主流搜尋與排序演算法之最佳／平均／最壞時間複雜度、空間複雜度與穩定性對照表",
            headers=(
                "演算法名稱",
                "最佳時間",
                "平均時間",
                "最壞時間",
                "額外空間與穩定性（Stability）",
            ),
            rows=(
                (
                    "線性搜尋（Linear Search）",
                    "O(1)",
                    "O(n)",
                    "O(n)",
                    "O(1) 空間 ・ 無須預先排序，適用於小型或未排序串列。",
                ),
                (
                    "二分搜尋（Binary Search）",
                    "O(1)",
                    "O(log n)",
                    "O(log n)",
                    "迭代版 O(1) 空間 ・ 必須具備已排序或單調性（Monotonicity）前提。",
                ),
                (
                    "插入排序（Insertion Sort）",
                    "O(n)（近乎有序）",
                    "O(n²)",
                    "O(n²)",
                    "O(1) 原地排序 ・ 穩定（Stable），極小規模（n <= 32）常數極小。",
                ),
                (
                    "合併排序（Merge Sort）",
                    "O(n log n)",
                    "O(n log n)",
                    "O(n log n)",
                    "O(n) 額外空間 ・ 穩定（Stable），保證無最壞退化，適合外部排序與鏈結串列排序。",
                ),
                (
                    "快速排序（Quick Sort）",
                    "O(n log n)",
                    "O(n log n)",
                    "O(n²)（Pivot 失衡）",
                    "O(log n) 遞迴堆疊 ・ 不穩定（Unstable），隨機化 Pivot 後實務快取表現極佳。",
                ),
                (
                    "Python 內建 Timsort（sort / sorted）",
                    "O(n)",
                    "O(n log n)",
                    "O(n log n)",
                    "O(n) 空間 ・ 穩定（Stable），融合 Insertion Sort 與自然區段 Merge Sort 之混合演算法。",
                ),
            ),
        ),
        walkthrough_title="逐步拆解：Merge Sort 分治排序 [38, 27, 43, 3] 與雙指標合併四步驟狀態追蹤",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1：Divide（遞迴對半拆分至基底條件 len <= 1）",
                state_snapshot="[38, 27, 43, 3] -> 左半 [38, 27] 與 右半 [43, 3] -> 拆至單元素 [38], [27], [43], [3]",
                explanation=(
                    "呼叫 merge_sort([38, 27, 43, 3])，計算 mid = 2，遞迴拆分左半 [38, 27] 與右半 [43, 3]。"
                    "下一層再各自對半拆為單一元素 [38]、[27]、[43]、[3]，觸發基底條件 if len(arr) <= 1: return arr，因為長度為 1 的陣列天然已排序。"
                ),
            ),
            WalkthroughStep(
                step_label="Step 2：Conquer 底層合併 — 局部子陣列兩兩有序歸併",
                state_snapshot="合併 ([38], [27]) -> left_half = [27, 38] | 合併 ([43], [3]) -> right_half = [3, 43]",
                explanation=(
                    "遞迴開始向上回傳：左分支比對 38 與 27，將較小的 27 先放入 merged，再放入 38，得到有序的 [27, 38]；"
                    "右分支比對 43 與 3，得到有序的 [3, 43]。此時最頂層的兩個子問題皆已完成排序。"
                ),
            ),
            WalkthroughStep(
                step_label="Step 3：Combine 頂層雙指標（i, j）線性比對合併",
                state_snapshot="left_half=[27, 38] (i), right_half=[3, 43] (j) -> 依序比對選出 3 -> 27 -> 38",
                explanation=(
                    "初始化雙指標 i = 0（指向 27）、j = 0（指向 3）："
                    "(1) 比對 27 vs 3：取右邊 3，j 推進至 1（指向 43），merged = [3]；"
                    "(2) 比對 27 vs 43：取左邊 27，i 推進至 1（指向 38），merged = [3, 27]；"
                    "(3) 比對 38 vs 43：取左邊 38，i 推進至 2（超出左半長度，結束 while 迴圈），merged = [3, 27, 38]。"
                ),
            ),
            WalkthroughStep(
                step_label="Step 4：尾端剩餘元素收尾（merged.extend）與穩定性保證",
                state_snapshot="右半尚餘 right_half[1:] == [43] -> merged.extend([43]) -> 最終結果 [3, 27, 38, 43]",
                explanation=(
                    "當其中一邊子陣列先取完時，另一邊剩下的元素（此處為 [43]）必然全部大於已合併元素且本身已排序，直接呼叫 merged.extend() 附加至尾端。"
                    "注意第 39 行判斷條件必須寫成 left_half[i] <= right_half[j]（包含等號），確保左右遇到相等值時優先取左半元素，維持相等元素的原始相對順序（Stable Sort）。"
                ),
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="陷阱一：二分搜尋區間定義混亂（閉區間 [left, right] vs. 左閉右開 [left, right)）導致無窮迴圈",
                symptom="在寫二分搜尋時，有時寫 while left <= right，有時寫 right = mid，結果在剩餘 2 個元素時卡死在無窮迴圈或漏查最後一個元素。",
                root_cause_and_fix=(
                    "根因分析：未固定「搜尋區間不變量（Loop Invariant）」。"
                    "正確對策：若像本章範例採用「雙閉區間 [left, right]（初始化 right = len(nums) - 1）」，則 while 條件必為 left <= right（因為 left == right 時區間內仍有 1 個合法元素需檢查），"
                    "且當 nums[mid] 已比對失敗時，mid 必須排除在下一輪區間外，故必寫 left = mid + 1 與 right = mid - 1。"
                ),
            ),
            PitfallItem(
                title="陷阱二：Merge Sort 合併時誤將 <= 寫成 < 破壞排序穩定性（Stability）",
                symptom="對包含多個欄位的物件（如先按分數排序、同分再保持原本報名順序）執行自訂 Merge Sort 後，同分者的先後順序被顛倒。",
                root_cause_and_fix=(
                    "根因分析：若寫成 if left_half[i] < right_half[j]，當左右兩邊元素相等時會跳進 else 分支先取右半邊（原本位置在後面）的元素，破壞了穩定性。"
                    "正確對策：合併條件務必使用 <=（if left_half[i] <= right_half[j]:），確保相等時永遠左半邊優先出列。"
                ),
            ),
            PitfallItem(
                title="陷阱三：不熟悉 Python 標準庫 bisect 而在面試中花 15 分鐘重造尋找插入點輪子",
                symptom="當題目需要「在已排序陣列中找出第一個 >= target 或 > target 的插入位置（Lower Bound / Upper Bound）」時，手寫變形二分搜尋卻在重複元素邊界出錯。",
                root_cause_and_fix=(
                    "根因分析：標準二分搜尋在遇到重複元素（如 [1, 2, 2, 2, 3] 找 2）時只能回傳任意一個 2 的索引，不保證是最左或最右邊界。"
                    "正確對策：熟記手寫二分搜尋模板以應對旋轉陣列等進階變形；但若為標準有序序列查邊界，在 Python 中可直接調用 C 語言加速的 bisect.bisect_left(a, x)（第一個 >= x 的索引）與 bisect.bisect_right(a, x)（第一個 > x 的索引）。"
                ),
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(
                number=704,
                title="Binary Search（標準二分搜尋法）",
                difficulty="Easy",
                pattern="雙閉區間 [left, right] 中點折半搜尋 ・ 時間 O(log n) / 空間 O(1)",
            ),
            LeetCodeProblem(
                number=33,
                title="Search in Rotated Sorted Array（搜尋旋轉排序陣列）",
                difficulty="Medium",
                pattern="二分搜尋判斷哪一半部維持嚴格有序 ・ 時間 O(log n) / 空間 O(1)",
            ),
            LeetCodeProblem(
                number=912,
                title="Sort an Array（排序陣列）",
                difficulty="Medium",
                pattern="分治法 Merge Sort 穩定排序實作 ・ 時間 O(n log n) / 空間 O(n)",
            ),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="Q1：為什麼二分搜尋計算中點時，許多教材與本章範例第 15 行都寫成 mid = left + (right - left) // 2，而不直接寫 (left + right) // 2？",
                answer=(
                    "在 C、C++、Java 等使用固定 32 位元有號整數（上限 2³¹ - 1 ≈ 21.4 億）的語言中，當陣列很大且 left 與 right 都超過 11 億時，"
                    "直接相加 (left + right) 會發生「整數溢位（Integer Overflow）」變成負數，引發陣列越界崩潰；改寫為 left + (right - left) // 2 則永遠不會超出 right 的範圍。"
                    "雖然 Python 3 的 int 支援任意精度大整數不會發生溢位，但在跨語言技術面試中寫出 left + (right - left) // 2 能展現工程師對數值邊界安全的嚴謹素養。"
                ),
            ),
            InterviewFAQ(
                question="Q2：Quick Sort（快速排序）平均速度很快且原地排序，為什麼許多系統底層（如 Python Timsort）對物件排序仍偏好 Merge Sort 的穩定概念？",
                answer=(
                    "主要有兩個原因：第一是「最壞時間複雜度保證」，Quick Sort 若遇到刻意構造的輸入或大量重複值且未做三向切分（3-Way Partition），最壞情況會退化至 O(n²)，"
                    "而 Merge Sort 無論輸入資料分布為何，時間複雜度永遠是鐵打的 O(n log n)；"
                    "第二是「穩定性（Stability）」，Quick Sort 在遠距交換元素時會打亂相等鍵值物件的原始順序，而 Merge Sort 天然穩定，這在多鍵值複合排序（如試算表先排姓名再排部門）中是不可或缺的正確性需求。"
                ),
            ),
            InterviewFAQ(
                question="Q3：Python 內建的 list.sort() 與 sorted() 使用的 Timsort 演算法，是如何做到在最佳情況下只需 O(n) 時間的？",
                answer=(
                    "Timsort 是由 Tim Peters 為 Python 設計的混合穩定排序演算法。它洞察到真實世界的資料通常已經包含許多「局部自然有序區段（Natural Runs，遞增或嚴格遞減區段）」。"
                    "Timsort 會先線性掃描陣列識別這些天然有序的 Run（若嚴格遞減則原地反轉為遞增；若長度不足 minrun 則以二分插入排序補齊），接著利用堆疊規則將這些 Run 智慧合併。"
                    "如果傳入的陣列本身已經排序好（或完全逆序），Timsort 只需一次 O(n) 掃描即可識別出單一完整 Run 並直接結束，無須做任何拆解合併！"
                ),
            ),
        ),
    ),
    # =========================================================================
    # Ch.04 雜湊表與二元搜尋樹
    # =========================================================================
    ChapterSpec(
        id="ch04",
        badge="Ch.04",
        title="雜湊表與二元搜尋樹（Hash Table & Binary Search Tree）",
        complexity="雜湊表平均讀寫 O(1) ・ 二元搜尋樹平衡搜尋/插入 O(log n) ・ 中序走訪 O(n)",
        summary="掌握面試出場率最高的雜湊碰撞處理（Separate Chaining）與 Two Sum O(n) 秒殺技巧，並實作二元搜尋樹（BST）與中序遞增走訪。",
        concepts=(
            "雜湊表（Hash Table / Python dict）：透過雜湊函式（Hash Function）將鍵值映射至桶位索引，達成平均 O(1) 的極速查找；當不同鍵值落入同一桶位產生碰撞（Collision）時，常以鏈結法（Separate Chaining）或開放定址法（Open Addressing）化解。經典白板題 Two Sum 即是利用 Hash Table 以空間換取時間，將雙層迴圈 O(n²) 降至單次掃描 O(n)。",
            "二元搜尋樹（Binary Search Tree, BST）：滿足「左子樹所有節點 < 根節點 < 右子樹所有節點」不變量（Invariant）的樹狀結構。在樹高平衡時搜尋與插入皆為 O(log n)，且對 BST 執行「左 -> 根 -> 右」中序走訪（In-order Traversal）即可在 O(n) 時間內直接輸出由小到大的排序結果。",
            "無序極速查找 vs. 有序範圍查找：Hash Table 擁有平均 O(1) 單點查詢優勢，但鍵值經過雜湊後失去大小順序，無法支援範圍查詢（Range Query）或前驅／後繼查找；BST 則透過樹狀偏序結構同時兼顧動態更新與有序性。",
        ),
        file="examples/ch04_hash_bst.py",
        lastmod="2026-11-17",
        keywords=(
            "Python 雜湊表",
            "Hash Table",
            "Two Sum 解法",
            "二元搜尋樹",
            "Binary Search Tree",
            "BST 中序走訪",
            "雜湊碰撞 Separate Chaining",
            "LeetCode 1",
        ),
        deep_intro=(
            "在軟體工程師白板面試中，流傳著一句名言：「當你不知道怎麼把 O(n²) 最佳化時，先想想能不能用雜湊表（Hash Table）以空間換取時間。」"
            "雜湊表的核心魔法在於雜湊函式（Hash Function）：它能將任意不可變鍵值（如字串 \"aily\" 或整數）轉換為固定長度的整數雜湊碼，再對桶位陣列長度取模（hash(key) % bucket_count），"
            "直接算出該鍵值在記憶體中的儲存桶位，讓查找、插入與刪除在平均情況下都不受資料總量 n 影響，達成驚人的 O(1) 常數時間！"
            "然而根據鴿籠原理（Pigeonhole Principle），當鍵值空間大於桶位數量時，必然會發生兩個不同鍵值算出相同桶位索引的「雜湊碰撞（Hash Collision）」。"
            "本章親手實作了最經典的「分離鏈結法（Separate Chaining）」碰撞處理機制，並展示如何用 dict 在單次迴圈 O(n) 時間內秒殺 LeetCode 第 1 題 Two Sum。"
            "與此同時，若業務場景需要「動態維護資料由小到大的順序」、「查詢排名第 k 小的元素」或「找出介於 [L, R] 之間的所有數值」，無序的雜湊表便無能為力——"
            "這正是二元搜尋樹（Binary Search Tree, BST）大顯身手的舞台。"
        ),
        comparison_table=ComparisonTable(
            caption="表 4-1：雜湊表（Hash Table）、平衡二元搜尋樹與退化二元搜尋樹之複雜度與功能特性對照表",
            headers=(
                "操作 / 特性維度",
                "雜湊表（Hash Table / dict）",
                "平衡二元搜尋樹（Balanced BST）",
                "退化二元搜尋樹（Skewed BST）",
                "架構選型關鍵決策點",
            ),
            rows=(
                (
                    "單點搜尋 / 插入 / 刪除（平均）",
                    "O(1)",
                    "O(log n)",
                    "O(n)（退化為單向鏈結串列）",
                    "純粹依 Key 精確查找（Exact Match）永遠優先選用 Hash Table。",
                ),
                (
                    "最壞情況時間複雜度",
                    "O(n)（全數碰撞落入同一桶）",
                    "O(log n)（紅黑樹 / AVL 旋轉維持）",
                    "O(n)（輸入已排序序列時必然發生）",
                    "一般 BST 若未搭配自平衡機制，切勿直接餵入已排序資料。",
                ),
                (
                    "依大小順序輸出全體元素",
                    "O(n log n)（需額外呼叫 sorted）",
                    "O(n)（直接執行 In-order 中序走訪）",
                    "O(n)（中序走訪）",
                    "BST 的「左 -> 根 -> 右」中序走訪天然就是遞增排序序列。",
                ),
                (
                    "範圍查詢 [L, R] 與最大/最小值",
                    "O(n)（必須全表掃描）",
                    "最大/最小 O(log n)；範圍 O(log n + k)",
                    "O(n)",
                    "資料庫索引（B+ Tree）與有序集合皆依賴搜尋樹的有序剪枝能力。",
                ),
                (
                    "鍵值（Key）型別限制",
                    "必須可雜湊（Hashable / 不可變）",
                    "必須可比較大小（Comparable, 支援 <）",
                    "必須可比較大小（支援 <）",
                    "Python dict 的 key 不能是 list；BST 的節點值則必須支援大小比較。",
                ),
            ),
        ),
        walkthrough_title="逐步拆解：Two Sum 單次雜湊掃描（nums = [2, 7, 11, 15], target = 9）與 BST 中序走訪追蹤",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1：Two Sum 第一輪（idx = 0, num = 2）— 計算補數並登記至 seen",
                state_snapshot="target = 9, num = 2 -> complement = 9 - 2 = 7 | 7 not in seen {} -> 寫入 seen = {2: 0}",
                explanation=(
                    "我們不再使用雙層迴圈往後找誰加 2 等於 9，而是反過來問：「之前看過的數字裡，有沒有 7（complement = target - num）？」"
                    "此時雜湊表 seen 為空，7 不在裡面，於是將當前數字與索引配對 2: 0 存入 seen，耗時 O(1)。"
                ),
            ),
            WalkthroughStep(
                step_label="Step 2：Two Sum 第二輪（idx = 1, num = 7）— O(1) 命中補數立即回傳",
                state_snapshot="target = 9, num = 7 -> complement = 9 - 7 = 2 | 2 in seen {2: 0} -> 立即回傳 (seen[2], 1) == (0, 1)！",
                explanation=(
                    "巡覽到索引 1 的數字 7 時，計算補數 complement = 9 - 7 = 2，執行 if complement in seen 查詢雜湊表。"
                    "瞬間命中先前存入的 seen[2] == 0，立即回傳 (0, 1)，連後面的 11 與 15 都不必再看，完美在單次掃描 O(n) 時間內收工！"
                ),
            ),
            WalkthroughStep(
                step_label="Step 3：BST 插入建樹 — 維持「左子樹 < 根 < 右子樹」不變量",
                state_snapshot="依序插入 [50, 30, 70, 20, 40, 60, 80] -> 根 50 | 左子樹根 30 (含 20, 40) | 右子樹根 70 (含 60, 80)",
                explanation=(
                    "第一個元素 50 成為 root。接著插入 30（30 < 50 放左子節點）、70（70 > 50 放右子節點）。"
                    "插入 40 時，先比對 40 < 50 往左走到 30，再比對 40 > 30 往右放到 30.right。每次往下走一層就排除一半子樹，高度平衡時僅需 O(log n) 步。"
                ),
            ),
            WalkthroughStep(
                step_label="Step 4：BST 中序走訪（In-order：左 -> 根 -> 右）自動產出遞增序列",
                state_snapshot="_traverse(left) -> append(node.val) -> _traverse(right) => [20, 30, 40, 50, 60, 70, 80]",
                explanation=(
                    "中序走訪從 50 一路遞迴往左深入到 30 再到葉節點 20：先印出 20，回到父節點印出 30，再走訪 30 的右子節點印出 40；"
                    "左子樹全數完成後回到樹根印出 50，接著以同樣規則走訪右子樹印出 60、70、80。由於嚴格遵循「左小、中根、右大」，輸出結果必為嚴格遞增序列！"
                ),
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="陷阱一：拿可變物件（如 list 或 dict）當作雜湊表（dict / set）的 Key 觸發 TypeError",
                symptom="在將座標或陣列狀態存入 dict / set 時寫出 visited.add([x, y])，立即拋出 TypeError: unhashable type: 'list'。",
                root_cause_and_fix=(
                    "根因分析：雜湊表依賴 Key 的雜湊值 hash(key) 來決定桶位索引。如果 Key 在存入後內容被修改（如 list.append），其雜湊值就會改變，導致在原本的桶位再也找不到該物件，破壞雜湊表不變量。"
                    "正確對策：在 Python 中作為 dict 或 set 的 Key 必須是不可變型別（Immutable）：請將 list 轉為 tuple(lst)（如 visited.add((x, y))），將 set 轉為 frozenset。"
                ),
            ),
            PitfallItem(
                title="陷阱二：驗證二元搜尋樹（LeetCode #98 Validate BST）時只檢查「左子節點 < 父節點 < 右子節點」",
                symptom="寫出 if node.left.val < node.val < node.right.val 就以為是合法 BST，結果遇到根為 50、右子節點為 70、但 70 的左子節點為 40（40 < 50 卻出現在 50 的右子樹！）時誤判為 True。",
                root_cause_and_fix=(
                    "根因分析：BST 的不變量要求「右子樹中的『所有』節點都必須大於根節點」，而不只是直接相連的右子節點。"
                    "正確對策：遞迴驗證時必須向下傳遞合法區間上下界 validate(node, low, high)（往左走更新上界 high = node.val；往右走更新下界 low = node.val），或直接檢查中序走訪序列是否嚴格遞增。"
                ),
            ),
            PitfallItem(
                title="陷阱三：對未平衡的一般 BST 依序插入已排序資料 [10, 20, 30, 40, 50] 導致退化為 O(n)",
                symptom="在測試時為了方便，將排序好的陣列依序呼叫 bst.insert(x)，結果樹高變成 n，搜尋速度退化得跟單向鏈結串列一樣慢。",
                root_cause_and_fix=(
                    "根因分析：當輸入序列單調遞增時，每個新節點都比前一個大，會一路掛在最右側（right -> right -> right），形成沒有任何左分支的「退化斜樹（Degenerate / Skewed Tree）」。"
                    "正確對策：若已知輸入為已排序陣列，應每次取中點 mid 作為子樹根遞迴建樹（LeetCode #108）；若為動態隨機插入，工業界資料庫與語言標準庫則會採用紅黑樹（Red-Black Tree）或 AVL 樹透過旋轉維持樹高 O(log n)。"
                ),
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(
                number=1,
                title="Two Sum（兩數之和）",
                difficulty="Easy",
                pattern="單次掃描雜湊表查詢補數（target - num） ・ 時間 O(n) / 空間 O(n)",
            ),
            LeetCodeProblem(
                number=98,
                title="Validate Binary Search Tree（驗證二元搜尋樹）",
                difficulty="Medium",
                pattern="遞迴傳遞上下界 (low, high) 或中序遞增檢查 ・ 時間 O(n) / 空間 O(h)",
            ),
            LeetCodeProblem(
                number=230,
                title="Kth Smallest Element in a BST（二元搜尋樹中第 K 小的元素）",
                difficulty="Medium",
                pattern="BST 中序走訪（In-order Traversal）第 k 個訪問節點 ・ 時間 O(H + k) / 空間 O(H)",
            ),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="Q1：本章 ChainingHashTable 使用「分離鏈結法」處理碰撞，那 CPython 內建的 dict 底層也是用鏈結法嗎？為什麼 Python 3.7+ 的 dict 能保持插入順序？",
                answer=(
                    "CPython 內建的 dict 採用的是「緊湊開放定址法（Compact Open Addressing）」，而非鏈結法。在 Python 3.6+ 改版後，dict 底層拆分為兩張陣列："
                    "一張是稀疏的雜湊索引表 indices（僅儲存整數偏移量，只佔 1～8 bytes），另一張是緊湊排列的 entries 陣列（依插入先後順序連續儲存 (hash, key, value)）。"
                    "當發生碰撞時，CPython 利用偽隨機探測序列在 indices 表中尋找下一個空槽。這項設計不僅讓 dict 的記憶體消耗大減 20%～25%，更因為 entries 陣列是依插入順序連續追加的，所以天然保證了迭代順序等於插入順序！"
                ),
            ),
            InterviewFAQ(
                question="Q2：什麼是雜湊表的「負載因子（Load Factor, α = n / m）」？當負載因子過高時雜湊表如何維持 O(1) 效能？",
                answer=(
                    "負載因子 α 定義為「已存入的元素數量 n」除以「總桶位數 m」。隨著 α 上升，發生雜湊碰撞的機率會急遽增加（例如開放定址法在 α > 2/3 時探測次數會明顯上升）。"
                    "為了維持 O(1) 平均讀寫效能，當 α 超過預設門檻（CPython dict 門檻為 2/3 ≈ 0.66；Java HashMap 為 0.75）時，雜湊表會自動觸發「擴容與重雜湊（Resize & Rehash）」："
                    "配置一張容量翻倍的新桶位陣列，並將所有既有鍵值重新計算 hash(key) % new_m 搬移過去，使攤銷時間複雜度依然維持在 O(1)。"
                ),
            ),
            InterviewFAQ(
                question="Q3：既然二元搜尋樹（BST）的中序走訪可以在 O(n) 時間內輸出排序結果，那是不是代表我們可以用 BST 在 O(n) 時間內完成任意陣列排序？",
                answer=(
                    "不能！這是一個非常經典的面試陷阱題。雖然對一棵「已經建好的 BST」執行中序走訪確實只要 O(n) 時間，但別忘了「把 n 個無序元素逐一 insert 進平衡 BST」的建樹過程："
                    "每次插入需耗時 O(log n)，插入 n 個元素的建樹總時間為 O(n log n)。因此「BST 建樹 O(n log n) + 中序走訪 O(n)」的總體時間複雜度依然是 O(n log n)，完全符合比較排序的 Ω(n log n) 理論下界。"
                ),
            ),
        ),
    ),
    # =========================================================================
    # Ch.05 圖論走訪與物件導向設計
    # =========================================================================
    ChapterSpec(
        id="ch05",
        badge="Ch.05",
        title="圖論走訪與物件導向設計（Graph BFS / DFS & OOP）",
        complexity="BFS / DFS 走訪與無權重最短路徑均為 O(V + E)",
        summary="以物件導向封裝鄰接串列（Adjacency List），實作廣度優先搜尋（BFS）、深度優先搜尋（DFS）與無權重圖最短路徑回溯。",
        concepts=(
            "廣度優先搜尋（BFS）vs. 深度優先搜尋（DFS）：BFS 搭配佇列（Queue / deque）由起點呈同心圓逐層向外擴散，因此第一次抵達終點時必為「最少步數最短路徑」；DFS 則利用遞迴（Call Stack）或顯式堆疊一條路走到底再回溯（Backtracking），常用於連通分量、拓樸排序與環路檢測。",
            "物件導向封裝（OOP Encapsulation）：將內部鄰接串列 `_adj` 與訪問狀態隱藏於 `Graph[T]` 類別方法內，對外提供乾淨的 `add_edge`、`bfs`、`dfs` 與 `shortest_path_bfs` 介面，兼具型別安全與高維護性。",
            "圖的表示法權衡：稀疏圖（Sparse Graph，邊數 E 遠小於 V²）採用鄰接串列（Adjacency List）僅需 O(V + E) 空間；稠密圖（Dense Graph）採用鄰接矩陣（Adjacency Matrix）雖需 O(V²) 空間，但能於 O(1) 時間判斷任兩點是否相連。",
        ),
        file="examples/ch05_graph_oop.py",
        lastmod="2026-11-17",
        keywords=(
            "Python 圖論",
            "Graph BFS DFS",
            "廣度優先搜尋",
            "深度優先搜尋",
            "最短路徑演算法",
            "鄰接串列 Adjacency List",
            "物件導向 OOP",
            "LeetCode 200",
        ),
        deep_intro=(
            "前面學過的鏈結串列與二元搜尋樹，其實都只是「圖（Graph, G = (V, E)）」的特例：鏈結串列是沒有分支的線性圖，而樹則是「連通且無環（Connected Acyclic）」的圖。"
            "一旦進入真實世界的網路拓樸、社群好友關係、地圖導航、套件相依性解析（如 pip / npm）或迷宮尋路，節點（Vertex, V）與邊（Edge, E）之間往往存在多對多連接與環路（Cycle），"
            "這時就必須仰賴圖論兩大核心走訪引擎：**廣度優先搜尋（Breadth-First Search, BFS）** 與 **深度優先搜尋（Depth-First Search, DFS）**。"
            "在工程架構上，初學者寫圖論題常把全域變數 dictionary、visited set 與鄰接表散落在腳本各處，導致多次查詢時狀態互相污染。"
            "本章特別結合 Python 3.12 泛型物件導向設計（Generic OOP，`class Graph(Generic[T])`），將底層鄰接串列 `_adj: dict[T, list[T]]` 嚴密封装，"
            "並將 `visited` 與 `parent` 狀態局部化於各演算法方法內，展示如何寫出同時具備工業級可讀性與 O(V + E) 最佳時間複雜度的圖論模組。"
        ),
        comparison_table=ComparisonTable(
            caption="表 5-1：圖論表示法（鄰接串列 vs. 鄰接矩陣）與走訪演算法（BFS vs. DFS）完整對照表",
            headers=(
                "比較項目 / 演算法",
                "核心資料結構",
                "時間複雜度",
                "空間複雜度",
                "最佳適用場景與關鍵特性",
            ),
            rows=(
                (
                    "鄰接串列（Adjacency List）",
                    "dict[T, list[T]]",
                    "巡覽所有鄰居 O(V + E)",
                    "O(V + E)",
                    "真實世界 95% 以上稀疏圖（社交網路、道路網、工作流）之標準首選。",
                ),
                (
                    "鄰接矩陣（Adjacency Matrix）",
                    "V × V 二維陣列",
                    "查兩點連線 O(1)；全圖走訪 O(V²)",
                    "O(V²)",
                    "僅適用於頂點數 V 很小（如 V <= 500）的稠密圖或 Floyd-Warshall 全點對最短路徑。",
                ),
                (
                    "廣度優先搜尋（BFS）",
                    "佇列 Queue（collections.deque）+ visited",
                    "O(V + E)",
                    "O(V)（佇列最大寬度）",
                    "像水波同心圓逐層擴散，保證在「無權重圖」中第一次抵達終點即為最少步數最短路徑。",
                ),
                (
                    "深度優先搜尋（DFS）",
                    "遞迴 Call Stack 或顯式 Stack + visited",
                    "O(V + E)",
                    "O(V)（最大遞迴深度）",
                    "不撞南牆不回頭再回溯（Backtracking），適合連通分量計數、環路檢測、拓樸排序與排列組合。",
                ),
                (
                    "BFS 最短路徑回溯（shortest_path_bfs）",
                    "deque + parent: dict[T, T | None]",
                    "O(V + E)",
                    "O(V)",
                    "利用 parent 字典記錄「誰把我帶進佇列」，抵達終點後逆向回推並 reverse() 還原完整路徑。",
                ),
            ),
        ),
        walkthrough_title="逐步拆解：無權重圖 BFS 最短路徑回溯（A -> F）四步驟佇列與 parent 字典追蹤",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1：初始化起點 A 的佇列與前驅字典 parent",
                state_snapshot="queue = deque(['A']) | parent = {'A': None}（兼作已訪問集合 visited）",
                explanation=(
                    "在 shortest_path_bfs('A', 'F') 中，我們巧妙地用 parent: dict[T, T | None] = {'A': None} 同時扮演兩個角色："
                    "一是判斷某頂點是否已被訪問過（nb not in parent），二是記錄每個頂點是由哪一個前驅頂點擴展而來的（起點 A 沒有前驅，故為 None）。"
                ),
            ),
            WalkthroughStep(
                step_label="Step 2：第 0 層擴展 — 彈出 A 並將第 1 層鄰居 B、C 入佇列",
                state_snapshot="popleft() -> 'A' | 擴展鄰居 B, C -> queue = deque(['B', 'C']) | parent = {'A': None, 'B': 'A', 'C': 'A'}",
                explanation=(
                    "從佇列首端彈出 A，檢視 A 的鄰居 ['B', 'C']。由於 B 與 C 都還不在 parent 中，立即登記 parent['B'] = 'A'、parent['C'] = 'A'，"
                    "並將 B、C 推入佇列尾端。這代表所有距離起點 A 步數為 1 的頂點皆已完成排隊。"
                ),
            ),
            WalkthroughStep(
                step_label="Step 3：第 1 層擴展 — 依序彈出 B、C 並將第 2 層鄰居 D、E 入佇列",
                state_snapshot="彈出 B -> 推入 D (parent['D']='B') | 彈出 C -> 推入 E (parent['E']='C') | queue = deque(['D', 'E'])",
                explanation=(
                    "接著彈出 B，其鄰居 A 已在 parent 中跳過，未訪問鄰居 D 登記 parent['D'] = 'B' 並入佇列；"
                    "再彈出 C，將未訪問鄰居 E 登記 parent['E'] = 'C' 並入佇列。此時佇列中全數為距離起點步數為 2 的頂點。"
                ),
            ),
            WalkthroughStep(
                step_label="Step 4：第 2 層擴展命中終點 F 並沿 parent 逆向還原最短路徑",
                state_snapshot="彈出 D -> 鄰居 F == goal！登記 parent['F']='D' | 逆推 F -> D -> B -> A，反轉得 ['A', 'B', 'D', 'F']",
                explanation=(
                    "彈出 D，發現鄰居 F 恰好等於目標 goal！立即記錄 parent['F'] = 'D'，接著從 step = 'F' 開始沿著 parent[step] 往回走："
                    "'F' -> 'D' -> 'B' -> 'A' -> None，得到逆序路徑 ['F', 'D', 'B', 'A']，最後呼叫 path.reverse() 即回傳最短路徑 ['A', 'B', 'D', 'F']。"
                ),
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="陷阱一：BFS 在「彈出佇列（popleft）」時才標記 visited，導致同一節點被重複推入佇列數十次",
                symptom="在網格地圖或稠密圖跑 BFS 時，雖然最後答案對，但執行時間極慢甚至在 LeetCode 觸發 Memory Limit Exceeded (MLE)。",
                root_cause_and_fix=(
                    "根因分析：若等到 curr = queue.popleft() 時才執行 visited.add(curr)，那麼在 curr 還在佇列中排隊等待的期間，"
                    "其他同樣連向 curr 的節點會發現 curr not in visited 為 True，因而把 curr 重複推入佇列許多次（在網格圖中每層重複率呈指數上升）。"
                    "正確對策：務必像本章範例第 48–49 行，在「準備將鄰居 nb 推入 queue 的當下」就立即執行 visited.add(nb)（或登記 parent[nb] = curr）！"
                ),
            ),
            PitfallItem(
                title="陷阱二：在「有權重圖（Weighted Graph，每條邊成本不同）」誤用一般 BFS 求最短路徑",
                symptom="地圖上 A 到 B 有一條直達高速公路（耗時 100 分鐘，1 步），以及一條經由 C 的替代道路（A->C 10 分鐘 + C->B 10 分鐘 = 20 分鐘，2 步），用 BFS 卻選出 100 分鐘的直達路。",
                root_cause_and_fix=(
                    "根因分析：標準 BFS 保證的是「最少邊數（Hops）」，而非「最小權重總和」。"
                    "正確對策：無權重圖（或所有邊權重皆相等）的最短路徑用 BFS O(V + E)；若邊具有非負權重（Non-negative Weights），必須結合第 7 章的最小堆積優先佇列（Min-Heap）改用 **Dijkstra 演算法** O((V + E) log V)。"
                ),
            ),
            PitfallItem(
                title="陷阱三：オブジェクト封裝時直接回傳內部參考 return self._adj[vertex] 破壞封裝安全性",
                symptom="外部呼叫者拿到 g.neighbors('A') 後對回傳的 list 執行 .append('Z') 或 .clear()，意外竄改了 Graph 內部的鄰接串列結構。",
                root_cause_and_fix=(
                    "根因分析：Python 的 list 是可變物件（Mutable），直接回傳內部屬性會暴露私有狀態的記憶體參照（Aliasing Bug）。"
                    "正確對策：如本章範例第 34 行 def neighbors(self, vertex: T) -> list[T]: return list(self._adj.get(vertex, []))，透過淺拷貝（Shallow Copy）回傳新串列，確保物件導向封裝的不變量。"
                ),
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(
                number=200,
                title="Number of Islands（島嶼數量）",
                difficulty="Medium",
                pattern="二維網格圖連通分量（Connected Components）BFS / DFS 染色走訪 ・ 時間 O(M × N) / 空間 O(M × N)",
            ),
            LeetCodeProblem(
                number=994,
                title="Rotting Oranges（腐爛的橘子）",
                difficulty="Medium",
                pattern="多源廣度優先搜尋（Multi-Source BFS）逐層計時擴散 ・ 時間 O(M × N) / 空間 O(M × N)",
            ),
            LeetCodeProblem(
                number=207,
                title="Course Schedule（課程表先修相依檢查）",
                difficulty="Medium",
                pattern="有向圖環路檢測：Kahn 演算法（入度 In-degree + BFS 拓樸排序）或三色標記 DFS ・ 時間 O(V + E)",
            ),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="Q1：為什麼圖論 BFS 與 DFS 的時間複雜度會寫成 O(V + E)，而不是 O(V × E) 或只寫 O(E)？",
                answer=(
                    "在使用鄰接串列（Adjacency List）並搭配 visited 集合時，每個頂點（Vertex）最多只會被放進佇列／遞迴呼叫 1 次，處理頂點本身的總時間為 O(V)；"
                    "而當某個頂點 u 被取出時，內層 for 迴圈只會巡覽 u 的鄰接邊（Degree of u）。將全圖所有頂點的鄰接邊加總起來，在有向圖剛好等於 E 條邊、無向圖等於 2E 條邊，因此巡覽邊的總時間為 O(E)。"
                    "之所以必須同時寫出 V + E，是因為若圖中有大量沒有連邊的孤立頂點（V >> E），耗時由 O(V) 主導；若為連通圖（E >= V - 1），則由 O(E) 主導，故寫為 O(V + E) 最為精確。"
                ),
            ),
            InterviewFAQ(
                question="Q2：面試遇到二維網格題（如迷宮或島嶼數量），什麼時候該選 BFS？什麼時候該選 DFS？",
                answer=(
                    "判斷準則非常明確："
                    "(1) 只要題目問「最少步數」、「最短距離」、「最少經過幾個轉折」或「多源同時擴散需要幾分鐘（如腐爛橘子 LeetCode #994）」，**100% 必選 BFS**，因為 DFS 第一條走到終點的路徑往往是繞遠路的；"
                    "(2) 若題目問「連通區塊總數（島嶼數量 #200）」、「是否存在任一合法路徑」或「列出所有可能路徑（Backtracking）」，DFS 程式碼更簡短直覺；但若網格高達 1000 × 1000，Python 遞迴 DFS 會觸發 RecursionError，此時改用迭代版 BFS 或顯式 Stack DFS 更為安全。"
                ),
            ),
            InterviewFAQ(
                question="Q3：什麼是「拓樸排序（Topological Sort）」？它在軟體工程實務中有哪些核心應用？",
                answer=(
                    "拓樸排序是針對「有向無環圖（Directed Acyclic Graph, DAG）」的一種線性排序：如果圖中存在一條從 u 指向 v 的有向邊（代表 u 必須先於 v 完成），那麼在排序結果中 u 必定排在 v 前面。"
                    "實務上最常見的實作是 **Kahn 演算法（BFS + 入度表 In-degree）**：先將所有入度為 0（沒有任何前置依賴）的節點推入佇列，每次彈出節點時將其下游鄰居的入度減 1，一旦鄰居入度歸零就推入佇列。"
                    "這正是大學選課擋修檢查（LeetCode #207）、套件管理員（pip / cargo）安裝順序解析、CI/CD Pipeline 任務排程與試算表公式重算引擎的核心演算法。"
                ),
            ),
        ),
    ),
    # =========================================================================
    # Ch.06 動態規劃與記憶化搜尋
    # =========================================================================
    ChapterSpec(
        id="ch06",
        badge="Ch.06",
        title="動態規劃與記憶化搜尋（Dynamic Programming & Memoization）",
        complexity="爬樓梯 O(n) 時間 / O(1) 空間 ・ 0/1 背包 O(N×W) 時間 / O(W) 空間 ・ LIS O(n log n)",
        summary="破除動態規劃（DP）心魔：從暴力遞迴的重疊子問題出發，掌握狀態轉移方程式、空間壓縮技巧、0/1 背包問題與最長遞增子序列（LIS）。",
        concepts=(
            "動態規劃兩大核心要素 — 重疊子問題（Overlapping Subproblems）與最佳子結構（Optimal Substructure）：當大問題的最佳解可由子問題的最佳解組合而成，且遞迴過程中不斷重複計算相同子問題時，透過記憶化（Memoization）或自底向上填表（Tabulation）即可將指數級 O(2ⁿ) 時間暴降至多項式時間。",
            "0/1 背包問題（0/1 Knapsack）一維空間壓縮關鍵：將二維 dp[i][w] 壓縮為一維 dp[w] 時，內層容量迴圈必須「由後往前（capacity 遞減至 weight）」更新，確保每件物品在同一輪只被選取一次；若正序更新則會變成每件物品可無限次選取的「完全背包問題（Unbounded Knapsack）」。",
            "最長遞增子序列（LIS）從 O(n²) 到 O(n log n) 的維度躍遷：利用貪婪原則維護各長度遞增子序列的「最小結尾元素陣列 tails」，由於 tails 天然嚴格遞增，每次只需以 bisect_left 二分搜尋更新對應位置。",
        ),
        file="examples/ch06_dynamic_programming.py",
        lastmod="2026-11-17",
        keywords=(
            "Python 動態規劃",
            "Dynamic Programming",
            "記憶化搜尋 Memoization",
            "0/1 背包問題 Knapsack",
            "最長遞增子序列 LIS",
            "爬樓梯問題 Climbing Stairs",
            "狀態轉移方程式",
            "LeetCode 300",
        ),
        deep_intro=(
            "「動態規劃（Dynamic Programming, DP）」往往是轉職者與學生在準備大廠技術面試時最恐懼的大魔王。"
            "許多人看到解答直接寫出一行神祕的狀態轉移方程式 dp[i] = dp[i-1] + dp[i-2]，卻不知道這個式子是怎麼推導出來的。"
            "其實，動態規劃一點都不神祕——它的本質就是**「不重複算已經算過的事」**！"
            "以爬樓梯問題（每次走 1 或 2 階，問爬到第 n 階有幾種走法）為例：若直接寫暴力遞迴 f(n) = f(n-1) + f(n-2)，計算 f(40) 時 f(38)、f(37) 等相同子問題會被重複展開上億次，時間複雜度高達 O(2ⁿ)。"
            "只要我們遵循 DP 解題四部曲：(1) 定義狀態意義、(2) 寫出狀態轉移方程式、(3) 確立基底條件（Base Cases）、(4) 決定計算順序與空間壓縮，"
            "就能從自頂向下的記憶化搜尋（Top-Down Memoization，搭配 Python 3 標準庫 `@functools.cache`），平滑演進到自底向上的填表法（Bottom-Up Tabulation），甚至將空間複雜度壓縮至極致的 O(1)。"
            "本章一次帶你實作三大經典模型：線性 DP（爬樓梯 O(1) 空間）、區間容量型 DP（0/1 背包問題一維滾動陣列）與子序列型 DP（O(n log n) 最長遞增子序列 LIS）。"
        ),
        comparison_table=ComparisonTable(
            caption="表 6-1：暴力遞迴、Top-Down 記憶化搜尋、Bottom-Up 表格法與空間壓縮 DP 全方位對照表",
            headers=(
                "實作方法 / DP 演進階段",
                "時間複雜度（以爬樓梯/背包為例）",
                "空間複雜度",
                "呼叫堆疊風險（RecursionError）",
                "實戰選型建議與優缺點",
            ),
            rows=(
                (
                    "暴力遞迴（Brute-Force Recursion）",
                    "O(2ⁿ)（指數級爆炸）",
                    "O(n)（遞迴深度）",
                    "高（n > 1000 崩潰）",
                    "僅用於白板題初期推導遞迴關係，n >= 35 即嚴重超時。",
                ),
                (
                    "自頂向下記憶化（Top-Down + @cache）",
                    "O(n) 或 O(N × W)",
                    "O(n) 或 O(N × W)（快取表 + 堆疊）",
                    "中（受限於 sys.getrecursionlimit）",
                    "思考最直覺！直接照題意寫遞迴加上 @functools.cache，且只會計算真正用到的稀疏子狀態。",
                ),
                (
                    "自底向上填表法（Bottom-Up 2D/1D Array）",
                    "O(n) 或 O(N × W)",
                    "O(n) 或 O(N × W)",
                    "零（純迴圈迭代，絕不爆堆疊）",
                    "工業級與大測資標準寫法，無函式呼叫開銷且 CPU 快取極為友善。",
                ),
                (
                    "滾動陣列 / 變數狀態壓縮（Space-Optimized）",
                    "O(n) 或 O(N × W)",
                    "爬樓梯 O(1) ／ 0/1 背包 O(W)",
                    "零（純迴圈迭代）",
                    "面試加分殺手鐧！當第 i 輪狀態只依賴第 i-1 輪時，即可捨棄舊維度大幅節省記憶體。",
                ),
                (
                    "貪婪 + 二分搜尋最佳化 DP（如 LIS tails）",
                    "O(n log n)（傳統 DP 為 O(n²)）",
                    "O(n)",
                    "零（純迴圈 + bisect_left）",
                    "針對最長遞增子序列（LIS），維護單調 tails 陣列將內層 O(n) 狀態轉移壓縮為 O(log n)。",
                ),
            ),
        ),
        walkthrough_title="逐步拆解：0/1 背包一維逆序更新（weights=[10,20,30], values=[60,100,120], cap=50）與 LIS 追蹤",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1：0/1 背包初始化一維陣列 dp[0..50] 全為 0，處理物品 1（重 10, 價值 60）",
                state_snapshot="物品 1 (w=10, v=60) 逆序更新 cap=50..10 -> dp[10..50] 全部變為 60",
                explanation=(
                    "初始化 dp = [0] * 51，其中 dp[c] 代表「在背包容量上限為 c 時所能獲得的最大價值」。"
                    "放入第一件物品（w=10, v=60），curr_cap 從 50 逆序往下走到 10，由於 dp[curr_cap - 10] 原本皆為 0，更新後所有容量 >= 10 的格位 dp[10..50] 值皆為 60。"
                ),
            ),
            WalkthroughStep(
                step_label="Step 2：處理物品 2（重 20, 價值 100）— 為何必須「由後往前（50 -> 20）」更新？",
                state_snapshot="curr_cap=50..30: max(60, dp[cap-20]+100) = 160 | curr_cap=29..20: max(60, dp[0..9]+100) = 100",
                explanation=(
                    "當 curr_cap = 50 時，我們讀取的是「尚未放入物品 2 的上一輪狀態」dp[30]（值為 60），因此 dp[50] = max(60, 60 + 100) = 160（同時選物品 1 與物品 2）；"
                    "接著當 curr_cap 降到 20 時，讀取 dp[0] = 0，更新 dp[20] = 100。"
                    "關鍵洞察：若我們「由前往後（20 -> 50）」正序更新，會先把 dp[20] 改成 100，等算到 dp[40] 時就會讀到剛剛改過的 dp[20]=100 再加 100 變成 200（把同一件物品 2 重複放了兩次！）。"
                ),
            ),
            WalkthroughStep(
                step_label="Step 3：處理物品 3（重 30, 價值 120）決策出最終最大價值 220",
                state_snapshot="curr_cap=50: max(原 dp[50]=160, dp[50-30]+120 = dp[20]+120 = 100+120 = 220) -> dp[50] = 220",
                explanation=(
                    "進入物品 3（w=30, v=120）：當 curr_cap = 50 時，比較「不拿物品 3（維持原值 160）」與「拿物品 3（剩餘容量 50 - 30 = 20 的最佳解 dp[20]=100 加上 120 = 220）」，"
                    "選取較大者 220（即選取物品 2 + 物品 3，總重 20 + 30 = 50，總價值 100 + 120 = 220），最終回傳 dp[50] == 220。"
                ),
            ),
            WalkthroughStep(
                step_label="Step 4：LIS 最長遞增子序列 [10, 9, 2, 5, 3, 7, 101, 18] 的 tails 貪婪演進",
                state_snapshot="10->[10] | 9->[9] | 2->[2] | 5->[2,5] | 3->[2,3] | 7->[2,3,7] | 101->[2,3,7,101] | 18->[2,3,7,18] (長度 4)",
                explanation=(
                    "在 length_of_lis 中，tails[i] 紀錄「長度為 i+1 的遞增子序列中，最小的結尾數字」（結尾越小，後面越容易接上其他數字）。"
                    "當讀到 3 時，以 bisect_left 在 [2, 5] 中找到索引 1，將 5 替換為更小的結尾 3（變成 [2, 3]）；"
                    "後續 7 與 101 接在尾端使長度增至 4，最後 18 替換 101 成為 [2, 3, 7, 18]，最終回傳 len(tails) == 4。"
                ),
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="陷阱一：混淆「0/1 背包（逆序迴圈）」與「完全背包（正序迴圈）」的內層容量遍歷方向",
                symptom="在寫硬幣找零（Coin Change，每種硬幣可無限使用）或 0/1 背包（每件物品限用一次）時，憑感覺亂寫 range(w, capacity + 1) 或 range(capacity, w - 1, -1)。",
                root_cause_and_fix=(
                    "根因分析：一維滾動陣列 dp[c] 中，左邊的 dp[c - w] 若在同一輪已經被更新過，就代表「已經拿過當前物品一次了」。"
                    "正確口訣：**「0/1 背包每物限拿一次，容量由大到小逆序跑（避免覆蓋上一輪舊狀態）；完全背包每物可無限拿，容量由小到大正序跑（刻意累加本輪已拿狀態）」**。"
                ),
            ),
            PitfallItem(
                title="陷阱二：誤以為 LIS 演算法最後的 tails 陣列內容就是「原始的最長遞增子序列本身」",
                symptom="面試官追問：「請印出最長遞增子序列的實際元素」，候選人直接 return tails，結果當輸入為 [2, 5, 3, 4] 時應是 [2, 3, 4]，但若有個極小值在最後如 [2, 5, 6, 1] 時，tails 會變成 [1, 5, 6]（1 在原陣列明明在 5 和 6 後面！）。",
                root_cause_and_fix=(
                    "根因分析：tails[i] 的定義是「長度為 i+1 的遞增子序列之最小結尾值」，用後面的小數字覆寫 tails[0] 只是為了看未來能不能接出更長的序列，並不會改變 tails 的總長度 len(tails)，但 tails 本身並非合法的單一子序列。"
                    "正確對策：len(tails) 保證 100% 等於 LIS 的正確長度；若題目要求還原實際序列，需額外維護一個 parent_idx 陣列記錄每個元素接在哪個前驅索引後面。"
                ),
            ),
            PitfallItem(
                title="陷阱三：使用 Python 二維陣列初始化時寫出 dp = [[0] * cols] * rows 導致整排連動修改 Bug",
                symptom="建立二維 DP 表格後執行 dp[0][1] = 99，卻驚見 dp[1][1]、dp[2][1] 每一列的第 1 欄全部同時變成 99！",
                root_cause_and_fix=(
                    "根因分析：外層的 * rows 只是將同一個內層 list 物件的參照（Reference）複製了 rows 份，所有列其實指向記憶體中的同一個 list！"
                    "正確對策：初始化二維 DP 表時，永遠使用串列生成式（List Comprehension）：dp = [[0] * cols for _ in range(rows)]，確保每一列都是獨立配置的 list 物件。"
                ),
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(
                number=70,
                title="Climbing Stairs（爬樓梯）",
                difficulty="Easy",
                pattern="線性動態規劃與滾動變數空間壓縮 ・ 時間 O(n) / 空間 O(1)",
            ),
            LeetCodeProblem(
                number=322,
                title="Coin Change（零錢兌換）",
                difficulty="Medium",
                pattern="完全背包型一維動態規劃（正序更新最小硬幣數） ・ 時間 O(S × n) / 空間 O(S)",
            ),
            LeetCodeProblem(
                number=300,
                title="Longest Increasing Subsequence（最長遞增子序列 LIS）",
                difficulty="Medium",
                pattern="貪婪單調 tails 陣列 + bisect_left 二分搜尋 ・ 時間 O(n log n) / 空間 O(n)",
            ),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="Q1：面試時要怎麼快速分辨一道求極值（最大／最小）的題目，應該用「貪婪演算法（Greedy）」還是「動態規劃（Dynamic Programming）」？",
                answer=(
                    "關鍵在於檢查「局部最佳選擇（Locally Optimal Choice）是否保證導向全局最佳解」。"
                    "可以嘗試舉一個簡單的 3～4 元素反例：以硬幣找零為例，若硬幣面額為 [1, 3, 4] 要湊出 6 元，貪婪法每次優先拿最大面額會選出 4 + 1 + 1（共 3 枚），"
                    "但真正的全局最佳解是 3 + 3（只需 2 枚）！這證明眼前的最大面額會卡死後續組合（不具備貪婪選擇性質），此時就必須使用動態規劃窮舉各子狀態的最佳轉移。"
                ),
            ),
            InterviewFAQ(
                question="Q2：在 Python 3.9+ 中，使用 @functools.cache（或 @lru_cache(None)）寫 Top-Down 記憶化搜尋有什麼需要注意的記憶體陷阱？",
                answer=(
                    "@functools.cache 會將函式所有呼叫過的參數組合 tuple 作為 dict 的 key 永久快取在記憶體中。"
                    "(1) 所有傳入遞迴函式的參數都必須是可雜湊的（Hashable，不能傳 list，需轉成索引或 tuple）；"
                    "(2) 若在 LeetCode 的 Solution 類別方法外層或長駐伺服器中使用 @cache，快取不會跨測資自動清空，可能導致記憶體洩漏（Memory Leak）。"
                    "建議將 @cache 標註在解題方法內部定義的巢狀輔助函式 def dfs(i, rem): 上，讓快取隨單次方法結束自動釋放，或改寫為可做空間壓縮的 Bottom-Up 迭代法。"
                ),
            ),
            InterviewFAQ(
                question="Q3：0/1 背包問題的時間複雜度 O(N × W) 看起來是兩個數字相乘，為什麼在計算複雜度理論中它卻被稱為「偽多項式時間（Pseudo-Polynomial Time）」？",
                answer=(
                    "在嚴格的計算理論中，時間複雜度是衡量「運算步數相對於『輸入資料編碼位元長度（Input Bit Length）』的成長率」。"
                    "物品數量 N 確實代表輸入陣列有 N 個元素，但背包容量 W 是一個「數值（Magnitude）」，在電腦二進位中表示整數 W 只需要 B = log₂(W) 個位元。"
                    "因此，O(N × W) 若換算成輸入位元長度 B，其實是 O(N × 2ᴮ)（相對於容量位元數呈指數成長！）。所以當題目給定 capacity 高達 10⁹ 時，一維 DP 陣列 O(W) 會直接爆記憶體，此時必須改用折半枚舉（Meet in the Middle）或改以價值總和作為 DP 狀態。"
                ),
            ),
        ),
    ),
    # =========================================================================
    # Ch.07 堆積、優先佇列與 Top-K 演算法
    # =========================================================================
    ChapterSpec(
        id="ch07",
        badge="Ch.07",
        title="堆積、優先佇列與 Top-K 演算法（Heap, Priority Queue & Top-K Elements）",
        complexity="Insert / Pop O(log n) ・ Peek O(1) ・ Top-K 篩選 O(n log k) ・ K 路合併 O(N log K)",
        summary="深入理解完全二元樹陣列映射與上浮／下沉（Sift-Up / Sift-Down）機制，親手實作泛型 MinHeap 並掌握大數據 Top-K 與多路歸併技巧。",
        concepts=(
            "完全二元樹的陣列零指標映射：二元堆積（Binary Heap）雖然邏輯上是一棵完全二元樹（Complete Binary Tree），但底層不需配置任何 left/right 指標節點，直接存放在一般陣列（Python list）中！對任意 0-based 索引 i，其父節點必為 (i - 1) // 2，左子節點必為 2*i + 1，右子節點必為 2*i + 2。",
            "海量資料 Top-K 問題的黃金法則：要在 n 筆資料中找出前 k 大元素，切勿直接對全體資料執行 sorted(nums)[:k]（耗時 O(n log n)、空間 O(n)）；應維護一個容量固定為 k 的「最小堆積（Min-Heap）」，堆頂即為目前前 k 大俱樂部的最低門檻，時間複雜度降至 O(n log k)、空間僅需 O(k)。",
            "多路歸併（Merge K Sorted Lists / Streams）：利用優先佇列同時追蹤 K 個已排序資料流的當前最小元素，每次在 O(log K) 時間內彈出全局最小值並推入該串列的下一個元素，是分散式資料庫外部排序與日誌時間軸合併的核心演算法。",
        ),
        file="examples/ch07_heap_priority_queue.py",
        lastmod="2026-11-17",
        keywords=(
            "Python 堆積 Heap",
            "優先佇列 Priority Queue",
            "heapq 教學",
            "Top-K 問題",
            "MinHeap 實作",
            "Merge K Sorted Lists",
            "完全二元樹",
            "LeetCode 347",
        ),
        deep_intro=(
            "在真實世界的後端系統與演算法面試中，我們經常面臨這類動態極值問題：「即時統計全站搜尋量最高的前 10 大熱門關鍵字（Top-K）」、「在急診室或作業系統排程中永遠優先處理權重最高的任務（Priority Queue）」、"
            "或是「將 50 台伺服器各自按時間排序好的日誌檔合併成單一全局時間軸（Merge K Sorted Streams）」。"
            "如果使用未排序陣列，每次插入雖只要 O(1)，但要找出最小值卻得掃描全表 O(n)；如果每次插入都重新排序整個陣列，單次更新成本又高達 O(n log n)。"
            "「二元堆積（Binary Heap）」正是為了打破這個兩難而生的精妙結構：它不要求整棵樹像 BST 那樣完全區分左右大小，只要求滿足一個極簡的**堆積序性質（Heap Property）**——"
            "在最小堆積（Min-Heap）中，**任何父節點的值永遠小於或等於其左右子節點的值**。"
            "這保證了全局最小元素永遠穩坐陣列索引 0 的堆頂（O(1) 讀取），且因為完全二元樹的高度嚴格限制為 ⌊log₂ n⌋，無論是插入新元素向上調整（Sift-Up）還是彈出堆頂後向下調整（Sift-Down），最多只需交換 O(log n) 次！"
        ),
        comparison_table=ComparisonTable(
            caption="表 7-1：二元堆積（Binary Heap）與其他容器在優先佇列及 Top-K 場景下之複雜度對照表",
            headers=(
                "操作項目 / 應用場景",
                "二元最小堆積（MinHeap / heapq）",
                "未排序陣列（Unsorted list）",
                "維持全排序陣列（Sorted list）",
                "複雜度成因與工程決策",
            ),
            rows=(
                (
                    "查看最小值（peek min）",
                    "O(1)（直接讀取 heap[0]）",
                    "O(n)（需全表掃描 min()）",
                    "O(1)（讀取首尾端）",
                    "Min-Heap 保證堆頂索引 0 必為全局最小元素。",
                ),
                (
                    "插入新元素（push / insert）",
                    "O(log n)（尾端附加 + _sift_up）",
                    "攤銷 O(1)",
                    "O(n)（bisect 定位 O(log n) + 搬移 O(n)）",
                    "堆積只需沿父節點路徑向上交換，路徑長度不超過樹高 log₂ n。",
                ),
                (
                    "彈出最小值（pop min）",
                    "O(log n)（末尾補頂 + _sift_down）",
                    "O(n)（尋找並搬移）",
                    "pop(0) 為 O(n) / 逆序 pop() 為 O(1)",
                    "把最後一個元素移到根節點再向下與較小子節點交換，避免 O(n) 陣列搬移。",
                ),
                (
                    "將現有 n 個元素原地建堆（heapify）",
                    "O(n)（自底向上 Sift-Down）",
                    "O(1)（無須處理）",
                    "O(n log n)（完整排序）",
                    "heapq.heapify(lst) 級數收斂證明其時間複雜度為線性 O(n)，非 O(n log n)！",
                ),
                (
                    "從 n 筆串流資料求前 k 大（Top-K）",
                    "時間 O(n log k) ／ 空間 O(k)",
                    "不適用",
                    "時間 O(n log n) ／ 空間 O(n)",
                    "當 n = 10⁸、k = 10 時，大小為 10 的 Min-Heap 僅需極小記憶體即可即時篩選。",
                ),
            ),
        ),
        walkthrough_title="逐步拆解：MinHeap 上浮／下沉操作與 Top-K 最大元素篩選四步驟狀態追蹤",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1：MinHeap 陣列索引映射與插入上浮（_sift_up）",
                state_snapshot="依序 push 5, 1, 8, 3 -> 插入 1 時與父節點 5 交換：[1, 5] -> 插入 8：[1, 5, 8] -> 插入 3 與父 5 交換：[1, 3, 8, 5]",
                explanation=(
                    "當我們對 [1, 5, 8] 執行 push(3) 時，3 先被放到陣列末尾索引 idx = 3。"
                    "計算其父節點索引 parent = (3 - 1) // 2 = 1（對應值為 5）。因為 3 < 5 違反最小堆積性質，將兩者交換，陣列變為 [1, 3, 8, 5]；"
                    "繼續向上比較索引 1 的父節點 (1 - 1) // 2 = 0（值為 1），因為 3 >= 1 滿足性質，立即結束上浮。"
                ),
            ),
            WalkthroughStep(
                step_label="Step 2：MinHeap 彈出堆頂與末尾補頂下沉（_sift_down）",
                state_snapshot="對 [1, 3, 8, 5] 執行 pop() -> 取出堆頂 1，將末尾 5 移至索引 0：[5, 3, 8] -> 與較小子節點 3 交換 -> [3, 5, 8]",
                explanation=(
                    "若直接刪除 _data[0] 會造成 O(n) 搬移，因此 pop() 的絕招是：先記下堆頂 top = 1，再用 _data.pop() O(1) 取出最後一個元素 5 覆寫到 _data[0]，變成 [5, 3, 8]。"
                    "接著從 idx = 0 執行 _sift_down：比較左子節點 (索引 1, 值 3) 與右子節點 (索引 2, 值 8)，挑出較小的子節點 3 與 5 交換，變成 [3, 5, 8]，瞬間恢復合法堆積！"
                ),
            ),
            WalkthroughStep(
                step_label="Step 3：Top-K 最大元素 — 為什麼找「前 k 大」卻要用「最小堆積（Min-Heap）」？",
                state_snapshot="nums = [64, 34, 25, 12, 22, 11, 90, -5], k = 3 | 前 3 個入堆後 min_heap = [25, 64, 34]（堆頂守門員 = 25）",
                explanation=(
                    "想像我們要選拔全校分數最高的 3 名學生進資優班（容量 k = 3）。我們只需要知道目前班上「第 3 名（最低分守門員）」是幾分即可！"
                    "用 Min-Heap 存這 3 個人時，堆頂 min_heap[0] 剛好就是目前前 3 大裡面的最小值（25）。"
                    "接下來讀到 12、22、11 時，因為都沒超過守門員 25，連進堆的資格都沒有，在 O(1) 時間內直接淘汰！"
                ),
            ),
            WalkthroughStep(
                step_label="Step 4：強者挑戰成功（heapreplace）與 K 路歸併（merge_k_sorted_lists）",
                state_snapshot="讀到 90 > 堆頂 25 -> heapreplace 踢掉 25 換入 90 -> min_heap 內為 {34, 64, 90}（堆頂新守門員 = 34）",
                explanation=(
                    "當讀到 90 時，90 > min_heap[0] (25)，呼叫 heapq.heapreplace(min_heap, 90) 在單次 O(log k) 下沉操作中踢掉 25 並換入 90，新守門員升為 34。"
                    "最後將這 k 個元素排好即得 [90, 64, 34]。同理，在 merge_k_sorted_lists 中，堆積內永遠只放 K 個串列各自當前的頭元素 (val, list_idx, elem_idx)，"
                    "每次彈出最小者後，立刻把該串列的下一個元素補進堆積，僅需 O(N log K) 時間即可完成合併。"
                ),
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="陷阱一：Python 標準庫 heapq 只有「最小堆積」，誤以為可以直接傳 reverse=True 變成最大堆積",
                symptom="想在 Python 使用最大堆積（Max-Heap，每次彈出最大值），卻發現 heapq.heappush 根本不接受 key 或 reverse 參數。",
                root_cause_and_fix=(
                    "根因分析：為了極致效能，Python 標準庫 heapq 僅實作了最小堆積（Min-Heap）。"
                    "正確對策：若元素為數值（int / float），在 push 入堆時將數值**取負號（heapq.heappush(max_heap, -val)）**，彈出時再取負號還原（-heapq.heappop(max_heap)），"
                    "原本最大的正數（如 100）取負號後變成最小的負數（-100），就會自動浮上 Min-Heap 的堆頂！"
                ),
            ),
            PitfallItem(
                title="陷阱二：在 heapq 中推入 (priority, task_object) Tuple 時，因 priority 平手而觸發 TypeError",
                symptom="在實作合併 K 個鏈結串列或 Dijkstra 時，推入 (node.val, node)，一旦遇到兩個節點 val 相等，立即拋出 TypeError: '<' not supported between instances of 'ListNode' and 'ListNode'。",
                root_cause_and_fix=(
                    "根因分析：Python 的 Tuple 比較是按字典序逐欄比對的：當第 0 欄 val 相等時，會自動比較第 1 欄；若第 1 欄是未定義 __lt__ 的自訂物件或 dict，就會直接報錯。"
                    "正確對策：像本章範例第 102 行那樣，在 Tuple 中間加入一個保證唯一且可比較的整數（如串列索引 list_idx 或遞增序號 tie_breaker）：(val, list_idx, node)，徹底阻斷比較落入自訂物件。"
                ),
            ),
            PitfallItem(
                title="陷阱三：把 heap 當作已排序陣列直接切片或索引（以為 heap[1] 就是第二小元素）",
                symptom="對一個已經 heapify 的陣列執行 heap[0], heap[1], heap[2]，以為這樣就能依序拿到第 1 小、第 2 小、第 3 小的元素。",
                root_cause_and_fix=(
                    "根因分析：最小堆積只保證「父節點 <= 子節點（所以 heap[0] 必為第 1 小）」，但完全不保證左子節點 heap[1] 與右子節點 heap[2] 誰大誰小，更不保證同層節點的順序！"
                    "正確對策：若要依序取出最小元素，必須透過迴圈不斷呼叫 heapq.heappop(heap)（每次耗時 O(log n)），才能觸發 _sift_down 將真正的次小元素推舉至堆頂。"
                ),
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(
                number=215,
                title="Kth Largest Element in an Array（陣列中的第 K 個最大元素）",
                difficulty="Medium",
                pattern="大小固定為 K 之最小堆積（Min-Heap）或 Quickselect ・ 時間 O(n log k) / 空間 O(k)",
            ),
            LeetCodeProblem(
                number=347,
                title="Top K Frequent Elements（前 K 個高頻元素）",
                difficulty="Medium",
                pattern="Counter 雜湊計數 + 大小為 K 之最小堆積篩選 (freq, num) ・ 時間 O(n log k) / 空間 O(n)",
            ),
            LeetCodeProblem(
                number=23,
                title="Merge k Sorted Lists（合併 K 個升序鏈結串列）",
                difficulty="Hard",
                pattern="優先佇列（Min-Heap）維護 K 個串列頭指標 ・ 時間 O(N log K) / 空間 O(K)",
            ),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="Q1：為什麼將現有長度為 n 的無序陣列原地轉為堆積（heapq.heapify），時間複雜度是線性的 O(n)，而不是 n 次插入的 O(n log n)？",
                answer=(
                    "如果從空堆積開始逐一呼叫 n 次 push（由下而上 Sift-Up），因為佔總數一半的底層葉節點都需要往上交換 log₂ n 層，總時間確實是 O(n log n)。"
                    "但 heapq.heapify(arr) 採用的是「Floyd 自底向上下沉法（Bottom-Up Sift-Down）」：從最後一個非葉節點（索引 n // 2 - 1）開始往索引 0 逆序執行 _sift_down。"
                    "關鍵在於：佔節點總數 50% 的最底層葉節點根本不需要下沉（0 步），佔 25% 的倒數第二層最多只下沉 1 步，佔 12.5% 的倒數第三層最多下沉 2 步……"
                    "根據錯位相減級數求和 Σ (n / 2^(h+1)) * h ≤ n * Σ (h / 2^h) = 2n，總交換次數上限嚴格不超過 2n，因此時間複雜度是極速的線性 O(n)！"
                ),
            ),
            InterviewFAQ(
                question="Q2：在面試被問到「從 1 億筆資料中找出前 10 大（Top-10）」時，為什麼用大小為 k 的最小堆積 O(n log k) 比先 heapify 全體再 pop k 次 O(n + k log n) 更受青睞？",
                answer=(
                    "關鍵在於**「記憶體限制（Space Complexity）與串流處理能力（Streaming）」**！"
                    "若採用 heapify 全體資料，你必須先把 1 億筆資料全部載入記憶體（耗費數 GB 空間），且無法處理源源不絕的即時資料流；"
                    "反之，維護一個大小固定為 k = 10 的最小堆積，記憶體中永遠只需要存放 10 個元素（空間複雜度 O(k)），每讀進一筆新資料只需與堆頂比較（99.99% 的資料甚至連堆都進不去就在 O(1) 被過濾掉），完美契合大數據與分散式系統的工程需求。"
                ),
            ),
            InterviewFAQ(
                question="Q3：Python 標準庫裡同時有 heapq 跟 queue.PriorityQueue，在寫演算法與後端開發時該如何選擇？",
                answer=(
                    "queue.PriorityQueue 其實只是在 heapq 外層包了一層 threading.Lock 互斥鎖，以提供多執行緒安全（Thread-Safety）。"
                    "在單執行緒的演算法面試（LeetCode）、資料分析或 asyncio 協程中，每次呼叫 PriorityQueue.put() / get() 都會平白付出鎖競爭與函式封裝的沉重開銷，速度比直接使用 heapq 慢上數倍。"
                    "因此：除非你正在撰寫多執行緒（threading）共享佇列，否則一律直接使用輕量高效的 heapq 模組。"
                ),
            ),
        ),
    ),
)
