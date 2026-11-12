"""接入脚本共用工具：读写 opencode 配置、复制模板。"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = REPO_ROOT / "templates"
SCHEMA_URL = "https://opencode.ai/config.json"
DEFAULT_REPO = "SwustLiC/Agent-Development-Standards"
DEFAULT_BRANCH = "main"
CORE_SUFFIX = "standards/python/core.md"
DEFAULT_RAW_URL = f"https://raw.githubusercontent.com/{DEFAULT_REPO}/{DEFAULT_BRANCH}/{CORE_SUFFIX}"
REFERENCE_DESCRIPTION = (
    "Python 规范：代码风格 / 文档风格 / 测试 (pytest) / 默认库选型 / 提交规范。"
    "编写或评审 Python 前先读对应文件。"
)


def read_json_object(path: Path) -> dict[str, Any] | None:
    """读取 JSON 对象；文件不存在、非法 JSON 或顶层不是对象时返回 None。"""
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    return data if isinstance(data, dict) else None


def write_json_object(path: Path, data: dict[str, Any]) -> None:
    """以两空格缩进和末尾换行写入 JSON。"""
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def set_core_instruction(data: dict[str, Any], entry: str) -> None:
    """把 core.md 指令替换为 entry，避免切换接入方式后重复注入。"""
    instructions = data.get("instructions")
    existing = instructions if isinstance(instructions, list) else []
    kept = [item for item in existing if not (isinstance(item, str) and item.endswith(CORE_SUFFIX))]
    kept.append(entry)
    data["instructions"] = kept


def set_reference(
    data: dict[str, Any],
    *,
    path: str | None = None,
    repository: str | None = None,
    branch: str | None = None,
) -> None:
    """写入 python-standards 引用；本地 path 与远程 repository 字段互斥。"""
    references = data.get("references")
    if not isinstance(references, dict):
        references = {}
    reference = references.get("python-standards")
    if not isinstance(reference, dict):
        reference = {}
    reference["description"] = REFERENCE_DESCRIPTION
    if path is not None:
        reference.pop("repository", None)
        reference.pop("branch", None)
        reference["path"] = path
    else:
        reference.pop("path", None)
        reference["repository"] = repository or DEFAULT_REPO
        reference["branch"] = branch or DEFAULT_BRANCH
    references["python-standards"] = reference
    data["references"] = references


def copy_if_missing(source: Path, dest: Path) -> bool:
    """目标不存在时复制模板，返回是否发生复制。"""
    if dest.exists():
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, dest)
    return True
