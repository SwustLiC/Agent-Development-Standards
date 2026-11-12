# 项目指令

- 本项目遵循团队 Python 规范（python-standards）：
  核心约定已通过 `instructions` 注入；细节见 `python-standards` 引用中的
  `code-style.md` / `doc-style.md` / `testing.md` / `libraries.md` / `commit.md`。
- 工具链：uv + ruff + mypy + pytest。
  - 依赖安装：`uv sync`
  - Lint：`uv run ruff check --fix .`
  - 格式化：`uv run ruff format .`
  - 类型检查：`uv run mypy`
  - 测试：`uv run pytest`
- 改动代码后：ruff、mypy、pytest 全部通过才算完成。
- 包结构为 src layout（`src/<package>/`，测试在 `tests/`）。
- 不手改生成文件（如 `uv.lock`）。
- <在此补充本项目特有信息：构建命令、目录说明、禁止事项等。>
