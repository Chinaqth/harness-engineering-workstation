# HmTest 记录迁移方案

## 当前事实

- 旧记录位于 Harness：`changes/20260809-hmtest-v1-v2-migration/`。
- 正确目标位置：`/Users/minikukala/DevEcoStudioProjects/hmtest/changes/20260809-hmtest-v1-v2-migration/`。
- HmTest 不是 Git 仓库，但新规则明确支持这种项目。
- HmTest 源代码尚未修改，本 G2 变更也不会修改或移动它。

## 恢复 HmTest 任务时的无损步骤

1. 确认目标目录不存在，避免覆盖独立记录。
2. 将旧目录完整复制到 HmTest 的 `changes/`，保留 Task Envelope、旧 Routing Plan 和中断证据。
3. 将人类可读 Markdown 转为中文；不得改写历史事实或伪造审批。
4. 使用 Resolver v2 重新生成 Routing Plan 3.0。预期选择 HarmonyOS 迁移 Capability，未选中的
   Domain Pack 1.0 依赖作为软 fallback 记录，状态进入 `needs_approval`。
5. 核对源目录和目标目录的文件清单与内容哈希。
6. 在 Harness 原位置保留只读指针，指向 HmTest 的权威记录；未经用户明确授权不得删除旧记录。
7. Owner 审批新的 scope fingerprint 后，才恢复装饰器迁移。

## 回滚

复制和核对阶段不删除源记录。若目标记录不完整，停止使用目标副本并从 Harness 源记录重新复制。
