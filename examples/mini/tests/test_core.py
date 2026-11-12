"""mini.core 的单元测试。"""

from pathlib import Path

import pytest

from mini.core import ConfigError, read_config, slugify, split_words


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("hello world", ["hello", "world"]),
        ("  spaced  out  ", ["spaced", "out"]),
        ("mixed123 words", ["mixed123", "words"]),
        ("", []),
    ],
)
def test_split_words(text: str, expected: list[str]) -> None:
    assert split_words(text) == expected


def test_slugify_basic() -> None:
    assert slugify("Hello, World!") == "hello-world"


def test_slugify_custom_separator() -> None:
    assert slugify("Hello World", separator="_") == "hello_world"


def test_slugify_drops_non_ascii() -> None:
    assert slugify("héllo wörld") == "hello-world"


def test_slugify_empty_input() -> None:
    assert slugify("!!!") == ""


def test_slugify_rejects_empty_separator() -> None:
    with pytest.raises(ConfigError, match="separator"):
        slugify("hello", separator="")


def test_read_config(tmp_path: Path) -> None:
    config_file = tmp_path / "app.conf"
    config_file.write_text(
        "# 注释行\n\nKEY=value\nother = with spaces\n",
        encoding="utf-8",
    )
    assert read_config(config_file) == {"KEY": "value", "other": "with spaces"}


def test_read_config_missing_file(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="配置文件不存在"):
        read_config(tmp_path / "missing.conf")


def test_read_config_malformed_line(tmp_path: Path) -> None:
    config_file = tmp_path / "bad.conf"
    config_file.write_text("no-equals-here\n", encoding="utf-8")
    with pytest.raises(ConfigError, match="第 1 行"):
        read_config(config_file)
