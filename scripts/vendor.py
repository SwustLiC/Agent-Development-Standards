"""把 standards/python/ 规范 vendor 到目标 Python 项目。

用法:
    python scripts/vendor.py <目标项目路径>

行为:
1. 拷贝 standards/python/ 到 <目标>/standards/python/（覆盖同名文件）。
2. 生成或合并 <目标>/opencode.json：加入相对 instructions 并启用 formatter。
3. 若 <目标>/AGENTS.md 不存在，从 templates/AGENTS.md 生成。

仅依赖标准库。目标 opencode.json 含注释（JSONC）或不是合法 JSON 时不做自动合并，仅提示。
重复执行是幂等的：规范文件覆盖更新，已有配置只补缺失字段。
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STANDARDS_SOURCE = REPO_ROOT / "standards" / "python"
AGENTS_TEMPLATE = REPO_ROOT / "templates" / "AGENTS.md"
INSTRUCTIONS_ENTRY = "standards/python/core.md"
SCHEMA_URL = "https://opencode.ai/config.json"


def copy_standards(target: Path) -> None:
    """拷贝规范文档到目标项目（覆盖式）。"""
    dest = target / "standards" / "python"
    shutil.copytree(STANDARDS_SOURCE, dest, dirs_exist_ok=True)
    print(f"[1/3] 已拷贝 standards/python/ -> {dest}")


def merge_opencode_json(target: Path) -> None:
    """生成或合并目标项目的 opencode.json。"""
    config_path = target / "opencode.json"
    data: object
    if config_path.exists():
        raw = config_path.read_text(encoding="utf-8")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            print(
                f"[2/3] {config_path.name} 含注释或不是合法 JSON，跳过自动合并；"
                f'请手动加入 "instructions": ["{INSTRUCTIONS_ENTRY}"] 与 "formatter": true'
            )
            return
        if not isinstance(data, dict):
            print(f"[2/3] {config_path.name} 顶层不是对象，跳过自动合并")
            return
    else:
        data = {"$schema": SCHEMA_URL}

    instructions = data.get("instructions")
    if not isinstance(instructions, list) or INSTRUCTIONS_ENTRY not in instructions:
        existing = instructions if isinstance(instructions, list) else []
        existing.append(INSTRUCTIONS_ENTRY)
        data["instructions"] = existing
    data["formatter"] = True
    config_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"[2/3] 已写入 {config_path}")


def copy_agents_md(target: Path) -> None:
    """缺失时从模板生成 AGENTS.md。"""
    dest = target / "AGENTS.md"
    if dest.exists():
        print(f"[3/3] {dest.name} 已存在，跳过")
        return
    shutil.copyfile(AGENTS_TEMPLATE, dest)
    print(f"[3/3] 已生成 {dest}")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    target = Path(argv[1]).resolve()
    if not target.is_dir():
        print(f"错误: 目标目录不存在: {target}")
        return 1
    copy_standards(target)
    merge_opencode_json(target)
    copy_agents_md(target)
    print("完成：在目标项目中启动 OpenCode 后，核心约定即通过 instructions 注入。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
