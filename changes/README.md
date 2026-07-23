# 变更提案

每个中大型变更使用一个目录：

```text
changes/<YYYYMMDD-short-name>/
├── requirements.md
├── task.md
└── decision.md      # 有重要取舍时使用
```

状态使用：`draft`、`approved`、`implementing`、`evaluating`、`done`、`cancelled`。

完成后移动到 `changes/archive/<year>/`。小型 G0 变更可以直接通过 PR 描述记录，但仍需验收标准和验证证据。
