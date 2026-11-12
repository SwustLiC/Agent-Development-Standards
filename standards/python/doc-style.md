# 文档与 docstring 规范

## 总原则

- 文档用中文书写；代码、命令、库名、配置键、类型名、错误名保留英文原文。
- 简洁直接，用祈使句；不写营销语言、不写"我们"视角的叙述。
- 示例必须可运行：命令真实存在，代码无省略号占位；示意性片段要显式标注。
- 能一句话说清的不用一段；同一事实不散落在多处文档里。

## Markdown 约定

- 一个文件一个 H1；章节用 H2；H3 以上谨慎使用。
- 标题末尾不加标点。
- 代码块必须标注语言：`python`、`bash`、`toml`、`jsonc`、`text` 等。
- 结构化对比（≥ 3 项）用表格；步骤用有序列表；并列项用无序列表（统一 `-`）。
- 列表、表格前后各留一个空行。
- 内部文档引用用相对路径链接。
- 表格表头与分隔行齐全，各行列数一致。

## docstring（Google 风格）

- 首行：一句话摘要（动词开头，尽量短）。
- 空行后是正文（可选）；公共 API 写 `Args` / `Returns` / `Raises`。
- 小节顺序：正文 → Args → Returns → Raises → Examples。
- 不在 docstring 里重复签名已有的类型标注，只写语义。
- 模块 docstring：一句话说明模块职责；私有成员（`_xxx`）可省略 docstring。

```python
def slugify(text: str, separator: str = "-") -> str:
    """把文本转换为 URL 友好的 slug。

    非字母数字字符统一替换为 separator。

    Args:
        text: 输入文本。
        separator: 词间分隔符。

    Returns:
        小写 slug。

    Raises:
        ConfigError: separator 为空时抛出。
    """
```

- 多参数时每个参数独占一行：参数名 + 冒号 + 空格 + 解释。

## README 模板

每个项目 README 至少包含以下章节（顺序固定）：

````markdown
# <项目名>

<一句话说明项目解决什么问题。>

## 安装

```bash
uv sync
```

## 快速上手

<最小可运行示例（≤ 10 行代码或一条命令）。>

## 用法

<主要功能与示例；复杂用法链接到 docs/ 下的详细文档。>

## 开发

```bash
uv run ruff check --fix .
uv run ruff format .
uv run mypy
uv run pytest
```

## 依赖

<关键第三方依赖及用途（表格）。>
````

## Changelog

- 遵循 Keep a Changelog 格式与 SemVer 版本号。
- 未发布改动记在 `## [Unreleased]` 分组下。
- 每组按 `### Added` / `### Changed` / `### Fixed` / `### Removed` 分类。
- 每条一句话，引用关联的 issue / PR 编号。

## 注释规范

- 注释解释"为什么"（动机、约束、坑、外部契约），不复述代码在做什么。
- 待办事项格式：`# TODO(负责人): 内容`，不写无主的 TODO。
- 禁止注释掉的死代码；要删就删，git 有历史。
- 魔法数字必须命名常量或就地注释来源。

## PR 描述规范

- 标题遵循 Conventional Commits（见 `commit.md`）。
- 正文按"动机 / 改动 / 自测记录 / 风险"四段组织。
- 自测记录必须包含：命令 + 结果（如 `uv run pytest` 通过，覆盖率 92%）。
