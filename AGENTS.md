# 项目指令（规范仓库自身）

- 本仓库是 Python agent 规范库；内容以 `standards/python/` 为唯一事实来源。
- 修改规范时的流程：
  1. 先改对应详细文档（`code-style.md` / `doc-style.md` / `testing.md` / `libraries.md` / `commit.md`）；
  2. 若涉及核心约定，同步更新 `standards/python/core.md`（它会被常驻注入，必须保持精简）；
  3. 涉及代码的规范用 `examples/mini`（canary）验证：ruff / mypy / pytest 全绿。
- 本仓库的 Python 代码（`examples/mini`、`scripts/`）遵循 `standards/python/`：
  - canary 的依赖与命令在 `examples/mini` 内执行：`uv sync`、`uv run ruff check .`、
    `uv run ruff format .`、`uv run mypy`、`uv run pytest`。
  - `scripts/vendor.py` 仅用标准库，直接 `python scripts/vendor.py <目标项目路径>` 即可运行。
- Markdown 文档风格遵循 `standards/python/doc-style.md`。
- 提交遵循 `standards/python/commit.md` 的 Conventional Commits。
