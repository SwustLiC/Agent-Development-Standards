# 代码风格规范

> 格式细节以 ruff 为准（行宽 100），本文聚焦 ruff 管不到的部分。
> 类型检查用 mypy（默认模式），公共 API 必须完整标注类型。
> 所有改动在提交前必须通过：`uv run ruff check .`、`uv run ruff format .`、`uv run mypy`。

## 中文文档与 ruff 规则

- 规范文档、docstring、注释用中文书写（全角标点）。
- ruff 的 RUF001 / RUF002 / RUF003（歧义 unicode 字符检查）在基线配置中显式
  `ignore`，与"中文为主"的文档语言约定保持一致；项目迁移配置时不要删掉这些 ignore。

## 模块与包结构

- src layout：业务代码放 `src/<package>/`，测试放 `tests/`。
- 每个包提供 `__init__.py`，在包入口用 `__all__` 显式导出公共 API。
- 模块 docstring 一句话说明模块职责。
- 禁止循环导入；出现循环依赖时拆分模块或下移依赖，而不是把 `import` 挪到函数内部了事。

## 导入

- 置顶、一行一个、禁止通配符导入。
- 分组排序由 ruff（isort 规则）保证：stdlib → 第三方 → 本项目。
- 默认 `import module` 后以 `module.func()` 调用；高频使用的单个符号可以
  `from module import Name`，命名冲突时用 `as` 起别名。
- 禁止未使用的导入（ruff F401）；`__init__.py` 中为导出而保留的导入要显式可见。

## 命名

- 变量、函数、模块、包：`snake_case`。
- 类：`PascalCase`。
- 模块级不可变常量：`UPPER_SNAKE_CASE`。
- 私有标识符：单下划线 `_name`；不要用双下划线触发 name mangling。
- 布尔值：`is_` / `has_` / `can_` 前缀（如 `is_ready`、`has_permission`）。
- 测试：`test_<对象>_<场景>`（如 `test_slugify_rejects_empty_separator`）。

## 类型注解

- 公共函数/方法必须完整标注（参数 + 返回值）；mypy 配置已开启 `disallow_untyped_defs`。
- 文件顶部加 `from __future__ import annotations`。
- 联合类型用 `X | None`（PEP 604），不用 `Optional[X]`。
- 集合用内置泛型：`list[str]`、`dict[str, int]`，不用 `typing.List` / `typing.Dict`。
- 抽象用 `Protocol`（鸭子类型）与 `TypeVar` 表达；避免滥用 `Any`。
- `# type: ignore` 仅在必要时使用，且必须附注释说明原因。

## 函数

- 单一职责；函数体建议不超过 30 行，明显过长时拆分。
- 参数不超过 8 个；更多时收敛为 `dataclass` 或 pydantic 模型。
- 禁止可变默认参数：需要容器参数时写 `def f(items: list[str] | None = None)`。
- 优先纯函数；副作用（IO、全局状态、时间）集中在函数边缘，便于测试。
- 用提前返回（guard clause）减少嵌套层级。

## 错误处理

- 只捕获具体异常；禁止裸 `except:`，避免宽泛的 `except Exception`
  （框架/进程顶层兜底除外）。
- 不吞异常：捕获后要么处理、要么记录日志、要么转换后重新抛出。
- 定义领域异常层次：项目统一基类（如 `class MyAppError(RuntimeError)`），
  具体异常继承 `ValueError` 或领域基类；对外 API 只抛领域异常。
- 不用异常控制流程。
- 错误信息要包含定位上下文：路径、参数、行号、外部响应码等。

## 文件与 IO

- 路径一律 `pathlib.Path`，不用 `os.path`。
- 读写文本显式 `encoding="utf-8"`。
- 临时文件/目录用 `tempfile` 或 pytest 的 `tmp_path`，不要写死系统临时目录。
- 大文件逐行迭代处理，不要一次性读入整个文件。

## 字符串

- 字符串拼接用 f-string；不用 `%` 格式化。
- 动态内容拼接列表用 `"".join(...)`，不用循环 `+=`。
- 多行字符串用三引号；不要用 `+` 拼接多行文本。

## 日志

- 服务用 stdlib `logging`（`logger = logging.getLogger(__name__)`），
  脚本/工具用 `loguru`。
- 禁止 `print` 调试输出。
- 级别语义：DEBUG 细节 / INFO 关键流程 / WARNING 可恢复异常 / ERROR 操作失败。
- 参数化记录：`logger.error("处理 %s 失败: %s", path, exc)`，不拼接字符串；
  记录异常用 `logger.exception(...)` 保留堆栈。

## 并发与异步

- 默认同步代码；只在真实 IO 密集且需要并发时使用 `asyncio`。
- 协程内禁止阻塞调用（同步 IO、`time.sleep`）；必要时用线程池承接。
- 共享可变状态必须显式加锁；优先用消息/队列传递状态而非共享内存。
- 线程/协程池规模显式配置，不依赖默认值。

## 数据结构

- 结构化数据用 `dataclass`（不可变加 `frozen=True`）或 pydantic（需要校验/序列化时）。
- 不用元组位置参数传递 3 个以上字段的结构化数据，可读性和维护性都会崩坏。
- 枚举值用 `enum.Enum`（或 `StrEnum`），不用裸字符串常量散落各处。
