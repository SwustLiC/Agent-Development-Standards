"""把 standards/python/ 规范 vendor 到目标 Python 项目。

用法:
    python scripts/vendor.py <目标项目路径> [--dest .opencode] [--gitignore]

行为:
1. 拷贝 standards/python/ 到 <目标>/<dest>/standards/python/（覆盖同名文件）。
2. 生成或合并 <目标>/opencode.json：相对 instructions、本地 python-standards 引用、formatter。
3. 若 <目标>/AGENTS.md 不存在，从 templates/AGENTS.md 生成。
4. --gitignore 时把 <dest>/standards/python/ 追加到 <目标>/.gitignore。

仅依赖标准库。目标 opencode.json 含注释（JSONC）或不是合法 JSON 时不做自动合并，仅提示。
重复执行是幂等的：规范文件覆盖更新，已有配置保留其他字段，只更新本规范相关字段。
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from _common import (
    SCHEMA_URL,
    TEMPLATES_DIR,
    copy_if_missing,
    read_json_object,
    set_core_instruction,
    set_reference,
    write_json_object,
)

STANDARDS_SOURCE = Path(__file__).resolve().parent.parent / "standards" / "python"
AGENTS_TEMPLATE = TEMPLATES_DIR / "AGENTS.md"
DEFAULT_DEST = ".opencode"


def normalize_dest(raw: str) -> str:
    """把 --dest 规范化为项目内的相对 POSIX 路径。"""
    dest = Path(raw)
    if dest.is_absolute():
        raise ValueError("--dest 必须是相对路径")
    if ".." in dest.parts:
        raise ValueError("--dest 不能包含 ..")
    parts = [part for part in dest.parts if part not in ("", ".")]
    if not parts:
        raise ValueError("--dest 不能为空，也不能指向项目根目录")
    return Path(*parts).as_posix()


def copy_standards(target: Path, dest: str) -> None:
    """拷贝规范文档到目标项目（覆盖式）。"""
    dest_dir = target / dest / "standards" / "python"
    shutil.copytree(STANDARDS_SOURCE, dest_dir, dirs_exist_ok=True)
    print(f"[1/4] 已拷贝 standards/python/ -> {dest_dir}")


def merge_opencode_json(target: Path, dest: str) -> None:
    """生成或合并目标项目的 opencode.json。"""
    config_path = target / "opencode.json"
    instructions_entry = f"{dest}/standards/python/core.md"
    reference_path = f"./{dest}/standards/python"
    manual_hint = (
        f'请手动加入 "instructions": ["{instructions_entry}"]、'
        f'"references.python-standards.path": "{reference_path}" 与 "formatter": true'
    )
    if config_path.exists():
        data = read_json_object(config_path)
        if data is None:
            print(f"[2/4] {config_path.name} 含注释或不是合法 JSON，跳过自动合并；{manual_hint}")
            return
    else:
        if (target / "opencode.jsonc").exists():
            print(f"[2/4] 检测到 opencode.jsonc，跳过自动生成；{manual_hint}")
            return
        data = {"$schema": SCHEMA_URL}
    set_core_instruction(data, instructions_entry)
    set_reference(data, path=reference_path)
    data["formatter"] = True
    write_json_object(config_path, data)
    print(f"[2/4] 已写入 {config_path}")


def update_gitignore(target: Path, entry: str) -> None:
    """把注入目录追加到 .gitignore，已存在时跳过。"""
    gitignore = target / ".gitignore"
    lines = gitignore.read_text(encoding="utf-8-sig").splitlines() if gitignore.exists() else []
    normalized = {
        line.strip().lstrip("/").rstrip("/")
        for line in lines
        if line.strip() and not line.strip().startswith("#")
    }
    entry = entry.rstrip("/")
    if any(entry == item or entry.startswith(f"{item}/") for item in normalized if item):
        print(f"[4/4] .gitignore 已包含 {entry}")
        return
    prefix = "" if not lines or lines[-1] == "" else "\n"
    with gitignore.open("a", encoding="utf-8") as file:
        file.write(f"{prefix}{entry}\n")
    print(f"[4/4] 已把 {entry} 追加到 .gitignore")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("target", help="目标项目路径")
    parser.add_argument(
        "--dest",
        default=DEFAULT_DEST,
        help=f"规范注入目录（相对目标项目，默认 {DEFAULT_DEST}）",
    )
    parser.add_argument(
        "--gitignore",
        action="store_true",
        help="把注入目录加入目标项目的 .gitignore",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    target = Path(args.target).resolve()
    if not target.is_dir():
        print(f"错误: 目标目录不存在: {target}")
        return 1
    try:
        dest = normalize_dest(args.dest)
    except ValueError as exc:
        print(f"错误: {exc}")
        return 2
    copy_standards(target, dest)
    merge_opencode_json(target, dest)
    if copy_if_missing(AGENTS_TEMPLATE, target / "AGENTS.md"):
        print(f"[3/4] 已生成 {target / 'AGENTS.md'}")
    else:
        print("[3/4] AGENTS.md 已存在，跳过")
    if args.gitignore:
        update_gitignore(target, f"{dest}/standards/python/")
    else:
        print("[4/4] 未修改 .gitignore（需要时加 --gitignore）")
    print("完成：在目标项目中启动 OpenCode 后，核心约定即通过 instructions 注入。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
