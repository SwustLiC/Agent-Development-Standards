# Agent Development Standards

面向 OpenCode（V2）的 Python 项目 agent 通用规范库：
代码怎么写、文档怎么写、测试怎么跑、依赖怎么选、提交怎么规范。

所有 Python 项目默认**引用**本仓库的规范，改一处、全部项目生效；
需要自包含或离线时用 vendor 复制。

## 规范如何生效

| 内容 | 机制 | 生效方式 |
| --- | --- | --- |
| 核心约定（精简版） | `opencode.json` 的 `instructions` → `core.md`（vendor 位于 `.opencode/standards/python/`） | 每次对话常驻注入 |
| 详细规范 | `opencode.json` 的 `references` → `python-standards` | agent 按需读取 |
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
├── scripts/
│   ├── reference.py           # 方式一：自动写入中央引用配置（纯标准库）
│   └── vendor.py              # 方式二：vendor 同步脚本（纯标准库）
└── .github/workflows/ci.yml   # CI：markdown + canary + 接入脚本冒烟
```

## 接入方式

### 方式一：中央引用（推荐，团队使用）

```bash
python scripts/reference.py <目标项目路径>
```

脚本会：

1. 生成或合并 `opencode.json`：写入远程 `instructions`、`python-standards` 引用与 `formatter`；
   已有合法 JSON 配置会保留其他设置，只更新本规范相关的字段。
2. 缺失时从 `templates/AGENTS.md` 生成 `AGENTS.md`。
3. 缺失时从 `templates/pyproject.toml` 生成 `pyproject.toml`
   （uv + ruff + mypy + pytest，记得替换占位项目名）。

仓库迁移或自托管时覆盖地址：

```bash
# GitHub：换 owner/repo 或分支
python scripts/reference.py <目标项目路径> --repo my-org/my-standards --branch main

# GitLab 等自托管：同时指定仓库地址与 core.md 的 raw 地址
python scripts/reference.py <目标项目路径> \
  --repo gitlab.example.com/group/repo \
  --raw-url https://gitlab.example.com/group/repo/-/raw/main/standards/python/core.md
```

在目标项目启动 OpenCode 即生效：核心约定常驻注入，
详细规范通过 `python-standards` 引用按需读取。

### 方式二：vendor（自包含 / 离线）

```bash
python scripts/vendor.py <目标项目路径>
```

- 把 `standards/python/` 拷贝到 `<目标>/.opencode/standards/python/`
  （更新时重跑即可覆盖）；
- 生成/合并根目录 `opencode.json`：相对 `instructions`、本地 `python-standards`
  引用与 `formatter`；
- 缺失时从 `templates/AGENTS.md` 生成根目录 `AGENTS.md`；
- `--dest <目录>` 改注入目录（默认 `.opencode`）；
- `--gitignore` 把 `<dest>/standards/python/` 追加到 `.gitignore`，
  控制规范是否随仓库上传。

`opencode.json` 与 `AGENTS.md` 保持在项目根目录，便于团队共享；
可变的规范副本在 `.opencode/standards/python/`，需要时加入 `.gitignore`：

```gitignore
.opencode/standards/python/
```

忽略规范副本后，新克隆或 CI 需要先运行一次
`python scripts/vendor.py <目标项目路径>`，否则 `instructions` 指向的文件不存在
（OpenCode 会跳过缺失文件）。

> 从旧版本升级：重跑脚本会把 `instructions` 从 `standards/python/core.md`
> 替换为 `.opencode/standards/python/core.md`；旧根目录下的 `standards/python/` 可删除。

适用：离线环境、不想把规范放在外部仓库、或需要规范随项目一起归档时。
需要归档时不要加 `--gitignore`。

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
  并用相对 `instructions` 路径验证 OpenCode 的向上查找解析。
- **CI**（`.github/workflows/ci.yml`）：
  markdownlint（文档）、ruff check、ruff format、mypy、pytest（canary），
  以及 `reference.py` / `vendor.py` 冒烟测试（含重复执行与旧配置迁移）。
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
