"""把中央引用配置写入目标 Python 项目。

用法:
    python scripts/reference.py <目标项目路径> [--repo owner/repo] [--branch main] [--raw-url URL]

行为:
1. 生成或合并 <目标>/opencode.json：远程 instructions、python-standards 引用、formatter。
2. 若 <目标>/AGENTS.md 不存在，从 templates/AGENTS.md 生成。
3. 若 <目标>/pyproject.toml 不存在，从 templates/pyproject.toml 生成。

仅依赖标准库。目标 opencode.json 含注释（JSONC）或不是合法 JSON 时不做自动合并，仅提示。
"""

from __future__ import annotations

import argparse
from pathlib import Path

from _common import (
    CORE_SUFFIX,
    DEFAULT_BRANCH,
    DEFAULT_RAW_URL,
    DEFAULT_REPO,
    TEMPLATES_DIR,
    copy_if_missing,
    read_json_object,
    set_core_instruction,
    set_reference,
    write_json_object,
)

CONFIG_TEMPLATE = TEMPLATES_DIR / "opencode.json"
AGENTS_TEMPLATE = TEMPLATES_DIR / "AGENTS.md"
PYPROJECT_TEMPLATE = TEMPLATES_DIR / "pyproject.toml"


def build_raw_url(repo: str, branch: str) -> str:
    """按 GitHub raw 地址规则生成 core.md 的 URL。"""
    return f"https://raw.githubusercontent.com/{repo}/{branch}/{CORE_SUFFIX}"


def write_config_from_template(
    target: Path,
    raw_url: str,
    repo: str,
    branch: str,
) -> None:
    """复制模板并替换仓库地址，保留模板中的说明注释。"""
    text = CONFIG_TEMPLATE.read_text(encoding="utf-8")
    text = text.replace(DEFAULT_RAW_URL, raw_url)
    text = text.replace(DEFAULT_REPO, repo)
    text = text.replace(f'"branch": "{DEFAULT_BRANCH}"', f'"branch": "{branch}"')
    (target / "opencode.json").write_text(text, encoding="utf-8")


def merge_existing_config(
    target: Path,
    raw_url: str,
    repo: str,
    branch: str,
) -> None:
    """合并已存在的合法 JSON 配置。"""
    config_path = target / "opencode.json"
    data = read_json_object(config_path)
    if data is None:
        print(
            f"[1/3] {config_path.name} 含注释或不是合法 JSON，跳过自动合并；"
            f'请手动加入 "instructions": ["{raw_url}"]、'
            f'"references.python-standards.repository": "{repo}" 与 "formatter": true'
        )
        return
    set_core_instruction(data, raw_url)
    set_reference(data, repository=repo, branch=branch)
    data["formatter"] = True
    write_json_object(config_path, data)
    print(f"[1/3] 已写入 {config_path}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("target", help="目标项目路径")
    parser.add_argument("--repo", default=DEFAULT_REPO, help="规范仓库（owner/repo）")
    parser.add_argument("--branch", default=DEFAULT_BRANCH, help="规范仓库分支")
    parser.add_argument("--raw-url", help="core.md 的原始地址；自托管 GitLab 时显式指定")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    target = Path(args.target).resolve()
    if not target.is_dir():
        print(f"错误: 目标目录不存在: {target}")
        return 1
    raw_url = args.raw_url or build_raw_url(args.repo, args.branch)
    config_path = target / "opencode.json"
    if config_path.exists():
        merge_existing_config(target, raw_url, args.repo, args.branch)
    elif (target / "opencode.jsonc").exists():
        print(
            f"[1/3] 检测到 opencode.jsonc，跳过自动生成；"
            f'请手动加入 "instructions": ["{raw_url}"]、'
            f'"references.python-standards.repository": "{args.repo}" 与 "formatter": true'
        )
    else:
        write_config_from_template(target, raw_url, args.repo, args.branch)
        print(f"[1/3] 已生成 {config_path}")
    if copy_if_missing(AGENTS_TEMPLATE, target / "AGENTS.md"):
        print(f"[2/3] 已生成 {target / 'AGENTS.md'}")
    else:
        print("[2/3] AGENTS.md 已存在，跳过")
    if copy_if_missing(PYPROJECT_TEMPLATE, target / "pyproject.toml"):
        print(
            f"[3/3] 已生成 {target / 'pyproject.toml'}；"
            "请把 your-project / your_package 替换为实际名称"
        )
    else:
        print("[3/3] pyproject.toml 已存在，跳过")
    print("完成：在目标项目中启动 OpenCode 后，核心约定即通过 instructions 注入。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
