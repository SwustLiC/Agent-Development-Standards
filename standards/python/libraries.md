# 默认库选型

## 选型原则

1. **优先 stdlib**：标准库能干净解决的不引入第三方库（`pathlib`、`json`、
   `datetime + zoneinfo`、`unittest.mock`、`argparse` 等）。
2. 成熟且活跃维护：稳定的主版本、持续发布、社区健康。
3. 类型友好：提供 `py.typed`、mypy 无告警的优先。
4. 许可证宽松（MIT / Apache-2.0 / BSD）。
5. 一个关注点一个库：同功能不并存两套（如 httpx 与 requests 只选一个）。

## 默认选型表

| 类别 | 默认选择 | 说明 / 备选 |
| --- | --- | --- |
| 包与环境管理 | uv | 替代 pip + venv + pip-tools；`uv.lock` 必须提交 |
| Lint / 格式化 | ruff | 单一工具管 lint、format、import 排序 |
| 类型检查 | mypy | 默认模式；备选 pyright |
| 测试框架 | pytest | 唯一测试框架 |
| 测试覆盖率 | pytest-cov | — |
| 测试并行 | pytest-xdist | `-n auto` |
| HTTP 客户端 | httpx | 同步/异步统一；新项目不引入 requests |
| Web 框架 | FastAPI | 简单脚本场景可不用框架 |
| 数据校验 / Schema | pydantic v2 | 配置场景用 pydantic-settings |
| CLI | typer | 一次性脚本用 stdlib argparse |
| 日志（服务） | stdlib logging | 分布式 JSON 日志用 structlog |
| 日志（脚本/工具） | loguru | — |
| 终端富输出 | rich | 表格、进度条、日志渲染 |
| 日期时间 | stdlib datetime + zoneinfo | 不引入 pytz |
| 重试 / 退避 | tenacity | — |
| 异步 | stdlib asyncio | 需要多后端抽象时用 anyio |
| 高性能 JSON | orjson | 仅在标准 json 成为瓶颈时 |
| 环境变量 | os.environ / pydantic-settings | 需要 .env 文件时用 python-dotenv |

## 不推荐清单

| 库 | 原因 | 替代 |
| --- | --- | --- |
| pytz | 已被标准库取代 | `datetime + zoneinfo` |
| requests（新项目） | 仅同步，功能被 httpx 覆盖 | httpx |
| mock | 早已并入标准库 | `unittest.mock` |
| six / future 兼容层 | 无 Py2 兼容需求 | 直接写 Py3 |
| pathlib2 等 backport | Py3.12+ 项目不需要 | stdlib |
| pip + venv（直用） | 无锁文件、环境不一致、速度慢 | uv |
| dateutil（默认） | 多数解析场景 stdlib `strptime` 足够 | 先评估，确需复杂解析再引入 |

## 依赖管理

- 依赖全部声明在 `pyproject.toml` 的 `dependencies`；开发依赖放
  `[dependency-groups] dev`。
- 版本约束写下界（如 `httpx>=0.27`），精确版本由 `uv.lock` 锁定；
  `uv.lock` 必须提交仓库。
- 不手改 `uv.lock`；增删依赖后运行 `uv lock` / `uv sync`。
- 新依赖引入流程：
  1. 确认 stdlib 与现有依赖解决不了；
  2. 查本文件的选型表与不推荐清单；
  3. 在 PR 描述中说明引入原因与替代方案评估。
- 定期（或收到安全公告后）升级并审计依赖：`uv lock --upgrade` 后跑全量测试。
