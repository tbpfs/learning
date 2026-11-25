#!/usr/bin/env python3
"""International English (en) content pack for learn.ai-purplemaple.com."""

from __future__ import annotations

from typing import Any

from affiliate_config import AffiliateResource
from chapter_content import (
    ChapterSpec,
    ComparisonTable,
    InterviewFAQ,
    LeetCodeProblem,
    PitfallItem,
    WalkthroughStep,
)

UI_EN: dict[str, Any] = {
    "site_name": "Purple Maple Python DSA Interactive Guide",
    "brand_creator_name": "Purple Maple (Wang Tzu-Feng / @tbpfs1)",
    "brand_website_name": "Purple Maple Official Portfolio (Wang Tzu-Feng)",
    "brand_anchor_portfolio": "Purple Maple (Wang Tzu-Feng) Official Portfolio (AI Music & Shirase Airi)",
    "brand_anchor_portfolio_short": "Purple Maple Official Portfolio",
    "brand_anchor_footer": "Purple Maple (Wang Tzu-Feng)",
    "page_title": "Python 3.12 Data Structures & Algorithms From Scratch | Purple Maple",
    "hero_eyebrow": "CS FUNDAMENTALS SERIES · DATA STRUCTURES · ALGORITHMS · OOP",
    "hero_h1": "Python 3.12 Data Structures & Algorithms From Scratch",
    "hero_intro_html": (
        "Hi, I am <strong>Purple Maple</strong>! Whether you are a CS student, switching careers into "
        "software engineering, or preparing for technical interviews, mastering data structures, algorithms, "
        "and clean object-oriented design in Python 3.12 is the highest-leverage foundation you can build."
    ),
    "cta_youtube": "▶ Watch Full YouTube Lecture Playlist (Mandarin)",
    "cta_github": "GitHub Source Repository",
    "cta_chapter_github": "View Chapter Source on GitHub",
    "og_image_alt": "Purple Maple (@tbpfs1) Python 3.12 Data Structures and Algorithms Interactive Tutorial featuring mascot Shirase Airi (Aily, crimson #fb7185 left eye and azure #38bdf8 right eye)",
    "index_keywords": (
        "Purple Maple, tbpfs, Python 3.12 tutorial, data structures and algorithms Python, "
        "singly linked list Python, stack and queue deque, binary search Python, merge sort Python, "
        "hash table separate chaining, two sum Python, binary search tree BST, graph BFS DFS OOP, "
        "dynamic programming 0/1 knapsack Python, longest increasing subsequence LIS, binary heap heapq Top-K"
    ),
    "index_desc_tpl": (
        "Free open-source Python 3.12 Data Structures, Algorithms, and OOP interactive handbook by Purple Maple (@tbpfs1), "
        "covering {chapter_titles_short} with verified live output, Big-O tables, and LeetCode interview guides."
    ),
    "index_og_desc_tpl": "Free Python 3.12 Data Structures & Algorithms Handbook by Purple Maple ({chapter_titles_short}).",
    "course_name": "Python 3.12 Data Structures & Algorithms From Scratch",
    "course_desc_tpl": (
        "Hands-on Python 3.12 data structures, algorithms, and object-oriented programming course by Purple Maple, "
        "covering {chapter_titles_short}."
    ),
    "index_aeo_capsule": (
        "Purple Maple's free open-source Python 3.12 DSA tutorial portal (<code>learn.ai-purplemaple.com/en/</code>) "
        "covers 7 core engineering chapters (Arrays & Linked Lists, Stacks & Queues, Binary Search & Merge Sort, "
        "Hash Tables & BST, Graph BFS/DFS & OOP, Dynamic Programming, and Binary Heaps & Top-K) with verified runtime "
        "outputs, Big-O comparison tables, CPython 3.12 internals, and LeetCode interview walkthroughs."
    ),
    "toc_aria": "Chapter Quick Navigation",
    "chapter_switcher_aria": "Course Chapter Switcher",
    "section_subnav_aria": "Chapter Section Navigation",
    "section_subnav_label": "Jump to section:",
    "nav_intro": "Overview & Core Concepts",
    "nav_video": "Video Lecture",
    "nav_comparison": "Big-O Comparison Table",
    "nav_walkthrough": "Step-by-Step Walkthrough",
    "nav_code": "Python 3.12 Implementation",
    "nav_pitfalls": "CPython 3.12 Pitfalls",
    "nav_interview": "LeetCode & Interview FAQ",
    "chapter_link_cta": "Read Deep-Dive Chapter ↗",
    "concepts_heading": "Core Concepts & Interview Highlights",
    "label_complexity": "Time / Space Complexity:",
    "label_source_path": "Source Path:",
    "code_accordion_summary_tpl": "Expand / Collapse {badge} Python 3.12 Full Implementation & Live Output (<code>{file}</code>)",
    "code_toolbar_tpl": "Python 3.12 Reference Implementation ({file})",
    "copy_btn": "Copy Code",
    "output_label_index": "▶ Verified Live Runtime Output",
    "output_label_chapter": "▶ Verified Live Runtime Output (Python 3.12 CI Execution)",
    "deep_dive_summary_tpl": "{badge} Exclusive Deep-Dive Guide Preview (Click to Expand / Collapse)",
    "deep_dive_table_label": "Full Big-O Comparison Table:",
    "deep_dive_faq_label": "Featured Technical Interview FAQs in This Chapter:",
    "deep_dive_cta_tpl": "Read {badge} Full Deep-Dive Chapter (Big-O Table + Walkthrough + Interview Guide) ->",
    "chapter_title_tpl": "{badge} {title} | Purple Maple Python 3.12 Guide",
    "chapter_desc_tpl": "Python 3.12 deep-dive tutorial by Purple Maple: {badge} {title}. {summary}",
    "chapter_keywords_prefix": "Purple Maple, Python 3.12 DSA, ",
    "chapter_eyebrow_tpl": "{badge} DEEP-DIVE CHAPTER · PYTHON 3.12 DATA STRUCTURES & ALGORITHMS",
    "back_to_index_label": "<- Back to Python 3.12 Data Structures & Algorithms Course Index",
    "chapter_intro_heading": "Engineering Context & Mental Model",
    "chapter_aeo_tpl": (
        "{badge} ({title}) teaches you to master {summary} Reference time and space complexity is "
        "<code>{complexity}</code>, backed by a zero-dependency Python 3.12 standard library implementation "
        "(<code>{file}</code>) with live CI-verified output."
    ),
    "comparison_heading": "Time & Space Complexity and Internal Architecture Comparison",
    "code_section_heading": "Zero-Dependency Python 3.12 Implementation & Verified Output",
    "pitfalls_heading": "CPython 3.12 Runtime Internals & Common Production Pitfalls",
    "pitfall_symptom_label": "Common Failure Symptom:",
    "pitfall_fix_label": "CPython Root Cause & Correct Pattern:",
    "interview_heading": "Essential LeetCode Problems & Software Engineering Interview FAQ",
    "interview_table_caption_tpl": "{badge} Must-Know LeetCode Whiteboard Problems & Reusable Patterns",
    "interview_th_num": "Problem",
    "interview_th_title": "Title",
    "interview_th_diff": "Difficulty",
    "interview_th_pattern": "Core Pattern & Complexity",
    "video_heading_tpl": "Companion Video Lecture ({views_label})",
    "video_intro": "Watch the visual walkthrough lecture (Mandarin Chinese audio with step-by-step code and diagram overlays) to build intuition, then verify every step against the Big-O tables and Python 3.12 code below:",
    "video_main_label": "Primary Lecture:",
    "video_playlist_cta": "Full 31-Video Playlist on YouTube ↗",
    "video_related_heading": "Related Topic Deep-Dive Videos (Mandarin Audio)",
    "video_desc_tpl": "Python 3.12 visual walkthrough lecture by Purple Maple (Mandarin Chinese audio with visual step-by-step diagrams): {badge} {title}. {summary}",
    "tech_article_headline_tpl": "{badge} {title} - Python 3.12 Data Structures & Algorithms Deep Dive",
    "breadcrumb_home_name": "Python 3.12 DSA Course Index",
    "resources_heading": "Curated References: Official Python 3.12 Docs & Classic CS Textbooks",
    "resources_note": "Note: All links below are non-sponsored official documentation and classic computer science textbook references that pair cleanly with the 7 hands-on Python 3.12 chapters on this site.",
    "resources_th_title": "Book / Documentation",
    "resources_th_platform": "Source",
    "resources_th_audience": "Best For",
    "resources_th_highlight": "How It Maps to This Course",
    "resources_th_action": "Explore",
    "chapter_resource_aria": "Official Python Documentation & Further Reading",
    "chapter_resource_note": "Further reading: Cross-check this chapter's data structures and CPython performance guarantees against the official Python 3.12 documentation.",
    "chapter_resource_cta": "Read Official Docs ↗",
    "fb_question": "Was this chapter helpful?",
    "fb_yes": "✓ Helpful",
    "fb_no": "Needs Work",
    "fb_note_placeholder": "Optional: Which section helped or felt unclear? (Max 200 chars, private)",
    "fb_note_aria": "Optional private feedback note",
    "fb_note_submit": "Send Feedback",
    "fb_ask_summary": "Still stuck on a concept? Ask Purple Maple privately (curated into chapter FAQs)",
    "fb_ask_sub": "To keep these tutorials spam-free and distraction-free, questions are reviewed privately and recurring topics are folded directly into the chapter FAQ.",
    "fb_ask_placeholder": "Type your question, e.g., why is this operation O(log n) instead of O(n)...",
    "fb_ask_aria": "Private question text",
    "fb_ask_submit": "Submit Question",
    "pager_aria": "Previous and Next Chapter Navigation",
    "pager_prev_tpl": "<- Previous: {badge} {short}",
    "pager_first": "<- First Chapter",
    "pager_home": "Back to Course Index",
    "pager_next_tpl": "Next: {badge} {short} ->",
    "pager_last": "Last Chapter ->",
    "study_guide_heading": "3-Stage Software Engineering DSA Study Roadmap",
    "study_guide_intro": "Many learners and career-switchers memorize LeetCode answers without internalizing why a data structure works in memory. Expand the 3-stage roadmap below for a structured study order:",
    "study_guide_summary": "Expand / Collapse: 3-Stage Interview Preparation Roadmap",
    "study_guide_items": (
        (
            "Stage 1 (Memory Models & Linear Structures):",
            'Implement <a href="ch01.html">Ch.01 Singly Linked Lists</a> and <a href="ch02.html">Ch.02 Stacks &amp; Queues</a> from scratch so pointer manipulation and the difference between <code>O(1)</code> and <code>O(n)</code> become second nature.',
        ),
        (
            "Stage 2 (Divide & Conquer, Hashing, Trees & Graphs):",
            'Master <a href="ch03.html">Ch.03 Binary Search &amp; Merge Sort</a>, <a href="ch04.html">Ch.04 Hash Tables (Two Sum) &amp; Binary Search Trees</a>, and <a href="ch05.html">Ch.05 Graph BFS / DFS Shortest Paths &amp; OOP</a> to internalize space-time trade-offs and clean encapsulation.',
        ),
        (
            "Stage 3 (Dynamic Programming, Heaps & Whiteboard Mastery):",
            'Tackle <a href="ch06.html">Ch.06 Dynamic Programming &amp; Memoization (0/1 Knapsack &amp; LIS)</a> and <a href="ch07.html">Ch.07 Binary Heaps &amp; Top-K Multi-Way Merge</a>, combining each chapter\'s Big-O table, CPython pitfall checklist, and LeetCode templates.',
        ),
    ),
    "privacy_heading": "Privacy Policy & Cookie Disclosure",
    "privacy_body_html": (
        'This website (learn.ai-purplemaple.com) uses Google AdSense advertising services and Google Analytics (GA4) / Google Tag Manager '
        'for anonymous traffic analytics. Google and its partners may use cookies (including the DART cookie) to serve personalized ads '
        'and measure aggregate readership. You may opt out of personalized advertising at any time via '
        '<a href="https://adssettings.google.com/" target="_blank" rel="noopener noreferrer">Google Ads Settings</a> or review the '
        '<a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener noreferrer">Google Advertising &amp; Privacy Policy</a>. '
        'Code copy buttons, question template copy buttons, and interactive quizzes run strictly in your local browser; helpfulness votes '
        'transmit only an anonymous satisfaction score and an HMAC rate-limit hash over HTTPS without storing raw IP addresses.'
    ),
    "footer_blog_label": "Purple Maple Tech & Creator Blog",
    "footer_github_label": "GitHub Source",
    "js_copied": "Copied ✓",
    "js_err_rate": "Daily limit reached. Please try again tomorrow.",
    "js_err_short": "Please enter at least 5 characters to describe your question.",
    "js_err_long": "Please keep your message within 400 characters.",
    "js_err_generic": "Submission failed. Please try again shortly.",
    "js_fb_thanks": "Thanks for your vote! Feel free to add an optional short note.",
    "js_fb_local_thanks": "Thanks for your vote! Saved locally in your browser.",
    "js_fb_note_ok": "✓ Feedback received. Thank you!",
    "qa_heading": "Questions or Stuck on This Chapter? Open a GitHub Issue",
    "qa_body": "To keep these chapters clean and spam-free, all technical questions, debugging help, and errata reports are hosted on GitHub Issues. Copy the structured question template below and open an issue so we can reproduce your environment quickly.",
    "qa_copy_btn": "Copy Question Template",
    "qa_copy_done": "Template Copied ✓",
    "qa_primary_cta": "Ask on GitHub Issues ↗",
    "qa_template_tpl": "[Purple Maple Press Question] {chapter_label}\n- Page URL: {page_url}\n- Observed behavior / error:\n- What I already tried:",
    "press_section_heading": "Purple Maple Press Technical Bookshelf",
    "press_section_intro": "Free open-source engineering monographs modeled on O'Reilly and MIT Press textbooks—each chapter pairs CI-verified zero-dependency Python 3.12 code with native architecture diagrams, production pitfalls, and self-check quizzes.",
    "book_status_serializing": "Serializing ({pub}/{total} Chapters Live)",
    "book_status_complete": "Complete Edition (7 Chapters)",
    "book_cta_open": "Open Book TOC ->",
    "book_cta_start_ch01": "Start Reading Ch.01",
    "book_cta_read_dsa": "Jump to All 7 Chapters ↓",
    "dsa_book_title": "Python 3.12 Data Structures & Algorithms Handbook",
    "dsa_book_desc": "Master Arrays & Linked Lists, Stacks & Queues, Binary Search & Merge Sort, Hash Tables & BSTs, Graphs & OOP, Dynamic Programming, and Binary Heaps with CI-verified code and LeetCode interview guides.",
    "dsa_cover_alt": "Purple Maple Press book cover illustration for Python 3.12 Data Structures & Algorithms Handbook featuring scholar-engineer Shirase Airi (Aily) studying binary trees and graphs (crimson #fb7185 left eye, azure #38bdf8 right eye)",
    "book_back_to_shelf": "<- Back to Purple Maple Press Bookshelf",
    "book_back_to_toc": "<- Back to {book_title} Table of Contents",
    "book_toc_heading": "Table of Contents (4 Parts × 10 Chapters)",
    "book_sidebar_summary": "Book Table of Contents (Expand / Collapse)",
    "book_coming_soon": "Coming Soon",
    "book_published_badge": "Live",
    "book_reading_time_tpl": "Estimated Reading Time: ~{mins} min",
    "book_audience_label": "Target Audience:",
    "book_objectives_heading": "What You Will Master in This Chapter",
    "book_diagram_heading": "Core Architecture & Data Flow Diagram",
    "book_walkthrough_heading": "Key Implementation Design Notes",
    "book_pitfalls_heading": "Production Pitfalls & Engineering Defenses",
    "book_pitfall_symptom_label": "Production Symptom:",
    "book_pitfall_fix_label": "Root Cause & Engineering Fix:",
    "book_quiz_heading": "Interactive Self-Check Quiz",
    "book_quiz_intro": "Select an option to check your answer and read the explanation instantly in your local browser. No personal data is sent.",
    "book_quiz_correct": "✓ Correct!",
    "book_quiz_wrong": "✗ Not quite — ",
    "book_faq_heading": "AI Engineering Technical Interview FAQ",
    "book_further_heading": "Further Reading & Official References",
    "book_pager_home": "Back to Book TOC",
    "book_nav_objectives": "Objectives",
    "book_nav_diagram": "Diagram",
    "book_nav_comparison": "Comparison",
    "book_nav_code": "Code",
    "book_nav_pitfalls": "Pitfalls",
    "book_nav_quiz": "Quiz",
    "book_nav_faq": "Interview FAQ",
}

YOUTUBE_EN: dict[str, dict[str, Any]] = {
    "ch01": {
        "video_id": "-LmHUlozTqE",
        "title": "Data Structures Explained: Arrays vs. Singly Linked Lists (Mandarin Audio + Visual Diagrams)",
        "upload_date": "2020-09-12T12:00:00+08:00",
        "views_label": "67,700+ views",
        "related": [
            ("ov_WvWbEryg", "Visual Intuition: Floyd's Tortoise & Hare Cycle Detection (LeetCode #141, Mandarin)"),
            ("2aSyeVdwATA", "Animated Walkthrough: In-Place Singly Linked List Reversal (LeetCode #206, Mandarin)"),
            ("7xBrPbmOsSs", "Data Structures Big-Picture Overview (28,200+ views, Mandarin)"),
            ("RObLhJlg2O8", "Programming Foundations: Variables, Types, Operators & Arrays (Mandarin)"),
        ],
    },
    "ch02": {
        "video_id": "0Kiunabmm0w",
        "title": "Data Structures Explained: Stacks (LIFO) & Queues (FIFO) (Mandarin Audio + Visual Diagrams)",
        "upload_date": "2020-09-13T12:00:00+08:00",
        "views_label": "35,500+ views",
        "related": [
            ("qys8Cs7J0wE", "Visual Intuition: Stacks & Valid Parentheses Matching (LeetCode #20, Mandarin)"),
            ("JSKtJqj2pwc", "Queue ADT & FIFO Scheduling Deep Dive (23,900+ views, Mandarin)"),
            ("hWrZPqJZXyg", "Functions, Overloading & the Recursive Call Stack (Mandarin)"),
        ],
    },
    "ch03": {
        "video_id": "DVDoyB5qDC4",
        "title": "Algorithms Explained: Quick Sort, Merge Sort & Searching Complexity (Mandarin Audio + Diagrams)",
        "upload_date": "2020-09-23T12:00:00+08:00",
        "views_label": "23,800+ views",
        "related": [
            ("3B4dXDxk_ck", "Animated Walkthrough: Merge Sort Divide & Conquer O(n log n) (Mandarin)"),
            ("C9Xes8wH6Co", "Merge Sort Step-by-Step Analysis (20,500+ views, Mandarin)"),
            ("iwCUOKhIhAA", "Algorithm Foundations & Big-O Time Complexity (19,100+ views, Mandarin)"),
            ("zO8kaBEy0M4", "Bubble Sort, Selection Sort & Insertion Sort Compared (18,100+ views, Mandarin)"),
            ("llSvc4rwxi0", "Binary Search O(log n) Walkthrough (13,300+ views, Mandarin)"),
        ],
    },
    "ch04": {
        "video_id": "xDwFMffqLbw",
        "title": "Data Structures Explained: Trees & Hash Tables Under the Hood (Mandarin Audio + Diagrams)",
        "upload_date": "2020-09-16T12:00:00+08:00",
        "views_label": "41,900+ views",
        "related": [
            ("rr322eEWAUo", "Animated Walkthrough: Hash Tables & LeetCode #1 Two Sum from O(n^2) to O(n) (Mandarin)"),
            ("vPvxEDyxI2w", "Hash Table Collisions & Bucket Design (28,000+ views, Mandarin)"),
            ("gA815MIEFg0", "Sets & Maps Internals Explained (18,900+ views, Mandarin)"),
        ],
    },
    "ch05": {
        "video_id": "c4R27mPT5kY",
        "title": "Algorithms Explained: Depth-First Search (DFS) & Breadth-First Search (BFS) (Mandarin Audio)",
        "upload_date": "2020-09-27T12:00:00+08:00",
        "views_label": "22,600+ views",
        "related": [
            ("ebkBxAvyFds", "Visual Intuition: BFS / DFS & Number of Islands (LeetCode #200, Mandarin)"),
            ("V_ajcNni6wk", "Core CS Curriculum: Data Structures, Algorithms & OOP (22,600+ views, Mandarin)"),
            ("5hYwLTVK4pY", "Complete Data Structures Big-O Cheat Sheet (15,000+ views, Mandarin)"),
        ],
    },
    "ch06": {
        "video_id": "M2kYdAA-FHY",
        "title": "Algorithms Explained: Dynamic Programming & State Transitions (Mandarin Audio + Diagrams)",
        "upload_date": "2020-09-29T12:00:00+08:00",
        "views_label": "31,700+ views",
        "related": [
            ("WhoRHltIukc", "Visual Intuition: Dynamic Programming & Coin Change (LeetCode #322, Mandarin)"),
            ("iLK48YAXjio", "Algorithm Paradigms: Brute Force, Greedy, Divide & Conquer, Backtracking (26,800+ views, Mandarin)"),
        ],
    },
    "ch07": {
        "video_id": "klbGg8dmYTM",
        "title": "Data Structures Explained: Binary Heaps & Priority Queues (Mandarin Audio + Diagrams)",
        "upload_date": "2020-09-17T12:00:00+08:00",
        "views_label": "26,800+ views",
        "related": [
            ("sFypmieNopU", "Visual Intuition: Min-Heaps & Top-K Elements (LeetCode #215, Mandarin)"),
            ("fHBw99bYLuo", "Heap Sort, Radix Sort & Bucket Sort Explained (13,200+ views, Mandarin)"),
        ],
    },
}

RESOURCES_EN: tuple[AffiliateResource, ...] = (
    AffiliateResource(
        partner_id="py312_docs_en",
        title="Official Python 3.12 Documentation: Data Structures & Standard Library",
        partner_label="Python.org",
        audience="All Python developers & interview candidates",
        highlight="Authoritative reference for list, collections.deque, dict, bisect, functools.cache, and heapq",
        url="https://docs.python.org/3.12/tutorial/datastructures.html",
        cta_label="Read Python Docs ↗",
        is_sponsored=False,
    ),
    AffiliateResource(
        partner_id="py_wiki_time_complexity_en",
        title="Python Wiki: Official TimeComplexity Reference Table",
        partner_label="Python Wiki",
        audience="Backend engineers & performance tuning",
        highlight="Exact average and worst-case CPython Big-O guarantees for list, deque, set, and dict operations",
        url="https://wiki.python.org/moin/TimeComplexity",
        cta_label="View Big-O Table ↗",
        is_sponsored=False,
    ),
    AffiliateResource(
        partner_id="grokking_algo_en",
        title="Grokking Algorithms (2nd Edition, Aditya Bhargava)",
        partner_label="Manning Publications",
        audience="Visual learners & career switchers",
        highlight="Illustrated intuition for binary search, hash tables, BFS/DFS, and dynamic programming (Ch.01-Ch.06)",
        url="https://www.manning.com/books/grokking-algorithms-second-edition",
        cta_label="View Book Info ↗",
        is_sponsored=False,
    ),
    AffiliateResource(
        partner_id="fluent_python_en",
        title="Fluent Python (2nd Edition, Luciano Ramalho)",
        partner_label="O'Reilly Media",
        audience="Intermediate to senior Python engineers",
        highlight="Deep dive into CPython memory layout, compact dict open addressing, typing generics, and data models",
        url="https://www.fluentpython.com/",
        cta_label="Visit Official Site ↗",
        is_sponsored=False,
    ),
)

CHAPTER_RESOURCES_EN: dict[str, tuple[str, str]] = {
    "ch01": (
        "Official Python 3.12 Reference: Built-in list & Sequence Data Structures",
        "https://docs.python.org/3.12/tutorial/datastructures.html",
    ),
    "ch02": (
        "Official Python 3.12 Reference: collections.deque Double-Ended Queue",
        "https://docs.python.org/3.12/library/collections.html#collections.deque",
    ),
    "ch03": (
        "Official Python 3.12 Reference: bisect Binary Search & Timsort Sorting HOWTO",
        "https://docs.python.org/3.12/library/bisect.html",
    ),
    "ch04": (
        "Official Python 3.12 Reference: Mapping Types (dict) & Hashability Rules",
        "https://docs.python.org/3.12/library/stdtypes.html#mapping-types-dict",
    ),
    "ch05": (
        "Official Python 3.12 Reference: typing.Generic & Object-Oriented Class Design",
        "https://docs.python.org/3.12/library/typing.html#generics",
    ),
    "ch06": (
        "Official Python 3.12 Reference: functools.cache Memoization Decorator",
        "https://docs.python.org/3.12/library/functools.html#functools.cache",
    ),
    "ch07": (
        "Official Python 3.12 Reference: heapq Heap Queue Algorithm & Priority Queues",
        "https://docs.python.org/3.12/library/heapq.html",
    ),
}

CODE_REPLACEMENTS_EN: dict[str, tuple[tuple[str, str], ...]] = {
    "ch01": (
        ("Ch.01 陣列與單向鏈結串列（Array & Singly Linked List）", "Ch.01 Arrays & Singly Linked List"),
        ("展示基礎節點（ListNode）與單向鏈結串列（SinglyLinkedList）的插入、刪除、搜尋與反轉操作。", "Demonstrates ListNode and SinglyLinkedList prepend, append, search, delete, and O(1)-space in-place reversal."),
        ("教學用單向鏈結串列實作（支援頭尾插入、指定值刪除、搜尋與原地反轉）。", "Educational singly linked list supporting O(1) prepend, append, search, remove, and in-place reverse."),
        ("在串列頭部插入新節點，時間複雜度 O(1)。", "Insert a new node at the head in O(1) time."),
        ("在串列尾部附加新節點，時間複雜度 O(n)。", "Append a new node at the tail in O(n) time."),
        ("搜尋目標值首次出現的索引（0-based），若不存在回傳 -1。", "Return the 0-based index of the first matching value, or -1 if absent."),
        ("刪除首次出現的目標值節點，成功回傳 True，不存在回傳 False。", "Remove the first node matching target; return True if removed else False."),
        ("原地（in-place）反轉鏈結串列，時間複雜度 O(n)，空間複雜度 O(1)。", "Reverse the linked list in place in O(n) time and O(1) extra space."),
        ("Ch.01 SinglyLinkedList 範例結果:", "Ch.01 SinglyLinkedList result:"),
    ),
    "ch02": (
        ("Ch.02 堆疊與佇列（Stack & Queue）", "Ch.02 Stack & Queue"),
        ("展示 LIFO 堆疊（含經典括號平衡檢查）與 FIFO 佇列的物件導向封裝實作。", "Demonstrates OOP encapsulation of a LIFO Stack (with balanced bracket validation) and a FIFO Queue."),
        ("後進先出（LIFO）堆疊。", "Last-In, First-Out (LIFO) stack."),
        ("先進先出（FIFO）佇列。", "First-In, First-Out (FIFO) queue backed by collections.deque."),
        ("利用 Stack 檢查字串中的 (), [], {} 括號是否成對且順序正確。", "Validate that (), [], and {} brackets in expr are properly balanced using a Stack."),
        ("Ch.02 括號平衡檢查 '{[()]}':", "Ch.02 Balanced brackets '{[()]}':"),
    ),
    "ch03": (
        ("Ch.03 搜尋與排序演算法（Search & Sort Algorithms）", "Ch.03 Search & Sort Algorithms"),
        ("展示二分搜尋法（Binary Search）與合併排序法（Merge Sort）。", "Demonstrates iterative Binary Search O(log n) and stable Divide-and-Conquer Merge Sort O(n log n)."),
        ("在已排序遞增序列中搜尋 target，回傳索引（0-based）；若不存在則回傳 -1。", "Search for target in a sorted ascending sequence; return 0-based index or -1 if not found."),
        ("使用分治法（Divide & Conquer）實作穩定合併排序，時間複雜度 O(n log n)。", "Return a new sorted list using stable Divide-and-Conquer Merge Sort in O(n log n) time."),
        ("Ch.03 Merge Sort 結果:", "Ch.03 Merge Sort result:"),
        ("| 27 的索引:", "| index of 27:"),
    ),
    "ch04": (
        ("Ch.04 雜湊表與二元搜尋樹（Hash Table & Binary Search Tree）", "Ch.04 Hash Table & Binary Search Tree"),
        ("展示鏈結法雜湊表（Chaining Hash Table）、LeetCode #1 Two Sum O(n) 解法與二元搜尋樹中序走訪（In-order Traversal）。", "Demonstrates a Separate-Chaining Hash Table, O(n) Two Sum (LeetCode #1), and BST in-order traversal."),
        ("以鏈結法（Separate Chaining）處理雜湊碰撞的雜湊表實作，平均讀寫複雜度 O(1)。", "Hash table resolving collisions via separate chaining with O(1) average lookup and insertion."),
        ("bucket_count 必須為正整數", "bucket_count must be a positive integer"),
        ("經典面試題 Two Sum：利用雜湊表在 O(n) 時間內找出兩數之和等於 target 的索引配對。", "Classic Two Sum: find two indices summing to target in O(n) time using a hash map."),
        ("二元搜尋樹（BST）：左子樹所有鍵值 < 根節點 < 右子樹所有鍵值，中序走訪必為遞增排序序列。", "Binary Search Tree maintaining left < root < right; in-order traversal yields ascending order."),
        ("Ch.04 Two Sum 索引:", "Ch.04 Two Sum indices:"),
        ("| BST 中序走訪:", "| BST inorder:"),
        ("| 搜尋 60:", "| contains 60:"),
    ),
    "ch05": (
        ("Ch.05 圖論走訪與物件導向設計（Graph BFS / DFS & Object-Oriented Programming）", "Ch.05 Graph Traversal (BFS / DFS) & Object-Oriented Design"),
        ("展示鄰接串列（Adjacency List）物件導向封裝、廣度優先搜尋（BFS）、深度優先搜尋（DFS）與無權重圖最短路徑。", "Demonstrates OOP encapsulation of an adjacency-list Graph with BFS, DFS, and unweighted shortest path."),
        ("以鄰接串列（Adjacency List）封裝之泛型圖論結構，時間複雜度 O(V + E)。", "Generic adjacency-list Graph supporting O(V + E) traversals."),
        ("廣度優先搜尋（Breadth-First Search）：利用佇列（Queue）由近而遠逐層擴散走訪，複雜度 O(V + E)。", "Breadth-First Search exploring vertices layer by layer with a FIFO deque in O(V + E) time."),
        ("深度優先搜尋（Depth-First Search）：一條路走到底再回溯（Backtracking），複雜度 O(V + E)。", "Depth-First Search exploring as deep as possible before backtracking in O(V + E) time."),
        ("利用 BFS 找出無權重圖中從 start 到 goal 的最少步數最短路徑。", "Find a minimum-hop shortest path from start to goal in an unweighted graph via BFS."),
        ("Ch.05 BFS 走訪:", "Ch.05 BFS order:"),
        ("| DFS 走訪:", "| DFS order:"),
        ("| A->F 最短路徑:", "| A->F shortest path:"),
    ),
    "ch06": (
        ("Ch.06 動態規劃與記憶化搜尋（Dynamic Programming & Memoization）", "Ch.06 Dynamic Programming & Memoization"),
        ("展示爬樓梯狀態壓縮 O(1) 空間解法、0/1 背包問題（一維滾動陣列）與最長嚴格遞增子序列（LIS O(n log n)）。", "Demonstrates O(1)-space Climbing Stairs, 1D rolling-array 0/1 Knapsack, and O(n log n) LIS."),
        ("計算爬到第 n 階樓梯的方法數（每次可跨 1 或 2 階）。", "Count distinct ways to climb n stairs taking 1 or 2 steps at a time."),
        ("採用自底向上（Bottom-Up）滾動變數狀態壓縮：", "Uses bottom-up rolling variables for constant space:"),
        ("- 時間複雜度：O(n)", "- Time complexity: O(n)"),
        ("- 空間複雜度：O(1)", "- Space complexity: O(1)"),
        ("階數 n 必須為非負整數", "n must be a non-negative integer"),
        ("經典 0/1 背包問題：在背包容量上限 capacity 內，每件物品最多選一次，求最大總價值。", "Classic 0/1 Knapsack: maximize total value within capacity using each item at most once."),
        ("採用一維滾動陣列並由後往前（capacity -> weight）逆序更新，避免同一物品被重複選取：", "Uses a 1D DP array iterated backwards (capacity -> weight) so each item is counted at most once:"),
        ("- 時間複雜度：O(N * W)，其中 N 為物品數、W 為 capacity", "- Time complexity: O(N * W), where N is item count and W is capacity"),
        ("- 空間複雜度：O(W)", "- Space complexity: O(W)"),
        ("capacity 必須為非負整數", "capacity must be a non-negative integer"),
        ("weights 與 values 長度必須一致", "weights and values must have the same length"),
        ("物品重量不可為負數", "item weight cannot be negative"),
        ("最長嚴格遞增子序列（Longest Increasing Subsequence, LeetCode #300）。", "Longest Strictly Increasing Subsequence (LeetCode #300)."),
        ("結合貪婪策略與二分搜尋（Patience Sorting）維護最小結尾陣列 tails：", "Combines greedy tails maintenance with binary search (Patience Sorting):"),
        ("- 時間複雜度：O(n log n)", "- Time complexity: O(n log n)"),
        ("- 空間複雜度：O(n)", "- Space complexity: O(n)"),
        ("Ch.06 DP 爬樓梯(n=10):", "Ch.06 DP climb_stairs(n=10):"),
        ("0/1 背包最大價值:", "0/1 knapsack max value:"),
        ("LIS 長度:", "LIS length:"),
    ),
    "ch07": (
        ("Ch.07 堆積、優先佇列與 Top-K 演算法（Heap, Priority Queue & Top-K Elements）", "Ch.07 Binary Heap, Priority Queue & Top-K Elements"),
        ("展示手寫泛型最小二元堆積（MinHeap）、Top-K 最大元素篩選與合併 K 個已排序序列。", "Demonstrates a generic Binary MinHeap, O(n log k) Top-K selection, and O(N log K) K-way merge."),
        ("以動態陣列封裝之最小二元堆積（Binary Min-Heap），支援 O(log n) 插入與彈出最小值。", "Array-backed Binary Min-Heap supporting O(log n) push and pop."),
        ("查看堆頂最小元素，時間複雜度 O(1)。", "Return the smallest item at the root in O(1) time without removing it."),
        ("插入新元素並執行上浮（Sift-Up）維護堆積性質，時間複雜度 O(log n)。", "Insert val and restore heap order via sift-up in O(log n) time."),
        ("彈出並回傳堆頂最小元素，將尾端元素移至堆頂後執行下沉（Sift-Down），時間複雜度 O(log n)。", "Remove and return the smallest item, restoring heap order via sift-down in O(log n) time."),
        ("利用大小固定為 k 的最小堆積，在 O(n log k) 時間與 O(k) 空間內找出前 k 大元素（由大到小回傳）。", "Find the k largest elements in O(n log k) time and O(k) space using a size-k min-heap."),
        ("利用最小堆積在 O(N log K) 時間內合併 K 個已排序遞增序列（LeetCode #23 核心邏輯）。", "Merge k sorted ascending sequences in O(N log K) time using a min-heap (LeetCode #23 pattern)."),
        ("Ch.07 MinHeap 依序彈出:", "Ch.07 MinHeap popped:"),
        ("Top-3 最大元素:", "Top-3 largest:"),
        ("合併 K 串列:", "Merged K lists:"),
    ),
}

OUTPUT_REPLACEMENTS_EN: dict[str, tuple[tuple[str, str], ...]] = {
    "ch01": (("Ch.01 SinglyLinkedList 範例結果:", "Ch.01 SinglyLinkedList result:"),),
    "ch02": (("Ch.02 括號平衡檢查 '{[()]}':", "Ch.02 Balanced brackets '{[()]}':"),),
    "ch03": (
        ("Ch.03 Merge Sort 結果:", "Ch.03 Merge Sort result:"),
        ("| 27 的索引:", "| index of 27:"),
    ),
    "ch04": (
        ("Ch.04 Two Sum 索引:", "Ch.04 Two Sum indices:"),
        ("| BST 中序走訪:", "| BST inorder:"),
        ("| 搜尋 60:", "| contains 60:"),
    ),
    "ch05": (
        ("Ch.05 BFS 走訪:", "Ch.05 BFS order:"),
        ("| DFS 走訪:", "| DFS order:"),
        ("| A->F 最短路徑:", "| A->F shortest path:"),
    ),
    "ch06": (
        ("Ch.06 DP 爬樓梯(n=10):", "Ch.06 DP climb_stairs(n=10):"),
        ("0/1 背包最大價值:", "0/1 knapsack max value:"),
        ("LIS 長度:", "LIS length:"),
    ),
    "ch07": (
        ("Ch.07 MinHeap 依序彈出:", "Ch.07 MinHeap popped:"),
        ("Top-3 最大元素:", "Top-3 largest:"),
        ("合併 K 串列:", "Merged K lists:"),
    ),
}

CHAPTERS_EN: tuple[ChapterSpec, ...] = (
    ChapterSpec(
        id="ch01",
        badge="Ch.01",
        short_title="Arrays & Singly Linked Lists",
        title="Python Arrays (list) & Singly Linked Lists",
        complexity="Prepend O(1) · Append / Search / Delete / In-Place Reverse O(n)",
        summary="Understand contiguous memory arrays (Python list) versus pointer-chained singly linked lists, O(1) random indexing versus O(1) head updates, and O(1)-space in-place linked list reversal in Python 3.12.",
        concepts=(
            "Contiguous memory vs. pointer chaining: Arrays (Python list) store object pointers in one contiguous memory block, enabling O(1) random indexing by offset arithmetic, whereas inserting at the head shifts all trailing pointers in O(n). Singly linked lists link scattered ListNode objects via next references, allowing O(1) head insertion (prepend) when the head pointer is known.",
            "In-place reversal with three pointers (prev, curr, nxt): Reversing a singly linked list without allocating a second list is one of the highest-frequency coding interview warm-ups. Tracking nxt before flipping curr.next = prev guarantees O(n) time and strictly O(1) auxiliary space.",
            "CPU cache locality in real systems: Modern CPUs fetch entire 64-byte cache lines on every memory read. Contiguous arrays exploit spatial locality and hardware prefetchers, while pointer-chasing across heap-allocated linked list nodes triggers frequent cache misses.",
        ),
        file="examples/ch01_array_linked_list.py",
        lastmod="2026-11-24",
        keywords=(
            "Python array vs linked list",
            "Python list internals",
            "singly linked list Python 3.12",
            "reverse linked list in place",
            "LeetCode 206 Python",
            "CPU cache locality arrays",
            "Floyd cycle detection",
            "dummy head node pattern",
        ),
        deep_intro=(
            "Before studying trees, graphs, or dynamic programming, every software engineer needs a concrete physical model of computer memory. "
            "Think of RAM as a single numbered row of lockers. A dynamic array such as Python's built-in list reserves a contiguous run of N pointer slots, "
            "so jumping directly to element i requires only one multiplication and one addition from the base address: pure O(1) random access. "
            "The trade-off appears the moment you insert or delete near the front of the array, because every subsequent element must shift one slot over in O(n) time. "
            "A singly linked list eliminates the contiguous-space requirement: each ListNode holds its payload val plus a next reference pointing to the next node anywhere on the heap. "
            "Prepending or popping from the head takes O(1) pointer reassignments, making linked structures the building block for hash-table chaining buckets, LRU caches (with doubly linked lists), and adjacency lists."
        ),
        comparison_table=ComparisonTable(
            caption="Operation Complexity & Memory Trade-Offs: Python list vs. Singly & Doubly Linked Lists",
            headers=("Operation / Property", "Python list (Dynamic Array)", "Singly Linked List", "Doubly Linked List"),
            rows=(
                ("Random Index Read (arr[i])", "O(1) - direct base + offset address", "O(n) - linear walk from head", "O(n) - walk from head or tail"),
                ("Insert / Delete at Head", "O(n) - shifts all trailing pointers", "O(1) - rewire head reference only", "O(1) - update head and prev links"),
                ("Append at Tail", "Amortized O(1) - O(n) on resize", "O(n) without tail / O(1) with tail", "O(1) - direct tail pointer append"),
                ("Search by Value", "O(n) linear (O(log n) if sorted)", "O(n) - forward linear scan only", "O(n) - linear scan"),
                ("Delete a Given Node Reference", "O(n) - shift remaining elements", "O(n) - must locate predecessor prev", "O(1) - splice prev and next directly"),
                ("CPU Cache Locality & Overhead", "High (contiguous pointer array)", "Low (node object header + next ptr)", "Low (object header + prev & next)"),
            ),
        ),
        walkthrough_title="Step-by-Step Three-Pointer Trace: In-Place Singly Linked List Reversal",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1: Initialize Pointers (List: 5 -> 10 -> 30 -> None)",
                state_snapshot="prev = None | curr = Node(5) | head = Node(5)",
                explanation="Before entering while curr is not None, initialize prev = None because the original head Node(5) will become the new tail whose next pointer must terminate at None. Set curr to head.",
            ),
            WalkthroughStep(
                step_label="Step 2: First Iteration - Save Next Node and Flip Node(5)",
                state_snapshot="nxt = Node(10) | Node(5).next = None | prev = Node(5) | curr = Node(10)",
                explanation="Always capture nxt = curr.next before mutating curr.next. Without that backup, writing curr.next = prev severs the only reference to the remaining list. Then advance both prev and curr one step forward.",
            ),
            WalkthroughStep(
                step_label="Step 3: Second Iteration - Reverse Middle Node(10) to Point at Node(5)",
                state_snapshot="nxt = Node(30) | Node(10).next = Node(5) | prev = Node(10) | curr = Node(30)",
                explanation="Store nxt = Node(30), point Node(10).next back to prev (Node(5)) to build the reversed prefix 10 -> 5 -> None, and slide prev to Node(10) and curr to the final node Node(30).",
            ),
            WalkthroughStep(
                step_label="Step 4: Final Iteration & Head Reassignment",
                state_snapshot="nxt = None | Node(30).next = Node(10) | prev = Node(30) | curr = None => self.head = prev",
                explanation="Point Node(30).next to Node(10), advance curr to None to exit the loop, and assign self.head = prev so the list now reads 30 -> 10 -> 5 -> None in strictly O(1) extra space.",
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="Pitfall 1: Overwriting curr.next Before Backing Up the Remainder (Lost Reference)",
                symptom="After calling reverse(), the list collapses to a single node and every subsequent node disappears.",
                root_cause_and_fix="Mutating curr.next destroys the only forward link to the unvisited suffix. Always preserve the exact 4-line invariant: (1) nxt = curr.next, (2) curr.next = prev, (3) prev = curr, (4) curr = nxt.",
            ),
            PitfallItem(
                title="Pitfall 2: Crashing on Head Deletion or Empty Lists",
                symptom="Executing prev.next = curr.next inside remove(target) raises AttributeError: 'NoneType' object has no attribute 'next' whenever the target sits at head.",
                root_cause_and_fix="When removing the head node, prev is None and requires updating self.head = curr.next. In interview problems that may delete or swap head, allocate a sentinel dummy = ListNode(0, head) so every real node shares a uniform predecessor.",
            ),
            PitfallItem(
                title="Pitfall 3: Assuming a Custom Python Linked List Uses Less Memory Than Built-In list",
                symptom="Replacing a Python list of 100,000 integers with custom ListNode instances multiplies RAM usage and slows iteration dramatically.",
                root_cause_and_fix="CPython's built-in list stores a compact C array of 8-byte PyObject* pointers, whereas every Python ListNode instance carries full object header and attribute overhead even with __slots__. Use built-in list for indexed sequences and collections.deque for O(1) double-ended queues.",
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(206, "Reverse Linked List", "Easy", "Three-pointer iterative / recursive reversal · Time O(n) / Space O(1)"),
            LeetCodeProblem(21, "Merge Two Sorted Lists", "Easy", "Dummy sentinel node + two-pointer zipper merge · Time O(n + m) / Space O(1)"),
            LeetCodeProblem(141, "Linked List Cycle", "Easy", "Floyd's Tortoise and Hare fast/slow pointers · Time O(n) / Space O(1)"),
            LeetCodeProblem(19, "Remove Nth Node From End of List", "Medium", "Fast pointer lead of N steps + dummy node single pass · Time O(n) / Space O(1)"),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="Why is Python list.append() amortized O(1) while list.insert(0, val) is always O(n)?",
                answer="CPython implements list as an over-allocated dynamic array, growing capacity by roughly 1.125x whenever it fills up. Most append() calls simply drop a pointer into the next free tail slot in O(1), amortizing occasional O(n) reallocations across all writes. Conversely, insert(0, val) must call memmove to shift every existing pointer right by one slot on every single invocation, costing O(n) every time.",
            ),
            InterviewFAQ(
                question="How do you detect a cycle in a singly linked list in O(1) space without modifying nodes?",
                answer="Use Floyd's Tortoise and Hare algorithm with two pointers starting at head: slow advances one step per iteration (slow = slow.next) while fast advances two steps (fast = fast.next.next). If no cycle exists, fast reaches None first. If a cycle exists, fast closes the gap by one node per iteration inside the loop until slow is fast, completing in O(n) time and O(1) extra space.",
            ),
            InterviewFAQ(
                question="When should you reach for a Dummy Head Node in linked list interview problems?",
                answer="Whenever an algorithm might delete, replace, or reorder the original head node (such as LeetCode #21 Merge Two Sorted Lists, #19 Remove Nth From End, or #203 Remove Linked List Elements). Initializing dummy = ListNode(0, head) gives the original head a valid predecessor so all mutations follow one branch, and you simply return dummy.next at the end.",
            ),
            InterviewFAQ(
                question="What is the difference between a Python array and a list, and when should you choose list, array.array, or NumPy?",
                answer="Python's built-in list is a dynamic array of PyObject pointers that holds mixed types with O(1) indexing and amortized O(1) append, making it the default choice for general engineering and algorithm interviews. The stdlib array.array stores homogeneous raw C primitives (such as int32 or float64) tightly in memory for lower RAM footprint and binary I/O. For heavy numeric computing or matrix math, use NumPy ndarray for contiguous memory layouts and vectorized C/SIMD speedups.",
            ),
        ),
    ),
    ChapterSpec(
        id="ch02",
        badge="Ch.02",
        short_title="Stacks & Queues",
        title="Stacks (LIFO) & Queues (FIFO) with collections.deque",
        complexity="Push / Pop / Enqueue / Dequeue: Strict O(1)",
        summary="Master Last-In First-Out (LIFO) and First-In First-Out (FIFO) abstract data types, avoid the O(n) list.pop(0) trap with collections.deque, and implement a balanced-bracket parser.",
        concepts=(
            "Stack (LIFO - Last-In, First-Out): Like a stack of plates, the most recently pushed item is popped first. Stacks power runtime function call frames, browser history back buttons, syntax bracket validation, and iterative Depth-First Search (DFS).",
            "Queue (FIFO - First-In, First-Out): Like a checkout line, the earliest arriving item is processed first. Never simulate a queue in Python with list.pop(0) (which triggers O(n) array shifts); always use collections.deque.popleft() for strict O(1) dequeue in Breadth-First Search (BFS) and task pipelines.",
            "Monotonic Stack pattern: Maintaining elements in strictly increasing or decreasing order inside a stack solves 'next greater element', 'daily temperatures', and 'largest rectangle in histogram' in linear O(n) time because each index enters and exits the stack at most once.",
        ),
        file="examples/ch02_stack_queue.py",
        lastmod="2026-11-24",
        keywords=(
            "Python stack and queue",
            "collections.deque vs list pop(0)",
            "Valid Parentheses Python",
            "LeetCode 20 Python",
            "LIFO FIFO data structures",
            "monotonic stack Python",
            "queue using two stacks",
            "CPython deque internals",
        ),
        deep_intro=(
            "Stacks and queues are not tied to one physical memory layout; they are Abstract Data Types (ADTs) that enforce a strict ordering contract at their endpoints. "
            "Restricting where elements can enter and leave makes complex program state predictable and verifiable. "
            "Stacks enforce Last-In, First-Out (LIFO) discipline: operating systems track active function invocations on the call stack, "
            "compilers validate nested scopes and parentheses, and editors implement multi-step Undo using stacks. "
            "Queues enforce First-In, First-Out (FIFO) fairness: OS task schedulers, network socket buffers, asynchronous message brokers, "
            "and level-order Breadth-First Search (BFS) all rely on FIFO queues to process items in exact arrival order."
        ),
        comparison_table=ComparisonTable(
            caption="Performance & Use-Case Matrix: Stack, collections.deque, Anti-Pattern list.pop(0), and Thread-Safe Queue",
            headers=("Implementation", "Order Model", "Insert (Push / Enqueue)", "Remove (Pop / Dequeue)", "Production & Interview Guidance"),
            rows=(
                ("Stack (Python list wrapper)", "LIFO", "list.append(x) - Amortized O(1)", "list.pop() - O(1)", "Recommended: compact cache-friendly tail ops for parsing, DFS, undo"),
                ("Queue (collections.deque)", "FIFO", "deque.append(x) - O(1)", "deque.popleft() - O(1)", "Recommended: doubly linked blocks give strict O(1) at both ends for BFS"),
                ("Anti-Pattern (list.pop(0))", "FIFO", "list.append(x) - Amortized O(1)", "list.pop(0) - O(n) shift trap", "Avoid! Shifting N-1 pointers per pop degrades BFS to O(n^2) and TLE"),
                ("Thread-Safe queue.Queue", "FIFO", "put(x) - O(1) + lock overhead", "get() - O(1) + lock overhead", "Built-in mutex & condition vars for multi-threaded producer/consumer"),
                ("Monotonic Stack", "Ordered LIFO", "Each item pushed <= 1x - Amortized O(1)", "Pop violating items - Amortized O(1)", "Linear O(n) solver for nearest greater/smaller element queries"),
            ),
        ),
        walkthrough_title="Step-by-Step Stack Trace: Balanced Bracket Validation on '{[()]}'",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1: Push Opening Brackets '{', '[', '(' onto the Stack",
                state_snapshot="Input: '{' -> '[' -> '(' | Stack (bottom -> top): ['{', '[', '(']",
                explanation="Whenever the scanner encounters an opening delimiter in {'(', '[', '{'}, a new nested scope begins. Push each symbol onto the stack top to remember the exact order in which scopes must close.",
            ),
            WalkthroughStep(
                step_label="Step 2: Match First Closing Bracket ')' Against Stack Top",
                state_snapshot="Input: ')' | pairs[')'] == '(' | stack.pop() -> '(' (match) | Remaining: ['{', '[']",
                explanation="By LIFO order, ')' must close the most recently opened unclosed bracket. Verify the stack is non-empty, pop '(', confirm it matches pairs[')'], and continue.",
            ),
            WalkthroughStep(
                step_label="Step 3: Unwind ']' and '}' Layer by Layer",
                state_snapshot="Read ']': pop() -> '[' OK | Read '}': pop() -> '{' OK | Remaining: []",
                explanation="Both ']' and '}' match the newly exposed stack tops '[' and '{'. If brackets were interleaved like '([)]', popping '(' when expecting '[' would immediately return False.",
            ),
            WalkthroughStep(
                step_label="Step 4: Confirm Empty Stack at End of Input",
                state_snapshot="Loop complete | stack.is_empty() == True => Return True",
                explanation="Never blindly return True when the loop finishes! An input like '(((' never triggers a mismatch branch inside the loop; checking stack.is_empty() guarantees every opening delimiter was properly closed.",
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="Pitfall 1: Calling list.pop(0) Inside a BFS Loop Causes Hidden O(n^2) Timeouts",
                symptom="Your graph traversal passes small unit tests instantly, then hits Time Limit Exceeded on inputs with 100,000 vertices.",
                root_cause_and_fix="Removing index 0 from a contiguous Python list forces CPython to memmove all remaining N-1 pointers forward on every iteration, turning N dequeues into O(n^2) work. Always import collections.deque and call popleft() for FIFO queues.",
            ),
            PitfallItem(
                title="Pitfall 2: Popping or Peeking an Empty Stack Without Short-Circuit Guarding",
                symptom="Inputs beginning with a closing bracket such as ')()' or ']' crash with IndexError: pop from empty list.",
                root_cause_and_fix="Always place the non-empty check (not stack.is_empty() or if stack:) on the left side of boolean AND/OR expressions so Python's short-circuit evaluation prevents invalid pop() or stack[-1] lookups.",
            ),
            PitfallItem(
                title="Pitfall 3: Returning True After the Loop Without Checking for Leftover Openers",
                symptom="Inputs such as '(((' or '{[' erroneously pass validation as True.",
                root_cause_and_fix="The loop body only catches extra closing brackets or type mismatches. Always conclude the function with return stack.is_empty() so dangling unclosed openers return False.",
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(20, "Valid Parentheses", "Easy", "LIFO stack pairing + empty-stack guard · Time O(n) / Space O(n)"),
            LeetCodeProblem(232, "Implement Queue using Stacks", "Easy", "Lazy transfer from in_stack to out_stack · Amortized Time O(1)"),
            LeetCodeProblem(155, "Min Stack", "Medium", "Parallel min-tracking stack (or encoded deltas) · getMin Time O(1)"),
            LeetCodeProblem(739, "Daily Temperatures", "Medium", "Monotonic decreasing stack storing indices · Time O(n) / Space O(n)"),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="How does CPython implement collections.deque internally, and why is random indexing d[i] slow?",
                answer="CPython implements deque as a doubly linked list of fixed-size memory blocks (typically 64 pointer slots per block) rather than one flat array. Tracking head/tail block pointers and offsets yields strict O(1) append, appendleft, pop, and popleft without shifting the entire sequence. However, indexing into the middle (d[i]) must traverse block links linearly, taking O(n) time.",
            ),
            InterviewFAQ(
                question="How can two LIFO stacks implement an amortized O(1) FIFO queue (LeetCode #232)?",
                answer="Maintain an in_stack for enqueue(x) (O(1) push) and an out_stack for dequeue()/peek(). Whenever out_stack is non-empty, pop directly in O(1). When out_stack is empty, pop every item from in_stack and push it onto out_stack; reversing order twice brings the earliest item to the top of out_stack. Because every element is pushed to in_stack once, moved once, and popped once, each operation costs amortized O(1).",
            ),
            InterviewFAQ(
                question="What problem clues tell you to apply a Monotonic Stack?",
                answer="Whenever a prompt asks for the nearest greater or smaller element to the left or right of every array position (such as LeetCode #739 Daily Temperatures, #496 Next Greater Element, or #84 Largest Rectangle in Histogram). Instead of an O(n^2) nested scan, push indices onto a monotonic stack and pop whenever the incoming element resolves pending waiting indices, achieving linear O(n) runtime.",
            ),
        ),
    ),
    ChapterSpec(
        id="ch03",
        badge="Ch.03",
        short_title="Binary Search & Merge Sort",
        title="Searching & Sorting Algorithms (Binary Search & Merge Sort)",
        complexity="Binary Search O(log n) · Merge Sort O(n log n) Stable",
        summary="Bridge the leap from O(n) linear scans to O(log n) binary search, implement stable Divide-and-Conquer Merge Sort in Python 3.12, and understand why Python's Timsort outperforms naive Quick Sort.",
        concepts=(
            "Binary Search (O(log n)): On any sorted or monotonic sequence, inspecting the midpoint eliminates half of all remaining candidates on every comparison—searching 1,000,000 sorted items takes at most 20 comparisons.",
            "Merge Sort (Divide & Conquer): Recursively splits the input in half down to single-element base cases, then zips sorted halves back together with two pointers. It guarantees O(n log n) time even in the worst case and preserves equal-key relative order (stability).",
            "Sorting stability & Python's Timsort: A stable sort keeps equal-key records in their original relative order, which is critical for multi-column sorting. Python's built-in sorted() and list.sort() use Timsort, blending Merge Sort with Insertion Sort to hit O(n) on nearly sorted real-world arrays.",
        ),
        file="examples/ch03_search_sort.py",
        lastmod="2026-11-24",
        keywords=(
            "binary search Python 3.12",
            "merge sort Python implementation",
            "divide and conquer algorithms",
            "Python Timsort explained",
            "stable vs unstable sorting",
            "LeetCode 704 binary search",
            "bisect module Python",
            "O(n log n) sorting",
        ),
        deep_intro=(
            "Searching and sorting are the twin workhorses of classical algorithm design. "
            "When data arrives unsorted, finding a target forces a linear scan across every element in O(n) time. "
            "Once the sequence is sorted into monotonic order, Binary Search cuts the search space in half on every step: "
            "across one billion (10^9) sorted records, linear search may check a billion entries, whereas binary search needs at most 30 comparisons (log2(10^9) ~ 29.89). "
            "To transform unsorted data into sorted order efficiently without risking quadratic O(n^2) worst-case stalls, "
            "this chapter builds stable Merge Sort using Divide and Conquer, hitting the comparison-sorting lower bound of O(n log n)."
        ),
        comparison_table=ComparisonTable(
            caption="Searching & Sorting Algorithms: Best/Average/Worst Time, Space, and Stability",
            headers=("Algorithm", "Best Time", "Average Time", "Worst Time", "Extra Space & Stability"),
            rows=(
                ("Linear Search", "O(1)", "O(n)", "O(n)", "O(1) space · Works on unsorted sequences"),
                ("Binary Search", "O(1)", "O(log n)", "O(log n)", "O(1) iterative space · Requires sorted/monotonic input"),
                ("Insertion Sort", "O(n)", "O(n^2)", "O(n^2)", "O(1) space · Stable (very fast on tiny/nearly sorted data)"),
                ("Merge Sort", "O(n log n)", "O(n log n)", "O(n log n)", "O(n) space · Stable (zero O(n^2) worst-case degradation)"),
                ("Quick Sort", "O(n log n)", "O(n log n)", "O(n^2)", "O(log n) call stack · Unstable (bad pivots degrade to O(n^2))"),
                ("Heap Sort", "O(n log n)", "O(n log n)", "O(n log n)", "O(1) in-place · Unstable"),
                ("Python Timsort (sorted / .sort)", "O(n)", "O(n log n)", "O(n log n)", "O(n) space · Stable (exploits natural sorted runs)"),
            ),
        ),
        walkthrough_title="Step-by-Step Trace: Merge Sort Divide & Conquer + Binary Search Lookup",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1: Divide Phase - Recursively Halve Until Subarrays Have Length <= 1",
                state_snapshot="[38, 27, 43, 3] => Left [38, 27] & Right [43, 3] => Base cases [38], [27], [43], [3]",
                explanation="merge_sort() splits the list at mid = len(arr) // 2 until every subarray contains at most one element. Any 0- or 1-element list is trivially sorted and serves as the recursion base case.",
            ),
            WalkthroughStep(
                step_label="Step 2: Conquer Level 1 - Zip Adjacent Base Elements with Two Pointers",
                state_snapshot="Merge [38] & [27] -> [27, 38] | Merge [43] & [3] -> [3, 43]",
                explanation="As recursion unwinds, pointers i and j compare the front of each sorted half and append the smaller item first, producing sorted pairs [27, 38] and [3, 43].",
            ),
            WalkthroughStep(
                step_label="Step 3: Conquer Level 2 - Zipper Merge [27, 38] and [3, 43]",
                state_snapshot="3 < 27 (take 3) -> 27 <= 43 (take 27) -> 38 <= 43 (take 38) -> extend tail [43]",
                explanation="Comparing left[i] and right[j] in linear time emits [3, 27, 38], then extends any unconsumed tail ([43]) in one slice copy to produce [3, 27, 38, 43].",
            ),
            WalkthroughStep(
                step_label="Step 4: Run Binary Search on Full Sorted Sample [3, 9, 10, 27, 38, 43, 82] for 27",
                state_snapshot="left = 0, right = 6 => mid = 3 => sorted_nums[3] == 27 (hit index 3 in 1 check!)",
                explanation="Computing mid = left + (right - left) // 2 = 3 lands directly on 27 on the very first probe, returning 0-based index 3.",
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="Pitfall 1: Updating left = mid or right = mid in Closed-Interval Binary Search",
                symptom="Searching for a missing target in while left <= right loops forever once left == right.",
                root_cause_and_fix="In a closed interval [left, right], once sorted_nums[mid] != target you have proven mid is not the answer. Always shrink strictly past mid using left = mid + 1 or right = mid - 1 so the interval shrinks by at least 1 every iteration.",
            ),
            PitfallItem(
                title="Pitfall 2: Writing < Instead of <= During Merge Breaks Stability",
                symptom="Sorting records by key reorders tied elements out of their original input sequence.",
                root_cause_and_fix="When left_half[i] == right_half[j], the left element originally appeared earlier. Using <= selects left_half[i] first and guarantees a strictly stable Merge Sort.",
            ),
            PitfallItem(
                title="Pitfall 3: Cross-Language Midpoint Overflow & Ignoring Python's C-Speed bisect",
                symptom="(left + right) // 2 overflows 32-bit signed integers in C++/Java when indices exceed 2^30, and hand-rolled binary search runs slower than C extensions in Python production code.",
                root_cause_and_fix="Write mid = left + (right - left) // 2 as a portable defensive habit across languages, and leverage Python's C-backed standard library bisect.bisect_left() in production code and timed assessments.",
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(704, "Binary Search", "Easy", "Closed-interval [left, right] template · Time O(log n) / Space O(1)"),
            LeetCodeProblem(33, "Search in Rotated Sorted Array", "Medium", "Identify the sorted half via mid and discard half · Time O(log n)"),
            LeetCodeProblem(34, "Find First and Last Position of Element in Sorted Array", "Medium", "Left/right boundary binary search (bisect_left / bisect_right) · Time O(log n)"),
            LeetCodeProblem(912, "Sort an Array", "Medium", "Hand-written Merge Sort avoiding Quick Sort O(n^2) worst case · Time O(n log n)"),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="How can you intuitively prove that Merge Sort runs in O(n log n) time?",
                answer="Halving an array of length n down to single elements creates a recursion tree of depth log2(n) + 1. Across every level of that tree, regardless of how many subarrays exist, the zipper-merge pass touches every element exactly once, doing O(n) work per level. Multiplying O(n) work per level by O(log n) levels yields O(n log n) in best, average, and worst cases.",
            ),
            InterviewFAQ(
                question="Why did Python choose Timsort (Merge Sort hybrid) over in-place Quick Sort for sorted() and list.sort()?",
                answer="Two reasons: First, Python guarantees sorting stability so multi-key sorts preserve prior ordering (for example sorting by score, then by department). Second, real-world datasets frequently contain pre-ordered chunks called natural runs; Timsort detects those runs, extends short runs with binary insertion sort, and merges them adaptively, achieving O(n) best-case speed on already-sorted inputs.",
            ),
            InterviewFAQ(
                question="Where does Binary Search apply beyond checking whether a number exists in a sorted array?",
                answer="Binary search works on any monotonic predicate over a search space ('Binary Search on the Answer'). Whenever feasibility flips once from False to True (if speed X works, every speed > X also works), you can binary search the answer space directly—classic examples include LeetCode #875 Koko Eating Bananas, #1011 Capacity To Ship Packages Within D Days, and #410 Split Array Largest Sum.",
            ),
        ),
    ),
    ChapterSpec(
        id="ch04",
        badge="Ch.04",
        short_title="Hash Tables & BSTs",
        title="Hash Tables & Binary Search Trees (Two Sum & In-Order BST)",
        complexity="Hash Table Average O(1) · Balanced BST O(log n) · In-Order Traversal O(n)",
        summary="Master Separate-Chaining Hash Tables, solve LeetCode #1 Two Sum in O(n) time, and build a Binary Search Tree with O(n) sorted in-order traversal in Python 3.12.",
        concepts=(
            "Hash Table (Python dict): Maps arbitrary hashable keys to array buckets via a hash function for O(1) average reads and writes. Collisions are handled through Separate Chaining or Open Addressing. Trading O(n) space for a hash map drops LeetCode #1 Two Sum from O(n^2) to single-pass O(n).",
            "Binary Search Tree (BST): Enforces the strict ordering invariant 'all left-subtree keys < root < all right-subtree keys'. Balanced BSTs deliver O(log n) search/insert and emit fully sorted sequences in O(n) via left -> root -> right in-order traversal.",
            "Load factor & rehashing: As the ratio alpha = N / M (entries to buckets) climbs, collision chains lengthen. Production hash tables automatically resize and rehash once alpha crosses a threshold (2/3 in CPython dict) to keep lookups amortized O(1).",
        ),
        file="examples/ch04_hash_bst.py",
        lastmod="2026-11-24",
        keywords=(
            "Python hash table implementation",
            "separate chaining vs open addressing",
            "Two Sum Python O(n)",
            "LeetCode 1 Python",
            "Binary Search Tree Python",
            "BST inorder traversal",
            "CPython dict internals",
            "validate BST LeetCode 98",
        ),
        deep_intro=(
            "If one mental reflex unlocks more coding interview problems than any other, it is this: whenever a brute-force solution wastes O(n^2) time repeatedly searching for a partner value, "
            "ask whether a Hash Table can trade O(n) space for O(1) lookups. "
            "By computing bucket = hash(key) % bucket_count, a hash table jumps straight to the target slot in constant average time. "
            "Yet hash tables are inherently unordered by key magnitude (Python 3.7+ dicts preserve insertion order, not sorted key order), so they cannot answer range queries like 'all keys between L and R' without scanning every entry. "
            "Binary Search Trees (BSTs) fill that exact gap: maintaining left < root < right enables both logarithmic search/insertion (when balanced) and natural sorted iteration via in-order traversal."
        ),
        comparison_table=ComparisonTable(
            caption="Hash Table vs. Balanced BST vs. Skewed Worst-Case BST Capabilities & Complexity",
            headers=("Operation / Capability", "Hash Table (Python dict)", "Balanced BST (AVL / Red-Black)", "Skewed BST (Worst Case)"),
            rows=(
                ("Point Lookup (Search / Get)", "Avg O(1) / Worst O(n) collisions", "O(log n) - discards half tree", "O(n) - degenerates into linked list"),
                ("Insert / Update (Put)", "Amortized O(1) / O(n) on rehash", "O(log n) - includes rotations", "O(n) - descends single chain"),
                ("Delete Key (Remove)", "Avg O(1)", "O(log n) - in-order successor swap", "O(n) - linear walk + unlink"),
                ("Emit All Keys Sorted", "O(n log n) - requires sorted()", "O(n) - direct in-order traversal", "O(n) - in-order traversal"),
                ("Range Query [L, R]", "O(n) - full table scan required", "O(log n + k) - prunes subtrees", "O(n) - no pruning possible"),
                ("Key Type Requirement", "Hashable & immutable", "Comparable (<, > ordering)", "Comparable (<, > ordering)"),
            ),
        ),
        walkthrough_title="Step-by-Step Trace: One-Pass Hash Map Two Sum & BST In-Order Traversal",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1: Two Sum Scans Index 0 (nums = [2, 7, 11, 15], target = 9)",
                state_snapshot="idx = 0, num = 2 | complement = 9 - 2 = 7 | 7 not in seen | store seen = {2: 0}",
                explanation="Read 2 and compute its required partner complement = 9 - 2 = 7. Since 7 is not yet in seen, record value-to-index mapping {2: 0} and move forward.",
            ),
            WalkthroughStep(
                step_label="Step 2: Two Sum Scans Index 1 - Immediate O(1) Hit",
                state_snapshot="idx = 1, num = 7 | complement = 9 - 7 = 2 | 2 in seen (index 0) => return (0, 1)",
                explanation="Read 7 and compute complement = 9 - 7 = 2. Looking up 2 in seen hits index 0 in O(1) time, returning (0, 1) without any nested loop.",
            ),
            WalkthroughStep(
                step_label="Step 3: Build BST from [50, 30, 70, 20, 40, 60, 80]",
                state_snapshot="Root = 50 | Left: 30 (L=20, R=40) | Right: 70 (L=60, R=80)",
                explanation="50 becomes the root; 30 < 50 descends left and 70 > 50 descends right; 20 and 40 attach under 30 while 60 and 80 attach under 70, creating a balanced 3-level BST.",
            ),
            WalkthroughStep(
                step_label="Step 4: Run In-Order Traversal (Left -> Root -> Right)",
                state_snapshot="Visit order: (20 -> 30 -> 40) -> 50 -> (60 -> 70 -> 80) => [20, 30, 40, 50, 60, 70, 80]",
                explanation="Recursion dives all the way to the leftmost leaf 20, prints parent 30, visits right child 40, emits root 50, and repeats symmetrically on the right subtree to produce a strictly ascending list.",
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="Pitfall 1: Using Mutable Containers (list, dict, set) as Dictionary Keys",
                symptom="Writing seen[[1, 2, 3]] = val in grouping problems raises TypeError: unhashable type: 'list'.",
                root_cause_and_fix="A hash table requires every key's hash to remain immutable for its lifetime, otherwise mutating a key would strand it in the wrong bucket. Convert sequences to immutable tuple(my_list) or sets to frozenset(my_set) before hashing.",
            ),
            PitfallItem(
                title="Pitfall 2: Inserting Pre-Sorted Data into an Unbalanced BST Degrades to O(n)",
                symptom="Inserting [10, 20, 30, 40, 50] sequentially turns BinarySearchTree into a right-skewed chain with O(n) lookups.",
                root_cause_and_fix="When every incoming key exceeds the prior one, every node hangs off right pointers. For sorted arrays, recursively pick the middle element arr[mid] as root (LeetCode #108); in production databases and standard libraries, self-balancing Red-Black or AVL trees rotate automatically.",
            ),
            PitfallItem(
                title="Pitfall 3: Validating a BST by Checking Only Immediate Children",
                symptom="A tree with root 50, left child 30, and 30's right child 60 passes a local left < parent < right check even though 60 > 50 violates the BST invariant.",
                root_cause_and_fix="Every descendant in the left subtree must be strictly less than the root. Pass valid open bounds validate(node, low, high) recursively ensuring low < node.val < high, or verify that an in-order traversal is strictly increasing.",
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(1, "Two Sum", "Easy", "One-pass hash map recording value -> index · Time O(n) / Space O(n)"),
            LeetCodeProblem(49, "Group Anagrams", "Medium", "Sorted-char tuple or 26-letter count tuple as dict key · Time O(n * k)"),
            LeetCodeProblem(98, "Validate Binary Search Tree", "Medium", "Recursive (low, high) range bounds or strictly increasing inorder · Time O(n)"),
            LeetCodeProblem(230, "Kth Smallest Element in a BST", "Medium", "In-order traversal stopping at the Kth visited node · Time O(H + k)"),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="This chapter demonstrates Separate Chaining—does CPython's built-in dict also use chaining?",
                answer="No. Separate chaining is ideal for teaching collision mechanics clearly, but CPython 3.6+ uses a highly optimized Compact Open Addressing layout. It separates a sparse hash-index table from a dense entries array storing (hash, key, value) tuples and resolves collisions with pseudo-random perturb probing, saving 20-25% RAM, preserving insertion order, and improving CPU cache hit rates.",
            ),
            InterviewFAQ(
                question="What is the practical difference between Pre-order, In-order, and Post-order binary tree traversals?",
                answer="They differ by when the root is processed: (1) Pre-order (Root -> Left -> Right) processes nodes on entry, ideal for cloning or serializing a tree; (2) In-order (Left -> Root -> Right) emits sorted ascending keys on a BST; (3) Post-order (Left -> Right -> Root) computes children first, making it essential for tree height, subtree aggregates, freeing resources, and bottom-up tree DP.",
            ),
            InterviewFAQ(
                question="Why is One-Pass Hash Table Two Sum cleaner than Two-Pass (pre-populating the entire map first)?",
                answer="Besides cutting a full pass over the input, one-pass lookup handles duplicate numbers cleanly—such as nums = [3, 3], target = 6. When visiting index 1, you check whether complement = 3 is already in seen before overwriting seen[3], immediately finding index 0 and returning (0, 1) without matching an element with itself.",
            ),
        ),
    ),
    ChapterSpec(
        id="ch05",
        badge="Ch.05",
        short_title="Graph BFS / DFS & OOP",
        title="Graph Traversal (BFS / DFS) & Object-Oriented Design",
        complexity="BFS / DFS Traversal & Unweighted Shortest Path: O(V + E)",
        summary="Encapsulate an adjacency-list Graph[T] with clean Python 3.12 OOP generics, and implement Breadth-First Search (BFS), Depth-First Search (DFS), and unweighted shortest-path reconstruction.",
        concepts=(
            "BFS vs. DFS traversal: BFS expands outward in concentric rings using a FIFO collections.deque, guaranteeing that the first visit to a target vertex yields the minimum-hop shortest path. DFS dives deep along one branch using recursion or an explicit stack before backtracking, excelling at connected components, topological sorting, and cycle detection.",
            "OOP encapsulation with generics: Hiding the internal adjacency dictionary _adj behind Graph[T] methods (add_vertex, add_edge, neighbors, bfs, dfs, shortest_path_bfs) enforces structural invariants cleanly while exposing a type-safe, maintainable public API.",
            "Sparse vs. dense graph representation: Real-world graphs (road networks, social graphs, package dependencies) are overwhelmingly sparse (E << V^2). An adjacency list uses only O(V + E) memory, far smaller than an O(V^2) adjacency matrix.",
        ),
        file="examples/ch05_graph_oop.py",
        lastmod="2026-11-24",
        keywords=(
            "Python graph BFS DFS",
            "adjacency list Python OOP",
            "unweighted shortest path BFS",
            "LeetCode 200 Number of Islands",
            "multi-source BFS Python",
            "Python typing Generic Graph",
            "BFS vs Dijkstra",
            "iterative DFS RecursionError",
        ),
        deep_intro=(
            "When relationships move beyond one-to-one sequences (lists) or one-to-many hierarchies (trees) into arbitrary many-to-many connections, you enter Graph Theory. "
            "Road navigation engines, social recommendation graphs, dependency resolvers, and game pathfinding all model entities as vertices (V) connected by edges (E). "
            "This chapter pairs graph algorithms with practical Object-Oriented Programming (OOP): encapsulating _adj: dict[T, list[T]] inside a generic Graph[T] class "
            "prevents callers from accidentally breaking bidirectional edges, triggering missing-key KeyErrors, or mutating internal neighbor lists."
        ),
        comparison_table=ComparisonTable(
            caption="Graph Representations (Adjacency List vs. Matrix) & Traversal Algorithms (BFS vs. DFS)",
            headers=("Representation / Algorithm", "Space Complexity", "Time Complexity", "Core Data Structure", "Best Production & Interview Use Cases"),
            rows=(
                ("Adjacency List", "O(V + E)", "Iterate neighbors O(deg(v))", "dict[T, list[T]]", "Default choice for sparse graphs (95% of real & LeetCode graphs)"),
                ("Adjacency Matrix", "O(V^2)", "Check edge (u, v) O(1)", "2D array matrix[V][V]", "Small dense graphs (V <= 500) needing constant-time edge checks"),
                ("Breadth-First Search (BFS)", "O(V) queue + visited", "O(V + E)", "FIFO queue (collections.deque)", "Unweighted shortest path, minimum steps, multi-source spreading"),
                ("Depth-First Search (DFS)", "O(V) recursion depth", "O(V + E)", "LIFO stack / call stack", "Connected components, backtracking, path enumeration, cycle checks"),
                ("BFS Parent Reconstruction", "O(V) parent dict", "O(V + E)", "deque + parent: dict[T, T|None]", "Returns both minimum hop distance and the exact vertex path"),
            ),
        ),
        walkthrough_title="Step-by-Step Trace: Unweighted BFS Shortest Path & Parent Backtracking (A -> F)",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1: Seed Starting Vertex 'A' (Distance Layer 0)",
                state_snapshot="queue = deque(['A']) | parent = {'A': None}",
                explanation="Enqueue 'A' and initialize parent = {'A': None}. The parent dictionary pulls double duty: it acts as the visited set to prevent revisiting vertices and records the exact predecessor that first discovered each vertex.",
            ),
            WalkthroughStep(
                step_label="Step 2: Expand Layer 1 - Pop 'A' and Enqueue Neighbors 'B' & 'C'",
                state_snapshot="popleft() -> 'A' | enqueue 'B', 'C' | parent = {'A': None, 'B': 'A', 'C': 'A'}",
                explanation="Pop 'A' from the left end of the deque. Both neighbors 'B' and 'C' are unseen, so record their parent as 'A' immediately before appending them to the queue.",
            ),
            WalkthroughStep(
                step_label="Step 3: Expand Layer 2 - Process 'B' and 'C' to Discover 'D' & 'E'",
                state_snapshot="pop 'B' -> enqueue 'D' (parent='B') | pop 'C' -> enqueue 'E' (parent='C') | queue = deque(['D', 'E'])",
                explanation="Processing 'B' skips already-visited 'A' and discovers 'D'; processing 'C' discovers 'E'. Every vertex now waiting in the queue is exactly 2 hops from 'A'.",
            ),
            WalkthroughStep(
                step_label="Step 4: Layer 3 Hits Goal 'F' - Backtrack via parent Map",
                state_snapshot="pop 'D' -> neighbor 'F' == goal | parent['F'] = 'D' | Backtrack: F->D->B->A => reverse ['A', 'B', 'D', 'F']",
                explanation="When 'D' inspects neighbor 'F', it hits goal immediately. Walking backwards through parent (F -> D -> B -> A -> None) and reversing yields a guaranteed minimum-hop shortest path ['A', 'B', 'D', 'F'].",
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="Pitfall 1: Marking Vertices Visited on Dequeue Instead of Enqueue in BFS",
                symptom="Grid BFS or dense graphs enqueue the same vertex dozens of times, triggering Memory Limit Exceeded or timeouts.",
                root_cause_and_fix="Golden rule of BFS: always call visited.add(nb) (or set parent[nb] = curr) right before queue.append(nb), never after popleft(). That guarantees every vertex enters the queue at most once.",
            ),
            PitfallItem(
                title="Pitfall 2: Applying Standard BFS to Graphs with Unequal Positive Edge Weights",
                symptom="When direct edge A -> C costs 100 km (1 hop) while A -> B -> C costs 20 km (2 hops), plain BFS wrongly picks A -> C.",
                root_cause_and_fix="Standard FIFO BFS minimizes hop count, not weighted distance. Whenever edges carry varying non-negative weights, swap the FIFO deque for a Min-Heap priority queue and run Dijkstra's algorithm in O((V + E) log V).",
            ),
            PitfallItem(
                title="Pitfall 3: Hitting Python's RecursionError on Deep Chain Graphs with Recursive DFS",
                symptom="Running recursive dfs() on a linear chain of more than 1,000 nodes raises RecursionError: maximum recursion depth exceeded.",
                root_cause_and_fix="CPython defaults to a call-stack limit of ~1,000 frames (sys.getrecursionlimit()). For large graphs with V > 1,000, rewrite DFS iteratively using an explicit Python list stack, or use iterative BFS.",
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(200, "Number of Islands", "Medium", "2D grid connected components via BFS / DFS flood fill · Time O(M * N)"),
            LeetCodeProblem(994, "Rotting Oranges", "Medium", "Multi-source BFS computing minimum spread minutes · Time O(M * N)"),
            LeetCodeProblem(207, "Course Schedule", "Medium", "Directed cycle detection (Kahn's in-degree BFS / 3-color DFS) · Time O(V + E)"),
            LeetCodeProblem(133, "Clone Graph", "Medium", "Hash map (old -> cloned node) combined with BFS / DFS · Time O(V + E)"),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="Why is BFS time complexity O(V + E) rather than O(V * E)?",
                answer="Because marking vertices visited on enqueue ensures every vertex enters and leaves the queue at most once (O(V) total). When vertex u is dequeued, we scan only its own adjacency list _adj[u] of length deg(u). Summing deg(u) across all vertices equals E in a directed graph (or 2E in an undirected graph), giving O(E) edge inspections and O(V + E) overall.",
            ),
            InterviewFAQ(
                question="Why encapsulate _adj inside a Graph[T] class instead of passing a raw dict[str, list[str]] everywhere?",
                answer="Encapsulation enforces the Single Responsibility Principle and protects graph invariants. Raw dicts force every caller to guard against KeyError on missing vertices, duplicate edges, and forgotten reverse edges in undirected graphs. Graph[T] centralizes those rules in add_vertex/add_edge and returns a defensive copy from neighbors() so external code cannot silently corrupt internal state.",
            ),
            InterviewFAQ(
                question="What is Multi-Source BFS, and why is it vastly faster than running separate single-source BFS calls?",
                answer="When multiple starting points spread simultaneously (like LeetCode #994 Rotting Oranges or #542 01 Matrix), running K independent BFS traversals costs O(K * V * E). Instead, push all K sources into the same deque at distance 0 before starting a single BFS loop; the wavefront reaches every cell at its exact shortest distance to the nearest source in one O(V + E) pass.",
            ),
        ),
    ),
    ChapterSpec(
        id="ch06",
        badge="Ch.06",
        short_title="Dynamic Programming",
        title="Dynamic Programming & Memoization (0/1 Knapsack & LIS)",
        complexity="Climbing Stairs O(n) / O(1) Space · 0/1 Knapsack O(N*W) · LIS O(n log n)",
        summary="Eliminate exponential O(2^n) brute-force recursion with overlapping subproblems, optimal substructure, 1D rolling-array 0/1 Knapsack, and O(n log n) Patience Sorting LIS.",
        concepts=(
            "Two pillars of Dynamic Programming: Overlapping Subproblems and Optimal Substructure. Caching solved subproblems eliminates millions of redundant recursive branches and turns exponential runtimes into polynomial time.",
            "Top-Down Memoization vs. Bottom-Up Tabulation: Top-down decorates recursion with a cache (such as Python's @functools.cache); bottom-up fills a DP table iteratively from base states and unlocks space compression down to O(1) rolling variables or a 1D O(W) array.",
            "Reverse-loop invariant in 1D 0/1 Knapsack: When compressing dp[i][w] into a single 1D array dp[w], the inner capacity loop MUST iterate backwards (capacity -> weight) so dp[cap - w] still reads the previous item's state rather than reusing the current item twice.",
        ),
        file="examples/ch06_dynamic_programming.py",
        lastmod="2026-11-24",
        keywords=(
            "dynamic programming Python",
            "0/1 knapsack Python 1D array",
            "longest increasing subsequence O(n log n)",
            "memoization functools.cache Python",
            "Climbing Stairs O(1) space",
            "LeetCode 300 LIS Python",
            "LeetCode 322 Coin Change",
            "bottom-up vs top-down DP",
        ),
        deep_intro=(
            "Dynamic Programming (DP) intimidates many engineers, yet its core idea is remarkably simple: remember previously computed subproblems so you never solve the same work twice, "
            "and compute states in dependency order from smallest to largest. "
            "Consider Climbing Stairs: reaching step n requires stepping up from either step n-1 or step n-2, giving f(n) = f(n-1) + f(n-2). "
            "Naive recursion recomputes f(20) thousands of times during f(40) in exponential O(2^n) time; keeping just two rolling integers (prev2, prev1) bottom-up solves it in O(n) time and O(1) space. "
            "This chapter extends that mental model to two signature interview problems: space-optimized 1D 0/1 Knapsack and O(n log n) binary-search-accelerated Longest Increasing Subsequence (LIS)."
        ),
        comparison_table=ComparisonTable(
            caption="Dynamic Programming Strategies: Naive Recursion, Memoization, Tabulation, Space Compression & LIS",
            headers=("DP Strategy / Pattern", "Time Complexity", "Space Complexity", "Core Mechanism", "Best Interview & Engineering Fit"),
            rows=(
                ("Naive Recursion", "O(2^n) exponential", "O(n) call stack", "Expands every branch without caching", "Tiny brute-force prototypes (n <= 20) only"),
                ("Top-Down Memoization", "O(states * transition)", "O(states + stack depth)", "Recursion + dict or @functools.cache", "Irregular state graphs, tree DP, interval DP"),
                ("Bottom-Up Tabulation", "O(states * transition)", "O(states)", "Iterative 1D/2D table from base cases", "Zero recursion overhead, immune to RecursionError"),
                ("Space-Optimized Bottom-Up", "O(states * transition)", "O(1) or 1D O(W)", "Keep only prior row / rolling variables", "Senior interview polish: O(1) stairs, O(W) knapsack"),
                ("LIS Patience Sorting", "O(n log n)", "O(n) tails array", "Greedy min tails + bisect_left", "Required for n up to 10^5 where O(n^2) DP times out"),
            ),
        ),
        walkthrough_title="Step-by-Step Trace: 1D Rolling-Array Reverse Loop in 0/1 Knapsack",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1: Initialize 1D DP Array for Capacity = 50",
                state_snapshot="dp = [0, 0, ..., 0] (length 51: max value for capacity 0..50 with 0 items is 0)",
                explanation="Allocate dp of size capacity + 1 where dp[cap] tracks the best achievable value using at most capacity cap. Before considering any items, every slot starts at 0.",
            ),
            WalkthroughStep(
                step_label="Step 2: Process Item 1 (w=10, v=60) Iterating Backwards cap = 50..10",
                state_snapshot="cap = 50..10: dp[cap] = max(dp[cap], dp[cap - 10] + 60) => dp[10..50] = 60",
                explanation="Scanning backwards ensures dp[cap - 10] is still 0 from the prior round, so every capacity >= 10 takes Item 1 at most once (yielding 60, never accidentally 120).",
            ),
            WalkthroughStep(
                step_label="Step 3: Process Item 2 (w=20, v=100) - Take vs. Skip Decision",
                state_snapshot="dp[30..50] = dp[10..30] + 100 = 160 (Items 1+2) | dp[20..29] = 100 | dp[10..19] = 60",
                explanation="For cap >= 30, combining Item 2 with prior dp[cap - 20] = 60 yields 160 > 60. Capacities 20..29 take Item 2 alone for 100.",
            ),
            WalkthroughStep(
                step_label="Step 4: Process Item 3 (w=30, v=120) - Optimal Result dp[50] = 220",
                state_snapshot="cap = 50: max(old dp[50]=160, dp[20] + 120 = 100 + 120 = 220) => dp[50] = 220",
                explanation="At cap = 50, reading prior-round dp[20] = 100 (Item 2 alone) plus Item 3's 120 gives 220 > 160, finding the optimal subset (Items 2 and 3, weight 50, value 220).",
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="Pitfall 1: Iterating Capacity Forward in 1D 0/1 Knapsack Turns It into Unbounded Knapsack",
                symptom="Writing for cap in range(w, capacity + 1): produces inflated totals far exceeding valid 0/1 combinations.",
                root_cause_and_fix="Forward iteration updates dp[10] with Item 1, then immediately reads that freshly updated dp[10] while computing dp[20], counting Item 1 multiple times. Rule of thumb: iterate backwards for 0/1 Knapsack (each item once), and forward only for Unbounded Knapsack (unlimited copies).",
            ),
            PitfallItem(
                title="Pitfall 2: Initializing Minimization DP Tables with 0 Instead of Infinity",
                symptom="In Coin Change (LeetCode #322), initializing all dp slots to 0 causes min() to return 0 for every amount.",
                root_cause_and_fix="Match initialization to your objective: maximization problems like Knapsack start at 0, whereas minimization problems must set dp[0] = 0 and all unreachable states to float('inf') (or amount + 1) so min() only accepts valid transitions.",
            ),
            PitfallItem(
                title="Pitfall 3: Treating the Patience-Sorting tails Array as the Actual LIS Subsequence",
                symptom="Printing tails after length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]) shows elements that did not appear in that original order.",
                root_cause_and_fix="In O(n log n) LIS, tails[k] strictly stores the smallest possible ending value among all increasing subsequences of length k + 1. Overwriting an earlier slot preserves len(tails) == exact LIS length; if you must reconstruct the actual elements, also store predecessor indices and backtrack.",
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(70, "Climbing Stairs", "Easy", "1D linear DP compressed to O(1) rolling variables · Time O(n) / Space O(1)"),
            LeetCodeProblem(198, "House Robber", "Medium", "Take/skip recurrence dp[i] = max(dp[i-1], dp[i-2] + nums[i]) · Time O(n) / Space O(1)"),
            LeetCodeProblem(322, "Coin Change", "Medium", "Unbounded knapsack minimum coins · Time O(amount * len(coins)) / Space O(amount)"),
            LeetCodeProblem(300, "Longest Increasing Subsequence", "Medium", "Greedy minimal tails + bisect_left binary search · Time O(n log n)"),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="What 4-step framework should you follow when solving an unseen DP problem in an interview?",
                answer="Walk the interviewer systematically through four steps: (1) Define the state (exact meaning of dp[i] or dp[i][j]); (2) Derive the recurrence relation (how the current state transitions from smaller subproblems); (3) Establish base cases and sentinel initialization (0 for max, inf for min); (4) Choose iteration order and evaluate space compression from 2D down to 1D or O(1).",
            ),
            InterviewFAQ(
                question="When should you choose Top-Down Memoization over Bottom-Up Tabulation?",
                answer="Top-down recursion with Python's @functools.cache is fastest to write in timed online assessments and skips unreachable states naturally in sparse tree/interval DP. In live engineering interviews, translating that solution into bottom-up tabulation with O(1) or O(W) space optimization eliminates RecursionError risk and demonstrates strong systems polish.",
            ),
            InterviewFAQ(
                question="What is the core intuition behind accelerating LIS from O(n^2) DP to O(n log n)?",
                answer="Suppose you have two length-3 increasing subsequences: [2, 5, 100] and [2, 5, 7]. Keeping the smaller tail (7) strictly dominates 100 because any future number greater than 100 is also greater than 7, plus values like 8 can extend 7. Because the minimal tail for length k+1 is always strictly greater than for length k, the tails array stays sorted, allowing O(log n) binary search (bisect_left) per element.",
            ),
        ),
    ),
    ChapterSpec(
        id="ch07",
        badge="Ch.07",
        short_title="Binary Heaps & Top-K",
        title="Binary Heaps, Priority Queues & Top-K Algorithms (heapq)",
        complexity="Heap Push / Pop O(log n) · Top-K O(n log k) · K-Way Merge O(N log K)",
        summary="Learn complete binary tree array-index math, sift-up and sift-down invariants, a generic MinHeap from scratch, and Python heapq patterns for O(n log k) Top-K and O(N log K) K-way merge.",
        concepts=(
            "Complete binary tree array mapping: A binary heap packs cleanly into a flat dynamic array with zero pointer overhead: parent of index i is (i - 1) // 2, left child is 2 * i + 1, and right child is 2 * i + 2.",
            "Streaming Top-K in O(n log k) time and O(k) space: Finding the 10 largest scores across 100 million events does not require O(n log n) full sorting. Maintain a size-K Min-Heap whose root acts as the Kth-largest gatekeeper; replace it only when a larger item arrives.",
            "K-Way Merge in O(N log K): Merging K sorted streams or linked lists (LeetCode #23) places the current frontier element of each stream into a Min-Heap, popping the global minimum and advancing that single stream in O(log K) per output item.",
        ),
        file="examples/ch07_heap_priority_queue.py",
        lastmod="2026-11-24",
        keywords=(
            "Python binary heap implementation",
            "Python heapq tutorial",
            "Top-K elements O(n log k)",
            "LeetCode 215 Kth Largest",
            "LeetCode 23 Merge k Sorted Lists",
            "sift-up sift-down MinHeap",
            "Python max heap negative trick",
            "Floyd O(n) heapify proof",
        ),
        deep_intro=(
            "OS CPU schedulers, hospital triage queues, A* and Dijkstra pathfinding, and real-time leaderboards cannot use plain FIFO queues; "
            "they need a Priority Queue that always dispatches the highest-priority (minimum or maximum) item next. "
            "An unsorted list inserts in O(1) but scans O(n) to find the minimum; keeping a list fully sorted pays O(n) shifts on every insertion. "
            "A Binary Heap strikes the ideal balance by relaxing full sorted order into the Heap Order Property: every parent is <= both children (Min-Heap) or >= both children (Max-Heap). "
            "The global extremum always sits at index 0 for O(1) peek, while sift-up insertions and sift-down removals walk at most the height of the tree in O(log n) time."
        ),
        comparison_table=ComparisonTable(
            caption="Priority Queue Implementations Compared: Binary Heap vs. Unsorted List vs. Sorted List vs. Full Sort",
            headers=("Operation / Scenario", "Binary Heap (MinHeap / heapq)", "Unsorted Python list", "Maintained Sorted list", "One-Shot sorted()"),
            rows=(
                ("Peek Min / Max", "O(1) - read _data[0] directly", "O(n) - full linear scan", "O(1) - read head or tail", "O(1) after sorting"),
                ("Insert New Item (Push)", "O(log n) - append + _sift_up", "Amortized O(1) - append", "O(n) - bisect O(log n) + shift", "No dynamic streaming"),
                ("Pop Min / Max", "O(log n) - swap tail + _sift_down", "O(n) - scan & shift delete", "Tail O(1) / Head O(n)", "No dynamic re-ordering"),
                ("Build From N Existing Items", "O(n) - Floyd bottom-up heapify", "O(n) - copy only", "O(n log n)", "O(n log n)"),
                ("Top-K Largest of N Items", "Time O(n log k) · Space O(k)", "Not suitable", "Time O(n * k) · Space O(k)", "Time O(n log n) · Space O(n)"),
                ("Merge K Sorted Lists (Total N)", "Time O(N log K) · Space O(K)", "Time O(N * K)", "Time O(N * K)", "Time O(N log N) · Space O(N)"),
            ),
        ),
        walkthrough_title="Step-by-Step Trace: MinHeap Sift-Up / Sift-Down & Size-K Top-3 Gatekeeper",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1: Push [5, 1, 8, 3] into MinHeap - Observe _sift_up Swaps",
                state_snapshot="push(5)->[5] | push(1)->[1, 5] | push(8)->[1, 5, 8] | push(3): 3<5 swap -> [1, 3, 8, 5]",
                explanation="Appending 3 at index 3 checks parent = (3 - 1) // 2 = 1 (value 5). Since 3 < 5 violates min-heap order, swap them; comparing index 1 with root 0 (value 1) satisfies 1 <= 3, stopping the sift-up.",
            ),
            WalkthroughStep(
                step_label="Step 2: Pop Minimum 1 - Move Tail to Root and _sift_down",
                state_snapshot="Pop 1 | Move tail 5 to root -> [5, 3, 8] | Swap 5 with smaller child 3 -> [3, 5, 8]",
                explanation="To preserve complete-tree shape without holes, move the last item (5) into index 0, compare children 3 and 8, and swap 5 downward with the smaller child (3), promoting 3 as the new minimum.",
            ),
            WalkthroughStep(
                step_label="Step 3: Top-3 Largest on [64, 34, 25, 12, 22, 11, 90] - Seed Size-3 Min-Heap",
                state_snapshot="First 3 items enter heap: min_heap = [25, 64, 34] (root 25 is the 3rd-largest gatekeeper)",
                explanation="Finding the K largest elements counter-intuitively uses a Min-Heap! Its root min_heap[0] is the weakest member currently inside the Top-3. Incoming values 12, 22, and 11 all lose to 25 and are discarded in O(1).",
            ),
            WalkthroughStep(
                step_label="Step 4: Incoming 90 Beats Gatekeeper 25 - heapreplace & Sort Descending",
                state_snapshot="90 > 25 => heapreplace(min_heap, 90) => [34, 64, 90] => descending output [90, 64, 34]",
                explanation="When 90 exceeds min_heap[0] (25), heapq.heapreplace evicts 25 and sifts 90 down in a single pass, leaving the exact top 3 elements [90, 64, 34].",
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="Pitfall 1: Using a Max-Heap of Size N for Streaming Top-K Largest",
                symptom="Pushing all N elements into a max-heap and popping K times blows up memory on large data streams.",
                root_cause_and_fix="Remember the inverse rule: find Top-K Largest with a size-K Min-Heap (evicting too-small items), and find Top-K Smallest with a size-K Max-Heap (evicting too-large items). Memory stays strictly bounded at O(k).",
            ),
            PitfallItem(
                title="Pitfall 2: Looking for a Built-In MaxHeap Class in Python's heapq Module",
                symptom="Implementing two-heap streaming median (LeetCode #295) stalls because heapq only provides min-heap functions.",
                root_cause_and_fix="Python's heapq is min-heap only. For numeric max-heaps, push negated values (heapq.heappush(max_heap, -val)) and negate again on pop (-heapq.heappop(max_heap)) so the largest magnitude floats cleanly to index 0.",
            ),
            PitfallItem(
                title="Pitfall 3: Pushing (priority, custom_obj) Tuples Crashes on Priority Ties",
                symptom="Executing heappush(heap, (node.val, node)) in LeetCode #23 raises TypeError: '<' not supported between instances of 'ListNode' and 'ListNode' whenever two nodes share the same val.",
                root_cause_and_fix="Python compares tuples element by element; on a tie in slot 0, it compares slot 1. Insert a unique tie-breaker counter or list index in the middle—(val, list_idx, node)—so ties always resolve before touching the unorderable object.",
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(215, "Kth Largest Element in an Array", "Medium", "Fixed size-K Min-Heap gatekeeper · Time O(n log k) / Space O(k)"),
            LeetCodeProblem(347, "Top K Frequent Elements", "Medium", "Counter frequency map + size-K Min-Heap · Time O(n log k)"),
            LeetCodeProblem(23, "Merge k Sorted Lists", "Hard", "Min-Heap holding (val, list_idx, elem_idx) · Time O(N log K)"),
            LeetCodeProblem(295, "Find Median from Data Stream", "Hard", "Balanced dual heaps (lower Max-Heap + upper Min-Heap) · Push O(log n) / Query O(1)"),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="Why can a Binary Heap live in a flat array with zero pointers while a general BST requires Node objects?",
                answer="A binary heap enforces the Complete Binary Tree shape: every level except possibly the last is completely filled, and the last level packs tightly from left to right with zero gaps. Numbering nodes 0, 1, 2... in level order lets pure arithmetic (left = 2*i + 1, right = 2*i + 2, parent = (i - 1) // 2) jump directly between parents and children. General BSTs can skew arbitrarily, which would waste exponential empty slots in an array.",
            ),
            InterviewFAQ(
                question="Pushing N items individually costs O(n log n)—why does heapq.heapify(arr) build a heap in linear O(n) time?",
                answer="heapify() runs Floyd's bottom-up sift-down algorithm. Half of all nodes (~N/2) are leaves requiring 0 work; ~N/4 nodes sit one level above leaves and sift at most 1 step; ~N/8 nodes sift at most 2 steps; only the single root can sift log2(N) steps. The geometric series sum of (N / 2^(h+1)) * h converges strictly below 2N, proving linear O(n) worst-case runtime.",
            ),
            InterviewFAQ(
                question="Why is heapq.heapreplace(min_heap, num) faster than heappop() followed by heappush() in top_k_largest?",
                answer="Calling heappop() then heappush() performs two full tree-height adjustments: one sift-down followed by one sift-up. Once you already know num > min_heap[0], heapq.heapreplace overwrites index 0 directly and executes a single sift-down pass, cutting constant-factor work in half.",
            ),
        ),
    ),
)
