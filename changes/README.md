# 变更提案与项目记录

## 记录归属

每项任务的 change 记录必须保存在任务所属目标项目的根目录：

```text
<project-root>/changes/<YYYYMMDD-short-name>/
```

该规则不依赖 Git。不得因为当前工作目录位于 Harness、Domain Pack 或工具仓库，就把其他项目的
任务记录写入这些仓库。只有当任务实际修改 Harness 或 Domain Pack 本身时，记录才属于相应仓库。
跨项目任务必须在计划中指定一个主要项目作为权威记录所有者，并以稳定路径或不可变 ID 链接其他
项目的局部证据；不得静默复制出多个相互竞争的权威记录。

使用显式项目根目录创建记录：

```bash
python3 /path/to/harness/scripts/init_change.py \
  20260809-short-name --project-root /absolute/path/to/project
```

命令不会通过 `.git` 猜测项目根目录，也不会覆盖已有记录。

## 文件结构

中大型变更使用独立目录：

```text
changes/<YYYYMMDD-short-name>/
├── requirements.md
├── task.md
├── acceptance.json
├── progress.md
├── contract.md
└── decision.md
```

允许状态：`draft`、`approved`、`implementing`、`evaluating`、`done`、`cancelled`。

风险对应要求：

- G0：可直接记录在任务或 Pull Request 描述中。
- G1：需要 `requirements.md`、`task.md` 和 `progress.md`。
- G2/G3：需要上面列出的完整文件集。

## 语言

`changes/**` 中面向人的解释性 Markdown 默认使用中文，包括需求、任务、进度、契约、决策和评估。
机器可读 JSON 的字段名、Schema、状态值和代码标识符保持英文；说明性字符串可以使用中文。用户明确
要求其他语言时以该要求为准。历史记录不要求批量翻译。

## 生命周期与验证

使用 ISO 日期填写 `Review-By`。活动变更超过该日期后必须刷新、完成或取消，否则知识整理检查失败。

通过专业能力路由的任务，应把有效 Task Envelope 和 Routing Plan 与 change 记录放在一起，或通过
不可变 ID 链接到等价的持久记录。路由记录不能替代按风险要求生成的执行文件。

评估前运行：

```bash
python3 /path/to/harness/scripts/validate_change.py <project-root>
```

只有验收状态终结且长期结论已经制度化后，才能移入 `changes/archive/<year>/`。旧项目记录的迁移必须
先复制、核对，再在原位置留下指针；不得静默移动或删除。
