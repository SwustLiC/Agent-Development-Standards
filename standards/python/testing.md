# 测试规范（pytest）

## 原则

- pytest 是唯一测试框架；不使用 `unittest` 测试类。
- 测试是可执行的规格：名字说明意图，断言说明预期。
- 快速、隔离、可重跑：不依赖执行顺序、不共享全局状态、不连真实网络/数据库。
- 测试行为而非实现：只通过公共接口断言，不测私有属性/方法。

## 目录与命名

- `tests/` 镜像 `src/`：`src/mini/core.py` → `tests/test_core.py`。
- 文件 `test_*.py`；函数 `test_<对象>_<场景>`。
- 默认保持扁平；包很大时按模块建子目录（`tests/mini/test_core.py`）。
- 共享 fixture 放 `conftest.py`：全局共享在 `tests/conftest.py`，
  子目录专用在对应子目录的 `conftest.py`；只被单个文件使用的 fixture 写在文件内。

## 写法

- 一个测试一个行为；结构按 given（准备）/ when（执行）/ then（断言）组织。
- 多用例同结构 → `@pytest.mark.parametrize`，不用复制粘贴多个测试函数。

```python
@pytest.mark.parametrize(
    ("text", "expected"),
    [("Hello, World!", "hello-world"), ("a  b", "a-b")],
)
def test_slugify(text: str, expected: str) -> None:
    assert slugify(text) == expected
```

- 浮点比较用 `pytest.approx`；异常用 `pytest.raises(..., match=...)`。
- 禁止占位测试（`assert True`、空函数）；没有断言的测试直接删掉。
- 不 sleep 等待异步结果；用显式事件等待或 mock 时间。

## Fixture

- 命名用名词（`user_db`、`http_client`），不加 `test_` 前缀。
- 默认 `function` 作用域；昂贵的资源（连接池、浏览器）才用 `session` / `module`。
- 需要清理时再 `yield`；能直接 `return` 就不要 `yield`。
- fixture 里不放业务逻辑——被测逻辑放 `src/`，fixture 只做准备/清理。
- 修改环境（环境变量、临时目录）优先用内建 `monkeypatch` / `tmp_path`。

## Marker 与运行

- 项目声明的 marker（在 `pyproject.toml` 的 `[tool.pytest.ini_options]` 中）：
  - `slow`：单条耗时超过约 2 秒的测试。
  - `integration`：需要外部服务（数据库、真实 HTTP）的测试。
- 常用命令：

```bash
uv run pytest -x                                    # 首个失败即停
uv run pytest -k "slug"                             # 按名字过滤
uv run pytest -m "not slow"                         # 跳过慢测试
uv run pytest -n auto                               # 并行（pytest-xdist）
uv run pytest --cov --cov-report=term-missing       # 覆盖率
```

- `integration` 测试：本地按需运行；CI 默认跳过，或在独立 job 提供依赖后运行。

## Mock 边界

- 只 mock 外部边界：网络、数据库、文件系统（必要时）、时钟、随机数、第三方 SDK。
- 不 mock 被测模块本身；不 mock 到断言实现细节（调用次数/参数）的程度。
- 工具选择：环境变量与补丁用 `monkeypatch`，对象替换用 stdlib `unittest.mock`；
  时间冻结在评估后引入 `freezegun`。
- mock 的返回值必须与被测逻辑依赖的真实契约一致，不为了通过测试而伪造行为。

## 覆盖率

- `pyproject.toml` 已开启分支覆盖（`branch = true`）。
- 不追求 100%；核心业务逻辑、错误分支、边界输入（空值/超长/非法格式）必须覆盖。
- 用 `--cov-report=term-missing` 定位未覆盖行，判断是补测试还是显式接受。

## 反模式

- 测试私有方法/属性。
- 把被测实现复制进测试当断言（测的是实现而非行为）。
- 无断言测试、`assert True`。
- 依赖测试执行顺序或共享可变状态。
- 用宽泛 `try/except` 包住测试体"吞掉"失败。
- 在测试里 `print` 调试，跑完忘记删。
