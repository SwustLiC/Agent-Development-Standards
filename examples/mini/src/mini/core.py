"""文本处理与简单配置文件读取。"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

_SLUG_INVALID_RE = re.compile(r"[^a-z0-9]+")
_WORD_RE = re.compile(r"\w+", re.UNICODE)


class ConfigError(ValueError):
    """配置错误。"""


def split_words(text: str) -> list[str]:
    """把文本拆分为词列表。

    按 Unicode 词字符（字母、数字、下划线）切分，忽略标点与空白。

    Args:
        text: 输入文本。

    Returns:
        词列表；空输入返回空列表。
    """
    return _WORD_RE.findall(text)


def slugify(text: str, separator: str = "-") -> str:
    """把文本转换为 URL 友好的 slug。

    先做 NFKD 归一化并转小写，丢弃无法映射为 ASCII 的字符，
    其余非字母数字字符统一替换为 separator。

    Args:
        text: 输入文本。
        separator: 词间分隔符，默认 "-"。

    Returns:
        小写 slug；无有效内容时返回空字符串。

    Raises:
        ConfigError: separator 为空时抛出。
    """
    if not separator:
        raise ConfigError("separator 不能为空")
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.lower().encode("ascii", "ignore").decode("ascii")
    return _SLUG_INVALID_RE.sub(separator, ascii_text).strip(separator)


def read_config(path: Path | str) -> dict[str, str]:
    """读取 `KEY=VALUE` 行格式的配置文件。

    支持空行与 `#` 开头的注释行；等号两侧空白会被去除。

    Args:
        path: 配置文件路径。

    Returns:
        配置项字典（按文件顺序）。

    Raises:
        ConfigError: 文件不存在或某行格式非法。
    """
    file_path = Path(path)
    if not file_path.is_file():
        raise ConfigError(f"配置文件不存在: {file_path}")
    result: dict[str, str] = {}
    for line_no, raw_line in enumerate(file_path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        key, sep, value = line.partition("=")
        if not sep or not key.strip():
            raise ConfigError(f"配置行格式非法 (第 {line_no} 行): {raw_line!r}")
        result[key.strip()] = value.strip()
    return result
