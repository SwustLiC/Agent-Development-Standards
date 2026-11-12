# Agent Development Standards

面向 OpenCode（V2）的 Python 项目 agent 通用规范库：
代码怎么写、文档怎么写、测试怎么跑、依赖怎么选、提交怎么规范。

所有 Python 项目**引用**（而非复制）本仓库的规范，改一处、全部项目生效。

## 规范如何生效

| 内容 | 机制 | 生效方式 |
| --- | --- | --- |
| 核心约定（精简版） | `opencode.json` 的 `instructions` → `standards/python/core.md` | 每次对话常驻注入 |
| 详细规范 | `opencode.json` 的 `references` → 本仓库（git） | agent 按需读取 |
| 代码格式 | `formatter` + ruff | 每次编辑后自动执行 |
| 项目特有说明 | 项目内 `AGENTS.md` | 每次对话常驻注入 |

## 仓库结构

```text
Agent-Development-Standards/
├── standards/python/          # 规范文档（唯一事实来源）
│   ├── core.md                # 常驻注入的精炼核心约定
│   ├── code-style.md          # 代码风格
│   ├── doc-style.md           # 文档与 docstring 风格
│   ├── testing.md             # pytest 测试约定
│   ├── libraries.md           # 默认库选型
│   └── commit.md              # 提交与 PR 规范
├── templates/                 # 目标项目接入用的模板
│   ├── pyproject.toml         # uv + ruff + mypy + pytest 基线
│   ├── AGENTS.md              # 薄项目指令
│   ├── opencode.json          # 中央引用模式的 opencode 配置
│   └── tests/conftest.py
├── examples/mini/             # canary 样例项目（应用全部规范）
├── scripts/vendor.py          # vendor 模式同步脚本（纯标准库）
└── .github/workflows/ci.yml   # CI：markdown + canary + vendor 冒烟
```

## 接入方式

### 方式一：中央引用（推荐，团队使用）

1. 复制 `templates/opencode.json` 到目标项目根目录；
   当前指向 `SwustLiC/Agent-Development-Standards`，仓库迁移时同步改地址。
2. 复制 `templates/AGENTS.md` 为目标项目的 `AGENTS.md`，
   补充项目特有信息（构建命令、目录结构、禁止事项等）。
3. 目标项目的 `pyproject.toml` 以 `templates/pyproject.toml` 为基线
   （uv + ruff + mypy + pytest）。
4. 在目标项目启动 OpenCode 即生效：核心约定常驻注入，
   详细规范通过 `python-standards` 引用按需读取。

> 自托管（GitLab 等）时：`instructions` 的 raw URL 改为
> `<host>/<group>/<repo>/-/raw/main/standards/python/core.md`，
> `references.repository` 改为可识别的仓库地址（支持 owner/repo、git URL、host/path 形式）。

### 方式二：vendor（自包含 / 离线）

```bash
python scripts/vendor.py <目标项目路径>
```

- 把 `standards/python/` 拷贝进目标仓库（更新时重跑即可覆盖）；
- 生成/合并目标项目的 `opencode.json`（相对路径 `instructions` + `formatter`）；
- 缺失时从 `templates/AGENTS.md` 生成 `AGENTS.md`。

适用：离线环境、不想把规范放在外部仓库、或需要规范随项目一起归档时。

## 规范文档一览

| 文件 | 内容 |
| --- | --- |
| `standards/python/core.md` | 常驻注入的精炼核心约定（工具链、代码/文档/测试/选型/提交摘要） |
| `standards/python/code-style.md` | 代码风格：格式、命名、类型注解、错误处理、日志、并发 |
| `standards/python/doc-style.md` | 文档风格：Markdown、docstring、README、changelog、注释 |
| `standards/python/testing.md` | 测试：pytest 布局、命名、fixture、marker、mock、覆盖率 |
| `standards/python/libraries.md` | 库选型：选型表、不推荐清单、依赖管理策略 |
| `standards/python/commit.md` | 提交与 PR：Conventional Commits、分支、PR 模板 |

## 自检

- **canary 样例**：`examples/mini` 是一个完整应用了全部规范的小项目，
  同时用相对 `instructions` 路径验证 vendor 模式的端到端可用性。
- **CI**（`.github/workflows/ci.yml`）：
  markdownlint（文档）、ruff check、ruff format、mypy、pytest（canary）
  与 vendor.py 冒烟测试。
- **本地运行**：

```bash
cd examples/mini
uv sync
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov
```

## 维护规范

1. 改对应详细文档；
2. 核心约定变化时同步 `standards/python/core.md`（常驻注入，必须保持精简）；
3. 涉及代码的规范在 `examples/mini` 验证（ruff / mypy / pytest 全绿）；
4. 提交遵循 `standards/python/commit.md` 的 Conventional Commits。

## 说明

- 仅支持 OpenCode **V2**：V2 只识别 `AGENTS.md`（不读 `CLAUDE.md`），
  配置为 `opencode.json(c)`，改动后自动热加载，无需重启。
- `core.md` 会被注入每个使用本规范的 Python 项目的每次对话，
  修改它要格外克制：只放"必须时刻遵守"的约定，细节放详细文档。
