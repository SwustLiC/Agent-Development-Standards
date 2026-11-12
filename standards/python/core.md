# Python 项目核心规范

> 本文件是常驻注入的精简核心约定。详细规则见 `python-standards` 引用中的对应文档：
> `code-style.md`（代码风格）、`doc-style.md`（文档风格）、`testing.md`（测试）、
> `libraries.md`（库选型）、`commit.md`（提交与 PR）。

## 工具链与命令

- 包与环境管理一律用 **uv**，禁止 `pip install` 到系统环境。
- 常用命令（在项目根目录执行）：
  - 安装依赖：`uv sync`
  - 运行命令：`uv run <cmd>`
  - Lint：`uv run ruff check --fix .`
  - 格式化：`uv run ruff format .`
  - 类型检查：`uv run mypy`
  - 测试：`uv run pytest`（快速定位失败用 `uv run pytest -x`）
- 改动代码后必须跑：ruff check + ruff format + mypy；新增/修改逻辑必须有测试。
- 不手改生成文件和 `uv.lock`；增删依赖后运行 `uv lock` / `uv sync`。

## 代码风格（摘要）

- 格式化由 ruff 决定（行宽 100），不手工调整格式。
- 命名：变量/函数 `snake_case`，类 `PascalCase`，常量 `UPPER_SNAKE_CASE`。
- 公共函数/方法必须完整类型注解；联合类型写 `X | None`（PEP 604），集合用内置泛型（`list[str]`）。
- 捕获具体异常，禁止裸 `except:` 和吞异常。
- 路径用 `pathlib.Path`，不用 `os.path`；读写文本显式 `encoding="utf-8"`。
- 字符串格式化用 f-string；禁止可变默认参数。
- import 置顶、一行一个、按 ruff 规则排序；禁止通配符 import。
- 日志用 stdlib `logging`（服务）或 `loguru`（脚本/工具），禁止 `print` 调试。
- 注释和 docstring 解释"为什么"，不复述代码。

## 文档风格（摘要）

- 文档用中文，代码、命令、库名、配置键、类型名保留英文。
- docstring 用 Google 风格：首行一句话摘要，随后 Args / Returns / Raises。
- 代码块必须标注语言（如 `python`、`bash`、`toml`）。
- README 必含：简介、安装、快速上手、用法、开发说明。
- Changelog 遵循 Keep a Changelog。

## 测试（摘要）

- 唯一测试框架是 **pytest**，不用 unittest 类。
- 目录镜像源码：`tests/test_<module>.py` 对应 `src/<package>/<module>.py`。
- 命名：文件 `test_*.py`，函数 `test_<对象>_<场景>`，共享 fixture 放 `conftest.py`。
- 断言用裸 `assert`；异常断言用 `pytest.raises(..., match=...)`。
- 慢/集成测试标 `@pytest.mark.slow` / `@pytest.mark.integration`，用 `-m` 分组运行。
- 只 mock 外部边界（网络、数据库、时钟、随机），不 mock 被测逻辑本身。
- 覆盖率：`uv run pytest --cov`；不追求 100%，核心逻辑与错误分支必须覆盖。

## 默认库选型（摘要）

| 场景 | 默认选择 |
| --- | --- |
| 包/环境管理 | uv |
| Lint/格式化 | ruff |
| 类型检查 | mypy（默认模式） |
| 测试 | pytest（+ pytest-cov、pytest-xdist） |
| HTTP 客户端 | httpx |
| 数据校验/配置 | pydantic v2 / pydantic-settings |
| Web 框架 | FastAPI |
| CLI | typer（简单脚本用 argparse） |
| 日志 | stdlib logging（服务）/ loguru（脚本工具） |
| 终端富输出 | rich |
| 日期时间 | stdlib datetime + zoneinfo |
| 重试 | tenacity |
| 异步 | stdlib asyncio |

- **优先 stdlib**：标准库能干净解决的不引入第三方库。
- 引入新依赖前先看 `libraries.md` 的选型表与不推荐清单。

## 提交与 PR（摘要）

- Commit 遵循 Conventional Commits：`type(scope): 简短摘要`。
- type 取值：feat | fix | docs | refactor | test | perf | build | ci | chore | revert。
- 一次提交一件事；破坏性变更加 `!` 并在 footer 写 `BREAKING CHANGE:`。
- 分支命名：`feat/xxx`、`fix/xxx` 等；`main` 分支保护，不直接提交。
- PR 标题同 Conventional Commits；提交前 ruff + mypy + pytest 全绿。
