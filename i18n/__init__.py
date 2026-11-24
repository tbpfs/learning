#!/usr/bin/env python3
"""Multilingual locale registry and fail-fast code/output localization for learn.ai-purplemaple.com."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Sequence

from chapter_content import ChapterSpec


@dataclass(frozen=True)
class LocaleConfig:
    code: str
    html_lang: str
    hreflang: str
    og_locale: str
    jsonld_lang: str
    url_prefix: str
    output_subdir: str
    switcher_label: str


LOCALES: tuple[LocaleConfig, ...] = (
    LocaleConfig(
        code="zh-TW",
        html_lang="zh-Hant",
        hreflang="zh-Hant",
        og_locale="zh_TW",
        jsonld_lang="zh-TW",
        url_prefix="",
        output_subdir="",
        switcher_label="繁體中文",
    ),
    LocaleConfig(
        code="zh-CN",
        html_lang="zh-Hans",
        hreflang="zh-Hans",
        og_locale="zh_CN",
        jsonld_lang="zh-Hans",
        url_prefix="/zh-cn",
        output_subdir="zh-cn",
        switcher_label="简体中文",
    ),
    LocaleConfig(
        code="en",
        html_lang="en",
        hreflang="en",
        og_locale="en_US",
        jsonld_lang="en",
        url_prefix="/en",
        output_subdir="en",
        switcher_label="English",
    ),
)

LOCALE_BY_CODE: dict[str, LocaleConfig] = {loc.code: loc for loc in LOCALES}

_CJK_RE = re.compile(r"[\u4e00-\u9fff]")
_FULLWIDTH_RE = re.compile(r"[\u3000-\u303f\uff01-\uff5e]")


def page_canonical_url(locale_code: str, page_filename: str | None = None) -> str:
    """Return canonical absolute URL for index (page_filename=None) or chapter page."""
    loc = LOCALE_BY_CODE[locale_code]
    base = f"https://learn.ai-purplemaple.com{loc.url_prefix}"
    if not page_filename:
        return f"{base}/"
    return f"{base}/{page_filename}"


def page_root_href(locale_code: str, page_filename: str | None = None) -> str:
    """Return root-absolute href (never index.html) for internal links and language switcher."""
    loc = LOCALE_BY_CODE[locale_code]
    if not page_filename:
        return f"{loc.url_prefix}/" if loc.url_prefix else "/"
    return f"{loc.url_prefix}/{page_filename}"


def localize_code_and_output(
    locale_code: str,
    ch_id: str,
    raw_source: str,
    raw_output: str,
    code_replacements: dict[str, Sequence[tuple[str, str]]],
    output_replacements: dict[str, Sequence[tuple[str, str]]],
) -> tuple[str, str]:
    """Deterministically localize displayed Python docstrings/errors/print labels & live stdout."""
    if locale_code == "zh-TW":
        return raw_source, raw_output

    src = raw_source
    for old, new in code_replacements[ch_id]:
        if old not in src:
            raise ValueError(f"[{locale_code}/{ch_id}] CODE_REPLACEMENTS miss: {old!r}")
        src = src.replace(old, new)

    out = raw_output
    for old, new in output_replacements[ch_id]:
        if old not in out:
            raise ValueError(f"[{locale_code}/{ch_id}] OUTPUT_REPLACEMENTS miss: {old!r}")
        out = out.replace(old, new)

    # Validate syntax of localized Python code
    compile(src, f"<{locale_code}:{ch_id}.py>", "exec")

    if locale_code == "en":
        cjk_src = _CJK_RE.findall(src)
        cjk_out = _CJK_RE.findall(out)
        fw_src = _FULLWIDTH_RE.findall(src)
        fw_out = _FULLWIDTH_RE.findall(out)
        if cjk_src or cjk_out or fw_src or fw_out:
            raise ValueError(
                f"[en/{ch_id}] Non-English leak after localization: "
                f"cjk_src={cjk_src[:5]}, cjk_out={cjk_out[:5]}, fw_src={fw_src[:5]}, fw_out={fw_out[:5]}"
            )
    return src, out


def load_locale_pack(locale_code: str) -> dict[str, Any]:
    """Load localized chapters, UI dictionary, YouTube metadata, resources, and code maps."""
    if locale_code == "zh-CN":
        from i18n import zh_cn

        return {
            "chapters": zh_cn.CHAPTERS_ZH_CN,
            "ui": zh_cn.UI_ZH_CN,
            "youtube": zh_cn.YOUTUBE_ZH_CN,
            "resources": zh_cn.RESOURCES_ZH_CN,
            "chapter_resources": zh_cn.CHAPTER_RESOURCES_ZH_CN,
            "code_replacements": zh_cn.CODE_REPLACEMENTS_ZH_CN,
            "output_replacements": zh_cn.OUTPUT_REPLACEMENTS_ZH_CN,
        }
    if locale_code == "en":
        from i18n import en

        return {
            "chapters": en.CHAPTERS_EN,
            "ui": en.UI_EN,
            "youtube": en.YOUTUBE_EN,
            "resources": en.RESOURCES_EN,
            "chapter_resources": en.CHAPTER_RESOURCES_EN,
            "code_replacements": en.CODE_REPLACEMENTS_EN,
            "output_replacements": en.OUTPUT_REPLACEMENTS_EN,
        }
    raise KeyError(f"Unsupported external locale pack: {locale_code}")
