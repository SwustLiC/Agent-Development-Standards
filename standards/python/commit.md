# 提交与 PR 规范

## Conventional Commits

提交信息格式：

```text
<type>(<scope>): <简短摘要>

[正文：说明动机与改动对比，可省略]

[footer：关联 issue、BREAKING CHANGE，可省略]
```

- `type`：必填，取值为下表之一。
- `scope`：可选，写模块/包名（如 `core`、`cli`）。
- 摘要：祈使语气（"fix bug" 而非 "fixed bug"），不超过 72 字符，末尾不加句号。
- 破坏性变更：type 后加 `!`（如 `feat!`），且 footer 必须写 `BREAKING CHANGE: <说明>`。
- 关联 issue：footer 写 `Closes #123` / `Refs #456`。

### type 取值

| type | 含义 |
| --- | --- |
| feat | 新功能 |
| fix | 缺陷修复 |
| docs | 仅文档 |
| refactor | 重构（不改变行为） |
| perf | 性能优化 |
| test | 增加或修正测试 |
| build | 构建系统或依赖变更 |
| ci | CI 配置变更 |
| chore | 其他杂项（不改 src 与 test） |
| revert | 回滚提交 |

## 提交粒度

- 一次提交只做一件事；提交可独立评审、可独立回滚。
- 功能开发中先拆"可编译 + 测试通过"的中间状态再逐步推进，不留半成品进历史。
- 格式化/重命名与逻辑改动分开提交。

## 分支

- `main` 受保护，禁止直接 push。
- 分支命名：`feat/<主题>`、`fix/<主题>`、`docs/<主题>`、`chore/<主题>`，
  主题用 kebab-case 短描述（如 `feat/slug-separator`）。
- 合并前 rebase `main` 并解决冲突。

## PR

- 标题沿用 Conventional Commits 格式。
- 小 PR 优先（建议 diff < 400 行）；大改动先拆。
- 合并前检查（checklist）：
  - [ ] `uv run ruff check .` 与 `uv run ruff format --check .` 通过
  - [ ] `uv run mypy` 通过
  - [ ] `uv run pytest` 通过，无未说明原因的跳过
  - [ ] 文档与注释已同步（含 README / changelog）
  - [ ] 无敏感信息（密钥、内部地址、个人数据）
  - [ ] 新增依赖已按 `libraries.md` 流程评估

### PR 描述模板

````markdown
## 动机

<为什么做这个改动。>

## 改动内容

<改了什么，关键设计决策。>

## 自测记录

- 命令与结果（如 `uv run pytest` 32 passed，覆盖率 91%）。

## 风险

<可能的影响面、回滚方式；没有则写"无"。>
````
