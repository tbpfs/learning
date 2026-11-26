#!/usr/bin/env python3
"""Mainland China Simplified Chinese (zh-Hans) content pack for learn.ai-purplemaple.com."""

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

UI_ZH_CN: dict[str, Any] = {
    "site_name": "紫枫 Purple Maple Python 编程教学",
    "brand_creator_name": "紫枫 (王紫枫 / Purple Maple)",
    "brand_website_name": "紫枫官方网站｜王紫枫 (Purple Maple)",
    "brand_anchor_portfolio": "王紫枫（紫枫 / Purple Maple）官方作品集（AI 音乐 & 白濑艾莉 Aily）",
    "brand_anchor_portfolio_short": "王紫枫（紫枫 / Purple Maple）官方作品集",
    "brand_anchor_footer": "王紫枫（紫枫 / Purple Maple）",
    "page_title": "从零开始写代码，轻松搞懂数据结构与算法 | 紫枫 (王紫枫 / Purple Maple)",
    "hero_eyebrow": "核心内功系列・数据结构 & 算法 & 面向对象",
    "hero_h1": "从零开始写代码，轻松搞懂数据结构与算法",
    "hero_intro_html": (
        "大家好，我是<strong>紫枫</strong>！无论是在校学生、准备转行后端开发的同学，"
        "还是想夯实底层内功的软件工程师，吃透「数据结构、算法、面向对象」都是告别刷题迷茫最扎实的基本功。"
    ),
    "cta_youtube": "▶ 观看 YouTube 完整教学播放列表",
    "cta_fb_group": "加入编程与 AI 学习问答群（Facebook）",
    "cta_github": "GitHub 开源代码仓库",
    "cta_chapter_github": "查看本章 GitHub 源码",
    "og_image_alt": "紫枫（王紫枫 / @tbpfs1）Python 数据结构与算法互动教学｜原创看板娘白濑艾莉（左红 #fb7185、右蓝 #38bdf8）",
    "index_keywords": (
        "紫枫, 王紫枫, Purple Maple, tbpfs, Python教程, 数据结构, 算法, 单向链表, 栈, 队列, "
        "二分查找, 归并排序, Merge Sort, 哈希表, Hash Table, 二叉搜索树, BST, 图论, BFS, DFS, "
        "动态规划, Dynamic Programming, 二叉堆, Heap, 优先队列, Top-K, 面向对象, OOP"
    ),
    "index_desc_tpl": (
        "紫枫（王紫枫 / Purple Maple / tbpfs）推出的 Python 3.12 数据结构、算法与面向对象系统实战教程，"
        "完整收录 {chapter_titles_short} 可运行代码与实测输出。"
    ),
    "index_og_desc_tpl": "紫枫（王紫枫 / Purple Maple）Python 3.12 数据结构与算法互动教程（{chapter_titles_short}）。",
    "course_name": "从零开始写代码，轻松搞懂数据结构与算法",
    "course_desc_tpl": (
        "紫枫（王紫枫 / Purple Maple）推出的 Python 3.12 数据结构、算法与面向对象实战课程，"
        "涵盖 {chapter_titles_short}。"
    ),
    "index_aeo_capsule": (
        "紫枫（王紫枫 / Purple Maple）Python 3.12 互动教学站（<code>learn.ai-purplemaple.com/zh-cn/</code>）"
        "收录 7 大核心章节（数组与链表、栈和队列、二分查找与归并排序、哈希表与 BST、图论 BFS/DFS 与 OOP、"
        "动态规划、二叉堆与 Top-K），每章均附真实运行输出、复杂度对比表、CPython 底层陷阱与力扣 LeetCode 面试详解，完全免费开源。"
    ),
    "toc_aria": "章节快速导航",
    "chapter_switcher_aria": "全课程章节切换",
    "section_subnav_aria": "本章段落导航",
    "section_subnav_label": "本章快速跳转：",
    "nav_intro": "核心概念与背景导论",
    "nav_video": "YouTube 实战教学视频",
    "nav_comparison": "复杂度与特性对比表",
    "nav_walkthrough": "分步状态拆解",
    "nav_code": "Python 3.12 完整实现",
    "nav_pitfalls": "CPython 底层陷阱",
    "nav_interview": "LeetCode 题号与面试 FAQ",
    "chapter_link_cta": "独立章节深度教程 ↗",
    "concepts_heading": "核心概念与面试重点解析",
    "label_complexity": "时间／空间复杂度：",
    "label_source_path": "源码路径：",
    "code_accordion_summary_tpl": "点击展开／收起 {badge} Python 3.12 完整实现源码与真实运行输出（<code>{file}</code>）",
    "code_toolbar_tpl": "Python 3.12 示例实现（{file}）",
    "copy_btn": "复制代码",
    "output_label_index": "▶ 真实运行验证输出",
    "output_label_chapter": "▶ 真实运行输出验证（Python 3.12 实测结果）",
    "deep_dive_summary_tpl": "{badge} 独立深度教程独家收录内容（点击展开／收起预览）",
    "deep_dive_table_label": "完整结构化对比表：",
    "deep_dive_faq_label": "本章软件工程师面试高频问答预告：",
    "deep_dive_cta_tpl": "阅读 {badge} 完整深度教程（复杂度表 ＋ 分步图解 ＋ 面试详解） →",
    "chapter_title_tpl": "{badge} {title} | 紫枫 (王紫枫 / Purple Maple) Python 教程",
    "chapter_desc_tpl": "紫枫（王紫枫 / Purple Maple）Python 3.12 深度教程：{badge} {title}。{summary}",
    "chapter_keywords_prefix": "紫枫, 王紫枫, Purple Maple, Python 3.12 教程, ",
    "chapter_eyebrow_tpl": "{badge} 独立深度教程・Python 3.12 数据结构与算法实战",
    "back_to_index_label": "← 返回《从零开始写代码，轻松搞懂数据结构与算法》全章节总目录",
    "chapter_intro_heading": "本章背景导论与工程应用场景",
    "chapter_aeo_tpl": (
        "{badge}《{title}》的核心目标是掌握 {summary} 时间／空间复杂度基准为 <code>{complexity}</code>，"
        "并以 Python 3.12 标准库（<code>{file}</code>）提供零依赖可运行验证示例。"
    ),
    "comparison_heading": "时间与空间复杂度暨底层结构对比表",
    "code_section_heading": "Python 3.12 标准库完整示例实现与运行输出",
    "pitfalls_heading": "Python 3.12 底层实现原理与常见实战陷阱",
    "pitfall_symptom_label": "常见错误现象：",
    "pitfall_fix_label": "CPython 底层根因与正确对策：",
    "interview_heading": "LeetCode 经典必刷题号与软件工程师技术面试 FAQ",
    "interview_table_caption_tpl": "{badge} 对应 LeetCode 高频白板题与解题模板",
    "interview_th_num": "题号",
    "interview_th_title": "题目名称",
    "interview_th_diff": "难度",
    "interview_th_pattern": "核心解题模式与复杂度",
    "video_heading_tpl": "本章对应 YouTube 实战教学视频（{views_label}）",
    "video_intro": "建议先观看紫枫配套中文讲解视频建立直观图像记忆，再对照下方复杂度表与 Python 3.12 标准库代码动手实践：",
    "video_main_label": "主讲视频：",
    "video_playlist_cta": "31 集完整算法基础播放列表 ↗",
    "video_related_heading": "本章延伸 YouTube 专题教学视频",
    "video_desc_tpl": "紫枫（王紫枫 / Purple Maple）中文实战教学视频：{badge} {title}。{summary}",
    "tech_article_headline_tpl": "{badge} {title} — Python 3.12 数据结构与算法深度教程",
    "breadcrumb_home_name": "Python 数据结构与算法总目录",
    "resources_heading": "紫枫精选：Python 数据结构与算法官方文档与经典参考书单",
    "resources_note": "说明：以下均为无赞助推广的免费官方文档与国际经典教材参考，配合本站 7 章 Python 3.12 可运行源码同步学习效果更佳。",
    "resources_th_title": "推荐书籍／文档",
    "resources_th_platform": "来源",
    "resources_th_audience": "适用人群",
    "resources_th_highlight": "与本章对应重点",
    "resources_th_action": "前往查看",
    "chapter_resource_aria": "本章延伸官方文档与刷题参考",
    "chapter_resource_note": "延伸参考：结合 Python 3.12 官方文档与对应力扣题单，把本章底层原理转化为面试与工程实战能力。",
    "chapter_resource_cta": "查阅延伸参考 ↗",
    "fb_question": "这篇教程对你有帮助吗？",
    "fb_yes": "✓ 有帮助",
    "fb_no": "待改进",
    "fb_note_placeholder": "选填：哪一段清晰或卡壳？（最多 200 字，不公开）",
    "fb_note_aria": "选填原因（不公开）",
    "fb_note_submit": "提交反馈",
    "fb_ask_summary": "还有编程概念卡壳？匿名提问给紫枫（整理进本章 FAQ）",
    "fb_ask_sub": "为保持阅读版面纯净、杜绝垃圾广告，提问不会直接公开；站长审阅后会将高频问题补充至本章技术 FAQ。",
    "fb_ask_placeholder": "输入你的疑问，例如：为什么这段时间复杂度是 O(log n)…",
    "fb_ask_aria": "匿名提问内容",
    "fb_ask_submit": "提交提问",
    "pager_aria": "上下章节导航",
    "pager_prev_tpl": "← 上一章：{badge} {short}",
    "pager_first": "← 已是第一章",
    "pager_home": "返回全章节总目录",
    "pager_next_tpl": "下一章：{badge} {short} →",
    "pager_last": "已是最后一章 →",
    "study_guide_heading": "软件工程师基本功修炼指南与学习路线图",
    "study_guide_intro": "许多初学者与转行同学在刷力扣（LeetCode）或准备技术面试时，常陷入「背答案却不懂底层原理」的困境。点击下方折叠面板展开三阶段循序渐进路线图：",
    "study_guide_summary": "点击展开／收起：三阶段刷题路线图与学习建议",
    "study_guide_items": (
        (
            "第一阶段（内存模型与线性结构）：",
            '先亲手实现 <a href="ch01.html">Ch.01 的单向链表</a>与 <a href="ch02.html">Ch.02 的栈 / 队列</a>，彻底理解引用与指针操作，以及时间复杂度 <code>O(1)</code> 与 <code>O(n)</code> 的本质差异。',
        ),
        (
            "第二阶段（分治查找、哈希检索、树与图论框架）：",
            '通过 <a href="ch03.html">Ch.03 的二分查找与归并排序（Merge Sort）</a>、<a href="ch04.html">Ch.04 的哈希表（Two Sum）与二叉搜索树（BST）</a>，再到 <a href="ch05.html">Ch.05 的图遍历（BFS / DFS 最短路径）与面向对象封装（OOP）</a>，掌握分治、空间换时间与抽象建模的核心思维。',
        ),
        (
            "第三阶段（进阶动态规划、优先队列与白板题实战）：",
            '深入 <a href="ch06.html">Ch.06 动态规划与记忆化搜索（0/1 背包与 LIS）</a>及 <a href="ch07.html">Ch.07 二叉堆与 Top-K 多路归并算法</a>，结合各章独立教程内的复杂度对比表、CPython 底层陷阱解析与配套教学视频完成实战闭环。',
        ),
    ),
    "privacy_heading": "隐私政策与 Cookie 声明 (Privacy Policy)",
    "privacy_body_html": (
        '本网站（learn.ai-purplemaple.com）使用 Google AdSense 第三方广告服务与 Google Analytics (GA4)／Google Tag Manager 网站流量分析服务。'
        'Google 及其合作伙伴可能使用 Cookie（包含 DART Cookie），根据用户访问本站或其他网站的记录提供个性化广告与匿名流量统计。'
        '您可随时前往 <a href="https://adssettings.google.com/" target="_blank" rel="noopener noreferrer">Google 广告设置页面</a> 停用个性化广告，'
        '或查阅 <a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener noreferrer">Google 广告与隐私政策</a>。'
        '本站代码复制、提问模板复制与随堂互动测验均在浏览器本地执行；读者点击「有帮助／待改进」时，仅通过加密通道发送匿名满意度评分与 HMAC 哈希限流标识，绝不公开展示留言或存储原始 IP。'
    ),
    "footer_blog_label": "紫枫技术与创作日志",
    "footer_github_label": "GitHub 源码",
    "footer_copyright_label": "版权与转载声明",
    "footer_copyright_notice": "© 2026 紫枫出版社（Purple Maple / 王紫枫）. All Rights Reserved. 示例代码采用 MIT 许可；专著正文与原创图解保留著作权（欢迎附原文链接节录引用，禁止全文搬运与未授权商用）。",
    "js_copied": "已复制 ✓",
    "js_err_rate": "今天的次数已用完，明天再来",
    "js_err_short": "请至少输入 5 个字描述你的疑问",
    "js_err_long": "字数请控制在 400 字以内",
    "js_err_generic": "提交失败，请稍后重试",
    "js_fb_thanks": "感谢反馈！欢迎选填一句原因帮助我们完善教程。",
    "js_fb_local_thanks": "感谢反馈！已记录于你的本地浏览器偏好设置。",
    "js_fb_note_ok": "✓ 已收到你的反馈，谢谢！",
    "qa_heading": "读到本章有疑问或实战卡壳？前往紫枫 Facebook 学习问答群讨论",
    "qa_body": "为保持阅读版面纯净、杜绝垃圾广告，本章所有技术提问、排错求助与代码交流统一集中于官方 Facebook 学习问答群。点击下方按钮可先一键复制标准提问模板，再到群组发帖，方便紫枫与社区伙伴快速帮你定位问题！",
    "qa_copy_btn": "一键复制提问模板",
    "qa_copy_done": "已复制提问模板 ✓",
    "qa_primary_cta": "前往 Facebook 学习群提问 ↗",
    "qa_template_tpl": "【紫枫出版社提问】{chapter_label}\n- 参考页面：{page_url}\n- 遇到的现象／报错信息：\n- 我已尝试过的方法：",
    "press_section_heading": "紫枫出版社（Purple Maple Press）技术专著书架",
    "press_section_intro": "对标欧莱礼（O'Reilly）与 MIT Press 教科书标准打造的免费开源技术专著系列：每章均附真实运行的 Python 3.12 零依赖源码、原生架构图解、生产环境避坑指南与互动测验。",
    "book_status_serializing": "连载中（已上线 {pub}/{total} 章）",
    "book_status_complete": "全书完结（共 7 章）",
    "book_cta_open": "翻开专著目录 →",
    "book_cta_start_ch01": "从 Ch.01 开始读",
    "book_cta_read_dsa": "前往下方 7 章完整目录 ↓",
    "dsa_book_title": "Python 3.12 数据结构与算法精解",
    "dsa_book_desc": "涵盖数组与链表、栈与队列、二分查找与归并排序、哈希表与 BST、图论 BFS/DFS、动态规划与二叉堆 Top-K，结合 31 集实战讲解视频与力扣 LeetCode 高频白板题。",
    "dsa_cover_alt": "紫枫出版社《Python 3.12 数据结构与算法精解》典藏书封插画：白濑艾莉（Aily）解析树与算法图谱（左眼绯红 #fb7185、右眼苍蓝 #38bdf8）",
    "book_back_to_shelf": "← 返回紫枫出版社总书架",
    "book_back_to_toc": "← 返回《{book_title}》全书目录",
    "book_toc_heading": "全书章节目录（4 大篇 × 10 章）",
    "book_sidebar_summary": "全书章节目录（点击展开／收起）",
    "book_coming_soon": "撰写中",
    "book_published_badge": "已上线",
    "book_reading_time_tpl": "预计精读时间：约 {mins} 分钟",
    "book_audience_label": "适用读者：",
    "book_objectives_heading": "读完本章你将彻底掌握",
    "book_diagram_heading": "核心系统架构与数据流图解",
    "book_walkthrough_heading": "关键源码设计拆解",
    "book_pitfalls_heading": "生产环境实战避坑与防御对策",
    "book_pitfall_symptom_label": "线上故障现象：",
    "book_pitfall_fix_label": "底层根因与工程对策：",
    "book_quiz_heading": "随堂互动测验（即时检验概念）",
    "book_quiz_intro": "点选选项即可在本地浏览器即时核对答案并查看深度解析，不上传任何个人数据。",
    "book_quiz_correct": "✓ 回答正确！",
    "book_quiz_wrong": "✗ 再想一下 — ",
    "book_faq_heading": "AI 工程师技术面试高频问答（FAQ）",
    "book_further_heading": "延伸阅读与官方原始论文／文档",
    "book_pager_home": "返回本书目录",
    "book_nav_objectives": "学习目标",
    "book_nav_diagram": "架构图解",
    "book_nav_comparison": "方案对比表",
    "book_nav_code": "Python 源码",
    "book_nav_pitfalls": "生产避坑",
    "book_nav_quiz": "随堂测验",
    "book_nav_faq": "面试 FAQ",
}

YOUTUBE_ZH_CN: dict[str, dict[str, Any]] = {
    "ch01": {
        "video_id": "-LmHUlozTqE",
        "title": "轻松搞懂数据结构：数组 (Array) 与单向链表 (Linked List) 底层原理解析",
        "upload_date": "2020-09-12T12:00:00+08:00",
        "views_label": "67,700+ 次播放",
        "related": [
            ("ov_WvWbEryg", "【零基础生活图解】用操场龟兔赛跑 3 分钟看懂链表环检测 (LeetCode #141)"),
            ("2aSyeVdwATA", "【动态图解】单向链表原地反转 (LeetCode #206) 三指针移动演示"),
            ("7xBrPbmOsSs", "轻松搞懂数据结构全景总览（28,200+ 播放）"),
            ("RObLhJlg2O8", "编程基础语法：变量、数据类型、运算符与数组"),
        ],
    },
    "ch02": {
        "video_id": "0Kiunabmm0w",
        "title": "轻松搞懂数据结构：栈 (Stack) 与队列 (Queue) 核心模型精讲",
        "upload_date": "2020-09-13T12:00:00+08:00",
        "views_label": "35,500+ 次播放",
        "related": [
            ("qys8Cs7J0wE", "【零基础生活图解】3 分钟看懂栈 Stack 与括号匹配 (LeetCode #20)"),
            ("JSKtJqj2pwc", "轻松搞懂数据结构：队列 Queue 详解（23,900+ 播放）"),
            ("hWrZPqJZXyg", "函数专题整理：基础、重载与递归调用栈"),
        ],
    },
    "ch03": {
        "video_id": "DVDoyB5qDC4",
        "title": "轻松搞懂算法：快速排序、归并排序与查找排序复杂度分析",
        "upload_date": "2020-09-23T12:00:00+08:00",
        "views_label": "23,800+ 次播放",
        "related": [
            ("3B4dXDxk_ck", "【动态图解】30 秒彻底搞懂归并排序 Merge Sort 分治法 O(n log n)"),
            ("C9Xes8wH6Co", "轻松搞懂算法：归并排序 Merge Sort 详解（20,500+ 播放）"),
            ("iwCUOKhIhAA", "算法概论与大 O 时间复杂度入门（19,100+ 播放）"),
            ("zO8kaBEy0M4", "冒泡排序、选择排序与插入排序详解（18,100+ 播放）"),
            ("llSvc4rwxi0", "查找算法：二分查找 Binary Search（13,300+ 播放）"),
        ],
    },
    "ch04": {
        "video_id": "xDwFMffqLbw",
        "title": "轻松搞懂数据结构：树 (Tree) 与哈希表 (Hash Table) 底层剖析",
        "upload_date": "2020-09-16T12:00:00+08:00",
        "views_label": "41,900+ 次播放",
        "related": [
            ("rr322eEWAUo", "【动态图解】哈希表 Hash Table ＋ LeetCode #1 两数之和从 O(n²) 降到 O(n)"),
            ("vPvxEDyxI2w", "轻松搞懂数据结构：哈希表 Hash Table（28,000+ 播放）"),
            ("gA815MIEFg0", "轻松搞懂数据结构：集合 Set 与映射 Map（18,900+ 播放）"),
        ],
    },
    "ch05": {
        "video_id": "c4R27mPT5kY",
        "title": "轻松搞懂算法：深度优先搜索 (DFS) 与广度优先搜索 (BFS) 图遍历实战",
        "upload_date": "2020-09-27T12:00:00+08:00",
        "views_label": "22,600+ 次播放",
        "related": [
            ("ebkBxAvyFds", "【零基础生活图解】水波扩散与迷宫探险 3 分钟看懂 BFS / DFS 与岛屿数量 (LeetCode #200)"),
            ("V_ajcNni6wk", "计算机专业核心课：数据结构、算法与面向对象（22,600+ 播放）"),
            ("5hYwLTVK4pY", "常见数据结构复杂度 Big-O 汇总（15,000+ 播放）"),
        ],
    },
    "ch06": {
        "video_id": "M2kYdAA-FHY",
        "title": "轻松搞懂算法：动态规划 (Dynamic Programming) 状态转移入门",
        "upload_date": "2020-09-29T12:00:00+08:00",
        "views_label": "31,700+ 次播放",
        "related": [
            ("WhoRHltIukc", "【零基础生活图解】3 分钟看懂动态规划 DP 与零钱兑换 (LeetCode #322)"),
            ("iLK48YAXjio", "常用算法策略：暴力法、贪心法、分治法、回溯法与分支限界（26,800+ 播放）"),
        ],
    },
    "ch07": {
        "video_id": "klbGg8dmYTM",
        "title": "轻松搞懂数据结构：二叉堆 (Heap) 与优先队列原理精讲",
        "upload_date": "2020-09-17T12:00:00+08:00",
        "views_label": "26,800+ 次播放",
        "related": [
            ("sFypmieNopU", "【零基础生活图解】3 分钟看懂堆 Heap 与 Top-K 筛选 (LeetCode #215)"),
            ("fHBw99bYLuo", "堆排序 (Heap Sort)、基数排序与桶排序详解（13,200+ 播放）"),
        ],
    },
}

RESOURCES_ZH_CN: tuple[AffiliateResource, ...] = (
    AffiliateResource(
        partner_id="py312_docs_zhcn",
        title="Python 3.12 官方简体中文文档（数据结构与标准库）",
        partner_label="Python.org 官方",
        audience="所有 Python 开发者／查阅标准库细节",
        highlight="权威说明 list、collections.deque、dict、bisect 与 heapq 底层复杂度与接口规范",
        url="https://docs.python.org/zh-cn/3.12/tutorial/datastructures.html",
        cta_label="阅读官方文档 ↗",
        is_sponsored=False,
    ),
    AffiliateResource(
        partner_id="py_wiki_complexity",
        title="Python Wiki：官方内置容器时间复杂度速查表",
        partner_label="Python Wiki",
        audience="算法面试／性能调优工程师",
        highlight="逐项列出 CPython list、deque、set、dict 各项操作的平均与最坏时间复杂度",
        url="https://wiki.python.org/moin/TimeComplexity",
        cta_label="查看复杂度表 ↗",
        is_sponsored=False,
    ),
    AffiliateResource(
        partner_id="grokking_algo_ref",
        title="《算法图解》（Grokking Algorithms 第二版・经典入门参考）",
        partner_label="经典技术书目",
        audience="零基础入门／偏好图解直观理解者",
        highlight="以全彩插图串联二分查找、哈希表、BFS/DFS 与动态规划，完美呼应 Ch.01–Ch.06",
        url="https://www.manning.com/books/grokking-algorithms-second-edition",
        cta_label="查看书目详情 ↗",
        is_sponsored=False,
    ),
    AffiliateResource(
        partner_id="fluent_python_ref",
        title="《流畅的 Python》（Fluent Python 第二版・进阶必读）",
        partner_label="O'Reilly 经典",
        audience="中高级工程师／深挖 CPython 底层",
        highlight="深入剖析序列内存布局、哈希表开放寻址与数据模型，衔接各章 CPython 底层陷阱",
        url="https://www.fluentpython.com/",
        cta_label="查看官方站点 ↗",
        is_sponsored=False,
    ),
)

CHAPTER_RESOURCES_ZH_CN: dict[str, tuple[str, str]] = {
    "ch01": (
        "延伸参考：Python 3.12 官方文档 — 列表 list 与数据结构内存模型详解",
        "https://docs.python.org/zh-cn/3.12/tutorial/datastructures.html",
    ),
    "ch02": (
        "延伸参考：Python 3.12 官方文档 — collections.deque 双端队列规范",
        "https://docs.python.org/zh-cn/3.12/library/collections.html#collections.deque",
    ),
    "ch03": (
        "延伸参考：Python 3.12 官方文档 — bisect 二分查找模块与 Timsort 排序指南",
        "https://docs.python.org/zh-cn/3.12/library/bisect.html",
    ),
    "ch04": (
        "延伸参考：Python 3.12 官方文档 — 映射类型 dict 哈希表与时间复杂度参考",
        "https://docs.python.org/zh-cn/3.12/library/stdtypes.html#mapping-types-dict",
    ),
    "ch05": (
        "延伸参考：Python 3.12 官方文档 — 类、泛型 typing.Generic 与面向对象封装",
        "https://docs.python.org/zh-cn/3.12/library/typing.html#generics",
    ),
    "ch06": (
        "延伸参考：Python 3.12 官方文档 — functools.cache 记忆化装饰器与递归优化",
        "https://docs.python.org/zh-cn/3.12/library/functools.html#functools.cache",
    ),
    "ch07": (
        "延伸参考：Python 3.12 官方文档 — heapq 最小堆队列算法与 Top-K 实战",
        "https://docs.python.org/zh-cn/3.12/library/heapq.html",
    ),
}

CODE_REPLACEMENTS_ZH_CN: dict[str, tuple[tuple[str, str], ...]] = {
    "ch01": (
        ("Ch.01 陣列與單向鏈結串列（Array & Singly Linked List）", "Ch.01 数组与单向链表（Array & Singly Linked List）"),
        ("展示基礎節點（ListNode）與單向鏈結串列（SinglyLinkedList）的插入、刪除、搜尋與反轉操作。", "演示基础节点（ListNode）与单向链表（SinglyLinkedList）的插入、删除、查找与反转操作。"),
        ("教學用單向鏈結串列實作（支援頭尾插入、指定值刪除、搜尋與原地反轉）。", "教学用单向链表实现（支持头尾插入、按值删除、查找与原地反转）。"),
        ("在串列頭部插入新節點，時間複雜度 O(1)。", "在链表头部插入新节点，时间复杂度 O(1)。"),
        ("在串列尾部附加新節點，時間複雜度 O(n)。", "在链表尾部追加新节点，时间复杂度 O(n)。"),
        ("搜尋目標值首次出現的索引（0-based），若不存在回傳 -1。", "查找目标值首次出现的下标（从 0 开始），若不存在返回 -1。"),
        ("刪除首次出現的目標值節點，成功回傳 True，不存在回傳 False。", "删除首次出现的目标值节点，成功返回 True，不存在返回 False。"),
        ("原地（in-place）反轉鏈結串列，時間複雜度 O(n)，空間複雜度 O(1)。", "原地（in-place）反转单向链表，时间复杂度 O(n)，空间复杂度 O(1)。"),
        ("Ch.01 SinglyLinkedList 範例結果:", "Ch.01 SinglyLinkedList 运行结果:"),
    ),
    "ch02": (
        ("Ch.02 堆疊與佇列（Stack & Queue）", "Ch.02 栈与队列（Stack & Queue）"),
        ("展示 LIFO 堆疊（含經典括號平衡檢查）與 FIFO 佇列的物件導向封裝實作。", "演示 LIFO 栈（含经典括号匹配校验）与 FIFO 队列的面向对象封装实现。"),
        ("後進先出（LIFO）堆疊。", "后进先出（LIFO）栈。"),
        ("先進先出（FIFO）佇列。", "先进先出（FIFO）队列。"),
        ("利用 Stack 檢查字串中的 (), [], {} 括號是否成對且順序正確。", "利用栈检查字符串中的 (), [], {} 括号是否成对且嵌套顺序正确。"),
        ("Ch.02 括號平衡檢查 '{[()]}':", "Ch.02 括号匹配校验 '{[()]}':"),
    ),
    "ch03": (
        ("Ch.03 搜尋與排序演算法（Search & Sort Algorithms）", "Ch.03 查找与排序算法（Search & Sort Algorithms）"),
        ("展示二分搜尋法（Binary Search）與合併排序法（Merge Sort）。", "演示二分查找（Binary Search）与归并排序（Merge Sort）。"),
        ("在已排序遞增序列中搜尋 target，回傳索引（0-based）；若不存在則回傳 -1。", "在有序递增序列中查找 target，返回下标（从 0 开始）；若不存在则返回 -1。"),
        ("使用分治法（Divide & Conquer）實作穩定合併排序，時間複雜度 O(n log n)。", "使用分治法（Divide & Conquer）实现稳定归并排序，时间复杂度 O(n log n)。"),
        ("Ch.03 Merge Sort 結果:", "Ch.03 Merge Sort 结果:"),
        ("| 27 的索引:", "| 27 的下标:"),
    ),
    "ch04": (
        ("Ch.04 雜湊表與二元搜尋樹（Hash Table & Binary Search Tree）", "Ch.04 哈希表与二叉搜索树（Hash Table & Binary Search Tree）"),
        ("展示鏈結法雜湊表（Chaining Hash Table）、LeetCode #1 Two Sum O(n) 解法與二元搜尋樹中序走訪（In-order Traversal）。", "演示拉链法哈希表（Chaining Hash Table）、LeetCode #1 两数之和 O(n) 解法与二叉搜索树中序遍历（In-order Traversal）。"),
        ("以鏈結法（Separate Chaining）處理雜湊碰撞的雜湊表實作，平均讀寫複雜度 O(1)。", "以拉链法（Separate Chaining）解决哈希冲突的哈希表实现，平均读写复杂度 O(1)。"),
        ("bucket_count 必須為正整數", "bucket_count 必须为正整数"),
        ("經典面試題 Two Sum：利用雜湊表在 O(n) 時間內找出兩數之和等於 target 的索引配對。", "经典面试题两数之和：利用哈希表在 O(n) 时间内找出两数之和等于 target 的下标配对。"),
        ("二元搜尋樹（BST）：左子樹所有鍵值 < 根節點 < 右子樹所有鍵值，中序走訪必為遞增排序序列。", "二叉搜索树（BST）：左子树所有键值 < 根节点 < 右子树所有键值，中序遍历必为递增有序序列。"),
        ("Ch.04 Two Sum 索引:", "Ch.04 两数之和下标:"),
        ("| BST 中序走訪:", "| BST 中序遍历:"),
        ("| 搜尋 60:", "| 查找 60:"),
    ),
    "ch05": (
        ("Ch.05 圖論走訪與物件導向設計（Graph BFS / DFS & Object-Oriented Programming）", "Ch.05 图论遍历与面向对象设计（Graph BFS / DFS & Object-Oriented Programming）"),
        ("展示鄰接串列（Adjacency List）物件導向封裝、廣度優先搜尋（BFS）、深度優先搜尋（DFS）與無權重圖最短路徑。", "演示邻接表（Adjacency List）面向对象封装、广度优先搜索（BFS）、深度优先搜索（DFS）与无权图最短路径。"),
        ("以鄰接串列（Adjacency List）封裝之泛型圖論結構，時間複雜度 O(V + E)。", "基于邻接表（Adjacency List）封装的泛型图结构，时间复杂度 O(V + E)。"),
        ("廣度優先搜尋（Breadth-First Search）：利用佇列（Queue）由近而遠逐層擴散走訪，複雜度 O(V + E)。", "广度优先搜索（Breadth-First Search）：利用队列由近及远逐层扩散遍历，复杂度 O(V + E)。"),
        ("深度優先搜尋（Depth-First Search）：一條路走到底再回溯（Backtracking），複雜度 O(V + E)。", "深度优先搜索（Depth-First Search）：一条路走到底再回溯（Backtracking），复杂度 O(V + E)。"),
        ("利用 BFS 找出無權重圖中從 start 到 goal 的最少步數最短路徑。", "利用 BFS 找出无权图中从 start 到 goal 的最少步数最短路径。"),
        ("Ch.05 BFS 走訪:", "Ch.05 BFS 遍历:"),
        ("| DFS 走訪:", "| DFS 遍历:"),
        ("| A->F 最短路徑:", "| A->F 最短路径:"),
    ),
    "ch06": (
        ("Ch.06 動態規劃與記憶化搜尋（Dynamic Programming & Memoization）", "Ch.06 动态规划与记忆化搜索（Dynamic Programming & Memoization）"),
        ("展示爬樓梯狀態壓縮 O(1) 空間解法、0/1 背包問題（一維滾動陣列）與最長嚴格遞增子序列（LIS O(n log n)）。", "演示爬楼梯状态压缩 O(1) 空间解法、0/1 背包问题（一维滚动数组）与最长严格递增子序列（LIS O(n log n)）。"),
        ("計算爬到第 n 階樓梯的方法數（每次可跨 1 或 2 階）。", "计算爬到第 n 阶楼梯的方法数（每次可跨 1 或 2 阶）。"),
        ("採用自底向上（Bottom-Up）滾動變數狀態壓縮：", "采用自底向上（Bottom-Up）滚动变量状态压缩："),
        ("- 時間複雜度：O(n)", "- 时间复杂度：O(n)"),
        ("- 空間複雜度：O(1)", "- 空间复杂度：O(1)"),
        ("階數 n 必須為非負整數", "阶数 n 必须为非负整数"),
        ("經典 0/1 背包問題：在背包容量上限 capacity 內，每件物品最多選一次，求最大總價值。", "经典 0/1 背包问题：在背包容量上限 capacity 内，每件物品最多选一次，求最大总价值。"),
        ("採用一維滾動陣列並由後往前（capacity -> weight）逆序更新，避免同一物品被重複選取：", "采用一维滚动数组并由后往前（capacity -> weight）逆序更新，避免同一物品被重复选取："),
        ("- 時間複雜度：O(N * W)，其中 N 為物品數、W 為 capacity", "- 时间复杂度：O(N * W)，其中 N 为物品数、W 为 capacity"),
        ("- 空間複雜度：O(W)", "- 空间复杂度：O(W)"),
        ("capacity 必須為非負整數", "capacity 必须为非负整数"),
        ("weights 與 values 長度必須一致", "weights 与 values 长度必须一致"),
        ("物品重量不可為負數", "物品重量不可为负数"),
        ("最長嚴格遞增子序列（Longest Increasing Subsequence, LeetCode #300）。", "最长严格递增子序列（Longest Increasing Subsequence, LeetCode #300）。"),
        ("結合貪婪策略與二分搜尋（Patience Sorting）維護最小結尾陣列 tails：", "结合贪心策略与二分查找（Patience Sorting）维护最小结尾数组 tails："),
        ("- 時間複雜度：O(n log n)", "- 时间复杂度：O(n log n)"),
        ("- 空間複雜度：O(n)", "- 空间复杂度：O(n)"),
        ("Ch.06 DP 爬樓梯(n=10):", "Ch.06 DP 爬楼梯(n=10):"),
        ("0/1 背包最大價值:", "0/1 背包最大价值:"),
        ("LIS 長度:", "LIS 长度:"),
    ),
    "ch07": (
        ("Ch.07 堆積、優先佇列與 Top-K 演算法（Heap, Priority Queue & Top-K Elements）", "Ch.07 二叉堆、优先队列与 Top-K 算法（Heap, Priority Queue & Top-K Elements）"),
        ("展示手寫泛型最小二元堆積（MinHeap）、Top-K 最大元素篩選與合併 K 個已排序序列。", "演示手写泛型最小二叉堆（MinHeap）、Top-K 最大元素筛选与合并 K 个有序序列。"),
        ("以動態陣列封裝之最小二元堆積（Binary Min-Heap），支援 O(log n) 插入與彈出最小值。", "基于动态数组封装的最小二叉堆（Binary Min-Heap），支持 O(log n) 插入与弹出最小值。"),
        ("查看堆頂最小元素，時間複雜度 O(1)。", "查看堆顶最小元素，时间复杂度 O(1)。"),
        ("插入新元素並執行上浮（Sift-Up）維護堆積性質，時間複雜度 O(log n)。", "插入新元素并执行上浮（Sift-Up）维护堆序性质，时间复杂度 O(log n)。"),
        ("彈出並回傳堆頂最小元素，將尾端元素移至堆頂後執行下沉（Sift-Down），時間複雜度 O(log n)。", "弹出并返回堆顶最小元素，将尾部元素移至堆顶后执行下沉（Sift-Down），时间复杂度 O(log n)。"),
        ("利用大小固定為 k 的最小堆積，在 O(n log k) 時間與 O(k) 空間內找出前 k 大元素（由大到小回傳）。", "利用大小固定为 k 的最小堆，在 O(n log k) 时间与 O(k) 空间内找出前 k 大元素（按降序返回）。"),
        ("利用最小堆積在 O(N log K) 時間內合併 K 個已排序遞增序列（LeetCode #23 核心邏輯）。", "利用最小堆在 O(N log K) 时间内合并 K 个升序有序序列（LeetCode #23 核心逻辑）。"),
        ("Ch.07 MinHeap 依序彈出:", "Ch.07 MinHeap 依次弹出:"),
        ("Top-3 最大元素:", "Top-3 最大元素:"),
        ("合併 K 串列:", "合并 K 个有序列表:"),
    ),
}

OUTPUT_REPLACEMENTS_ZH_CN: dict[str, tuple[tuple[str, str], ...]] = {
    "ch01": (("Ch.01 SinglyLinkedList 範例結果:", "Ch.01 SinglyLinkedList 运行结果:"),),
    "ch02": (("Ch.02 括號平衡檢查 '{[()]}':", "Ch.02 括号匹配校验 '{[()]}':"),),
    "ch03": (
        ("Ch.03 Merge Sort 結果:", "Ch.03 Merge Sort 结果:"),
        ("| 27 的索引:", "| 27 的下标:"),
    ),
    "ch04": (
        ("Ch.04 Two Sum 索引:", "Ch.04 两数之和下标:"),
        ("| BST 中序走訪:", "| BST 中序遍历:"),
        ("| 搜尋 60:", "| 查找 60:"),
    ),
    "ch05": (
        ("Ch.05 BFS 走訪:", "Ch.05 BFS 遍历:"),
        ("| DFS 走訪:", "| DFS 遍历:"),
        ("| A->F 最短路徑:", "| A->F 最短路径:"),
    ),
    "ch06": (
        ("Ch.06 DP 爬樓梯(n=10):", "Ch.06 DP 爬楼梯(n=10):"),
        ("0/1 背包最大價值:", "0/1 背包最大价值:"),
        ("LIS 長度:", "LIS 长度:"),
    ),
    "ch07": (
        ("Ch.07 MinHeap 依序彈出:", "Ch.07 MinHeap 依次弹出:"),
        ("合併 K 串列:", "合并 K 个有序列表:"),
    ),
}

CHAPTERS_ZH_CN: tuple[ChapterSpec, ...] = (
    ChapterSpec(
        id="ch01",
        badge="Ch.01",
        short_title="Python 数组与单向链表",
        title="Python 数组（list）与单向链表（Array & Singly Linked List）",
        complexity="头部插入 O(1) ・ 尾部追加 / 查找 / 删除 / 原地反转 O(n)",
        summary="完整解析 Python 数组（list 动态数组）与单向链表（Linked List）的连续内存布局、下标 O(1) 随机访问与指针串联差异，附 Python 3.12 泛型实现与 O(1) 空间原地反转。",
        concepts=(
            "连续内存 vs. 指针串联：数组（Array / Python list）依托连续内存块实现 O(1) 下标随机访问，但在头部或中间插入元素需搬移后续元素（O(n)）；单向链表（Singly Linked List）通过节点 Node 与 next 引用动态串联，已知头节点时可在 O(1) 时间内完成头部插入（prepend）。",
            "白板题必考「原地反转（In-place Reverse）」：借助 prev、curr、nxt 三个指针迭代翻转 next 指向，无需额外开辟新链表，额外空间复杂度严格控制在 O(1)，是软件工程师算法面试出场率最高的基础题型。",
            "CPU 缓存亲和性（Cache Locality）：现代处理器读取内存时会按整条缓存行（Cache Line，通常 64 字节）预加载。连续排布的数组能充分受益于空间局部性；而链表节点分散在堆内存中，频繁解引用容易触发缓存未命中（Cache Miss）。",
        ),
        file="examples/ch01_array_linked_list.py",
        lastmod="2026-11-24",
        keywords=(
            "Python 数组",
            "Python list",
            "Python 单向链表",
            "Singly Linked List",
            "反转链表",
            "Reverse Linked List",
            "Python list 底层原理",
            "数组与链表对比",
            "LeetCode 206",
            "双指针算法",
        ),
        deep_intro=(
            "在学习任何进阶算法之前，软件工程师都必须先建立清晰的「内存物理模型」。"
            "计算机内存可以抽象为一排编号连续的储物柜：数组（Array）要求一次性申请连续 N 个槽位，"
            "因此只要知道起始基址（Base Address）与单个元素宽度，CPU 就能用一次乘法和加法在 O(1) 常数时间内直接定位第 i 个元素；"
            "但一旦要在数组最前方插入新数据，就必须把后面所有元素整体向后挪动一格，带来 O(n) 的搬移开销。"
            "与之相对，单向链表（Singly Linked List）不要求连续物理空间，每个节点（ListNode）除保存数据值 val 外，"
            "还维护指向下一个节点地址的引用指针 next。这种设计让「头部插入与头部删除」只需改写引用即可在 O(1) 内完成，"
            "也是后续实现拉链法哈希表桶位、LRU 缓存（搭配双向链表）与图论邻接表的底层基石。"
        ),
        comparison_table=ComparisonTable(
            caption="数组（Python list 动态数组）、单向链表与双向链表操作复杂度对比表",
            headers=("操作项目 ／ 结构特性", "Python list（动态数组）", "单向链表（Singly Linked List）", "双向链表（Doubly Linked List）"),
            rows=(
                ("按下标随机读取 (Index Access)", "O(1) — 基址加偏移量直接定位", "O(n) — 需从 head 顺序遍历", "O(n) — 需从头或尾顺序遍历"),
                ("头部插入 ／ 删除 (Prepend / Pop Head)", "O(n) — 需搬移后续全部元素指针", "O(1) — 仅更新 head 引用指向", "O(1) — 更新 head 与 prev 指针"),
                ("尾部追加 (Append at Tail)", "均摊 O(1) — 满载扩容时为 O(n)", "无 tail 指针 O(n) ／ 有 tail 指针 O(1)", "O(1) — 直接通过 tail 指针串联"),
                ("按值查找 (Search by Value)", "O(n) — 线性扫描（有序可二分 O(log n)）", "O(n) — 仅支持单向线性遍历", "O(n) — 线性遍历"),
                ("已知节点删除自身 (Delete Given Node)", "O(n) — 需搬移后续元素填补空缺", "O(n) — 需先从头定位前驱节点 prev", "O(1) — 直接拼接 prev 与 next"),
                ("CPU 缓存亲和性与额外内存", "高（连续指针数组，空间局部性佳）", "低（每节点含 next 引用与对象头）", "低（每节点含 prev 与 next 双引用）"),
            ),
        ),
        walkthrough_title="原地反转单向链表（In-place Reverse）三指针分步状态追踪",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1：初始状态与指针配置（链表 5 -> 10 -> 30 -> None）",
                state_snapshot="prev = None | curr = Node(5) | head = Node(5)",
                explanation="在进入 while curr is not None 循环前，将前驱指针 prev 初始化为 None（因为原头节点 Node(5) 反转后会成为新的尾节点，其 next 必须指向 None），当前指针 curr 则指向 head。",
            ),
            WalkthroughStep(
                step_label="Step 2：第一轮迭代 — 暂存后继节点并翻转 Node(5) 指针",
                state_snapshot="nxt = Node(10) | Node(5).next = None | prev = Node(5) | curr = Node(10)",
                explanation="最关键的第一步是先用 nxt = curr.next 备份 Node(10) 的引用，否则一旦执行 curr.next = prev 将 Node(5) 指向 None，后续整条链表就会彻底断链丢失。随后同步将 prev 与 curr 向前推进一步。",
            ),
            WalkthroughStep(
                step_label="Step 3：第二轮迭代 — 翻转中间节点 Node(10) 指向 Node(5)",
                state_snapshot="nxt = Node(30) | Node(10).next = Node(5) | prev = Node(10) | curr = Node(30)",
                explanation="先记录 nxt = Node(30)，再将 Node(10).next 改指回 prev（即 Node(5)），形成局部反转链 10 -> 5 -> None。随后 prev 推进至 Node(10)，curr 推进至尾节点 Node(30)。",
            ),
            WalkthroughStep(
                step_label="Step 4：第三轮迭代与收尾 — 完成反转并更新 self.head",
                state_snapshot="nxt = None | Node(30).next = Node(10) | prev = Node(30) | curr = None => self.head = prev",
                explanation="将 Node(30).next 指向 Node(10)，此时 curr 推进至 nxt（即 None）退出循环。最后务必执行 self.head = prev，将链表头指针正式更新为 Node(30)，完成 30 -> 10 -> 5 -> None 的 O(1) 空间原地反转。",
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="陷阱一：反转或删除节点时未先备份 curr.next 导致「断链（Lost Reference）」",
                symptom="在手写 reverse() 时若先写 curr.next = prev 再写 curr = curr.next，循环结束后只剩单个节点，其余节点全部丢失。",
                root_cause_and_fix="一旦覆写 curr.next，原本通往后继节点的唯一引用就被清空了。标准安全顺序永远是：1. 先备份 nxt = curr.next → 2. 修改指向 curr.next = prev → 3. 推进 prev = curr → 4. 推进 curr = nxt。",
            ),
            PitfallItem(
                title="陷阱二：忽略删除头节点（head）或空链表的边界条件（Edge Cases）",
                symptom="实现 remove(target) 时直接执行 prev.next = curr.next，当待删目标正好是首节点（head）时抛出 AttributeError: 'NoneType' object has no attribute 'next'。",
                root_cause_and_fix="当目标位于头节点时 prev 为 None，必须特判 self.head = curr.next；算法面试中更推荐引入「虚拟头节点（Dummy Head Node, dummy = ListNode(0, head)）」，让包含原 head 在内的全部真实节点都拥有前驱节点，大幅简化分支。",
            ),
            PitfallItem(
                title="陷阱三：误以为在 Python 中手写 SinglyLinkedList 比内置 list 更省内存",
                symptom="为了省内存把几十万条整数改存进自定义 Python ListNode 类，结果内存占用反而暴涨数倍且遍历速度明显下降。",
                root_cause_and_fix="CPython 3.12 内置 list 底层是 C 语言连续的 PyObject* 指针数组（每项仅占 8 字节指针外加少量预留槽位）；而每个自定义 Python ListNode 实例都带有完整对象头与属性结构（即便启用 __slots__ 也远大于 8 字节）。工程实战中除非需要高频双端增删（应选 collections.deque）或教学演练，否则一律优先选用内置 list。",
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(206, "Reverse Linked List（反转单向链表）", "Easy", "三指针原地迭代反转 ／ 递归反转 ・ 时间 O(n) / 空间 O(1)"),
            LeetCodeProblem(21, "Merge Two Sorted Lists（合并两个有序链表）", "Easy", "虚拟头节点（Dummy Node）＋双指针拉链合并 ・ 时间 O(n + m) / 空间 O(1)"),
            LeetCodeProblem(141, "Linked List Cycle（环形链表检测）", "Easy", "Floyd 龟兔赛跑算法（快慢双指针 Fast & Slow Pointers） ・ 时间 O(n) / 空间 O(1)"),
            LeetCodeProblem(19, "Remove Nth Node From End of List（删除链表倒数第 N 个节点）", "Medium", "快指针先走 N 步＋虚拟头节点单次扫描 ・ 时间 O(n) / 空间 O(1)"),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="为什么 Python 的 list.append() 时间复杂度是「均摊 O(1)」，而 list.insert(0, val) 却是 O(n)？",
                answer="CPython 的 list 基于动态数组实现，扩容时会按约 1.125 倍进行「超额预分配（Over-allocation）」。因此绝大多数 append() 只需直接写入尾部预留空槽，耗时 O(1)；仅在满载时才重新分配更大连续内存并拷贝旧指针，将该次 O(n) 成本平摊到历次写入后即为均摊 O(1)。相反，list.insert(0, val) 必须把下标 0 之后的全部元素指针向右整体搬移一格，每次调用都固定消耗 O(n) 时间。",
            ),
            InterviewFAQ(
                question="面试官要求在 O(1) 额外空间内判断单向链表是否有环（Cycle），且不能修改节点结构，该如何实现？",
                answer="标准解法是「Floyd 龟兔赛跑算法（快慢双指针）」。设定慢指针 slow = head（每轮走 1 步：slow = slow.next）与快指针 fast = head（每轮走 2 步：fast = fast.next.next）。若链表无环，fast 会率先触达 None；若存在环，进入环后快指针每轮都会将与慢指针的距离缩短 1 步，最终必定在环内相遇（slow is fast），时间复杂度 O(n)，额外空间严格为 O(1)。",
            ),
            InterviewFAQ(
                question="什么场景下应该在链表题中引入「虚拟头节点（Dummy Node）」？",
                answer="只要题目操作可能「修改、删除或替换原有头节点 head」（例如合并两个有序链表 LeetCode #21、移除指定值节点 #203、删除倒数第 N 个节点 #19、反转区间链表 #92），不使用 Dummy Node 就必须手写大量 if prev is None 特判。提前构造 dummy = ListNode(0, head) 并令 prev = dummy，所有真实节点便统一拥有合法前驱，结束时直接 return dummy.next 即可，代码简洁且不易遗漏边界。",
            ),
            InterviewFAQ(
                question="Python 数组（array）和 list（列表）有什么区别？开发中该选 list、array.array 还是 NumPy 数组？",
                answer="Python 内置的 list 本质上是「动态指针数组」，支持混存任意类型元素，随机访问 O(1)、尾部 append 均摊 O(1)，是日常工程与算法刷题的首选。标准库 array.array 仅存放单一 C 原生数值类型（如 int32 / float64），内存更紧凑，适合省内存或读写二进制缓冲区的场景。若涉及大规模数值计算与矩阵运算，则应选用 NumPy ndarray，借助连续内存与底层 C/SIMD 向量化实现数十倍加速。",
            ),
        ),
    ),
    ChapterSpec(
        id="ch02",
        badge="Ch.02",
        short_title="栈与队列（Stack & Queue）",
        title="栈与队列（Stack & Queue）",
        complexity="Push / Pop / Enqueue / Dequeue 均为 O(1)",
        summary="掌握后进先出（LIFO）与先进先出（FIFO）两大抽象数据类型（ADT），并通过栈实现经典面试高频题：多层级括号匹配校验器。",
        concepts=(
            "栈（Stack，后进先出 LIFO）：如同摞盘子，最后压入的元素最先弹出。广泛应用于函数调用栈（Call Stack）、浏览器后退历史、语法括号匹配校验与深度优先搜索（DFS）。",
            "队列（Queue，先进先出 FIFO）：如同排队购票，最先入队的元素最先处理。在 Python 中切勿使用 list.pop(0)（会引发 O(n) 内存搬移），应采用 collections.deque 双端队列达成真正的 O(1) 两端操作，广泛用于广度优先搜索（BFS）与异步任务队列。",
            "单调栈（Monotonic Stack）进阶模板：在维持栈 LIFO 特性的同时强制栈内元素保持单调递增或递减，可在 O(n) 线性时间内解决「下一个更大元素」与「柱状图最大矩形面积」等中高频面试题。",
        ),
        file="examples/ch02_stack_queue.py",
        lastmod="2026-11-24",
        keywords=(
            "Python 栈",
            "Python 队列",
            "Stack and Queue",
            "collections.deque",
            "有效括号匹配",
            "Valid Parentheses",
            "LIFO FIFO",
            "LeetCode 20",
        ),
        deep_intro=(
            "栈（Stack）与队列（Queue）并非特定的底层内存排布，而是定义了「数据进出顺序契约」的抽象数据类型（Abstract Data Type, ADT）。"
            "通过将读写行为限定在特定端点，我们可以让复杂的程序执行状态变得高度可控。"
            "栈遵循「后进先出（Last-In, First-Out, LIFO）」原则：操作系统维护每个线程的函数调用栈（Call Stack）、"
            "编译器校验嵌套表达式与括号匹配、编辑器的撤销（Undo）操作栈，底层全都在使用栈。"
            "队列则遵循「先进先出（First-In, First-Out, FIFO）」原则：从操作系统任务调度器、网络数据包缓冲区（Buffer）、"
            "微服务架构中的消息队列（Message Queue），到图论中求解无权图最短路径的广度优先搜索（BFS），都依赖队列确保公平与按层推进的顺序。"
        ),
        comparison_table=ComparisonTable(
            caption="栈（Stack）、双端队列（collections.deque）与错误队列写法（list.pop(0)）性能对比表",
            headers=("数据结构 ／ 实现方式", "核心顺序模型", "写入操作（Push / Enqueue）", "取出操作（Pop / Dequeue）", "工程实战建议与适用场景"),
            rows=(
                ("Stack（底层封装 Python list）", "后进先出 (LIFO)", "list.append(x) — 均摊 O(1)", "list.pop() — O(1)", "推荐！内存紧凑且尾端操作极快，适合括号匹配、DFS、撤销记录"),
                ("Queue（底层封装 collections.deque）", "先进先出 (FIFO)", "deque.append(x) — O(1)", "deque.popleft() — O(1)", "推荐！底层为双向分块链表，两端读写严格 O(1)，适合 BFS 与任务调度"),
                ("错误 Queue（使用 list.pop(0)）", "先进先出 (FIFO)", "list.append(x) — 均摊 O(1)", "list.pop(0) — O(n) 性能陷阱", "严禁在刷题或大队列中使用！每次 pop(0) 都会搬移整段数组导致超时 TLE"),
                ("线程安全队列（queue.Queue）", "先进先出 (FIFO)", "put(x) — O(1) 含锁开销", "get() — O(1) 含锁开销", "内置互斥锁，专用于多线程生产者／消费者并发通信模型"),
                ("单调栈（Monotonic Stack）", "具单调性的 LIFO", "每个元素最多入栈 1 次 — 均摊 O(1)", "破坏单调性即弹出 — 均摊 O(1)", "求解数组中每个元素左侧／右侧首个更大或更小值的 O(n) 利器"),
            ),
        ),
        walkthrough_title="多层级括号匹配校验（is_balanced_brackets('{[()]}')）栈状态分步追踪",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1：依次读取左括号 '{'、'['、'(' — 全部压入栈顶",
                state_snapshot="输入字符: '{' -> '[' -> '(' | Stack 内部状态（底 -> 顶）: ['{', '[', '(']",
                explanation="当扫描到任意左括号（属于 opening 集合 {'(', '[', '{'}）时，代表开启了一层尚未闭合的作用域，直接调用 stack.push(ch) 将其压入栈顶等待后续匹配。",
            ),
            WalkthroughStep(
                step_label="Step 2：读取首个右括号 ')' — 校验栈顶是否为对应 '('",
                state_snapshot="输入字符: ')' | 查表 pairs[')'] == '(' | stack.pop() -> '('（匹配成功）| Stack 剩余: ['{', '[']",
                explanation="遇到右括号 ')' 时，按 LIFO 原则它必须与「最近出现且尚未闭合的左括号」配对。此时校验栈非空，且弹出的栈顶元素正好是 '('，该层小括号成功抵消。",
            ),
            WalkthroughStep(
                step_label="Step 3：依次读取 ']' 与 '}' — 逐层向外弹出配对",
                state_snapshot="读取 ']': pop() 得 '[' ✓ | 读取 '}': pop() 得 '{' ✓ | Stack 剩余: []",
                explanation="接着遇到 ']' 与 '}'，分别与栈顶的 '[' 及 '{' 精准匹配并弹出。若遇到类似 '([)]' 的交错嵌套，stack.pop() 弹出的是 '(' 而非 '['，函数会立即返回 False。",
            ),
            WalkthroughStep(
                step_label="Step 4：字符串扫描结束 — 检查 stack.is_empty() 确认无残留左括号",
                state_snapshot="循环结束 | stack.is_empty() == True => 最终返回 True",
                explanation="遍历完所有字符后不可直接返回 True，必须校验 stack.is_empty()！若输入为 '((('，循环中不会触发任何失配分支，唯有确认栈已彻底清空，才能保证所有左括号均有匹配闭合。",
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="陷阱一：在 BFS 或队列题中误写 queue.pop(0) 造成隐蔽的 O(n²) 超时（TLE）",
                symptom="算法逻辑完全正确，小用例秒过，但在力扣遇到 N = 10^5 节点的图或树时直接超时（Time Limit Exceeded）。",
                root_cause_and_fix="Python 的 list 是连续内存数组，执行 list.pop(0) 删除首元素后，CPython 必须调用 memmove 将后面 N-1 个指针整体前移，单次耗时 O(n)，N 次出队总耗时退化为 O(n²)。请养成固定习惯：凡需 FIFO 队列，首行先写 from collections import deque，一律使用 popleft()。",
            ),
            PitfallItem(
                title="陷阱二：对空栈执行 pop() 或 peek() 前忘记判空",
                symptom="在括号匹配遇到以右括号开头的输入（如 ')()' 或 ']'）时，程序直接崩溃抛出 IndexError: pop from empty list。",
                root_cause_and_fix="任何需要从栈或队列读取或弹出顶端元素的条件判断（包含括号校验、单调栈 while stack and stack[-1] < cur），都必须把非空检查放在逻辑与的最左侧，利用短路求值保护后续操作。",
            ),
            PitfallItem(
                title="陷阱三：括号校验循环结束后直接 return True，漏判纯左括号输入",
                symptom="测试输入 '(((' 或 '{[' 时，函数错误返回 True。",
                root_cause_and_fix="循环体内的比较只负责捕获「右括号多余」或「种类不匹配」；若输入全是左括号，循环只会不断入栈。因此函数末行必须写 return stack.is_empty()，确保没有未闭合的左括号残留。",
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(20, "Valid Parentheses（有效的括号）", "Easy", "栈配对校验与空栈边界保护 ・ 时间 O(n) / 空间 O(n)"),
            LeetCodeProblem(232, "Implement Queue using Stacks（用栈实现队列）", "Easy", "输入栈 in_stack ＋ 输出栈 out_stack 惰性倒腾 ・ 均摊时间 O(1)"),
            LeetCodeProblem(155, "Min Stack（最小栈）", "Medium", "主栈搭配辅助最小值栈（或差值编码） ・ getMin 时间 O(1)"),
            LeetCodeProblem(739, "Daily Temperatures（每日温度）", "Medium", "单调递减栈存下标（Monotonic Stack） ・ 时间 O(n) / 空间 O(n)"),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="Python 的 collections.deque 底层是如何实现的？为何它两端增删都是 O(1)，却不适合随机访问中间下标？",
                answer="CPython 的 deque（双端队列）底层并非单一连续数组，而是由多个固定长度（通常 64 个指针槽）的连续内存块组成的「双向分块链表（Doubly Linked List of Blocks）」。由于维护了首尾块指针与块内偏移量，两端执行 append()、appendleft()、pop()、popleft() 均为严格 O(1)；但若按 d[i] 访问中间位置，则需跨块顺序遍历链表，时间复杂度退化为 O(n)。",
            ),
            InterviewFAQ(
                question="如何只用两个栈（LIFO）实现一个均摊 O(1) 的队列（FIFO，LeetCode #232）？",
                answer="维护两个栈：in_stack 专责接收 enqueue 入队，out_stack 专责提供 dequeue 与 peek。enqueue(x) 直接压入 in_stack（O(1)）；dequeue() 时若 out_stack 非空直接弹出（O(1)），若为空则将 in_stack 全部元素逐一弹出压入 out_stack，经过两次后进先出翻转后，最早入队的元素便浮到 out_stack 栈顶。每个元素一生最多入 in_stack 一次、倒腾一次、出 out_stack 一次，故均摊复杂度为 O(1)。",
            ),
            InterviewFAQ(
                question="什么是「单调栈（Monotonic Stack）」？遇到哪些题干信号应当立刻联想到它？",
                answer="单调栈要求栈内元素从底到顶始终维持单调递增或递减。每当新元素准备入栈前，用 while 循环弹出栈顶所有破坏单调性的元素。凡是要求在数组中为每个元素寻找「左侧或右侧第一个比它大（或小）的位置」（如 LeetCode #739 每日温度、#496 下一个更大元素、#84 柱状图中最大矩形），暴力双层循环需 O(n²)，改用单调栈存下标即可将总时间压至线性 O(n)。",
            ),
        ),
    ),
    ChapterSpec(
        id="ch03",
        badge="Ch.03",
        short_title="二分查找与归并排序",
        title="查找与排序算法（Search & Sort Algorithms）",
        complexity="二分查找 O(log n) ・ 归并排序（Merge Sort）O(n log n)",
        summary="对比线性查找与二分查找的量级跨越，并以分治法（Divide & Conquer）实现稳定排序算法归并排序（Merge Sort）。",
        concepts=(
            "二分查找（Binary Search）：在「有序」序列中每次比较中点即可折半排除一半候选区间，将查找复杂度从线性 O(n) 降至对数级 O(log n)（100 万条数据最多仅需约 20 次比较）。",
            "归并排序（Merge Sort）：经典「分治法（Divide and Conquer）」代表，先递归将数组对半拆分至单元素基底，再以双指针线性归并两个有序子数组。无论最好、平均还是最坏输入，时间复杂度恒稳 O(n log n)，且天然具备稳定排序（Stable Sort）性质。",
            "稳定性（Stability）与 Timsort：当两条记录键值相等时，若排序后仍保持其原始相对先后次序，则称算法稳定。Python 内置 sorted() 与 list.sort() 采用融合归并排序与插入排序优势的 Timsort，兼具稳定与工程级高速表现。",
        ),
        file="examples/ch03_search_sort.py",
        lastmod="2026-11-24",
        keywords=(
            "二分查找",
            "Binary Search",
            "归并排序",
            "Merge Sort",
            "分治法 Divide and Conquer",
            "Python 排序算法",
            "Timsort",
            "时间复杂度 O(n log n)",
        ),
        deep_intro=(
            "查找（Searching）与排序（Sorting）是计算机科学最核心的算法基石。"
            "当数据杂乱无序时，要在 N 条记录中定位目标值只能从头到尾逐项扫描（线性查找 Linear Search，时间复杂度 O(n)）。"
            "然而一旦数据经由排序整理为单调递增序列，我们便能施展「二分查找（Binary Search）」——每轮直接检视区间正中元素，"
            "目标偏大则舍弃左半、目标偏小则舍弃右半。每比较一次，搜索空间即刻减半："
            "面对 10 亿（10^9）条有序数据，线性查找最坏需跑 10 亿次，而二分查找至多 30 次比较即可锁定结果（log2(10^9) ≈ 29.89）！"
            "为了将无序输入高效转化为有序序列，本章通过「分治法（Divide and Conquer）」实现归并排序（Merge Sort），"
            "一举突破 O(n²) 简单排序瓶颈，达到比较排序的理论下界 O(n log n)。"
        ),
        comparison_table=ComparisonTable(
            caption="主流查找与排序算法时间复杂度、空间复杂度与稳定性完整对比表",
            headers=("算法名称", "最好时间", "平均时间", "最坏时间", "额外空间复杂度与稳定性（Stability）"),
            rows=(
                ("线性查找 (Linear Search)", "O(1)", "O(n)", "O(n)", "空间 O(1) ・ 无需预先排序"),
                ("二分查找 (Binary Search)", "O(1)", "O(log n)", "O(log n)", "迭代版空间 O(1) ・ 前提：序列有序或具备单调性"),
                ("插入排序 (Insertion Sort)", "O(n)", "O(n²)", "O(n²)", "空间 O(1) ・ 稳定排序（小规模或近乎有序数据极快）"),
                ("归并排序 (Merge Sort)", "O(n log n)", "O(n log n)", "O(n log n)", "空间 O(n) ・ 稳定排序（绝无 O(n²) 最坏退化）"),
                ("快速排序 (Quick Sort)", "O(n log n)", "O(n log n)", "O(n²)", "空间 O(log n) 递归栈 ・ 不稳定排序（基准选取失当时退化）"),
                ("堆排序 (Heap Sort)", "O(n log n)", "O(n log n)", "O(n log n)", "空间 O(1) 原地排序 ・ 不稳定排序"),
                ("Python Timsort (sorted / .sort)", "O(n)", "O(n log n)", "O(n log n)", "空间 O(n) ・ 稳定排序（自动利用自然有序段 Run 与二分插入）"),
            ),
        ),
        walkthrough_title="归并排序（Merge Sort）分治拆分与双指针归并分步追踪",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1：递归拆分阶段（Divide）— 对半切分直至子数组长度 <= 1",
                state_snapshot="[38, 27, 43, 3] => 左半 [38, 27] 与 右半 [43, 3] => 基底 [38], [27], [43], [3]",
                explanation="merge_sort() 通过 mid = len(arr) // 2 持续递归切分左右两半。当子数组只剩 1 个元素（len(arr) <= 1）时，单元素本身已有序，直接返回作为递归终止条件（Base Case）。",
            ),
            WalkthroughStep(
                step_label="Step 2：底层双指针归并（Conquer Level 1）— 两两合并为长度 2 的有序段",
                state_snapshot="归并 [38] 与 [27] -> [27, 38] | 归并 [43] 与 [3] -> [3, 43]",
                explanation="每层递归返回时，利用双指针 i=0, j=0 对比左右两个有序子数组的首部元素，将较小值优先写入 merged 列表，形成局部有序的 [27, 38] 与 [3, 43]。",
            ),
            WalkthroughStep(
                step_label="Step 3：顶层双指针拉链式归并（Conquer Level 2）— 合并 [27, 38] 与 [3, 43]",
                state_snapshot="对比 27 vs 3 (取 3) -> 对比 27 vs 43 (取 27) -> 对比 38 vs 43 (取 38) -> 尾部拼接 43",
                explanation="i 指向 [27, 38] 起点、j 指向 [3, 43] 起点：1. 3 < 27 取 3（j=1）；2. 27 <= 43 取 27（i=1）；3. 38 <= 43 取 38（i=2 走完左半）；4. 将右半剩余 [43] 直接 extend 追加到末尾。",
            ),
            WalkthroughStep(
                step_label="Step 4：在排序结果上执行二分查找（binary_search([3, 9, 10, 27, 38, 43, 82], 27)）",
                state_snapshot="left = 0, right = 6 => mid = 3 => sorted_nums[3] == 27（一次命中下标 3！）",
                explanation="完整 7 个数字排序后为 [3, 9, 10, 27, 38, 43, 82]。二分查找计算 mid = 0 + (6 - 0) // 2 = 3，读取下标 3 正好命中 27，仅比较 1 次即返回下标 3。",
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="陷阱一：二分查找边界更新误写为 left = mid 或 right = mid 导致死循环",
                symptom="在闭区间 [left, right]（循环条件 while left <= right）查找不存在的目标时，程序卡死在 left == right 无法退出。",
                root_cause_and_fix="既然采用闭区间 [left, right]，一旦确认 sorted_nums[mid] != target，下标 mid 本身就已被排除！下一轮范围必须严格收缩为 left = mid + 1 或 right = mid - 1，保证每次迭代区间长度至少缩减 1。",
            ),
            PitfallItem(
                title="陷阱二：归并排序比较条件错写成 < 而非 <=，破坏稳定性（Stability）",
                symptom="合并左右子数组时写成 if left_half[i] < right_half[j]:，导致键值相等的记录在排序后先后顺序颠倒。",
                root_cause_and_fix="当左半元素与右半元素相等（left_half[i] == right_half[j]）时，因左半元素在原始输入中靠前，必须优先取左半元素（使用 <=），才能严格维持相等键值的原始相对次序。",
            ),
            PitfallItem(
                title="陷阱三：跨语言整数溢出习惯与 Python 标准库 bisect 实战",
                symptom="在 C++/Java 写 mid = (left + right) / 2 当 left + right 超过 2^31 - 1 时会发生有符号整型溢出变负。",
                root_cause_and_fix="虽然 Python 3 的 int 支持任意精度大整数不会溢出，但在跨语言面试中坚持写 mid = left + (right - left) // 2 能体现扎实的防御式编程素养。此外 Python 实战与竞赛可直接调用 C 语言实现的标准库 bisect.bisect_left(arr, target) 完成极速二分定位。",
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(704, "Binary Search（标准二分查找）", "Easy", "闭区间 [left, right] 模板 ・ 时间 O(log n) / 空间 O(1)"),
            LeetCodeProblem(33, "Search in Rotated Sorted Array（搜索旋转排序数组）", "Medium", "借 mid 判定哪一侧保持单调递增再收缩区间 ・ 时间 O(log n)"),
            LeetCodeProblem(34, "Find First and Last Position of Element in Sorted Array", "Medium", "左右边界二分查找（bisect_left / bisect_right） ・ 时间 O(log n)"),
            LeetCodeProblem(912, "Sort an Array（排序数组）", "Medium", "手写归并排序避免快速排序最坏 O(n²) 退化 ・ 时间 O(n log n)"),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="为什么归并排序（Merge Sort）的时间复杂度是 O(n log n)？如何直观推导？",
                answer="把长度为 n 的数组不断对半切分直至单元素，总共需要切分 log2(n) 层（递归树高度约 log n + 1）。而在递归树的「每一层」中，无论被拆成多少小段，将该层所有子数组通过双指针线性归并涉及的总元素数恰好都是 n，因此单层工作量恒为 O(n)。将「每层 O(n)」乘以「层数 O(log n)」，即得无论原始输入顺序如何，总时间复杂度恒为 O(n log n)。",
            ),
            InterviewFAQ(
                question="既然快速排序平均很快且原地排序，为何 Python 内置 sorted() 与 list.sort() 选择基于归并思想的 Timsort？",
                answer="核心原因有二：其一是「稳定性」，Python 保证多关键字排序时相等元素的原始次序不被打乱（如先按分数再按部门排序），而原地快排不稳定；其二是「真实数据局部有序性」，业务数组常包含大量自然有序片段（Natural Runs），Timsort 会自动识别这些片段并用二分插入扩展，再结合高效归并策略，使近乎有序的数据在 O(n) 最佳时间内瞬间完成排序。",
            ),
            InterviewFAQ(
                question="二分查找只能用来「查某个数是否在有序数组里」吗？还有哪些高阶用法？",
                answer="二分查找的本质不是「查数组」，而是「在具备单调性的答案空间上定位可行解边界」。只要问题满足「若答案 X 可行，则所有大于 X 的值均可行；若 X 不可行，则更小的值也均不可行」，即可直接「二分答案（Binary Search on Answer）」！高频代表题包括爱吃香蕉的珂珂（LeetCode #875）、在 D 天内送达包裹的最低运载能力（#1011）与分割数组的最大值（#410）。",
            ),
        ),
    ),
    ChapterSpec(
        id="ch04",
        badge="Ch.04",
        short_title="哈希表与二叉搜索树",
        title="哈希表与二叉搜索树（Hash Table & Binary Search Tree）",
        complexity="哈希表平均读写 O(1) ・ 平衡二叉搜索树查找/插入 O(log n) ・ 中序遍历 O(n)",
        summary="掌握面试出场率最高的哈希冲突解决（拉链法 Separate Chaining）与两数之和 O(n) 秒杀技巧，并手写二叉搜索树（BST）与中序递增遍历。",
        concepts=(
            "哈希表（Hash Table / Python dict）：借助哈希函数将键映射到桶下标，实现平均 O(1) 极速检索；当不同键落入同一桶位发生冲突（Collision）时，常用拉链法（Separate Chaining）或开放寻址法（Open Addressing）化解。经典面试题两数之和（Two Sum）正是利用哈希表以空间换时间，将 O(n²) 降为单次扫描 O(n)。",
            "二叉搜索树（Binary Search Tree, BST）：满足「左子树全部节点 < 根节点 < 右子树全部节点」结构不变量的树形结构。在树高平衡时查找与插入均为 O(log n)，且执行「左 -> 根 -> 右」中序遍历（In-order Traversal）即可在 O(n) 内直接输出升序序列。",
            "负载因子（Load Factor）与动态扩容（Rehashing）：当哈希表内元素数量 N 与桶总数 M 之比（α = N / M）偏高时冲突激增；现代哈希表会在 α 超过阈值（如 CPython dict 为 2/3）时自动扩容并重新散列。",
        ),
        file="examples/ch04_hash_bst.py",
        lastmod="2026-11-24",
        keywords=(
            "Python 哈希表",
            "Hash Table",
            "两数之和 Two Sum",
            "二叉搜索树",
            "Binary Search Tree BST",
            "哈希冲突 拉链法",
            "中序遍历 Inorder Traversal",
            "LeetCode 1",
        ),
        deep_intro=(
            "在软件工程技术面试中，若有一句口诀能帮你打开一半以上算法题的突破口，那就是：「遇到 O(n²) 重复查找瓶颈时，先想能否用哈希表（Hash Table）以空间换时间！」"
            "哈希表通过哈希函数 hash(key) % bucket_count 将任意可哈希键直接映射为数组下标，达成平均 O(1) 的增删改查。"
            "但哈希表本质上是按散列分布而非按键大小排序的（即便 Python 3.7+ dict 保留插入顺序，也不支持按键值大小范围检索），无法高效回答「大于 X 且小于 Y 的全部记录」或「第 K 小键值」。"
            "这正是二叉搜索树（Binary Search Tree, BST）登场的场景：BST 严格维持「左子树所有值 < 根节点 < 右子树所有值」的有序不变量，"
            "不仅支持平均 O(log n) 的动态插入与查找，还能通过中序遍历（In-order Traversal）天然输出递增有序结果。"
        ),
        comparison_table=ComparisonTable(
            caption="哈希表（Hash Table）、平衡二叉搜索树与退化斜树复杂度及能力对比表",
            headers=("操作项目 ／ 结构特性", "哈希表（Hash Table / dict）", "平衡二叉搜索树（Balanced BST）", "退化二叉搜索树（Skewed BST 最坏情况）"),
            rows=(
                ("单键查找 (Search / Get)", "平均 O(1) ／ 极端冲突最坏 O(n)", "O(log n) — 每次比较排除半棵子树", "O(n) — 退化为单向链表"),
                ("插入与更新 (Insert / Put)", "均摊 O(1) ／ 扩容重哈希时 O(n)", "O(log n) — 含旋转平衡维护", "O(n) — 顺序下降至最深叶节点"),
                ("删除键 (Remove / Delete)", "平均 O(1)", "O(log n) — 找中序后继替换", "O(n) — 线性查找后删除"),
                ("按键值升序输出全部元素", "O(n log n) — 需额外调用 sorted()", "O(n) — 直接中序遍历 (In-order)", "O(n) — 中序遍历"),
                ("区间范围查询 (Range Query [L, R])", "O(n) — 必须全表扫描过滤", "O(log n + k) — 剪枝跳过无关子树", "O(n) — 无法有效剪枝"),
                ("键类型约束 (Key Constraint)", "必须可哈希且不可变 (Hashable)", "必须支持大小比较运算 (<, >)", "必须支持大小比较运算 (<, >)"),
            ),
        ),
        walkthrough_title="两数之和 O(n) 单次哈希扫描与 BST 中序遍历（In-order）分步状态追踪",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1：两数之和扫描下标 0（nums = [2, 7, 11, 15], target = 9）",
                state_snapshot="idx = 0, num = 2 | complement = 9 - 2 = 7 | 7 not in seen | 写入 seen = {2: 0}",
                explanation="读取首个数字 2，计算所需补数 complement = 9 - 2 = 7。查询哈希表 seen 发现 7 尚未出现，因此将当前值与下标 {2: 0} 存入字典 seen。",
            ),
            WalkthroughStep(
                step_label="Step 2：两数之和扫描下标 1 — O(1) 瞬间命中补数并返回",
                state_snapshot="idx = 1, num = 7 | complement = 9 - 7 = 2 | 2 in seen (下标 0) => 返回 (0, 1)",
                explanation="读取第二个数字 7，计算 complement = 9 - 7 = 2。查询 seen 在 O(1) 内命中键 2（对应下标 0），立即返回 (0, 1)，彻底省去双层循环枚举。",
            ),
            WalkthroughStep(
                step_label="Step 3：构建二叉搜索树（依次插入 [50, 30, 70, 20, 40, 60, 80]）",
                state_snapshot="Root = 50 | 左子树: 30 (左 20, 右 40) | 右子树: 70 (左 60, 右 80)",
                explanation="首个数字 50 成为根节点；30 < 50 挂入左子树、70 > 50 挂入右子树；随后 20 < 30 挂在 30 左侧、40 > 30 挂在 30 右侧，形成三层满二叉搜索树。",
            ),
            WalkthroughStep(
                step_label="Step 4：执行中序遍历（左子树 -> 根节点 -> 右子树）输出升序序列",
                state_snapshot="遍历顺序: (20 -> 30 -> 40) -> 50 -> (60 -> 70 -> 80) => [20, 30, 40, 50, 60, 70, 80]",
                explanation="递归函数 _traverse 先一路向左深入至最左叶节点 20 收集，回溯至父节点 30，再访问右子节点 40；完成左半部后输出根 50，再同构遍历右子树，零额外排序即得升序列表。",
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="陷阱一：将可变容器（list、dict、set）当作哈希表键触发 TypeError",
                symptom="做字母异位词分组时误写 seen[[1, 2, 3]] = val，运行时直接抛出 TypeError: unhashable type: 'list'。",
                root_cause_and_fix="哈希表要求键的哈希值在生命周期内恒定不变（否则修改内容后哈希值变化，再也定位不到原桶位）。在 Python 中如需用序列作字典键，应先转为不可变的 tuple(my_list)；若以集合为键，则改用 frozenset(my_set)。",
            ),
            PitfallItem(
                title="陷阱二：将「已排序数组」直接顺序插入普通 BST，导致树高退化为 O(n) 斜树",
                symptom="若依次将 [10, 20, 30, 40, 50] 插入未自平衡的 BinarySearchTree，查找时间从 O(log n) 退化为 O(n)。",
                root_cause_and_fix="因每个新元素都大于前驱，所有节点会一路挂在右侧形成单链。若已知输入有序，应每次取中点 arr[mid] 为根递归建树（LeetCode #108）；工程库则多采用红黑树（Red-Black Tree）或 AVL 树借旋转维持平衡。",
            ),
            PitfallItem(
                title="陷阱三：校验二叉搜索树（Validate BST）时只检查「左子节点 < 父节点 < 右子节点」",
                symptom="面对根为 50、左子为 30，而 30 的右子为 60 的树时，错误判定合法（但 60 > 50 违背了左子树全体小于根的约束）。",
                root_cause_and_fix="BST 不变量要求「左子树全部后代节点」都严格小于根节点。正确校验有两法：1. 递归透传开区间上下界 validate(node, low, high)，验证 low < node.val < high；2. 执行中序遍历并检查输出是否严格单调递增。",
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(1, "Two Sum（两数之和）", "Easy", "哈希表记录已访问数值与下标单次扫描 ・ 时间 O(n) / 空间 O(n)"),
            LeetCodeProblem(49, "Group Anagrams（字母异位词分组）", "Medium", "将排序字符元组或 26 字母频次元组作 dict 键 ・ 时间 O(n * k)"),
            LeetCodeProblem(98, "Validate Binary Search Tree（验证二叉搜索树）", "Medium", "递归透传 (low, high) 上下界或中序严格递增校验 ・ 时间 O(n)"),
            LeetCodeProblem(230, "Kth Smallest Element in a BST（BST 中第 K 小的元素）", "Medium", "中序遍历第 K 个访问节点即为答案 ・ 时间 O(H + k)"),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="本教程用「拉链法（Separate Chaining）」演示哈希冲突，Python 内置 dict 底层也是拉链法吗？",
                answer="教学常以拉链法（每桶存列表）直观展示冲突处理；但 CPython 3.6+ 内置 dict 采用高度优化的「紧凑开放寻址法（Compact Open Addressing）」。它将稀疏下标索引表（Indices）与紧凑存储实际 (hash, key, value) 的条目数组（Entries）拆离，冲突时采用伪随机探测（Perturb Probing）找空槽，不仅节省 20%～25% 内存，还天然保留插入顺序并大幅提升缓存命中率。",
            ),
            InterviewFAQ(
                question="二叉树的前序（Pre-order）、中序（In-order）、后序（Post-order）遍历有什么区别与实际用途？",
                answer="三者差异在于「根节点何时被处理」：1. 前序（根 -> 左 -> 右）见到节点即处理，适合克隆整棵树或序列化；2. 中序（左 -> 根 -> 右）对 BST 执行可直接得到升序序列；3. 后序（左 -> 右 -> 根）需等左右子树算毕再汇总当前节点，广泛用于求树高、子树和、资源释放与树形 DP。",
            ),
            InterviewFAQ(
                question="在两数之和（Two Sum）中，为何「边遍历边入表（One-pass）」优于「先全入表再查表（Two-pass）」？",
                answer="除减少一趟遍历外，One-pass 能自然处理「两个相同数字相加等于 target」的重复用例（如 nums = [3, 3], target = 6）。扫描到下标 1 的第二个 3 时，先查 complement = 3 是否在 seen 中，此时 seen[3] 正记录下标 0，立即配对返回 (0, 1)，既不会被后值覆盖也不会自己配对自己。",
            ),
        ),
    ),
    ChapterSpec(
        id="ch05",
        badge="Ch.05",
        short_title="图遍历 BFS/DFS 与 OOP",
        title="图论遍历与面向对象设计（Graph BFS / DFS & OOP）",
        complexity="BFS / DFS 遍历与无权图最短路径均为 O(V + E)",
        summary="通过面向对象封装邻接表（Adjacency List），实现广度优先搜索（BFS）、深度优先搜索（DFS）与无权图最短路径回溯。",
        concepts=(
            "广度优先搜索（BFS）vs. 深度优先搜索（DFS）：BFS 配合队列（deque）从起点同心圆逐层外扩，首次抵达终点必为「最少步数最短路径」；DFS 依靠递归调用栈或显式栈一路到底再回溯，常用于连通分量、拓扑排序与环检测。",
            "面向对象封装（OOP Encapsulation）：将内部邻接表 _adj 与访问细节隐藏在 Graph[T] 类内部，对外暴露清晰的 add_edge、bfs、dfs 与 shortest_path_bfs 接口，兼具类型安全与高可维护性。",
            "稀疏图与稠密图存储选型：现实网络（社交关系、道路网、网页拓扑）绝大多数属于「稀疏图（边数 E 远小于 V²）」，邻接表仅耗 O(V + E) 空间，远优于邻接矩阵的 O(V²)。",
        ),
        file="examples/ch05_graph_oop.py",
        lastmod="2026-11-24",
        keywords=(
            "图论算法",
            "广度优先搜索 BFS",
            "深度优先搜索 DFS",
            "Python 面向对象 OOP",
            "邻接表 Adjacency List",
            "无权图最短路径",
            "LeetCode 200 岛屿数量",
            "Graph Traversal",
        ),
        deep_intro=(
            "当实体间关系不再是「一对一（线性表）」或「一对多（层次树）」，而是任意两节点都可能彼此相连的「多对多网络」时，我们就步入了图论（Graph Theory）的世界。"
            "从导航路网、社交好友推荐、包管理器依赖解析，到迷宫寻路与游戏 AI 决策，背后全都是由顶点（Vertex, V）与边（Edge, E）构成的图结构。"
            "本章同步展示中大型工程极为关键的「面向对象设计（Object-Oriented Programming, OOP）」理念："
            "借助 Python 泛型将底层邻接表 _adj: dict[T, list[T]] 封装进 Graph[T] 类中，"
            "让调用方无需关心字典初始化或去重边细节，直接调用高阶语义方法即可安全完成 BFS、DFS 与最短路径回溯。"
        ),
        comparison_table=ComparisonTable(
            caption="图存储结构（邻接表 vs. 邻接矩阵）与遍历算法（BFS vs. DFS）完整对比表",
            headers=("对比维度 ／ 算法", "空间复杂度", "遍历／查询时间复杂度", "核心数据结构", "最佳工程与面试应用场景"),
            rows=(
                ("邻接表 (Adjacency List)", "O(V + E)", "遍历全部邻居 O(deg(v))", "dict[T, list[T]]", "稀疏图首选（95% 实战与力扣图论题标准表示法）"),
                ("邻接矩阵 (Adjacency Matrix)", "O(V²)", "判断两点是否直连 O(1)", "二维数组 matrix[V][V]", "顶点数 V 极小（如 V <= 500）且边极稠密的完全图"),
                ("广度优先搜索 (BFS)", "O(V) 队列与 visited", "O(V + E)", "FIFO 队列 (collections.deque)", "无权图最短路径、最少步数状态转换、多源同时扩散"),
                ("深度优先搜索 (DFS)", "O(V) 递归栈深度", "O(V + E)", "LIFO 栈 ／ 递归调用栈", "连通分量计数、路径全枚举、回溯法、有向图判环"),
                ("BFS 最短路径回溯 (Parent Map)", "O(V) 记录前驱节点", "O(V + E)", "deque + parent: dict[T, T|None]", "不仅求出最短跳数，还能完整还原起点到终点的顶点路径"),
            ),
        ),
        walkthrough_title="无权图 BFS 最短路径与 Parent 回溯（shortest_path_bfs('A', 'F')）分步追踪",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1：初始化起点 'A'（距离第 0 层）",
                state_snapshot="queue = deque(['A']) | parent = {'A': None}",
                explanation="从起点 'A' 出发，将 'A' 放入双端队列 queue，并在前驱字典 parent 记录 {'A': None}。parent 字典一举两得：既替代 visited 集合防止重复访问，又记录每个节点首次被哪一父节点扩展而来。",
            ),
            WalkthroughStep(
                step_label="Step 2：扩散第 1 层 — 弹出 'A' 并将邻居 'B'、'C' 入队",
                state_snapshot="popleft() -> 'A' | 探索邻居 'B', 'C' | queue = deque(['B', 'C']) | parent = {'A': None, 'B': 'A', 'C': 'A'}",
                explanation="从队首弹出 'A'，发现邻居 'B' 与 'C' 均不在 parent 中，立刻登记 parent['B'] = 'A'、parent['C'] = 'A' 并推入队尾，完成距离为 1 的首层同心圆搜索。",
            ),
            WalkthroughStep(
                step_label="Step 3：扩散第 2 层 — 依次弹出 'B' 与 'C'，探索 'D' 与 'E'",
                state_snapshot="弹出 'B' -> 入队 'D' (parent['D']='B') | 弹出 'C' -> 入队 'E' (parent['E']='C') | queue = deque(['D', 'E'])",
                explanation="弹出 'B' 时跳过已登记的 'A'，新邻居 'D' 写入 parent['D'] = 'B'；接着弹出 'C'，新邻居 'E' 写入 parent['E'] = 'C'。此时队列保存着距离起点 2 步的节点 ['D', 'E']。",
            ),
            WalkthroughStep(
                step_label="Step 4：扩散第 3 层命中终点 'F' — 沿 parent 字典反向回溯还原最短路径",
                state_snapshot="弹出 'D' -> 邻居 'F' == goal | parent['F'] = 'D' | 回溯: F -> D -> B -> A => reverse() 得 ['A', 'B', 'D', 'F']",
                explanation="弹出 'D' 时发现邻居 'F' 正好命中终点 goal！登记 parent['F'] = 'D' 后，从 'F' 顺着 parent 一路倒推回起点（F -> D -> B -> A -> None），最后反转列表即得最少步数最短路径 ['A', 'B', 'D', 'F']。",
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="陷阱一：在 BFS 中等到「出队（popleft）时」才标记 visited，导致节点重复入队爆内存",
                symptom="在网格图或稠密图跑 BFS 时，同一节点被周围多个邻居反复推入队列数十次，触发内存超限（MLE）或超时（TLE）。",
                root_cause_and_fix="BFS 黄金铁律：必须在「把邻居 nb 放入 queue 的前一瞬间」立刻执行 visited.add(nb)（或写入 parent[nb] = curr）！如此同层其他节点再扫到 nb 时即可直接跳过，确保每个顶点严格只入队一次。",
            ),
            PitfallItem(
                title="陷阱二：在「边含不同正权重（Weighted Graph）」的图上误用普通 BFS 求最短路",
                symptom="地图上 A 直达 C 距离 100 公里（1 步），而 A 经 B 到 C 仅 10 + 10 = 20 公里（2 步），普通 BFS 却错判 A -> C 最短。",
                root_cause_and_fix="普通 BFS（FIFO deque）求的是「最少边数（跳数）」。只有当全部边权重相等或无权时，最少边数才等价最短路；若边含不同非负权重，必须将普通队列换成最小堆优先队列，改用 Dijkstra 算法（复杂度 O((V + E) log V)）。",
            ),
            PitfallItem(
                title="陷阱三：在极深长链图上使用递归 DFS，触发 Python 默认递归栈上限 RecursionError",
                symptom="当图退化为超 1,000 个节点的长链时，递归版 dfs() 直接抛出 RecursionError: maximum recursion depth exceeded。",
                root_cause_and_fix="CPython 默认最大递归深度约 1,000（可通过 sys.getrecursionlimit() 查看）。面对 V > 1,000 的大规模图，应改用「显式栈（Python list 迭代 push/pop）」实现非递归 DFS，或直接采用迭代式 BFS，彻底避开调用栈溢出。",
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(200, "Number of Islands（岛屿数量）", "Medium", "二维网格连通分量 BFS / DFS 遍历标记 ・ 时间 O(M * N)"),
            LeetCodeProblem(994, "Rotting Oranges（腐烂的橘子）", "Medium", "多源广度优先搜索（Multi-source BFS）求最少分钟数 ・ 时间 O(M * N)"),
            LeetCodeProblem(207, "Course Schedule（课程表依赖环检测）", "Medium", "有向图判环（Kahn 入度 BFS 拓扑排序 ／ 三色标记 DFS） ・ 时间 O(V + E)"),
            LeetCodeProblem(133, "Clone Graph（克隆无向图）", "Medium", "哈希表（原节点 -> 克隆节点映射）结合 BFS / DFS 深拷贝 ・ 时间 O(V + E)"),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="为什么广度优先搜索（BFS）的时间复杂度是 O(V + E)，而不是 O(V * E)？",
                answer="因为有 visited 集合（或 parent 字典）保护，每个顶点最多入队一次、出队一次，该部分总计 O(V)。每当顶点 u 出队时，我们仅扫描它自身的邻接表 _adj[u]（长度为度 deg(u)）。将全部顶点的邻接表长度求和，有向图恰为 E、无向图为 2E，故扫描所有边的总次数为 O(E)。两部分相加即为线性 O(V + E)。",
            ),
            InterviewFAQ(
                question="工程代码中为何把邻接表 _adj 封装在 Graph[T] 类内，而不是把 dict[str, list[str]] 裸露在外直接读写？",
                answer="这体现了面向对象的「封装（Encapsulation）」与「单一职责原则（SRP）」。若将裸字典暴露在外，每个调用点都要自行防范顶点缺失导致的 KeyError、无向边漏写反向边与重复加边等问题；封装进 Graph[T] 后，所有不变量由 add_vertex 与 add_edge 统一把关，neighbors() 返回浅拷贝避免外部误篡改内部结构。",
            ),
            InterviewFAQ(
                question="什么是「多源 BFS（Multi-source BFS）」？它和跑多次单源 BFS 有何区别？",
                answer="当问题存在多个起点同时向外扩散（如 LeetCode #994 多颗腐烂橘子同时传染，或 #542 01 矩阵求每个 1 到最近 0 的距离）时，若对每个起点单独跑 BFS 会达到 O(K * V * E) 超时。正确做法是在初始化阶段把「全部起点」一次性压入同一个 deque 作为第 0 层，仅跑唯一一趟 BFS 扩散，即可在 O(V + E) 时间内求得全部节点到最近源点的最短距离。",
            ),
        ),
    ),
    ChapterSpec(
        id="ch06",
        badge="Ch.06",
        short_title="动态规划与记忆化搜索",
        title="动态规划与记忆化搜索（Dynamic Programming & Memoization）",
        complexity="爬楼梯状态压缩 O(n) 时间 / O(1) 空间 ・ 0/1 背包 O(N×W) ・ LIS 最长递增子序列 O(n log n)",
        summary="破除暴力递归 O(2^n) 指数爆炸瓶颈，吃透重叠子问题、最优子结构、一维滚动数组状态压缩与二分贪心优化 LIS。",
        concepts=(
            "动态规划两大核心前提：「重叠子问题（Overlapping Subproblems）」与「最优子结构（Optimal Substructure）」。通过缓存已计算的子问题结果，彻底消除暴力递归中成千上万次重复分支计算。",
            "自顶向下记忆化搜索 vs. 自底向上状态转移表：Top-Down 在递归函数上挂载缓存（如 Python @functools.cache）；Bottom-Up 则从初始状态 dp[0] 顺序填表，并常可利用滚动变量或一维数组将空间复杂度压缩至 O(1) 或 O(W)。",
            "0/1 背包一维逆序更新精髓：将二维 dp[i][w] 压缩为一维 dp[w] 时，内层容量循环必须「从大到小（capacity -> weight）逆序遍历」，才能确保读取 dp[cap - w] 时拿到的是「上一轮尚未放入当前物品」的旧状态。",
        ),
        file="examples/ch06_dynamic_programming.py",
        lastmod="2026-11-24",
        keywords=(
            "动态规划",
            "Dynamic Programming DP",
            "记忆化搜索 Memoization",
            "0/1 背包问题 Knapsack",
            "最长递增子序列 LIS",
            "爬楼梯 Climbing Stairs",
            "状态转移方程",
            "LeetCode 70 300 322",
        ),
        deep_intro=(
            "很多初学者与转行工程师一听到「动态规划（Dynamic Programming, 简称 DP）」就望而生畏，"
            "其实 DP 的本质非常朴素：「记住算过的答案，以空间换时间，并按依赖拓扑序由小到大推出最终解」。"
            "以经典的爬楼梯（Climbing Stairs）为例：抵达第 n 阶的最后一步只能来自第 n-1 阶跨 1 步或第 n-2 阶跨 2 步，"
            "因此方法数满足状态转移方程 f(n) = f(n-1) + f(n-2)。若写纯暴力递归，f(40) 会把 f(20) 重复计算上万遍，时间复杂度飙升至指数级 O(2^n)；"
            "只要我们自底向上从第 0 阶、第 1 阶顺序累加，并且只保留前两阶的滚动变量（prev2, prev1），"
            "就能在 O(n) 时间、O(1) 额外空间内瞬间算出答案！"
            "本章进一步带你攻克面试最常考的两大进阶模型：0/1 背包一维滚动数组与 O(n log n) 二分优化的最长严格递增子序列（LIS）。"
        ),
        comparison_table=ComparisonTable(
            caption="动态规划实现策略（暴力递归、记忆化搜索、二维/一维 DP 与滚动压缩）完整对比表",
            headers=("实现策略 ／ 算法模型", "时间复杂度", "空间复杂度", "核心实现机制", "工程与白板题适用场景"),
            rows=(
                ("暴力递归 (Naive Recursion)", "O(2^n) 指数级爆炸", "O(n) 调用栈", "直接递归展开全部分支，无缓存", "仅适用 n <= 20 极小规模枚举，大用例必超时"),
                ("Top-Down 记忆化搜索 (Memoization)", "O(状态总数 × 转移成本)", "O(状态总数 + 递归深度)", "递归搭配 dict 或 @functools.cache", "状态转移方向不规则、无需算满所有状态的树形／区间 DP"),
                ("Bottom-Up 标准填表法 (Tabulation)", "O(状态总数 × 转移成本)", "O(状态总数)", "开辟一维或二维 dp 数组由基底迭代填表", "零递归调用开销，无栈溢出风险，逻辑最清晰"),
                ("Bottom-Up 空间状态压缩", "O(状态总数 × 转移成本)", "O(1) 或降维 O(W)", "仅保留上一轮所需的少量变量或单行数组", "爬楼梯 O(1) 空间、0/1 背包一维 O(W) 空间面试加分写法"),
                ("LIS 二分贪心优化 (Patience Sorting)", "O(n log n)", "O(n) 维护 tails 数组", "用 bisect_left 维护各长度递增子序列最小结尾", "当 n 达 10^5 时替代传统 O(n²) DP 的唯一正解"),
            ),
        ),
        walkthrough_title="0/1 背包问题一维滚动数组逆序更新（knapsack_01）分步状态追踪",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1：初始化一维 DP 数组（背包容量 capacity = 50）",
                state_snapshot="dp = [0, 0, ..., 0]（长度 51，代表容量 0 ~ 50 未装任何物品时最大价值皆为 0）",
                explanation="创建长度为 capacity + 1 的一维数组 dp，其中 dp[cap] 表示「背包容量上限为 cap 时可获得的最大总价值」。初始全部置 0。",
            ),
            WalkthroughStep(
                step_label="Step 2：处理第 1 件物品（重量 w=10, 价值 v=60）— 由 cap=50 逆序更新至 10",
                state_snapshot="cap = 50..10: dp[cap] = max(dp[cap], dp[cap - 10] + 60) => dp[10..50] 全部更新为 60",
                explanation="内层循环从 cap = 50 倒推回 10。因读取的 dp[cap - 10] 都是本轮尚未改写过的 0，容量 10 以上的槽位都只放入一件物品 1，价值更新为 60（不会误放两次变成 120）。",
            ),
            WalkthroughStep(
                step_label="Step 3：处理第 2 件物品（重量 w=20, 价值 v=100）— 逆序决策选或不选",
                state_snapshot="dp[50..30] = dp[20..0] + 100 = 160（同时装入物品 1 与 2）| dp[20..29] = 100 | dp[10..19] = 60",
                explanation="当 cap >= 30 时，对比「不放物品 2（保持 60）」与「腾出 20 容量放入物品 2（dp[cap-20] + 100 = 160）」，更新为 160；20 <= cap < 30 则更新为单放物品 2 的价值 100。",
            ),
            WalkthroughStep(
                step_label="Step 4：处理第 3 件物品（重量 w=30, 价值 v=120）— 得出最终最大价值 dp[50] = 220",
                state_snapshot="cap = 50: max(原 dp[50]=160, dp[50-30] + 120 = 100 + 120 = 220) => dp[50] = 220",
                explanation="最后考虑重量 30、价值 120 的物品 3。在 cap = 50 时读取上一轮 dp[20]（价值 100，即单放物品 2）加上物品 3 的 120 得到 220 > 160，成功锁定最优组合（物品 2 与物品 3，总重 50、总价值 220）。",
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="陷阱一：0/1 背包一维数组把内层容量循环写成「从小到大正序」，意外变成完全背包",
                symptom="在每件物品限选一次的 0/1 背包中，内层误写 for cap in range(w, capacity + 1):，算出结果远超正确答案。",
                root_cause_and_fix="若从小到大正序更新，算 dp[10] 时放入物品 1，接着算 dp[20] 读取 dp[20 - 10] 就会读到「刚放过物品 1 的 dp[10]」，导致同一物品被重复装入！牢记口诀：0/1 背包一维容量必逆序（大到小）；完全背包（物品可无限选）一维容量才用正序（小到大）。",
            ),
            PitfallItem(
                title="陷阱二：写对了状态转移方程，却设错了基底值与非法状态初始化",
                symptom="在零钱兑换（Coin Change）求最少硬币数时把 dp 全初始化为 0，导致所有 min() 结果永远被 0 吞掉。",
                root_cause_and_fix="初始值须紧扣目标是 max 还是 min：求最大价值（如背包）可初始化为 0；求最小成本／最少步数（如 LeetCode #322 零钱兑换）时，除基底 dp[0] = 0 外其余位置必须设为正无穷 float('inf')（或 amount + 1）。",
            ),
            PitfallItem(
                title="陷阱三：在最长递增子序列（LIS）中误把 tails 数组当成本身就是最终子序列",
                symptom="运行 length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]) 时直接把 tails 当作子序列打印，发现元素顺序与原数组不符。",
                root_cause_and_fix="在 O(n log n) 二分贪心 LIS 算法中，tails[k] 的严格语义是「所有长度为 k+1 的递增子序列里，结尾最小的那个值」。用较小新值覆盖中间槽位是为了让后续更容易接上更长序列，len(tails) 100% 等于 LIS 长度；若需还原具体序列本身，还需额外记录前驱下标数组再回溯。",
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(70, "Climbing Stairs（爬楼梯）", "Easy", "一维线性 DP 与滚动变量 O(1) 空间压缩 ・ 时间 O(n) / 空间 O(1)"),
            LeetCodeProblem(198, "House Robber（打家劫舍）", "Medium", "选与不选转移 dp[i] = max(dp[i-1], dp[i-2] + nums[i]) ・ 时间 O(n) / 空间 O(1)"),
            LeetCodeProblem(322, "Coin Change（零钱兑换）", "Medium", "完全背包模型求最少硬币数 ・ 时间 O(amount * len(coins)) / 空间 O(amount)"),
            LeetCodeProblem(300, "Longest Increasing Subsequence（最长严格递增子序列）", "Medium", "贪心维护最小结尾 tails ＋ 二分查找 bisect_left ・ 时间 O(n log n)"),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="白板面试遇到陌生动态规划（DP）题时，标准的「破题四步法」是什么？",
                answer="建议按以下四步清晰向面试官陈述：1. 定义状态：明确 dp[i] 或 dp[i][j] 的物理含义；2. 推导状态转移方程：拆解当前状态如何由更小子问题决策转移而来（如选与不选取 max）；3. 确定基底与初始化：设好 dp[0] 与合法／非法初值；4. 确定遍历方向与空间优化：确认计算顺序满足无后效性依赖，并评估是否可用滚动变量降维。",
            ),
            InterviewFAQ(
                question="Top-Down 记忆化搜索与 Bottom-Up 填表法在实战中该如何取舍？",
                answer="限时笔试（OA）或状态依赖复杂（如树形 DP、博弈区间 DP）时，用 Python 3.9+ 内置 @functools.cache 配合 Top-Down 递归写起来最快且天然跳过无效状态；正式技术面试中，改写为 Bottom-Up 填表并顺手展示空间降维（O(n) -> O(1) 或 O(N*W) -> O(W)）是极具说服力的资深加分项，也彻底消除栈溢出隐患。",
            ),
            InterviewFAQ(
                question="为什么求「最长严格递增子序列（LIS）」能从传统 DP 的 O(n²) 提速到 O(n log n)？核心直觉是什么？",
                answer="关键在于贪心直觉：假设当前存在两个长度同为 3 的递增子序列 [2, 5, 100] 与 [2, 5, 7]，为了让后续新数（如 8）更容易接上形成长度 4，我们只关心「相同长度下结尾越小越好」的代表！由此维护记录各长度最小结尾的数组 tails，可严格证明 tails 必然单调递增，因此每读入新数 x 不再线性回扫 O(n)，而是直接对 tails 做 O(log n) 的二分查找（bisect_left）替换或追加。",
            ),
        ),
    ),
    ChapterSpec(
        id="ch07",
        badge="Ch.07",
        short_title="二叉堆、优先队列与 Top-K",
        title="二叉堆、优先队列与 Top-K 算法（Heap, Priority Queue & Top-K Elements）",
        complexity="堆 Push / Pop O(log n) ・ Top-K 筛选 O(n log k) ・ 合并 K 个有序序列 O(N log K)",
        summary="深入理解完全二叉树数组下标映射与上浮／下沉机制，手写泛型 MinHeap 并实现海量数据 Top-K 与多路归并算法。",
        concepts=(
            "二叉堆（Binary Heap）与数组下标映射：堆是一棵「完全二叉树」，无需指针节点，单数组即可零空洞存储：下标 i 的父节点为 (i - 1) // 2，左子节点为 2 * i + 1，右子节点为 2 * i + 2。",
            "海量数据 Top-K 最优解：要在 1 亿条数据中挑出最大的前 K 项（如 K = 10），无需全量排序（耗时 O(n log n) 且内存爆炸），只需维护容量固定为 K 的「最小堆（Min-Heap）」，新值大于堆顶守门员时即替换下沉，时间仅 O(n log k)、空间仅 O(k)。",
            "多路归并（K-Way Merge）：需要将 K 个有序数据流或链表合并为单一有序序列时，用最小堆保存各路当前最小代表，每次弹出全局最小值并推入该路下一元素，即可在 O(N log K) 时间内完成。",
        ),
        file="examples/ch07_heap_priority_queue.py",
        lastmod="2026-11-24",
        keywords=(
            "二叉堆 Binary Heap",
            "优先队列 Priority Queue",
            "Python heapq 教程",
            "Top-K 问题算法",
            "MinHeap 实现",
            "合并 K 个有序链表",
            "LeetCode 215 23 347",
            "Sift-Up Sift-Down",
        ),
        deep_intro=(
            "在操作系统进程调度、急诊分诊、游戏寻路算法（A* / Dijkstra）与实时排行榜系统中，"
            "我们不再需要先进先出的普通队列，而是「谁优先级最高（或值最小／最大），谁先出队」的优先队列（Priority Queue）。"
            "若用无序数组实现，插入虽是 O(1)，但每次找极值需 O(n)；若每次插入都保持全数组有序，单次维护又要 O(n)。"
            "「二叉堆（Binary Heap）」在两者间取得了完美平衡：它不要求整棵树完全排序，只维护「父节点恒小于等于（最小堆）或大于等于（最大堆）左右子节点」的堆序性质（Heap Order Property）。"
            "如此一来，全局极值永远稳居数组下标 0 的堆顶（O(1) 读取），而插入后的上浮（Sift-Up）与弹出堆顶后的下沉（Sift-Down）都只沿树高调整，时间复杂度严格稳定在 O(log n)！"
        ),
        comparison_table=ComparisonTable(
            caption="优先队列底层实现方案（二叉堆、无序数组、有序数组与全量排序）性能对比表",
            headers=("操作项目 ／ 应用场景", "二叉堆（MinHeap / heapq）", "无序数组（Unsorted list）", "维护有序数组（Sorted list）", "一次性全量排序（sorted()）"),
            rows=(
                ("查看极值 (Peek Min / Max)", "O(1) — 直接读取 _data[0]", "O(n) — 需全数组线性扫描", "O(1) — 读取首或尾元素", "排序后 O(1)"),
                ("插入新元素 (Push / Insert)", "O(log n) — 尾部追加并 _sift_up", "均摊 O(1) — 直接 append", "O(n) — 二分 O(log n) + 搬移 O(n)", "不支持动态流式插入"),
                ("弹出极值 (Pop Min / Max)", "O(log n) — 尾部补顶并 _sift_down", "O(n) — 找极值并搬移删除", "移除尾部 O(1) ／ 移除首部 O(n)", "不支持动态高效重排"),
                ("将 N 条现成数据建堆", "O(n) — Floyd 自底向上 heapify", "O(n) — 直接拷贝", "O(n log n)", "O(n log n)"),
                ("N 条海量数据求前 K 大 (Top-K)", "时间 O(n log k) ・ 空间 O(k)", "不适用", "时间 O(n * k) ・ 空间 O(k)", "时间 O(n log n) ・ 空间 O(n)"),
                ("合并 K 个有序列表（总长 N）", "时间 O(N log K) ・ 空间 O(K)", "时间 O(N * K)", "时间 O(N * K)", "时间 O(N log N) ・ 空间 O(N)"),
            ),
        ),
        walkthrough_title="MinHeap 上浮／下沉维护与固定容量 K 最小堆筛选 Top-K 分步追踪",
        walkthrough_steps=(
            WalkthroughStep(
                step_label="Step 1：MinHeap 依次插入 [5, 1, 8, 3] — 观察上浮（_sift_up）过程",
                state_snapshot="push(5) -> [5] | push(1): 1 < 5 上浮交换 -> [1, 5] | push(8) -> [1, 5, 8] | push(3): 3 < 5 上浮 -> [1, 3, 8, 5]",
                explanation="当 push(3) 追加到下标 3 时，计算父下标 parent = (3 - 1) // 2 = 1（值为 5）。由于 3 < 5 违背最小堆性质，交换 3 与 5；继续比较下标 1 与根下标 0（值为 1），1 <= 3 满足条件，停止上浮。",
            ),
            WalkthroughStep(
                step_label="Step 2：调用 MinHeap.pop() 弹出堆顶 1 — 尾元素补位并下沉（_sift_down）",
                state_snapshot="取出堆顶 1 | 尾元素 5 移至下标 0 -> [5, 3, 8] | 5 与较小子节点 3 交换 -> [3, 5, 8]",
                explanation="弹出最小值 1 后，为保持完全二叉树无空洞，将末尾元素 5 移到下标 0。随后执行 _sift_down(0)：对比左子节点 3（下标 1）与右子节点 8（下标 2），选出较小的 3 与 5 交换，堆顶更新为次小值 3。",
            ),
            WalkthroughStep(
                step_label="Step 3：Top-3 最大元素筛选（nums = [64, 34, 25, 12, 22, 11, 90]）— 构建容量 3 守门员",
                state_snapshot="前 3 个数直接入堆: min_heap = [25, 64, 34]（堆顶 min_heap[0] == 25 为当前第 3 大守门员）",
                explanation="求「前 K 大」反而要用「最小堆（Min-Heap）」！因为最小堆顶 min_heap[0] 恰是「暂列前 K 名中最弱的门槛（第 K 大）」。后续扫到的 12、22、11 均低于门槛 25，直接淘汰不入堆。",
            ),
            WalkthroughStep(
                step_label="Step 4：遇到强者 90 > 守门员 25 — 执行 heapreplace 替换并降序输出",
                state_snapshot="90 > 25 => heapreplace(min_heap, 90) => min_heap = [34, 64, 90] => 降序输出 [90, 64, 34]",
                explanation="扫描到末尾 90 时，90 > min_heap[0] (25)，调用 heapq.heapreplace 踢出 25 并让 90 下沉就位，最终堆内留存的 [34, 64, 90] 即全数组最大的前 3 名。",
            ),
        ),
        pitfalls=(
            PitfallItem(
                title="陷阱一：求「前 K 大（Top-K Largest）」却误用最大堆，或搞反最小堆／最大堆方向",
                symptom="把全部 N 条记录全塞进最大堆再弹出 K 次，在流式海量数据下直接撑爆内存。",
                root_cause_and_fix="牢记反向口诀：「求前 K 大，用容量 K 的最小堆（淘汰太小的数）；求前 K 小，用容量 K 的最大堆（淘汰太大的数）」。堆大小始终锁死在 K，额外空间严格 O(k)。",
            ),
            PitfallItem(
                title="陷阱二：Python 标准库 heapq 只提供最小堆（Min-Heap），需要最大堆时不知如何实现",
                symptom="手写对顶双堆求数据流中位数（LeetCode #295）或最大优先队列时找不到 MaxHeap 类。",
                root_cause_and_fix="Python 的 heapq 仅实现了最小堆。面对数值型最大堆需求，最简洁惯用的工程技巧是「入堆取反 heapq.heappush(max_heap, -val)，出堆再取反还原 -heapq.heappop(max_heap)」：原数越大，取反后越小，自然浮至最小堆顶！",
            ),
            PitfallItem(
                title="陷阱三：把 (priority, obj) 放入 heapq 时，优先级相同且 obj 不可比较导致 TypeError",
                symptom="合并 K 个有序链表（LeetCode #23）或自定义任务调度写 heappush(heap, (node.val, node))，当两节点值相等时抛出 TypeError: '<' not supported between instances of 'ListNode' and 'ListNode'。",
                root_cause_and_fix="Python 比较元组是按列从左到右进行的：第 0 列相等时会自动比较第 1 列！若第 1 列是不支持 < 的自定义对象即崩溃。标准解法是在中间插入永不重复的递增序号或列表下标 (val, list_idx, node)（如本章 merge_k_sorted_lists），让平手在第 2 列直接分出胜负。",
            ),
        ),
        leetcode_problems=(
            LeetCodeProblem(215, "Kth Largest Element in an Array（数组中的第 K 个最大元素）", "Medium", "维护容量 K 的最小堆（Min-Heap） ・ 时间 O(n log k) / 空间 O(k)"),
            LeetCodeProblem(347, "Top K Frequent Elements（前 K 个高频元素）", "Medium", "Counter 哈希计数 ＋ 容量 K 最小堆筛频率 ・ 时间 O(n log k)"),
            LeetCodeProblem(23, "Merge k Sorted Lists（合并 K 个升序链表）", "Hard", "最小堆存放 (val, list_idx, elem_idx) 多路归并 ・ 时间 O(N log K)"),
            LeetCodeProblem(295, "Find Median from Data Stream（数据流的中位数）", "Hard", "对顶双堆（左半最大堆 + 右半最小堆平衡大小） ・ 插入 O(log n) / 查询 O(1)"),
        ),
        interview_faqs=(
            InterviewFAQ(
                question="为什么完全二叉树可以直接用一维数组存储，而普通二叉搜索树（BST）必须用指针节点？",
                answer="因为二叉堆强制满足「完全二叉树」形态——除最后一层外每层满载，且末层节点全部靠左紧密排列，绝无空洞。在零空洞前提下按层序编号 0, 1, 2...，就能用纯算术公式 left = 2*i + 1、right = 2*i + 2 与 parent = (i - 1) // 2 精准换算父子关系，省去全部指针开销；而普通 BST 可能任意偏斜，硬存数组会浪费海量空位。",
            ),
            InterviewFAQ(
                question="将 N 个无序元素逐一 push() 建堆需 O(n log n)，为何 heapq.heapify(arr) 原地建堆只需线性 O(n)？",
                answer="因为 heapify() 采用「Floyd 自底向上下沉法」：数组后半段约 N/2 个叶节点无需下沉（耗时 0）；倒数第二层约 N/4 个节点最多下沉 1 层；倒数第三层约 N/8 个节点最多下沉 2 层……唯有根节点可能下沉 log2(N) 层。级数求和 Σ (N / 2^(h+1)) * h 严格收敛于上界 2N，因此整体时间复杂度是线性 O(n)！",
            ),
            InterviewFAQ(
                question="在 top_k_largest 中，当 num > min_heap[0] 时为何调用 heapq.heapreplace 比先 heappop 再 heappush 更快？",
                answer="若先 heappop() 再 heappush()，会先做一次完整下沉（Sift-Down），再做一次完整上浮（Sift-Up），共两趟树高调整。而在已确认新元素大于堆顶的前提下，直接调用 heapq.heapreplace(min_heap, num) 一步覆盖堆顶并只执行唯一一次下沉，常数开销直接减半。",
            ),
        ),
    ),
)
