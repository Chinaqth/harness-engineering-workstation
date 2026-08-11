# 决策记录

- Status: approved
- Date: 2026-08-11
- Decision owners: Harness project owner (conversation approval)

## 背景

已安装 Harness 应作为可用基层和能力层，不应等于所有项目都无条件采用其工作流。

## 备选方案

- 在每个项目 `AGENTS.md` 中写激活指令：自然语言不利于严格校验。
- 维护全局项目注册表：会让 Harness 主动管理项目，不符合就地判断理念。
- 使用多字段项目配置：超出当前最小需求。

## 决策

使用项目根目录 `.harness.json`，且文档仅允许 `contract_code` 与 `enabled`。适配器
先要求 `contract_code` 精确等于 `harness-engineering`，匹配后才判断 `enabled` 是否为
JSON 布尔值 `true`。

## 后果

更新后，未放置合法桥接文件的项目不会加载 Harness Kernel。已有项目若要继续使用 Harness，
需在项目根目录显式添加该文件。

## 重新审视条件

当需要多契约并存、monorepo 子项目覆盖，或者按任务条件启用时，创建新的独立变更提案。
